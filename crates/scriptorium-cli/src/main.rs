use anyhow::{Context, Result, bail, ensure};
use clap::{Parser, Subcommand};
use scriptorium_core::{
    assets::{AssetRecord, AssetStore, Provenance},
    config::Config,
    network::{self, DownloadPolicy},
    planning::{self, KnowledgePlan, VisualState},
    rendering, research,
    validation::{self, NoteDraft, VisualReceipt},
};
use serde::{Serialize, de::DeserializeOwned};
use std::{
    fs,
    io::{self, Write},
    path::{Path, PathBuf},
};

#[derive(Parser)]
#[command(
    name = "scribe",
    version,
    about = "Rust local visual planning, research retrieval and verified publication"
)]
struct Cli {
    #[arg(long, global = true)]
    config: Option<PathBuf>,
    #[command(subcommand)]
    command: Command,
}
#[derive(Subcommand)]
enum Command {
    Notes {
        #[command(subcommand)]
        action: Notes,
    },
    Assets {
        #[command(subcommand)]
        action: Assets,
    },
    Research {
        #[arg(long, required = true)]
        url: Vec<String>,
        #[arg(long)]
        cache: PathBuf,
    },
    Renderers,
    Render {
        #[arg(long)]
        spec: PathBuf,
        #[arg(long)]
        output: PathBuf,
    },
    Config {
        #[arg(long)]
        vault: PathBuf,
        #[arg(long)]
        note: PathBuf,
    },
    Validate {
        file: PathBuf,
    },
}
#[derive(Subcommand)]
enum Notes {
    Plan {
        #[arg(long)]
        spec: PathBuf,
    },
    Audit {
        #[arg(long)]
        vault: PathBuf,
        #[arg(long)]
        plan: PathBuf,
        #[arg(long)]
        receipts: PathBuf,
    },
    Publish {
        #[arg(long)]
        vault: PathBuf,
        #[arg(long)]
        destination: PathBuf,
        #[arg(long)]
        plan: PathBuf,
        #[arg(long)]
        receipts: PathBuf,
        #[arg(long)]
        drafts: PathBuf,
    },
}
#[derive(Subcommand)]
enum Assets {
    Render {
        #[arg(long)]
        vault: PathBuf,
        #[arg(long)]
        note: PathBuf,
        #[arg(long)]
        spec: PathBuf,
        #[arg(long)]
        visual_id: Option<String>,
    },
    Fetch {
        #[arg(long)]
        vault: PathBuf,
        #[arg(long)]
        note: PathBuf,
        #[arg(long)]
        url: String,
        #[arg(long)]
        provenance: PathBuf,
        #[arg(long)]
        visual_id: Option<String>,
    },
    Import {
        #[arg(long)]
        vault: PathBuf,
        #[arg(long)]
        note: PathBuf,
        #[arg(long)]
        file: PathBuf,
        #[arg(long)]
        mime: String,
        #[arg(long)]
        provenance: PathBuf,
        #[arg(long)]
        visual_id: Option<String>,
    },
    Verify {
        #[arg(long)]
        vault: PathBuf,
        #[arg(long)]
        note: PathBuf,
        #[arg(long)]
        record: PathBuf,
    },
    Embed {
        #[arg(long)]
        vault: PathBuf,
        #[arg(long)]
        note: PathBuf,
        #[arg(long)]
        record: PathBuf,
        #[arg(long)]
        alt: String,
    },
}
fn read<T: DeserializeOwned>(path: &Path) -> Result<T> {
    serde_json::from_slice(&fs::read(path).with_context(|| format!("read {}", path.display()))?)
        .with_context(|| format!("parse {}", path.display()))
}
fn output(value: &impl Serialize) -> Result<()> {
    println!("{}", serde_json::to_string_pretty(value)?);
    Ok(())
}
fn store(vault: &Path, note: &Path, config: &Config) -> Result<AssetStore> {
    AssetStore::new(vault, config.attachment_dir(vault, note)?)
}
fn asset_output(record: AssetRecord, visual_id: Option<String>) -> Result<()> {
    if let Some(id) = visual_id {
        ensure!(!id.trim().is_empty(), "visual ID must not be empty");
        output(&VisualReceipt {
            visual_id: id,
            local_path: record.local_path.clone(),
            sha256: record.sha256.clone(),
            provenance: serde_json::to_value(&record.provenance)?,
            state: VisualState::Verified,
        })
    } else {
        output(&record)
    }
}
#[tokio::main]
async fn main() {
    if let Err(e) = run().await {
        let _ = writeln!(
            io::stderr(),
            "{}",
            serde_json::json!({"error":format!("{e:#}")})
        );
        std::process::exit(1);
    }
}
async fn run() -> Result<()> {
    let cli = Cli::parse();
    let config = Config::load(cli.config.as_deref())?;
    match cli.command {
        Command::Notes { action } => match action {
            Notes::Plan { spec } => output(&planning::build_plan(read(&spec)?)?)?,
            Notes::Audit {
                vault,
                plan,
                receipts,
            } => {
                let report = validation::audit_collection(
                    &vault,
                    &read::<KnowledgePlan>(&plan)?,
                    &read::<Vec<VisualReceipt>>(&receipts)?,
                )?;
                output(&report)?;
                ensure!(
                    report.artifact_complete,
                    "collection has unfulfilled artifact obligations"
                );
            }
            Notes::Publish {
                vault,
                destination,
                plan,
                receipts,
                drafts,
            } => {
                output(&validation::publish_collection(
                    &vault,
                    &destination,
                    &read::<KnowledgePlan>(&plan)?,
                    &read::<Vec<VisualReceipt>>(&receipts)?,
                    &read::<Vec<NoteDraft>>(&drafts)?,
                )?)?;
            }
        },
        Command::Renderers => output(&rendering::families())?,
        Command::Render { spec, output: path } => {
            let artifact = rendering::render(&read(&spec)?)?;
            ensure!(
                path.extension().and_then(|p| p.to_str()) == Some(artifact.extension.as_str()),
                "output extension must match {}",
                artifact.extension
            );
            let mut file = fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(&path)
                .context("create artifact; existing files are preserved")?;
            file.write_all(&artifact.bytes)?;
            file.sync_all()?;
            output(
                &serde_json::json!({"path":path,"mime":artifact.mime,"sha256":scriptorium_core::cache::hash(&artifact.bytes),"renderer":artifact.renderer}),
            )?;
        }
        Command::Config { vault, note } => output(
            &serde_json::json!({"config":config,"attachment_directory":config.attachment_dir(&vault,&note)?}),
        )?,
        Command::Validate { file } => {
            validation::validate_properties(&fs::read_to_string(file)?)?;
            output(
                &serde_json::json!({"valid_properties":true,"educational_review_required":true}),
            )?;
        }
        Command::Research { url, cache } => {
            let report = research::retrieve(url, config, cache).await?;
            output(&report)?;
            ensure!(report.complete, "one or more sources failed");
        }
        Command::Assets { action } => match action {
            Assets::Render {
                vault,
                note,
                spec,
                visual_id,
            } => {
                let spec: serde_json::Value = read(&spec)?;
                let objective = spec
                    .get("objective")
                    .and_then(|x| x.as_str())
                    .context("render specification needs objective")?;
                let artifact = rendering::render(&spec)?;
                if artifact.mime != "image/svg+xml" {
                    bail!(
                        "this backend produces a nonimage artifact; image asset publication requires SVG or a decoded raster"
                    );
                }
                asset_output(
                    store(&vault, &note, &config)?.store_generated(&artifact, objective)?,
                    visual_id,
                )?;
            }
            Assets::Import {
                vault,
                note,
                file,
                mime,
                provenance,
                visual_id,
            } => {
                ensure!(
                    fs::metadata(&file)?.len() <= scriptorium_core::assets::MAX_BYTES as u64,
                    "input exceeds image limit"
                );
                let record = store(&vault, &note, &config)?.store_bytes(
                    &fs::read(file)?,
                    &mime,
                    read(&provenance)?,
                )?;
                asset_output(record, visual_id)?;
            }
            Assets::Fetch {
                vault,
                note,
                url,
                provenance,
                visual_id,
            } => {
                let mut p: Provenance = read(&provenance)?;
                p.validate()?;
                ensure!(
                    p.image_url == url,
                    "provenance image URL must match requested URL"
                );
                let policy = DownloadPolicy {
                    max_bytes: config
                        .max_download_bytes
                        .min(scriptorium_core::assets::MAX_BYTES),
                    timeout_seconds: config.timeout_seconds,
                    max_redirects: 3,
                };
                let downloaded = network::fetch_image(&url, &policy).await?;
                p.retrieved_at = scriptorium_core::cache::now()?;
                p.final_url = Some(downloaded.final_url.clone());
                let record = store(&vault, &note, &config)?.store_bytes(
                    &downloaded.bytes,
                    &downloaded.mime,
                    p,
                )?;
                asset_output(record, visual_id)?;
            }
            Assets::Verify {
                vault,
                note,
                record,
            } => {
                store(&vault, &note, &config)?.verify(&read(&record)?)?;
                output(&serde_json::json!({"verified":true}))?;
            }
            Assets::Embed {
                vault,
                note,
                record,
                alt,
            } => {
                println!(
                    "{}",
                    store(&vault, &note, &config)?.embed(&read(&record)?, &alt)?
                );
            }
        },
    }
    Ok(())
}

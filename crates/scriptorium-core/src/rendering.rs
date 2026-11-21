//! Reproducible, bounded renderers. No renderer infers scientific input data.
use anyhow::{Context, Result, bail, ensure};
use base64::Engine;
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RenderedArtifact {
    pub renderer: String,
    pub mime: String,
    pub extension: String,
    pub bytes: Vec<u8>,
}
pub fn families() -> Value {
    json!({
        "R1":["scientific","coordinates","svg","table"],"R2":["scientific","coordinates","table"],
        "R3":["graph","scientific","coordinates","svg","table"],"R4":["svg","mask","graph","scientific","table"],
        "R5":["graph","mermaid","svg","table","interactive"],"R6":["scientific","table","graph"],
        "R7":["graph","mermaid","table"],"R8":["coordinates","graph","table"],"R9":["external","scientific","graph","table"],
        "R10":["interactive"],"R11":["external","imagegen"],"R12":["table"],
        "limitations":{"imagegen":"requires host adapter; unavailable in deterministic Rust core","external":"use AssetStore and network::fetch_image with provenance","mermaid":"validated source; host rendering pending","interactive":"fixed state viewer; browser execution untested"}
    })
}
fn text<'a>(v: &'a Value, key: &str) -> Result<&'a str> {
    let s = v[key]
        .as_str()
        .with_context(|| format!("missing string {key}"))?;
    ensure!(
        !s.trim().is_empty() && s.len() <= 4096,
        "empty or oversized {key}"
    );
    Ok(s)
}
fn arr<'a>(v: &'a Value, key: &str) -> Result<&'a Vec<Value>> {
    v[key]
        .as_array()
        .with_context(|| format!("missing array {key}"))
}
fn num(v: &Value) -> Result<f64> {
    let x = v.as_f64().context("expected number")?;
    ensure!(
        x.is_finite() && x.abs() <= 1e100,
        "nonfinite or unbounded numeric value"
    );
    Ok(x)
}
fn esc(s: &str) -> String {
    s.replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
        .replace('"', "&quot;")
        .replace('\'', "&apos;")
}
fn tick(x: f64) -> String {
    if x != 0. && (x.abs() < 0.001 || x.abs() >= 1e6) {
        format!("{x:.3e}")
    } else {
        format!("{x:.4}")
    }
}
fn label(out: &mut String, x: f64, y: f64, s: &str) {
    out.push_str(&format!(
        "<text x=\"{x:.4}\" y=\"{y:.4}\" font-size=\"12\" fill=\"#172033\">{}</text>",
        esc(s)
    ));
}
fn start(title: &str, w: u32, h: u32) -> String {
    format!(
        "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {w} {h}\" role=\"img\"><title>{}</title><rect width=\"{w}\" height=\"{h}\" fill=\"white\"/>",
        esc(title)
    )
}

pub fn render(spec: &Value) -> Result<RenderedArtifact> {
    ensure!(
        serde_json::to_vec(spec)?.len() <= 1024 * 1024,
        "render specification exceeds byte limit"
    );
    let objective = text(spec, "objective")?;
    let backend = text(spec, "renderer")?;
    let (body, mime, extension) = match backend {
        "scientific" => (scientific(spec, objective)?, "image/svg+xml", "svg"),
        "graph" => (graph(spec, objective, false)?, "image/svg+xml", "svg"),
        "coordinates" => (graph(spec, objective, true)?, "image/svg+xml", "svg"),
        "svg" => (architecture(spec, objective)?, "image/svg+xml", "svg"),
        "mask" => (mask(spec, objective)?, "image/svg+xml", "svg"),
        "table" => (
            table(spec.get("table").unwrap_or(spec))?,
            "text/markdown",
            "md",
        ),
        "mermaid" => (mermaid(spec)?, "text/plain", "mmd"),
        "interactive" => (interactive(spec, objective)?, "text/html", "html"),
        "external" => {
            bail!("external figures require explicit provenance and AssetStore download/import")
        }
        "imagegen" => bail!("imagegen requires a host adapter; unavailable in deterministic core"),
        _ => bail!("unsupported renderer {backend}"),
    };
    if mime == "image/svg+xml" {
        inspect_svg(body.as_bytes())?;
    }
    Ok(RenderedArtifact {
        renderer: backend.into(),
        mime: mime.into(),
        extension: extension.into(),
        bytes: body.into_bytes(),
    })
}

fn scientific(spec: &Value, title: &str) -> Result<String> {
    let xlabel = text(spec, "xlabel")?;
    let ylabel = text(spec, "ylabel")?;
    let units = text(spec, "units")?;
    text(spec, "interpretation")?;
    ensure!(
        spec.get("error_bars").is_none() || spec["error_bars"] == false,
        "error bars require a capable external backend"
    );
    if spec["empirical"] == true {
        ensure!(
            spec["verified_comparable_claims"]
                .as_array()
                .is_some_and(|a| !a.is_empty()),
            "empirical series require verified comparable claims"
        );
    }
    if let Some(equation) = spec["equation"].as_str() {
        ensure!(
            equation.len() <= 2000
                && equation
                    .chars()
                    .filter(|c| !c.is_alphanumeric() && !c.is_whitespace())
                    .count()
                    <= 200,
            "equation exceeds validation budget"
        );
        let mut depth = 0usize;
        for c in equation.chars() {
            if c == '(' {
                depth += 1;
                ensure!(depth <= 32, "equation nesting limit");
            } else if c == ')' {
                depth = depth.saturating_sub(1);
            }
        }
    }
    let expression = spec["equation"]
        .as_str()
        .map(|s| s.replace("**", "^").parse::<meval::Expr>())
        .transpose()?;
    let evaluate = |x: f64| -> Result<f64> {
        let mut ctx = meval::Context::new();
        ctx.var("x", x);
        if let Some(parameters) = spec["parameters"].as_object() {
            for (name, value) in parameters {
                ensure!(name != "x", "parameter cannot override x");
                ctx.var(name, num(value)?);
            }
        }
        let y = expression
            .as_ref()
            .context("equation missing")?
            .eval_with_context(ctx)?;
        ensure!(
            y.is_finite() && y.abs() <= 1e100,
            "equation produced nonfinite or unbounded number"
        );
        Ok(y)
    };
    let mut series: BTreeMap<String, Vec<(f64, f64)>> = BTreeMap::new();
    if let Some(data) = spec["data"].as_object() {
        for (name, points) in data {
            let values = points.as_array().context("series must be an array")?;
            ensure!(
                (2..=10_000).contains(&values.len()),
                "series needs 2-10000 samples"
            );
            let mut parsed = Vec::new();
            for p in values {
                let pair = p.as_array().context("point must be [x,y]")?;
                ensure!(pair.len() == 2, "point must have exactly two coordinates");
                let (x, y) = (num(&pair[0])?, num(&pair[1])?);
                if expression.is_some() {
                    let expected = evaluate(x)?;
                    ensure!(
                        (y - expected).abs() <= 1e-12 + 1e-9 * y.abs().max(expected.abs()),
                        "series disagrees with equation"
                    );
                }
                parsed.push((x, y));
            }
            series.insert(name.clone(), parsed);
        }
    } else {
        let xs = arr(spec, "x_values")?;
        ensure!(
            (2..=10_000).contains(&xs.len()),
            "equation needs bounded sample grid"
        );
        let points = xs
            .iter()
            .map(|x| {
                let x = num(x)?;
                Ok((x, evaluate(x)?))
            })
            .collect::<Result<Vec<_>>>()?;
        series.insert(spec["label"].as_str().unwrap_or("equation").into(), points);
    }
    ensure!(
        !series.is_empty() && series.len() <= 12,
        "plot requires 1-12 series"
    );
    let all: Vec<_> = series.values().flatten().collect();
    let xmin = all.iter().map(|p| p.0).fold(f64::INFINITY, f64::min);
    let xmax = all.iter().map(|p| p.0).fold(f64::NEG_INFINITY, f64::max);
    let mut ymin = all.iter().map(|p| p.1).fold(f64::INFINITY, f64::min);
    let mut ymax = all.iter().map(|p| p.1).fold(f64::NEG_INFINITY, f64::max);
    ensure!(xmax > xmin, "plot needs a nonzero x range");
    if ymax == ymin {
        let padding = (ymin.abs() * 0.05).max(1.);
        ymin -= padding;
        ymax += padding;
    }
    let mut out = start(title, 800, 540);
    label(&mut out, 70., 24., title);
    label(&mut out, 260., 425., xlabel);
    label(&mut out, 5., 44., ylabel);
    label(&mut out, 70., 450., &format!("Units: {units}"));
    out.push_str("<path d=\"M70 50 V360 H740\" fill=\"none\" stroke=\"#172033\"/>");
    for i in 0..=5 {
        let t = i as f64 / 5.;
        label(
            &mut out,
            70. + 670. * t,
            385.,
            &tick(xmin + (xmax - xmin) * t),
        );
        label(
            &mut out,
            2.,
            360. - 310. * t,
            &tick(ymin + (ymax - ymin) * t),
        );
    }
    let colors = [
        "#245ac6", "#b93b26", "#08795c", "#7434aa", "#d97706", "#be185d", "#0891b2", "#65a30d",
        "#4f46e5", "#57534e", "#c026d3", "#0f766e",
    ];
    for (i, (name, points)) in series.iter().enumerate() {
        let coords = points
            .iter()
            .map(|(x, y)| {
                format!(
                    "{:.4},{:.4}",
                    70. + (x - xmin) / (xmax - xmin) * 670.,
                    360. - (y - ymin) / (ymax - ymin) * 310.
                )
            })
            .collect::<Vec<_>>()
            .join(" ");
        out.push_str(&format!(
            "<polyline points=\"{coords}\" fill=\"none\" stroke=\"{}\" stroke-width=\"2\"/>",
            colors[i]
        ));
        label(
            &mut out,
            70. + (i % 4) as f64 * 180.,
            475. + (i / 4) as f64 * 20.,
            name,
        );
    }
    out.push_str("</svg>");
    Ok(out)
}

fn graph_inputs(spec: &Value) -> Result<(&Vec<Value>, &Vec<Value>)> {
    let nodes = arr(spec, "nodes")?;
    let edges = arr(spec, "edges")?;
    ensure!(
        !nodes.is_empty() && nodes.len() <= 100 && edges.len() <= 300,
        "graph limits"
    );
    let mut ids = BTreeSet::new();
    for node in nodes {
        let id = text(node, "id")?;
        ensure!(
            id.chars().all(|c| c.is_ascii_alphanumeric() || c == '_') && ids.insert(id),
            "invalid/duplicate node id"
        );
        ensure!(text(node, "label")?.len() <= 120, "label exceeds limit");
    }
    for edge in edges {
        let a = text(edge, "source")?;
        let b = text(edge, "target")?;
        ensure!(
            a != b && ids.contains(a) && ids.contains(b),
            "unknown edge endpoint or unsupported self-loop"
        );
    }
    Ok((nodes, edges))
}
fn graph(spec: &Value, title: &str, coordinates: bool) -> Result<String> {
    let (nodes, edges) = graph_inputs(spec)?;
    let mut pos = BTreeMap::new();
    let (w, h) = if coordinates {
        (700, 660)
    } else {
        (1000, nodes.len().div_ceil(4) as u32 * 140 + 60)
    };
    let mut out = start(title, w, h);
    if coordinates {
        let units = text(spec, "units")?;
        label(
            &mut out,
            10.,
            25.,
            &format!("Equal axis scale; units: {units}"),
        );
        let points = nodes
            .iter()
            .map(|n| Ok((text(n, "id")?, num(&n["x"])?, num(&n["y"])?)))
            .collect::<Result<Vec<_>>>()?;
        let xmin = points.iter().map(|p| p.1).fold(f64::INFINITY, f64::min);
        let ymin = points.iter().map(|p| p.2).fold(f64::INFINITY, f64::min);
        let extent = points
            .iter()
            .map(|p| (p.1 - xmin).max(p.2 - ymin))
            .fold(1., f64::max);
        for (id, x, y) in points {
            pos.insert(
                id,
                (
                    60. + 500. * (x - xmin) / extent,
                    580. - 500. * (y - ymin) / extent,
                ),
            );
        }
    } else {
        for (i, node) in nodes.iter().enumerate() {
            pos.insert(
                text(node, "id")?,
                (120. + (i % 4) as f64 * 240., 75. + (i / 4) as f64 * 140.),
            );
        }
    }
    for edge in edges {
        let (x1, y1) = pos[text(edge, "source")?];
        let (x2, y2) = pos[text(edge, "target")?];
        out.push_str(&format!(
            "<line x1=\"{x1:.4}\" y1=\"{y1:.4}\" x2=\"{x2:.4}\" y2=\"{y2:.4}\" stroke=\"#475569\"/>"
        ));
        if !coordinates {
            let angle = (y2 - y1).atan2(x2 - x1);
            let bound =
                (90. / angle.cos().abs().max(1e-12)).min(35. / angle.sin().abs().max(1e-12));
            let tx = x2 - (bound + 2.) * angle.cos();
            let ty = y2 - (bound + 2.) * angle.sin();
            out.push_str(&format!(
                "<polygon points=\"{tx:.4},{ty:.4} {:.4},{:.4} {:.4},{:.4}\" fill=\"#475569\"/>",
                tx - 10. * (angle - 0.5).cos(),
                ty - 10. * (angle - 0.5).sin(),
                tx - 10. * (angle + 0.5).cos(),
                ty - 10. * (angle + 0.5).sin()
            ));
        }
        if let Some(s) = edge["label"].as_str() {
            label(&mut out, (x1 + x2) / 2., (y1 + y2) / 2. - 12., s);
        }
    }
    for node in nodes {
        let (x, y) = pos[text(node, "id")?];
        if coordinates {
            out.push_str(&format!(
                "<circle cx=\"{x:.4}\" cy=\"{y:.4}\" r=\"4\" fill=\"#245ac6\"/>"
            ));
            label(
                &mut out,
                x + 6.,
                y - 7.,
                &format!("{} ({}, {})", text(node, "label")?, node["x"], node["y"]),
            );
        } else {
            out.push_str(&format!("<rect x=\"{}\" y=\"{}\" width=\"180\" height=\"70\" rx=\"7\" fill=\"#eef3ff\" stroke=\"#245ac6\"/>",x-90.,y-35.));
            let chars: Vec<_> = text(node, "label")?.chars().collect();
            for (i, chunk) in chars.chunks(25).enumerate() {
                label(
                    &mut out,
                    x - 82.,
                    y - 17. + i as f64 * 12.,
                    &chunk.iter().collect::<String>(),
                );
            }
        }
    }
    out.push_str("</svg>");
    Ok(out)
}

fn string_set(v: &Value) -> Result<BTreeSet<String>> {
    v.as_array()
        .context("expected string array")?
        .iter()
        .map(|s| Ok(s.as_str().context("expected string")?.to_owned()))
        .collect()
}
/// Information-flow validation preserves transitive provenance and ownership.
pub fn validate_flow(flow: &Value) -> Result<()> {
    let mut known = string_set(&flow["external_inputs"])?;
    let mut provenance: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
    let branches = arr(flow, "branches")?;
    ensure!(
        !branches.is_empty() && branches.len() <= 100,
        "flow needs bounded branches"
    );
    let mut ids = BTreeSet::new();
    for b in branches {
        ensure!(ids.insert(text(b, "id")?), "duplicate branch id");
        for field in ["labels", "readout", "shared_parameters", "gradient_owner"] {
            ensure!(b.get(field).is_some(), "missing branch field {field}");
        }
        let inputs = string_set(&b["inputs"])?;
        ensure!(inputs.is_subset(&known), "unknown flow input");
        let mut reachable = inputs.clone();
        for i in &inputs {
            if let Some(p) = provenance.get(i) {
                reachable.extend(p.iter().cloned());
            }
        }
        let allowed = string_set(&b["accessible"])?;
        let required = string_set(&b["requires"])?;
        let forbidden = string_set(&b["forbidden"])?;
        let attention = string_set(&b["attention_permissions"])?;
        ensure!(
            required.is_subset(&allowed)
                && required.is_subset(&reachable)
                && allowed.is_subset(&reachable)
                && attention.is_subset(&allowed)
                && reachable.is_disjoint(&forbidden),
            "flow access/provenance contradiction"
        );
        for output in string_set(&b["outputs"])? {
            ensure!(known.insert(output.clone()), "multiply owned flow output");
            provenance.insert(output, reachable.clone());
        }
    }
    Ok(())
}
fn architecture(spec: &Value, title: &str) -> Result<String> {
    if let Some(flow) = spec.get("flow") {
        validate_flow(flow)?;
        let branches = arr(flow, "branches")?;
        let mut out = start(title, 900, 80 + branches.len() as u32 * 120);
        for (i, b) in branches.iter().enumerate() {
            let y = 55. + i as f64 * 120.;
            let labels = [
                string_set(&b["inputs"])?
                    .into_iter()
                    .collect::<Vec<_>>()
                    .join(", "),
                text(b, "id")?.into(),
                string_set(&b["outputs"])?
                    .into_iter()
                    .collect::<Vec<_>>()
                    .join(", "),
            ];
            for (j, s) in labels.iter().enumerate() {
                let x = 10. + j as f64 * 295.;
                out.push_str(&format!("<rect x=\"{x}\" y=\"{y}\" width=\"260\" height=\"55\" fill=\"#eef3ff\" stroke=\"#245ac6\"/>"));
                label(&mut out, x + 8., y + 30., s);
                if j < 2 {
                    out.push_str(&format!("<path d=\"M{} {} h34 l-6 -5 m6 5 l-6 5\" fill=\"none\" stroke=\"#172033\"/>",x+260.,y+27.));
                }
            }
            label(
                &mut out,
                300.,
                y + 76.,
                &format!(
                    "readout={}; gradient={}; forbidden={}",
                    b["readout"], b["gradient_owner"], b["forbidden"]
                ),
            );
        }
        out.push_str("</svg>");
        return Ok(out);
    }
    let components = arr(spec, "components")?;
    ensure!(
        !components.is_empty() && components.len() <= 16,
        "architecture needs 1-16 components; larger layouts require graph backend"
    );
    let mut out = start(title, components.len() as u32 * 220, 180);
    for (i, c) in components.iter().enumerate() {
        let x = 10 + i * 220;
        out.push_str(&format!("<rect x=\"{x}\" y=\"30\" width=\"180\" height=\"90\" rx=\"8\" fill=\"#eef3ff\" stroke=\"#245ac6\"/>"));
        label(&mut out, (x + 8) as f64, 60., text(c, "label")?);
        label(&mut out, (x + 8) as f64, 90., text(c, "shape")?);
        if i + 1 < components.len() {
            out.push_str(&format!(
                "<path d=\"M{} 75 h35 l-6 -5 m6 5 l-6 5\" fill=\"none\" stroke=\"#172033\"/>",
                x + 180
            ));
        }
    }
    out.push_str("</svg>");
    Ok(out)
}
fn mask(spec: &Value, title: &str) -> Result<String> {
    let m = if let Some(flow) = spec.get("flow") {
        validate_flow(flow)?;
        &flow["mask"]
    } else {
        spec.get("mask")
            .context("mask requires segment permissions")?
    };
    let segments = arr(m, "segments")?;
    ensure!(segments.len() <= 100, "segment limit");
    let permissions = m["permissions"]
        .as_object()
        .context("mask permissions missing")?;
    let causal = m["causal"].as_bool().context("mask causal flag missing")?;
    let mut ids = BTreeSet::new();
    let mut tokens = Vec::new();
    for segment in segments {
        let id = text(segment, "id")?;
        ensure!(ids.insert(id.to_string()), "duplicate segment id");
        let count = segment["length"]
            .as_u64()
            .context("invalid segment length")?;
        ensure!(
            count <= 64 && tokens.len() + count as usize <= 64,
            "mask limited to 64 tokens"
        );
        for j in 0..count {
            tokens.push((id.to_owned(), j));
        }
    }
    ensure!(
        !tokens.is_empty() && permissions.keys().cloned().collect::<BTreeSet<_>>() == ids,
        "missing/unknown segment permission"
    );
    let mut allowed = BTreeMap::new();
    for (id, p) in permissions {
        let p = string_set(p)?;
        ensure!(p.is_subset(&ids), "unknown permitted segment");
        allowed.insert(id.clone(), p);
    }
    let matrix: Vec<Vec<bool>> = tokens
        .iter()
        .enumerate()
        .map(|(i, (q, _))| {
            tokens
                .iter()
                .enumerate()
                .map(|(j, (k, _))| allowed[q].contains(k) && (!causal || j <= i))
                .collect()
        })
        .collect();
    if let Some(expected) = m.get("expected") {
        ensure!(
            *expected == serde_json::to_value(&matrix)?,
            "mask contradicts expected matrix"
        );
    }
    if let Some(indices) = m["readout_indices"].as_array() {
        for i in indices {
            ensure!(
                i.as_u64().is_some_and(|v| v < tokens.len() as u64),
                "readout index outside context"
            );
        }
    }
    let mut out = start(
        title,
        tokens.len() as u32 * 28 + 210,
        tokens.len() as u32 * 28 + 130,
    );
    for (i, row) in matrix.iter().enumerate() {
        for (j, cell) in row.iter().enumerate() {
            out.push_str(&format!(
                "<rect x=\"{}\" y=\"{}\" width=\"27\" height=\"27\" fill=\"{}\"/>",
                120 + j * 28,
                60 + i * 28,
                if *cell { "#245ac6" } else { "#eeeeee" }
            ));
        }
        label(
            &mut out,
            4.,
            78. + i as f64 * 28.,
            &format!("q {}:{}", tokens[i].0, tokens[i].1),
        );
        label(&mut out, 120. + i as f64 * 28., 45., &format!("k{i}"));
    }
    label(
        &mut out,
        10.,
        tokens.len() as f64 * 28. + 100.,
        "Rows=query; columns=key. Blue=allowed; gray=forbidden.",
    );
    out.push_str("</svg>");
    Ok(out)
}

fn table(spec: &Value) -> Result<String> {
    let objective = text(spec, "objective")?;
    let interpretation = text(spec, "interpretation")?;
    let columns: Vec<String> = if let Some(kind) = spec["type"].as_str() {
        let names: &[&str] = match kind {
            "definition" => &["term", "meaning"],
            "variable" => &["symbol", "meaning", "domain", "units"],
            "comparison" => &["method", "criterion", "value", "conditions", "source"],
            "execution" => &["step", "state", "output"],
            "complexity" => &["method", "time", "space", "assumptions"],
            "experimental" => &[
                "method",
                "metric",
                "value",
                "units",
                "conditions",
                "source",
                "uncertainty",
            ],
            "architecture" => &["component", "input", "output", "operation"],
            "failure" => &[
                "symptom",
                "latent_property",
                "candidate_cause",
                "diagnostic",
                "evidence_status",
                "remediation",
            ],
            "decision" => &["constraint", "alternative", "tradeoff"],
            "evidence" => &["claim", "source", "location"],
            "prerequisite" => &["concept", "dependency", "knowledge"],
            "formula" => &["formula", "symbols", "assumptions", "applicability"],
            _ => bail!("unknown table type"),
        };
        names.iter().map(|s| s.to_string()).collect()
    } else {
        arr(spec, "columns")?
            .iter()
            .map(|c| {
                Ok(c.get("name")
                    .unwrap_or(c)
                    .as_str()
                    .context("column must have name")?
                    .to_owned())
            })
            .collect::<Result<Vec<_>>>()?
    };
    let rows = arr(spec, "rows")?;
    ensure!(
        !columns.is_empty() && columns.len() <= 32 && !rows.is_empty() && rows.len() <= 1000,
        "table dimensions exceed limits"
    );
    let cell = |v: &Value| -> Result<String> {
        let s = if let Some(s) = v.as_str() {
            s.to_owned()
        } else {
            v.to_string()
        };
        ensure!(
            !s.trim().is_empty()
                && s.len() <= 4096
                && !v.is_null()
                && !s.contains(['\n', '\r'])
                && !s.contains("```")
                && !matches!(
                    s.to_ascii_lowercase().as_str(),
                    "fast" | "slow" | "good" | "bad"
                ),
            "table has missing, unqualified or multiline cell"
        );
        Ok(s.replace('|', "&#124;"))
    };
    if matches!(spec["type"].as_str(), Some("comparison" | "experimental")) {
        for key in [
            "conditions",
            "units",
            if spec["type"] == "comparison" {
                "criterion"
            } else {
                "metric"
            },
        ] {
            let values: BTreeSet<_> = rows.iter().map(|r| r[key].to_string()).collect();
            ensure!(
                values.len() <= 1,
                "incomparable table conditions, metrics or units"
            );
        }
    }
    let mut out = format!(
        "{objective}\n\n| {} |\n| {} |\n",
        columns.join(" | "),
        vec!["---"; columns.len()].join(" | ")
    );
    for row in rows {
        let cells = if let Some(values) = row.as_array() {
            ensure!(values.len() == columns.len(), "table row width mismatch");
            values.iter().map(cell).collect::<Result<Vec<_>>>()?
        } else {
            ensure!(row.is_object(), "row must be object or array");
            columns
                .iter()
                .map(|c| cell(&row[c]))
                .collect::<Result<Vec<_>>>()?
        };
        out.push_str(&format!("| {} |\n", cells.join(" | ")));
    }
    out.push_str(&format!("\n{interpretation}\n"));
    Ok(out)
}
fn mermaid(spec: &Value) -> Result<String> {
    let (nodes, edges) = graph_inputs(spec)?;
    let safe = |s: &str| -> String {
        s.chars()
            .map(|c| {
                if c.is_alphanumeric() || " .,()-_".contains(c) {
                    c.to_string()
                } else {
                    format!("#{};", c as u32)
                }
            })
            .collect()
    };
    let mut out = "flowchart TD\n".to_owned();
    for n in nodes {
        out.push_str(&format!(
            "  {}[\"{}\"]\n",
            text(n, "id")?,
            safe(text(n, "label")?)
        ));
    }
    for e in edges {
        out.push_str(&format!(
            "  {} -->|\"{}\"| {}\n",
            text(e, "source")?,
            safe(e["label"].as_str().unwrap_or("")),
            text(e, "target")?
        ));
    }
    Ok(out)
}
fn interactive(spec: &Value, title: &str) -> Result<String> {
    let frames = arr(spec, "frames")?;
    ensure!(
        (2..=200).contains(&frames.len()),
        "interactive needs 2-200 frames"
    );
    for frame in frames {
        text(frame, "label")?;
        ensure!(
            frame["state"]
                .as_str()
                .context("frame state must be textual")?
                .len()
                <= 10_000,
            "frame exceeds limit"
        );
    }
    let data = serde_json::to_string(frames)?
        .replace('<', "\\u003c")
        .replace('>', "\\u003e")
        .replace('&', "\\u0026");
    let script = format!(
        "const frames={data};const slider=document.getElementById('step');function show(){{const f=frames[Number(slider.value)];document.getElementById('label').textContent=f.label;document.getElementById('state').textContent=f.state;}}slider.addEventListener('input',show);show();"
    );
    let hash = base64::engine::general_purpose::STANDARD.encode(Sha256::digest(script.as_bytes()));
    Ok(format!(
        "<!doctype html><html><head><meta charset=\"utf-8\"><meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; script-src 'sha256-{hash}'; base-uri 'none'\"><title>{}</title></head><body><h1>{}</h1><label>Step <input id=\"step\" type=\"range\" min=\"0\" max=\"{}\" value=\"0\"></label><h2 id=\"label\"></h2><pre id=\"state\"></pre><script>{script}</script></body></html>",
        esc(title),
        esc(title),
        frames.len() - 1
    ))
}

/// Strict passive SVG subset; no scripts, URLs, styles, entities or foreign XML.
pub fn inspect_svg(bytes: &[u8]) -> Result<crate::assets::ImageInspection> {
    ensure!(
        !bytes.is_empty() && bytes.len() <= crate::assets::MAX_BYTES,
        "SVG byte limit"
    );
    let mut reader = quick_xml::Reader::from_reader(bytes);
    let mut depth = 0usize;
    let mut root_seen = false;
    let mut closed = false;
    let mut dimensions = None;
    let mut namespace = false;
    loop {
        let event = reader.read_event()?;
        let is_empty = matches!(&event, quick_xml::events::Event::Empty(_));
        match event {
            quick_xml::events::Event::Start(e) | quick_xml::events::Event::Empty(e) => {
                ensure!(!closed, "SVG has multiple roots");
                let name = std::str::from_utf8(e.name().as_ref())?.to_owned();
                ensure!(
                    matches!(
                        name.as_str(),
                        "svg"
                            | "title"
                            | "desc"
                            | "rect"
                            | "text"
                            | "path"
                            | "polyline"
                            | "polygon"
                            | "line"
                            | "circle"
                            | "ellipse"
                            | "g"
                    ),
                    "active/unknown SVG element"
                );
                ensure!(name != "svg" || !root_seen, "nested SVG is unsupported");
                if !root_seen {
                    ensure!(name == "svg", "root must be SVG");
                    root_seen = true;
                }
                for attr in e.attributes() {
                    let attr = attr?;
                    let key = std::str::from_utf8(attr.key.as_ref())?;
                    let value = attr.unescape_value()?.to_string();
                    let lower = value.to_ascii_lowercase();
                    ensure!(
                        !key.to_ascii_lowercase().starts_with("on")
                            && !key.ends_with("href")
                            && key != "style"
                            && !lower.contains("url")
                            && !lower.contains("javascript:")
                            && !lower.contains("data:"),
                        "unsafe SVG attribute"
                    );
                    ensure!(
                        matches!(
                            key,
                            "xmlns"
                                | "viewBox"
                                | "role"
                                | "x"
                                | "y"
                                | "x1"
                                | "y1"
                                | "x2"
                                | "y2"
                                | "width"
                                | "height"
                                | "rx"
                                | "ry"
                                | "cx"
                                | "cy"
                                | "r"
                                | "fill"
                                | "stroke"
                                | "stroke-width"
                                | "font-size"
                                | "points"
                                | "d"
                                | "text-anchor"
                        ),
                        "unknown SVG attribute"
                    );
                    if name == "svg" && key == "xmlns" {
                        ensure!(
                            value == "http://www.w3.org/2000/svg",
                            "invalid SVG namespace"
                        );
                        namespace = true;
                    }
                    if name == "svg" && key == "viewBox" {
                        let nums = value
                            .split_whitespace()
                            .map(|s| s.parse::<f64>())
                            .collect::<std::result::Result<Vec<_>, _>>()?;
                        ensure!(
                            nums.len() == 4
                                && nums.iter().all(|v| v.is_finite())
                                && nums[2] > 0.
                                && nums[3] > 0.
                                && nums[2] <= 10_000.
                                && nums[3] <= 10_000.,
                            "invalid SVG dimensions"
                        );
                        dimensions = Some(crate::assets::ImageInspection {
                            width: nums[2].ceil() as u32,
                            height: nums[3].ceil() as u32,
                        });
                    }
                }
                if !is_empty {
                    depth += 1;
                    ensure!(depth <= 100, "SVG nesting limit");
                } else if depth == 0 {
                    closed = true;
                }
            }
            quick_xml::events::Event::End(_) => {
                ensure!(depth > 0, "unbalanced SVG");
                depth -= 1;
                if depth == 0 {
                    closed = true;
                }
            }
            quick_xml::events::Event::Text(t) => {
                let text = t.decode()?;
                if depth == 0 {
                    ensure!(text.trim().is_empty(), "text outside SVG root");
                }
            }
            quick_xml::events::Event::GeneralRef(r) => {
                let name = std::str::from_utf8(r.as_ref())?;
                ensure!(
                    depth > 0 && matches!(name, "lt" | "gt" | "amp" | "quot" | "apos"),
                    "unsupported SVG entity"
                );
            }
            quick_xml::events::Event::Eof => break,
            _ => bail!("SVG declarations, entities and active content are not supported"),
        }
    }
    ensure!(
        root_seen && closed && depth == 0 && namespace,
        "missing/unclosed SVG root or namespace"
    );
    dimensions.context("SVG needs viewBox")
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn constant_series_has_labeled_padded_range() {
        let s = json!({"renderer":"scientific","objective":"Constant signal","data":{"constant":[[0,2],[1,2]]},"xlabel":"time","ylabel":"amplitude","units":"seconds, volts","interpretation":"Constant amplitude"});
        let out = String::from_utf8(render(&s).unwrap().bytes).unwrap();
        assert!(out.contains("1.0000"));
        assert!(out.contains("3.0000"));
        assert!(!out.contains("NaN"));
    }
    #[test]
    fn scientific_equation_and_mismatch() {
        let s = json!({"renderer":"scientific","objective":"Square curve","equation":"x**2","x_values":[0,1,2],"xlabel":"x","ylabel":"y","units":"dimensionless","interpretation":"Quadratic growth"});
        let a = render(&s).unwrap();
        assert!(String::from_utf8(a.bytes).unwrap().contains("polyline"));
        let mut bad = s;
        bad["data"] = json!({"wrong":[[0,0],[1,8]]});
        assert!(render(&bad).is_err());
    }
    #[test]
    fn graph_escape_and_unknown_edge() {
        let mut s = json!({"renderer":"graph","objective":"Flow","nodes":[{"id":"A","label":"<script>"},{"id":"B","label":"Output"}],"edges":[{"source":"A","target":"B"}]});
        let out = String::from_utf8(render(&s).unwrap().bytes).unwrap();
        assert!(out.contains("&lt;script&gt;"));
        s["edges"][0]["target"] = json!("unknown");
        assert!(render(&s).is_err());
    }
    #[test]
    fn causal_mask_from_permissions() {
        let s = json!({"renderer":"mask","objective":"Permissions","mask":{"segments":[{"id":"text","length":2}],"permissions":{"text":["text"]},"causal":true,"expected":[[true,false],[true,true]]}});
        assert!(render(&s).is_ok());
        let mut bad = s;
        bad["mask"]["expected"] = json!([[true, true], [true, true]]);
        assert!(render(&bad).is_err());
    }
    #[test]
    fn rejects_active_svg() {
        for s in [
            "<svg viewBox=\"0 0 10 10\"><script>x</script></svg>",
            "<!DOCTYPE svg><svg viewBox=\"0 0 10 10\"></svg>",
            "<svg viewBox=\"0 0 10 10\" onload=\"x\"></svg>",
        ] {
            assert!(inspect_svg(s.as_bytes()).is_err());
        }
    }
    #[test]
    fn interactive_escapes_script() {
        let s = json!({"renderer":"interactive","objective":"Steps","frames":[{"label":"A","state":"</script><script>alert(1)</script>"},{"label":"B","state":"done"}]});
        let a = String::from_utf8(render(&s).unwrap().bytes).unwrap();
        assert!(a.contains("script-src 'sha256-"));
        assert!(!a.contains("<script>alert"));
    }
}

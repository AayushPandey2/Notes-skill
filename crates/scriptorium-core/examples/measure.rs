use scriptorium_core::{
    assets::AssetStore,
    cache::{Cache, hash},
    rendering::render,
    validation::validate_properties,
};
use serde_json::json;
use std::{hint::black_box, time::Instant};
fn sample(mut run: impl FnMut(), count: u32) -> Vec<f64> {
    run();
    (0..7)
        .map(|_| {
            let start = Instant::now();
            for _ in 0..count {
                run();
            }
            start.elapsed().as_secs_f64() * 1000.0 / f64::from(count)
        })
        .collect()
}
fn main() -> anyhow::Result<()> {
    let spec = json!({"renderer":"scientific","objective":"Quadratic growth","data":{"square":[[-2,4],[-1,1],[0,0],[1,1],[2,4]]},"xlabel":"x","ylabel":"square","units":"dimensionless","interpretation":"A reproducible original function"});
    let note = "---\ntopic: Quadratics\ntags: [topic/quadratics]\nmaster_topic: Mathematics\ndomain: Mathematics\nnote_type: deep-notes\n---\n# Quadratics\n";
    let temp = tempfile::tempdir()?;
    let store = AssetStore::new(temp.path(), "assets")?;
    let artifact = render(&spec)?;
    let record = store.store_generated(&artifact, "Quadratic growth")?;
    let cache = Cache::new(temp.path().join("cache"), 60)?;
    cache.put("fixture", &spec)?;
    let report = json!({
        "scientific_render_ms":sample(|| { black_box(render(black_box(&spec)).unwrap()); },100),
        "properties_validation_ms":sample(|| { validate_properties(black_box(note)).unwrap(); },100),
        "sha256_64k_ms":sample(|| { black_box(hash(black_box(&[42u8;65536]))); },1000),
        "asset_verify_ms":sample(|| { store.verify(black_box(&record)).unwrap(); },100),
        "cache_lookup_ms":sample(|| { black_box(cache.get::<serde_json::Value>("fixture").unwrap()); },100),
        "scope":"Local deterministic operations only. No network, model reasoning, scientific review or full generation latency."
    });
    println!("{}", serde_json::to_string_pretty(&report)?);
    Ok(())
}

use serde_json::{Value, json};
use std::{fs, path::Path, process::Command};

fn invoke(args: &[&str]) -> Value {
    let out = Command::new(env!("CARGO_BIN_EXE_scribe"))
        .args(args)
        .output()
        .unwrap();
    assert!(
        out.status.success(),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    serde_json::from_slice(&out.stdout).unwrap()
}
fn write(path: &Path, value: &Value) {
    fs::write(path, serde_json::to_vec_pretty(value).unwrap()).unwrap();
}

#[test]
fn cli_publishes_complementary_local_visuals_across_domains() {
    for (topic, domain, title, values, objective) in [
        (
            "Quadratics",
            "Mathematics",
            "Function evaluation",
            vec![[0, 0], [1, 1], [2, 4]],
            "Compare squared values",
        ),
        (
            "Resistance",
            "Engineering",
            "Circuit flow",
            vec![[0, 0], [1, 2], [2, 4]],
            "Interpret voltage versus current",
        ),
        (
            "Attention",
            "Artificial intelligence",
            "Weighted aggregation",
            vec![[0, 1], [1, 2], [2, 3]],
            "Inspect a supplied score series",
        ),
        (
            "Binary search",
            "Computer science",
            "Search states",
            vec![[0, 8], [1, 4], [2, 2]],
            "Trace remaining candidates",
        ),
        (
            "Historical chronology",
            "History",
            "Event ordering",
            vec![[0, 1], [1, 2], [2, 3]],
            "Compare supplied chronological positions",
        ),
    ] {
        let temp = tempfile::tempdir().unwrap();
        let vault = temp.path().to_str().unwrap();
        fs::create_dir(temp.path().join(".obsidian")).unwrap();
        fs::write(
            temp.path().join(".obsidian/app.json"),
            r#"{"attachmentFolderPath":"figures"}"#,
        )
        .unwrap();
        let mut receipts = Vec::new();
        let mut embeds = String::new();
        for (index, spec) in [
            json!({"renderer":"scientific","objective":objective,"data":{"fixture":values},"xlabel":"Input","ylabel":"Output","units":"fixture units","interpretation":"Supplied numerical example, not empirical evidence"}),
            json!({"renderer":"graph","objective":title,"nodes":[{"id":"input","label":"Input"},{"id":"step","label":title},{"id":"output","label":"Output"}],"edges":[{"source":"input","target":"step"},{"source":"step","target":"output"}]}),
        ].iter().enumerate() {
            let spec_path = temp.path().join(format!("spec-{index}.json")); write(&spec_path,spec);
            let id = format!("v{index}");
            let receipt = invoke(&["assets","render","--vault",vault,"--note","Collection/01.md","--spec",spec_path.to_str().unwrap(),"--visual-id",&id]);
            assert_eq!(receipt["state"],"verified");
            let asset = receipt["local_path"].as_str().unwrap().replace('\\',"/");
            assert!(asset.starts_with("figures/"));
            assert!(temp.path().join(&asset).is_file());
            embeds.push_str(&format!("\n![[{asset}]]\n"));
            receipts.push(receipt);
        }
        let spec = json!({"topic":topic,"concepts":[{"id":"main","title":topic,"objectives":[objective,title],"complexity":4}],"visuals":[
            {"id":"v0","concept_id":"main","objective":objective,"category":"numerical_plot","description":"A reproducible supplied numerical series","required_information":["axis values","units"],"renderer":"scientific","family":"scientific_statistical","verification_method":"Reproduce numerical input and check labels","placement":"Collection/01.md"},
            {"id":"v1","concept_id":"main","objective":title,"category":"information_flow","description":"A distinct directed dependency view","required_information":["input","step","output"],"renderer":"graph","family":"knowledge_graphs","verification_method":"Check all directed edges against authored process","placement":"Collection/01.md"}
        ]});
        let plan_path = temp.path().join("plan.json");
        write(&plan_path, &spec);
        let plan = invoke(&["notes", "plan", "--spec", plan_path.to_str().unwrap()]);
        assert!(plan["planning_warnings"].as_array().unwrap().is_empty());
        write(&plan_path, &plan);
        let receipts_path = temp.path().join("receipts.json");
        write(&receipts_path, &json!(receipts));
        let drafts_path = temp.path().join("drafts.json");
        let content = format!(
            "---\ntopic: {topic}\ntags: [topic/fixture]\nmaster_topic: {topic}\ndomain: {domain}\nnote_type: deep-notes\n---\n# {topic}\n\nThis integration fixture checks local artifacts. Educational review remains required.\n{embeds}"
        );
        write(
            &drafts_path,
            &json!([{"path":"Collection/01.md","content":content}]),
        );
        let result = invoke(&[
            "notes",
            "publish",
            "--vault",
            vault,
            "--destination",
            "Collection",
            "--plan",
            plan_path.to_str().unwrap(),
            "--receipts",
            receipts_path.to_str().unwrap(),
            "--drafts",
            drafts_path.to_str().unwrap(),
        ]);
        assert_eq!(result["publication_state"], "published");
        assert_eq!(result["audit"]["verified_assets"], 2);
        let args = [
            "notes",
            "audit",
            "--vault",
            vault,
            "--plan",
            plan_path.to_str().unwrap(),
            "--receipts",
            receipts_path.to_str().unwrap(),
        ];
        assert_eq!(invoke(&args)["artifact_complete"], true);
        fs::write(
            temp.path()
                .join(receipts[0]["local_path"].as_str().unwrap()),
            b"tampered",
        )
        .unwrap();
        let failed = Command::new(env!("CARGO_BIN_EXE_scribe"))
            .args(args)
            .output()
            .unwrap();
        assert!(!failed.status.success());
        let audit: Value = serde_json::from_slice(&failed.stdout).unwrap();
        assert_eq!(audit["artifact_complete"], false);
        assert!(
            audit["missing_representations"]
                .as_array()
                .unwrap()
                .contains(&json!("v0"))
        );
    }
}

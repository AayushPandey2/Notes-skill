//! Typed visual obligations. A deterministic planner validates supplied learning
//! objectives; it does not claim to infer pedagogical sufficiency from keywords.
use anyhow::{Result, bail, ensure};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

fn version() -> u32 {
    1
}
fn complexity() -> u8 {
    1
}
fn required() -> bool {
    true
}
fn source_policy() -> String {
    "adaptive".into()
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct KnowledgePlan {
    #[serde(default = "version")]
    pub schema_version: u32,
    pub topic: String,
    #[serde(default = "source_policy")]
    pub source_policy: String,
    pub concepts: Vec<Concept>,
    /// All note paths audited even when they contain no planned images.
    #[serde(default)]
    pub notes: Vec<String>,
    #[serde(default)]
    pub known_prerequisites: Vec<String>,
    #[serde(default)]
    pub visuals: Vec<VisualSpec>,
    #[serde(default)]
    pub planning_warnings: Vec<String>,
    /// Preserve educational contracts not yet executed by the Rust core.
    #[serde(flatten)]
    pub extensions: BTreeMap<String, serde_json::Value>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Concept {
    pub id: String,
    pub title: String,
    pub objectives: Vec<String>,
    #[serde(default)]
    pub prerequisites: Vec<String>,
    #[serde(default = "complexity")]
    pub complexity: u8,
    #[serde(default)]
    pub visual_needs: Vec<VisualNeed>,
    #[serde(flatten)]
    pub extensions: BTreeMap<String, serde_json::Value>,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum VisualCategory {
    Architecture,
    InformationFlow,
    ComponentDetail,
    ShapeTrace,
    NumericalPlot,
    Heatmap,
    Comparison,
    Schematic,
    Graph,
    ResearchFigure,
    Spatial,
    Table,
    ComputationalTrace,
}

/// All twelve logical UMRIA families remain expressible; renderer availability
/// must be checked separately and never implies an artifact has been produced.
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum RendererFamily {
    MathematicalGeometric,
    ScientificStatistical,
    EngineeringSystems,
    AiMl,
    ComputerScience,
    DataAnalytics,
    KnowledgeGraphs,
    SpatialStructures,
    ResearchEvidence,
    Interactive,
    ExternalMedia,
    StructuredTables,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct VisualNeed {
    pub id: String,
    pub objective: String,
    pub category: VisualCategory,
    pub description: String,
    pub required_information: Vec<String>,
    pub renderer: String,
    pub family: RendererFamily,
    pub verification_method: String,
    /// Vault-relative Markdown file in which this visual must appear.
    pub placement: String,
    #[serde(default)]
    pub preferred_source: Option<String>,
    #[serde(default = "required")]
    pub required: bool,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct VisualSpec {
    pub concept_id: String,
    #[serde(flatten)]
    pub need: VisualNeed,
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord)]
#[serde(rename_all = "snake_case")]
pub enum VisualState {
    Planned,
    Validated,
    Stored,
    Verified,
    Embedded,
    Published,
}

impl VisualState {
    pub fn advance(self, next: Self) -> Result<Self> {
        let valid = matches!(
            (self, next),
            (Self::Planned, Self::Validated)
                | (Self::Validated, Self::Stored)
                | (Self::Stored, Self::Verified)
                | (Self::Verified, Self::Embedded)
                | (Self::Embedded, Self::Published)
        );
        ensure!(
            valid,
            "visual state transition must advance exactly one stage"
        );
        Ok(next)
    }
}

pub fn build_plan(mut plan: KnowledgePlan) -> Result<KnowledgePlan> {
    ensure!(plan.schema_version == 1, "unsupported plan schema version");
    ensure!(!plan.topic.trim().is_empty(), "topic is required");
    let mut note_paths = BTreeSet::new();
    for note in &plan.notes {
        crate::validation::relative_path(std::path::Path::new(note))?;
        ensure!(
            note.ends_with(".md") && note_paths.insert(note),
            "note paths must be unique Markdown files"
        );
    }
    ensure!(
        ["adaptive", "strict", "source_first", "open"].contains(&plan.source_policy.as_str()),
        "invalid source_policy"
    );
    ensure!(
        !plan.concepts.is_empty(),
        "at least one substantive concept is required"
    );
    let mut ids = BTreeSet::new();
    for c in &plan.concepts {
        ensure!(
            !c.id.trim().is_empty() && ids.insert(c.id.clone()),
            "concept IDs must be nonempty and unique"
        );
        ensure!(
            !c.title.trim().is_empty() && !c.title.contains(['\n', '\r']),
            "concept title must be a nonempty line"
        );
        ensure!(
            !c.objectives.is_empty() && c.objectives.iter().all(|o| !o.trim().is_empty()),
            "concept {} needs objectives",
            c.id
        );
        ensure!((1..=5).contains(&c.complexity), "complexity must be 1..5");
    }
    let known: BTreeSet<_> = plan.known_prerequisites.iter().cloned().collect();
    ensure!(
        known.is_disjoint(&ids),
        "known external prerequisites must not overlap owned concepts"
    );
    for c in &plan.concepts {
        for p in &c.prerequisites {
            ensure!(
                ids.contains(p) || known.contains(p),
                "unknown prerequisite {p}"
            );
        }
    }
    let mut ordered = Vec::new();
    let mut done = known;
    while ordered.len() < plan.concepts.len() {
        let Some(c) = plan
            .concepts
            .iter()
            .find(|c| !ordered.contains(&c.id) && c.prerequisites.iter().all(|p| done.contains(p)))
        else {
            bail!("cyclic concept prerequisites");
        };
        ordered.push(c.id.clone());
        done.insert(c.id.clone());
    }
    let ranks: BTreeMap<_, _> = ordered
        .into_iter()
        .enumerate()
        .map(|(i, id)| (id, i))
        .collect();
    plan.concepts.sort_by_key(|c| ranks[&c.id]);
    let mut visuals: BTreeMap<String, VisualSpec> = BTreeMap::new();
    for v in plan.visuals.drain(..) {
        ensure!(
            visuals.insert(v.need.id.clone(), v).is_none(),
            "duplicate visual ID"
        );
    }
    for c in &plan.concepts {
        for need in &c.visual_needs {
            let spec = VisualSpec {
                concept_id: c.id.clone(),
                need: need.clone(),
            };
            if let Some(old) = visuals.get(&need.id) {
                ensure!(
                    serde_json::to_value(old)? == serde_json::to_value(&spec)?,
                    "conflicting visual ID {}",
                    need.id
                );
            } else {
                visuals.insert(need.id.clone(), spec);
            }
        }
    }
    let mut distinct = BTreeSet::new();
    for v in visuals.values() {
        let n = &v.need;
        ensure!(
            ids.contains(&v.concept_id),
            "visual has unknown concept {}",
            v.concept_id
        );
        ensure!(
            [
                &n.id,
                &n.objective,
                &n.description,
                &n.renderer,
                &n.verification_method,
                &n.placement
            ]
            .iter()
            .all(|s| !s.trim().is_empty()),
            "visual fields must be nonempty"
        );
        ensure!(
            !n.required_information.is_empty()
                && n.required_information.iter().all(|i| !i.trim().is_empty()),
            "visual must declare required information"
        );
        ensure!(
            n.placement.ends_with(".md"),
            "visual placement must be a Markdown note"
        );
        crate::validation::relative_path(std::path::Path::new(&n.placement))?;
        let key = (
            v.concept_id.clone(),
            n.category.clone(),
            n.objective.trim().to_lowercase(),
        );
        ensure!(
            distinct.insert(key),
            "duplicate visual representation for {}",
            v.concept_id
        );
    }
    plan.visuals = visuals.into_values().collect();
    plan.planning_warnings.clear();
    for c in &plan.concepts {
        let representations: BTreeSet<_> = plan
            .visuals
            .iter()
            .filter(|v| v.concept_id == c.id)
            .map(|v| &v.need.category)
            .collect();
        if c.complexity >= 4 && representations.len() < 2 {
            plan.planning_warnings.push(format!("{}: complex concept has fewer than two complementary representation types; review learning objectives", c.id));
        }
    }
    Ok(plan)
}

#[cfg(test)]
mod tests {
    use super::*;
    fn plan() -> KnowledgePlan {
        serde_json::from_value(serde_json::json!({"topic":"Circuits", "concepts":[{"id":"current","title":"Current","objectives":["Trace charge flow"],"complexity":4}]})).unwrap()
    }
    #[test]
    fn does_not_invent_visuals() {
        let p = build_plan(plan()).unwrap();
        assert!(p.visuals.is_empty());
        assert_eq!(p.planning_warnings.len(), 1);
    }
    #[test]
    fn rejects_cycle_and_unknown_prerequisites() {
        let mut p = plan();
        p.concepts[0].prerequisites.push("current".into());
        assert!(build_plan(p).is_err());
        let mut p = plan();
        p.known_prerequisites.push("current".into());
        p.concepts[0].prerequisites.push("current".into());
        assert!(build_plan(p).is_err());
        let mut p = plan();
        p.concepts[0].prerequisites.push("unknown".into());
        assert!(build_plan(p).is_err());
    }
    #[test]
    fn cannot_skip_fulfillment_stages() {
        assert!(
            VisualState::Planned
                .advance(VisualState::Published)
                .is_err()
        );
        assert_eq!(
            VisualState::Stored.advance(VisualState::Verified).unwrap(),
            VisualState::Verified
        );
    }
}

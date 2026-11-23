# Deep Learning experimental lab

Use for tensor computation, architecture, gradients, and training dynamics. Keep this hierarchy and opening fields from [the lab contract](../../workflows/notes-creation/experimental-lab.md). Each subsection needs an explained example, observable deliverable, and visual only where it teaches; avoid invented training runs. Retain an inapplicable heading with a specific reason. Rust is optional.

The section prompts below define purpose and content. Use this companion check for a concrete example, evidence, visual opportunity, and common mistake at each section; “always” means the section has a role even in a paper investigation. Retain a heading and explain a specific missing dependency if no genuine artifact can be produced.

| Section | Example and evidence/deliverable | Visual opportunity | Avoid; genuine limit |
|---|---|---|---|
| 01 | Classify images; state target and measurable outcome | Task-to-output diagram | Avoid claiming accuracy before measurement; always |
| 02 | `(batch, channel, height, width)` shape table and split record | Labeled tensor axes | Avoid swapping channel order; sequence axes matter only for sequence tasks |
| 03 | Two-input forward trace and scalar loss | Architecture and activation curve | Avoid unexplained matrix dimensions; a loss needs a defined target |
| 04 | Small affine layer with calculated intermediate values | Forward-operation trace | Avoid implementing a full framework; code may be replaced by manual arithmetic if no execution tool |
| 05 | Derivative of one weight and hand update | Gradient arrows | Avoid conflating derivative with output; full backprop only for the chosen small example |
| 06 | Complete training loop and shape checks | Batch-to-update flow | Avoid missing `zero_grad` or eval mode; framework execution remains unverified until run |
| 07 | Controlled learning-rate comparison table | Actual loss curves | Avoid invented curves; a planned trial stays unfilled |
| 08 | Train/validation/test and checkpoint plan | Data and model lifecycle | Avoid selecting checkpoints on test data; checkpoint artifacts require actual training |
| 09 | Per-class or per-case error record | Verified confusion matrix or examples | Avoid one aggregate score hiding failures; class metrics need class targets |
| 10 | NaN or shape-error diagnostic walkthrough | Failure trace | Avoid generic warnings; a specific failure may be illustrative if labeled |
| 11 | Batch-memory estimate with assumptions | Memory components diagram | Avoid fabricated throughput; GPU results need measured hardware |
| 12 | Manual vs framework output on same input | Architecture comparison | Avoid comparing unlike losses or data; a second architecture needs a learning purpose |
| 13 | Shape, gradient, and controlled-change tasks | Diagram to annotate | Avoid tasks requiring unavailable compute; always |
| 14 | Predict an update and diagnose one trace | Trace table | Avoid API trivia; always |
| 15 | State mechanism, evidence, and limits | Usually no new image | Avoid converting planned experiments into findings; always |

## LAB SECTION 01 — INTRODUCTION AND LEARNING OBJECTIVES
### Task and success
State task, targets, output meaning, success criterion, prerequisites, and smallest useful model; show a workflow map, not an unearned performance claim.
## LAB SECTION 02 — TASK, DATA, AND TENSOR DESIGN
### Dimensions and boundaries
Define train/validation/test boundaries, batch, sequence, channel, feature, and spatial axes where relevant. Provide a shape table from input to target and a representative tensor; avoid ambiguous axis order.
## LAB SECTION 03 — MATHEMATICAL AND COMPUTATIONAL FOUNDATIONS
### Forward computation and loss
Explain operation shapes, activations, loss construction, initialization assumptions, and one numeric forward trace. Give formula folds and an architecture/tensor-flow image or Mermaid as appropriate; avoid confusing forward values with gradients.
## IMPLEMENTATION TRACK A — MECHANISM FROM FIRST PRINCIPLES
Choose the smallest operation that reveals differentiation, not a whole framework.
## LAB SECTION 04 — FORWARD PASS AND CORE OPERATIONS
### Trace an example
Show complete educational code or a manual computation, intermediate shapes and values, and output interpretation. State execution status and numerical precision.
## LAB SECTION 05 — GRADIENTS, BACKPROPAGATION, AND PARAMETER UPDATES
### Chain rule and update
Derive one small gradient, trace its flow and parameter update, distinguish differentiation from forward computation, and check sign and scale. Use a gradient-flow figure; avoid claiming a full model is manually differentiated.
## IMPLEMENTATION TRACK B — FRAMEWORK IMPLEMENTATION
Explain which operations autograd supplies.
## LAB SECTION 06 — MODEL MODULES, AUTOGRAD, AND TRAINING LOOP
### Runnable structure
Show version-checked module, batch loop, loss, backward pass, optimizer step, and gradient clearing; explain accumulation and train/eval modes. Include shape checks and status. Avoid silently applying inference behavior during training.
## EXPERIMENTAL INVESTIGATION
Separate planned trials from observed evidence.
## LAB SECTION 07 — TRAINING DYNAMICS AND CONTROLLED EXPERIMENTS
### Variables and curves
Vary learning rate, initialization, regularization, or batch size one at a time. Record controls, checkpoints, loss/metric tables and actual plots if available; do not sketch results as observations.
## PROFESSIONAL IMPLEMENTATION TRACK
Carry a bounded task from dataset to new-input prediction.
## LAB SECTION 08 — END-TO-END DEEP LEARNING WORKFLOW
### Reproducible pipeline
Cover preprocessing boundaries, architecture choice, validation, checkpoint selection, stopping, held-out evaluation, and inference. Discuss resources and verified environment limits. Use workflow Mermaid and a relevant architecture figure.
## FINAL VALIDATION AND LEARNING
Separate quality, reliability, and cost.
## LAB SECTION 09 — EVALUATION AND ERROR ANALYSIS
### Held-out evidence
Define task-appropriate metrics, baselines, per-case errors, and limits; use an actual confusion matrix or example analysis only when data exists.
## LAB SECTION 10 — NUMERICAL RELIABILITY AND DEBUGGING
### Diagnose failures
Check NaN/Inf, exploding or vanishing gradients, shape errors, loss/activation mismatches, forgotten gradient clearing, and overfitting; pair symptoms with concrete checks.
## LAB SECTION 11 — EFFICIENCY AND RESOURCE TRADE-OFFS
### Memory and compute
Explain batch size, parameter/activation memory, precision, throughput, and measured versus estimated cost without fabricating benchmarks.
## LAB SECTION 12 — IMPLEMENTATION AND ARCHITECTURE COMPARISON
### Match assumptions
Compare the small manual mechanism, framework model, and one justified architecture alternative on same inputs, outputs, and tradeoffs.
## LAB SECTION 13 — PRACTICAL CHALLENGES
### Tasks and checks
Offer shape tracing, gradient checking, and one controlled training change with deliverables.
## LAB SECTION 14 — FINAL LEARNING CHECKPOINT
### Explain a failure
Ask learners to predict shapes, explain a gradient update, and diagnose a training trace with answer guidance.
## LAB SECTION 15 — FINAL SUMMARY
### Transfer
Summarize tensor flow, gradient flow, evidence, and limitations.

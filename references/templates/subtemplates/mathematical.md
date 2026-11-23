# Mathematical composition

Activate for a displayed equation, a mathematical objective, or a worked numerical problem (MATH-01 through MATH-10).

Before composition, supply the equation, its purpose, symbol meanings and types, prerequisite explanations, operation order, assumptions, and any numerical inputs. Supply dimensions for matrix operations. Use the twelve stages defined in [math_gates.md](../../../shared/math_gates.md); adapt stage depth to the actual formula rather than inventing irrelevant examples.

The runtime owner is `scriptorium/engines/mathematics.py`. `render_formula_component` binds a displayed formula to its immediately following collapsed Obsidian explanation. `deconstruct_equation` exposes the same component to the canonical Writer in `scriptorium/engines/composition/writing.py`. `build_worked_solution` uses that component and verifies declared intermediate arithmetic.

The component returns per-stage `supplied` / `not_supplied` evidence. Missing evidence does not mean a stage was verified or deliberately omitted. Dimensions and arithmetic are checked when supplied; mathematical truth and teaching quality require review of the actual artifact.

Keep intermediate arithmetic inside folds inline. Distinct displayed derivation steps need separate sibling formula-and-fold components. Never nest display math inside a formula explanation.

Validation runs on the actual composed Markdown through `validate_formula_folds`; malformed, missing, generic or recursively nested explanations fail composition. Correct the affected equation record and regenerate its component. Use `check_dimension_compatibility`, `verify_worked_calculation`, and `verify_math_deconstruction` for the additional applicable checks. Do not replace a failure with a generic explanation.

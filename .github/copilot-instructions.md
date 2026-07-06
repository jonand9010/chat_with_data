# Copilot Instructions: AI Reliability Analyst MVP

## Project purpose

This repository implements an MVP for an AI Reliability Analyst: a chat-with-data system for the NASA C-MAPSS turbofan degradation dataset.

The system should let a user ask natural-language questions about engine health, degradation, sensors, remaining useful life, anomalies, and comparisons. Answers may include textual summaries, tables, plots, and diagnostic analyses.

The project is not a generic text-to-SQL demo. Treat it as an analytics architecture project with clear separation between:

1. Data layer
2. Semantic layer
3. Analytics/tool layer
4. Planner/agent layer
5. Answer synthesis/UI layer

Prioritize clarity, composability, testability, and analytical correctness over cleverness.

---

## Core architectural principle

Do not let the LLM directly query raw data, execute arbitrary Python, or invent columns.

The agent should create a structured analysis plan using known semantic concepts and registered analytics tools. Python code should validate the plan and execute only approved tools.

Preferred flow:

```text
User question
  -> planner agent
  -> typed AnalysisPlan
  -> validated tool execution
  -> result objects
  -> answer synthesis
```

The LLM plans. The application executes.

---

## Preferred stack

Use Python.

Preferred libraries:

* pandas for dataframe manipulation
* duckdb for analytical SQL over local files
* pyarrow/parquet for processed data storage
* pydantic for schemas and validation
* plotly or matplotlib for plots
* scikit-learn for PCA, clustering, anomaly detection, and simple models
* scipy/statsmodels where useful
* pytest for tests

Optional later:

* LangGraph for graph-based agent orchestration
* Streamlit or FastAPI + frontend for UI
* dbt-style YAML files for semantic definitions
* vector search for documentation RAG

Keep the MVP local-first and simple.

---

## Expected repository structure

Prefer this structure unless there is a good reason to change it:

```text
.
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
├── src/
│   └── reliability_analyst/
│       ├── data/
│       ├── semantic/
│       ├── analytics/
│       ├── agent/
│       ├── plotting/
│       └── app/
├── tests/
├── configs/
│   └── semantic_layer.yaml
├── pyproject.toml
└── README.md
```

Use small modules with explicit responsibilities.

---

## Dataset assumptions

The first target dataset is the NASA C-MAPSS turbofan degradation dataset.

Typical columns after processing should use readable names:

```text
engine_id
cycle
operating_setting_1
operating_setting_2
operating_setting_3
sensor_1
...
sensor_21
rul
```

Do not rely on anonymous column names such as `s1`, `T24`, or `column_5` unless the code clearly maps them to semantic names.

---

## Semantic layer

Represent domain concepts explicitly.

Examples:

```text
Entity:
- engine

Time axis:
- cycle

Measures:
- rul
- health_index
- anomaly_score
- sensor_trend
- degradation_rate

Dimensions:
- engine_id
- operating_regime
- cycle_bucket

Analysis concepts:
- degradation
- failure risk
- sensor drift
- outlier engine
- similar engines
- early warning sensor
```

When adding new analytics functionality, update the semantic layer if the functionality introduces a new concept, metric, dimension, or tool.

The semantic layer should be machine-readable where possible, preferably YAML or Pydantic models.

---

## Analytics tools

Expose analytical operations as registered tools.

Good tool examples:

```text
summarize_engine(engine_id)
plot_sensor(engine_ids, sensor)
compare_engines(engine_ids)
rank_degrading_engines(sensor, top_n)
correlate_sensors_with_rul(top_n)
compute_health_index(method)
detect_anomalous_engines(method)
cluster_engines(features, n_clusters)
run_pca(features)
find_change_points(engine_id, sensor)
estimate_rul(engine_id)
```

Each tool should:

1. Have typed inputs
2. Validate arguments
3. Return a structured result object
4. Avoid printing directly
5. Avoid hidden global state
6. Be unit-testable

Prefer returning objects like:

```python
{
    "type": "table" | "plot" | "text" | "metric",
    "title": "...",
    "data": ...,
    "metadata": {...}
}
```

---

## Planner agent

The planner should produce a typed plan, not free-form instructions.

Use Pydantic models such as:

```python
class PlanStep(BaseModel):
    step_id: int
    tool: ToolName
    reason: str
    args: dict[str, Any]

class AnalysisPlan(BaseModel):
    user_question: str
    interpretation: str
    steps: list[PlanStep]
    final_answer_style: Literal["summary", "diagnostic_report", "plot_first"]
```

The planner must only choose from registered tools.

If the question cannot be answered with available tools or semantic concepts, the planner should return a graceful limitation rather than hallucinating capabilities.

---

## Agent behavior

When implementing agent logic, follow these rules:

* Prefer simple deterministic routing before adding complex agent behavior.
* Make intermediate plans inspectable.
* Log the selected tools, arguments, and reasons.
* Validate all tool arguments before execution.
* Never execute arbitrary code generated by the LLM.
* Never let the LLM invent dataframe columns.
* Never silently ignore failed tool calls.
* Return useful error messages with suggested next steps.
* Keep the first MVP explainable and debuggable.

---

## Analytical standards

Analyses should be statistically modest and honest.

When implementing methods:

* Distinguish correlation from causation.
* Report assumptions.
* Avoid overclaiming failure predictions.
* Prefer simple baselines before advanced models.
* Make train/test split logic explicit.
* Avoid data leakage when using RUL.
* Remember that each engine is a trajectory, not an independent row.
* Use cycle-aware logic for time-series features.
* Explain whether results are per-cycle, per-engine, or aggregate.

For degradation analysis, prefer trajectory-based reasoning over single-row comparisons.

---

## Code style

Write clear, typed Python.

Use:

* type hints
* Pydantic schemas where helpful
* small functions
* descriptive names
* docstrings for public functions
* pytest tests for nontrivial logic

Avoid:

* large notebooks as core implementation
* hidden mutable global state
* magical column assumptions
* long procedural scripts
* tightly coupling plotting, data access, and analysis
* letting UI code contain analytical logic

---

## Testing expectations

For each new analytics tool, add tests covering:

1. Valid input
2. Invalid sensor name or engine ID
3. Expected output structure
4. Edge cases such as too few cycles
5. No accidental mutation of input data

For the planner/executor, test that:

1. Only registered tools can run
2. Invalid tool names fail safely
3. Missing arguments fail clearly
4. A valid plan executes in order
5. Tool results preserve step IDs

---

## Plotting guidelines

Plotting functions should not directly show figures unless explicitly requested by the caller.

Return figure objects or serializable plot specifications.

Plots should have:

* clear title
* labeled axes
* relevant units
* readable legends
* no unnecessary styling complexity

For the MVP, prioritize:

* sensor over cycle
* health index over cycle
* RUL distribution
* degradation ranking
* PCA scatter
* cluster summaries

---

## Data layer guidelines

Keep raw data immutable.

Use this progression:

```text
raw NASA files
  -> cleaned dataframe
  -> feature-enriched dataframe
  -> analytics-ready parquet
```

Processing code should be reproducible.

Do not manually edit processed files.

Use stable column names across the project.

---

## Semantic YAML example

If creating or editing `configs/semantic_layer.yaml`, prefer a structure like:

```yaml
entities:
  engine:
    key: engine_id
    description: One turbofan engine observed over operating cycles.

time:
  primary_axis: cycle

measures:
  rul:
    column: rul
    description: Remaining useful life measured in cycles.
  health_index:
    derived: true
    description: Normalized degradation score.

dimensions:
  engine_id:
    column: engine_id
  operating_regime:
    derived: true

tools:
  summarize_engine:
    description: Summarize the health and degradation pattern of one engine.
  rank_degrading_engines:
    description: Rank engines by degradation trend.
```

---

## MVP priorities

Implement in this order:

1. Data loader and cleaner
2. Semantic layer definition
3. A few deterministic analytics tools
4. Plan schema and executor
5. Mock planner
6. LLM planner
7. Text answer synthesis
8. Plot generation
9. Simple UI
10. Evaluation examples

Do not start with a complex UI or multi-agent architecture.

---

## Design philosophy

This project should feel like a junior version of a real analytics copilot for engineering systems.

The goal is not merely to answer:

```text
What is the average value of sensor_11?
```

The goal is to answer:

```text
Which engines appear to be degrading unusually quickly, what evidence supports that, and what should we inspect next?
```

Always favor analytical workflows over one-shot queries.

---

## When uncertain

When implementation choices are ambiguous:

1. Prefer the simplest working version.
2. Preserve architectural boundaries.
3. Make behavior explicit and testable.
4. Add TODOs for future sophistication.
5. Avoid premature abstraction unless it protects the core layer separation.

Do not invent external services, cloud infrastructure, or production complexity unless explicitly asked.

# Specify Interview Reference

## Intent

Use this phase to define WHAT to build and WHY it matters.
The output should answer: "Who needs what capability, under what scope, with what acceptance criteria?"

## In-Scope Signals

- User roles and core usage scenarios.
- Business/user value and problem statement.
- Functional requirements and non-goals.
- Scope boundaries and assumptions.
- Measurable, testable acceptance criteria.

## Out-of-Scope Signals (Usually Plan-Level)

- Exact stack/framework/library decisions.
- API/module/class-level implementation design.
- Deployment scripts, service wiring, infra details.
- Low-level algorithm choices unless required for requirement clarity.

## Phase-Fit Challenge Rules

When user provides HOW details that should be in plan, warn and redirect.

Reply in Chinese with this pattern:

- `提醒：这条偏实现方案，更适合 /speckit.plan。当前是 /speckit.specify（定义需求与验收）。`
- `你要我：1) 改写为需求表述（推荐）2) 记录到 plan 候选 3) 原样保留（不推荐）？`

## Rewrite Heuristics

- Convert implementation language into requirement language.
- Keep the user value and observable behavior.

Examples:

- `Use NVML to read GPU metrics` -> `System shall collect GPU telemetry with stable and reliable mechanism.`
- `Use PID control` -> `System shall adjust fan speed smoothly with bounded oscillation under load changes.`

## Draft Quality Checklist

- Does every requirement describe behavior/outcome, not implementation?
- Are non-goals explicit to prevent scope creep?
- Are acceptance criteria measurable?
- Is user value clearly stated?

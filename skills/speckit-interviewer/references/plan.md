# Plan Interview Reference

## Intent

Use this phase to define HOW to implement the approved scope.
The output should answer: "What architecture and technical decisions will deliver the specified requirements safely and verifiably?"

## In-Scope Signals

- Tech stack and runtime constraints.
- Module boundaries and control/data flow.
- Key design decisions with trade-offs.
- Failure modes, protection strategy, and recovery conditions.
- Validation strategy: quick checks, stability tests, fault injection tests.
- v1 vs v2 rollout strategy to avoid over-design.

## Out-of-Scope Signals

- Rewriting project constitution principles from scratch.
- Introducing new product requirements that were never specified.
- Broad business-goal debate better handled in `specify`.

## Phase-Fit Challenge Rules

When user introduces requirement changes that belong to specify, warn first.

Reply in Chinese with this pattern:

- `提醒：这条是需求范围变化，更适合先更新 /speckit.specify。当前是 /speckit.plan（实现设计阶段）。`
- `你要我：1) 先按现有范围继续 plan（推荐）2) 先整理成 specify 补充点 3) 强行并入当前 plan（不推荐）？`

When user gives only abstract principles, push toward implementable design detail.

Reply in Chinese with this pattern:

- `提醒：这条偏原则层，建议补充可执行设计信息（模块、数据流、失败处理、验证方法）。`

## Decision Prompt Bank

Use short option-based questions with recommendations:

- Telemetry source: `NVML` (recommended) vs shell parsing.
- Control strategy v1: segmented curve + rate limiter (recommended) vs direct PID.
- Safety fallback policy: fixed safe profile vs temperature-tiered fallback.
- Runtime mode: foreground CLI + daemon wrapper vs daemon-first with diagnostics CLI.

## Draft Quality Checklist

- Are critical implementation decisions explicit and justified?
- Are failure handling and recovery conditions concrete?
- Is the validation path actionable and testable?
- Does plan stay within specified scope (or explicitly mark scope assumptions)?

## Auto Review Severity

Classify each candidate item before drafting:

- `BLOCK`
  - Introduces new product requirements/scope not agreed in `specify`.
  - Lacks actionable failure handling for critical paths.
  - Uses only principle-level text without implementable design decisions.
- `WARN`
  - Decision is present but rationale/trade-off is weak.
  - Validation path is partial (missing stability or fault-injection coverage).

If any `BLOCK` exists, resolve first (rewrite, park, or force-keep with explicit risk note).

## Review Output Template (Chinese)

Use concise Chinese output:

- `审查结果：BLOCK <n> 条，WARN <m> 条。`
- `关键问题：`
  - `1) ...`
  - `2) ...`
- `建议操作：1) 按建议修改（推荐）2) 仅修复 BLOCK 3) 原样保留`

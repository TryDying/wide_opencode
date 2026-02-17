# Constitution Interview Reference

## Intent

Use this phase to define governance-level principles and long-lived constraints.
The output should answer: "What rules must always hold for this project?"

## In-Scope Signals

- Safety principles and fail-safe baseline policy.
- Reliability and observability obligations.
- Change governance and documentation discipline.
- Compatibility and versioning policy.
- Organizational constraints that are truly long-term policy.

## Out-of-Scope Signals (Usually Plan-Level)

- Exact language/runtime versions.
- Concrete deployment mechanics (`systemd` unit names, file paths, package names).
- Detailed implementation algorithms and parameter values.
- Specific tool/library choices unless they are explicit organization policy.

## Phase-Fit Challenge Rules

When user content is too implementation-specific, do not accept it silently.

Reply in Chinese with this pattern:

- `提醒：这条偏实现细节，更适合 /speckit.plan。当前是 /speckit.constitution。`
- `你要我：1) 改写为治理原则（推荐）2) 记录到 plan 候选 3) 原样保留（不推荐）？`

## Rewrite Heuristics

- Convert concrete mechanisms into policy-level wording.
- Preserve user intent, remove implementation coupling.

Examples:

- `Use Python 3.11 + systemd` -> `Adopt stable, maintainable runtime and standardized service operation model.`
- `Fallback fan speed is exactly 60%` -> `Fallback to a calibrated safe speed profile with explicit lower bound and verification.`

## Draft Quality Checklist

- Is each item a principle/policy rather than implementation detail?
- Are obligations auditable and testable?
- Are change/compatibility rules explicit?
- Are safety and diagnostics non-negotiable?

## Auto Review Severity

Classify each candidate item before drafting:

- `BLOCK`
  - Encodes direct implementation choices (language version, deployment path, service unit names, concrete APIs/libraries) without explicit "organization policy" framing.
  - Introduces exact control parameters or algorithm-level details.
  - Adds product scope/feature commitments that belong to `specify`.
- `WARN`
  - Principle wording is too vague to audit.
  - Obligation is meaningful but lacks clear boundary/trigger.

If any `BLOCK` exists, resolve first (rewrite, park, or force-keep with explicit risk note).

## Review Output Template (Chinese)

Use concise Chinese output:

- `审查结果：BLOCK <n> 条，WARN <m> 条。`
- `关键问题：`
  - `1) ...`
  - `2) ...`
- `建议操作：1) 按建议修改（推荐）2) 仅修复 BLOCK 3) 原样保留`

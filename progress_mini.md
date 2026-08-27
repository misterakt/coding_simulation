# Senior Data Engineer Python Mini Practice Progress

Last updated: 2026-08-27

Use this file to track every exercise run with `docs/senior_data_engineer_python_interview_mini_prompt.md`.

## Current Status

- Practice state: Stage ended on 2026-08-27
- Topics completed: 1 of 10
- Attempts recorded: 3
- Final stage result: Pass — C4/P4/T3/J4
- Resume priority: 2 — Deduplication and idempotency
- Default timebox: 10 minutes
- Next exercise ID: MINI-002
- Current streak: 1 pass

## Stage 1 Closure

Completed `MINI-001 — Validate a Payment Record` after two focused revisions.

### Improvement demonstrated

- Progressed from C2/P2/T2/J2 to C4/P4/T3/J4.
- Replaced mixed boolean/string output with a consistent `list[str]`.
- Correctly rejected non-string and whitespace-only payment IDs.
- Explicitly rejected boolean amounts while keeping zero valid.
- Returned multiple validation failures in deterministic requirement order.
- Simplified the final control flow by returning the collected errors directly.
- Introduced stable validation error codes and connected row-level results to quarantine and metric concepts.

### Carry forward

- Use canonical, consistently spelled error codes and preserve an explicitly supplied output contract.
- Turn every important boundary into a submitted test, especially zero and multiple simultaneous errors.
- When adding record context, retain a source-level fallback ID because the business ID may itself be invalid.
- Emit low-cardinality aggregate metrics by error code; do not use `payment_id` as a metric label.

## Priority Queue

Work from the highest priority downward. Repeat a topic when the result is `Retry` or when the same weakness appears again.

| Priority | Topic | Status | Best score | Next action |
| --- | --- | --- | --- | --- |
| 1 | Validation and malformed input | Solid | C4/P4/T3/J4 | Recheck exact output text in a later exercise. |
| 2 | Deduplication and idempotency | Not started | — | Start MINI-002. |
| 3 | Dictionary lookup and grouping | Not started | — | Pending. |
| 4 | Transformation and parsing | Not started | — | Pending. |
| 5 | Reconciliation | Not started | — | Pending. |
| 6 | Tests and edge cases | Not started | — | Pending. |
| 7 | Retry, pagination, and resumability | Not started | — | Pending. |
| 8 | Streaming and memory safety | Not started | — | Pending. |
| 9 | Schema evolution and contracts | Not started | — | Pending. |
| 10 | Event and orchestration state | Not started | — | Pending. |

Status values: `Not started`, `Practicing`, `Solid`, or `Revisit`.

## Exercise Log

Add one row after every exercise, including retries.

| Date | ID | Priority/topic | Type | Task | Result | Scores C/P/T/J | Time | Revision made | Next step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-08-27 | MINI-001 | 1 — Validation and malformed input | Implement | Validate a payment record | Retry | C2/P2/T2/J2 | Not recorded | Not yet | Correct type boundaries and return only specified error strings. |
| 2026-08-27 | MINI-001-R1 | 1 — Validation and malformed input | Update | Revise payment validation | Revise | C3/P3/T2/J3 | Not recorded | Removed successful booleans; rejected integer IDs and boolean amounts. | Reject whitespace IDs, match supplied example messages, and add boundary assertions. |
| 2026-08-27 | MINI-001-R2 | 1 — Validation and malformed input | Update | Complete payment validation | Pass | C4/P4/T3/J4 | Not recorded | Fixed whitespace handling, simplified control flow, and added boundary assertions. | Start Priority 2 deduplication; recheck exact output text later. |

Score key: `C` correctness, `P` Python quality, `T` testing, `J` production judgment. Each score is out of 5.

## Compact Session Notes

For each exercise, add only information useful for the next attempt.

### MINI-001 — Validate a Payment Record

- Assumption or approach: Used one nested checker per field and collected their results.
- Main issue found: R2 satisfies the functional rules. Error wording still differs from the supplied example, and zero/multi-error cases are not asserted in the submitted file.
- Revision: Completed in MINI-001-R2; final cleanup removed the unused flag and introduced stable error codes. Externally verified against all requested boundary cases.
- One thing to remember: A non-empty string requirement needs both `isinstance(value, str)` and a stripped-content check.
- Recommended next exercise: MINI-002 — deduplication and idempotency.

## Completion Standard

A topic becomes `Solid` when both are true:

- the latest relevant exercise is a `Pass`
- correctness is at least 4/5 with no critical edge-case gap

Mark a topic `Revisit` if the same issue appears in two later exercises.

## Next Session

This stage is closed. When ready to resume, use the mini prompt and say:

> Start mini. Use the next priority in `progress_mini.md`. Do not give hints unless I ask.

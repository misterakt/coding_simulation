# Senior Data Engineer Python Mini Practice Progress

Last updated: 2026-09-07

Use this file to track every exercise run with `docs/senior_data_engineer_python_interview_mini_prompt.md`.

## Current Status

- Practice state: Active; MINI-004 completed on 2026-09-07
- Topics completed: 4 of 10
- Attempts recorded: 17
- Latest result: Pass — C5/P3/T4/J4
- Resume priority: 5 — Reconciliation
- Default timebox: 10 minutes
- Next exercise ID: MINI-005
- Current streak: 2 passes

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
| 1 | Validation and malformed input | Solid | C4/P4/T3/J4 | Rechecked type boundaries and exact exceptions in MINI-004. |
| 2 | Deduplication and idempotency | Solid | C5/P4/T4/J4 | Recheck ordered uniqueness and exact empty-output contracts later. |
| 3 | Dictionary lookup and grouping | Solid | C5/P5/T4/J5 | Covered in MINI-003. |
| 4 | Transformation and parsing | Solid | C5/P3/T4/J4 | Recheck parse-then-validate flow and exception tests in a separate exercise. |
| 5 | Reconciliation | Not started | — | Start MINI-005. |
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
| 2026-09-01 | MINI-002 | 2 — Deduplication and idempotency | Implement | Deduplicate ingestion events and report conflicts | Revise | C2/P2/T2/J2 | Not recorded | Retained first events and avoided input mutation. | Distinguish identical duplicates from conflicts and return `([], [])` for empty input. |
| 2026-09-01 | MINI-002-R1 | 2 — Deduplication and idempotency | Update | Add retained-event lookup and equality comparison | Revise | C3/P3/T2/J3 | Not recorded | Replaced the retained-event list scan with a keyed dictionary and correctly ignored identical duplicates. | Preserve conflict discovery order, remove field-specific debug output, and fix the empty return shape. |
| 2026-09-01 | MINI-002-R2 | 2 — Deduplication and idempotency | Update | Complete ordered conflict handling | Pass | C5/P4/T3/J4 | Not recorded | Used insertion-ordered dictionaries, returned a stable two-list tuple, and removed unsafe debug output. | Add an explicit non-mutation assertion and explain scale behavior. |
| 2026-09-01 | MINI-002-R3 | 2 — Deduplication and idempotency | Update | Add non-mutation coverage and final cleanup | Pass | C5/P4/T4/J4 | Not recorded | Added a `deepcopy`-based non-mutation assertion and simplified the final return. | Start Priority 3 dictionary lookup and grouping. |
| 2026-09-04 | MINI-003 | 3 — Dictionary lookup and grouping | Implement | Aggregate usage events by account | Pass | C5/P5/T4/J5 | 10 mins | First-pass clean solution with dictionary grouping, order preservation, and complexity analysis. | Start Priority 4 transformation and parsing. |
| 2026-09-07 | MINI-004 | 4 — Transformation and parsing | Implement | Normalize a usage record | Revise | C3/P2/T2/J3 | Not recorded | Normalized happy paths and returned an exact three-field result. | Reject every unsupported unit with the exact exception and test failures independently. |
| 2026-09-07 | MINI-004-R1 | 4 — Transformation and parsing | Update | Correct invalid-unit handling | Revise | C3/P2/T3/J3 | Not recorded | Added missing-unit rejection and separated submitted invalid calls. | Reject unsupported types and translate conversion errors to the contract message. |
| 2026-09-07 | MINI-004-R2 | 4 — Transformation and parsing | Update | Expand numeric validation | Revise | C3/P3/T2/J4 | Not recorded | Added non-finite numeric checks and unsupported-type handling. | Parse strings before applying negativity and finiteness rules. |
| 2026-09-07 | MINI-004-R3 | 4 — Transformation and parsing | Update | Restructure unit parsing | Retry | C1/P2/T1/J3 | Not recorded | Began restructuring conversion flow, but left invalid syntax. | Restore runnable code and implement one parse-then-validate path. |
| 2026-09-07 | MINI-004-R4 | 4 — Transformation and parsing | Update | Validate parsed numeric strings | Retry | C2/P2/T2/J4 | Not recorded | Restored valid syntax and kept finite-value validation. | Accept zero strings, reject negative strings, and translate parsing errors exactly. |
| 2026-09-07 | MINI-004-R5 | 4 — Transformation and parsing | Update | Separate identifier and unit parsing | Revise | C2/P3/T2/J3 | Not recorded | Introduced focused identifier and unit helpers. | Raise exceptions instead of returning exception objects, then validate parsed units. |
| 2026-09-07 | MINI-004-R6 | 4 — Transformation and parsing | Update | Complete parsed-unit validation | Revise | C4/P3/T2/J4 | Not recorded | Correctly raised unit errors and applied shared negative and finite checks. | Reject non-string identifiers instead of returning `None`. |
| 2026-09-07 | MINI-004-R7 | 4 — Transformation and parsing | Update | Complete usage normalization | Pass | C5/P3/T2/J4 | Not recorded | Rejected malformed identifiers and passed 7 valid and 19 invalid external checks without mutation. | Start Priority 5 reconciliation; recheck exception-test design later. |
| 2026-09-07 | MINI-004-R8 | 4 — Transformation and parsing | Test | Add reliable normalization tests | Pass | C5/P3/T4/J4 | Not recorded | Added table-driven valid and invalid cases, exact exception assertions, explicit no-exception failure, and non-mutation checks. | Start Priority 5 reconciliation; repeat the failure-path pattern in a separate exercise. |

Score key: `C` correctness, `P` Python quality, `T` testing, `J` production judgment. Each score is out of 5.

## Compact Session Notes

For each exercise, add only information useful for the next attempt.

### MINI-001 — Validate a Payment Record

- Assumption or approach: Used one nested checker per field and collected their results.
- Main issue found: R2 satisfies the functional rules. Error wording still differs from the supplied example, and zero/multi-error cases are not asserted in the submitted file.
- Revision: Completed in MINI-001-R2; final cleanup removed the unused flag and introduced stable error codes. Externally verified against all requested boundary cases.
- One thing to remember: A non-empty string requirement needs both `isinstance(value, str)` and a stripped-content check.
- Recommended next exercise: MINI-002 — deduplication and idempotency.

### MINI-002 — Deduplicate Ingestion Events

- Assumption or approach: Retained the first complete event in an insertion-ordered dictionary keyed by `event_id` and used a second dictionary for ordered, unique conflict IDs.
- Main issue found: The initial version classified identical repeats as conflicts and returned the wrong shape for empty input; the first revision also used a set conversion that could lose conflict-discovery order.
- Revision: Compared repeats with the retained event, preserved both output orders, returned `([], [])` for empty input, removed field-specific debug output, and added a `deepcopy`-based non-mutation assertion.
- One thing to remember: A generator only removes eager output buffering; exact global deduplication still requires O(u) state for `u` unique IDs unless that state is partitioned or moved to an external store.
- Recommended next exercise: MINI-003 — dictionary lookup and grouping, with exact empty and ordering assertions from the start.

### MINI-003 — Aggregate Usage Events by Account

- Assumption or approach: Iterated through records with $O(1)$ dictionary lookups to build two-level nested dictionary groupings.
- Main issue found: None. Clean first-pass implementation with preserved insertion order and correct $O(N)$ time / $O(U)$ space bounds.
- Revision: None needed.
- One thing to remember: When writing a non-mutation test assertion, clone the input before calling the function (`before = deepcopy(events)`), run `aggregate_usage_by_account(events)`, then assert `events == before`.
- Recommended next exercise: MINI-004 — transformation and parsing.

### MINI-004 — Normalize a Usage Record

- Assumption or approach: Used separate helpers to normalize identifiers and parse numeric units, followed by shared domain validation.
- Main issue found: Early revisions mixed parsing with validation, returned exception objects instead of raising them, and used exception tests that could falsely pass when the function returned normally.
- Revision: Parsed integer, decimal, zero, and scientific-notation strings into one numeric candidate; rejected malformed identifiers, booleans, negative and non-finite values; and returned an exact new dictionary. The final test revision added table-driven cases, exact exception assertions, explicit failure when no exception is raised, and valid/invalid non-mutation checks.
- One thing to remember: Parse into a canonical value first, validate that value second, and make exception tests fail explicitly when no exception is raised.
- Recommended next exercise: MINI-005 — reconciliation, while carrying forward exact failure-path testing.

## Completion Standard

A topic becomes `Solid` when both are true:

- the latest relevant exercise is a `Pass`
- correctness is at least 4/5 with no critical edge-case gap

Mark a topic `Revisit` if the same issue appears in two later exercises.

## Next Session

MINI-004 is complete. When ready to continue, use the mini prompt and say:

> Start mini. Use the next priority in `progress_mini.md`. Do not give hints unless I ask.

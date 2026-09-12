# Senior Data Engineer Python Mini Practice Progress

Last updated: 2026-09-12

Use this file to track every exercise run with `docs/senior_data_engineer_python_interview_mini_prompt.md`.

## Current Status

- Practice state: Active; MINI-009 completed on 2026-09-12
- Topics completed: 9 of 10
- Attempts recorded: 32
- Latest result: Pass — C5/P3/T3/J4
- Resume priority: 10 — Event and orchestration state
- Default timebox: 10 minutes
- Next exercise ID: MINI-010
- Current streak: 5 passes

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
| 2 | Deduplication and idempotency | Solid | C5/P4/T4/J4 | Ordered keyed lookup rechecked in MINI-005. |
| 3 | Dictionary lookup and grouping | Solid | C5/P5/T4/J5 | Covered in MINI-003. |
| 4 | Transformation and parsing | Solid | C5/P3/T4/J4 | Recheck parse-then-validate flow and exception tests in a separate exercise. |
| 5 | Reconciliation | Solid | C5/P3/T3/J4 | Recheck order-specific tests and bounded-state reconciliation later. |
| 6 | Tests and edge cases | Solid | C5/P4/T5/J4 | Ordering and executable assertions rechecked with assistance in MINI-009; repeat independently later. |
| 7 | Retry, pagination, and resumability | Solid | C5/P4/T4/J4 | Recheck exact per-cursor attempt counts and malformed-page handling later. |
| 8 | Streaming and memory safety | Solid | C5/P3/T4/J4 | Recheck key-based partitioning and partition sizing on unsorted inputs later. |
| 9 | Schema evolution and contracts | Solid | C5/P3/T3/J4 | Recheck allowed changes, non-mutation tests, and numeric precision in a later contract task. |
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
| 2026-09-07 | MINI-005 | 5 — Reconciliation | Implement | Reconcile invoice snapshots | Revise | C3/P3/T2/J3 | Not recorded | Built keyed lookups and exact duplicate-ID failure handling. | Preserve all required output orders and assert valid results exactly. |
| 2026-09-07 | MINI-005-R1 | 5 — Reconciliation | Update | Fix ordered reconciliation | Revise | C4/P3/T3/J3 | Not recorded | Restored deterministic missing-ID order and compared only contract fields. | Drive `changed` from source order and remove linear list membership. |
| 2026-09-07 | MINI-005-R2 | 5 — Reconciliation | Update | Complete linear ordered reconciliation | Pass | C5/P3/T3/J4 | Not recorded | Derived all classifications from insertion-ordered dictionaries, compared only amount/status, and passed ordering, duplicate, empty, extra-field, and non-mutation checks. | Start Priority 6 tests and edge cases; add deliberately reversed-order cases. |
| 2026-09-09 | MINI-006 | 6 — Tests and edge cases | Test | Test loadable file selection | Revise | C3/P4/T3/J3 | Not recorded | Added empty, duplicate, normal, mismatch, ordering, and non-mutation cases. | Make the ordering fixture isolate order and cover duplicate arrivals. |
| 2026-09-09 | MINI-006-R1 | 6 — Tests and edge cases | Test | Correct test coverage gaps | Retry | C2/P3/T3/J3 | Not recorded | Added duplicate-arrival and successful-path mutation cases. | Fix tuple syntax, execute the valid-case table, and correct the second ordering fixture. |
| 2026-09-09 | MINI-006-R2 | 6 — Tests and edge cases | Test | Complete ordering fixtures | Revise | C4/P3/T4/J4 | Not recorded | Corrected both reversed-order fixtures and added the valid-case loop. | Call the function with the loop variables rather than later mutation-test variables. |
| 2026-09-09 | MINI-006-R3 | 6 — Tests and edge cases | Test | Complete loadable-file tests | Pass | C5/P4/T5/J4 | Not recorded | Produced executable contract-driven tests that expose duplicate handling and manifest-order defects while checking empty, mismatch, unexpected, and non-mutation behavior. | Start Priority 7 retry, pagination, and resumability. |
| 2026-09-10 | MINI-007 | 7 — Retry, pagination, and resumability | Update | Add retry and safe-resume behavior to a paginated loader | Revise | C3/P3/T3/J3 | Not recorded | Retried `TimeoutError` on the same cursor and reset the allowance after success. | Return the failed cursor when attempts are exhausted instead of falling through to an undefined page. |
| 2026-09-10 | MINI-007-R1 | 7 — Retry, pagination, and resumability | Update | Correct exhausted-retry control flow | Revise | C3/P3/T2/J3 | Not recorded | Returned completed records with the failed cursor after exhaustion. | Fix the off-by-one attempt count and reset attempts independently for each successful page. |
| 2026-09-10 | MINI-007-R2 | 7 — Retry, pagination, and resumability | Update | Fix per-cursor retry accounting | Pass | C5/P3/T4/J4 | Not recorded | Limited calls to `max_attempts`, reset the allowance per successful page, and retained a safe resume cursor. | Clean up names and unused imports; later recheck the pattern on a multi-page partial failure. |
| 2026-09-10 | MINI-007-R3 | 7 — Retry, pagination, and resumability | Update | Complete resumable paginated loader | Pass | C5/P4/T4/J4 | Not recorded | Used a clear remaining-attempt counter and executable success, recovery, and exhaustion assertions. | Start Priority 8 streaming and memory safety. |
| 2026-09-11 | MINI-008 | 8 — Streaming and memory safety | Implement | Reconcile sorted file streams | Pass | C5/P3/T4/J4 | Not recorded | Implemented a generator-based merge join, corrected one-sided advancement and exhaustion handling, and added empty-stream coverage. | Start Priority 9 schema evolution; later recheck deterministic key partitioning for unsorted inputs. |
| 2026-09-12 | MINI-009 | 9 — Schema evolution and contracts | Implement | Check a schema change | Revise | C3/P3/T1/J3 | Not recorded | Detected all breaking-change categories, but set-based removals lost order and the test loop discarded comparisons. | Process existing fields in current order, additions afterward, and assert test results. |
| 2026-09-12 | MINI-009-R1 | 9 — Schema evolution and contracts | Update | Correct ordered compatibility reporting | Revise | C5/P3/T2/J3 | Not recorded | Implemented two ordered passes and executable assertions; passed 36 external ordering permutations and non-mutation checks. | Add the requested conflicting-order regression fixture. |
| 2026-09-12 | MINI-009-R2 | 9 — Schema evolution and contracts | Test | Complete schema-change regression coverage | Pass | C5/P3/T3/J4 | Not recorded | Added the ordering fixture, removed unsupported None handling and the leftover ellipsis, and discussed downstream contracts and numeric widening. | Start Priority 10 event and orchestration state; later recheck float exactness and allowed-change tests. |

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

### MINI-005 — Reconcile Invoice Snapshots

- Assumption or approach: Indexed source and target records by `invoice_id`, rejected duplicate IDs, and derived classifications through keyed membership checks.
- Main issue found: The initial set-based outputs lost encounter order; the first revision then built overlap IDs in target order even though `changed` required source order. Submitted tests did not initially assert results or deliberately reverse shared-ID order.
- Revision: Iterated the source dictionary for source-ordered outputs and the target dictionary for target-ordered output, compared only `amount` and `status`, and retained linear O(n + m) lookup behavior.
- One thing to remember: To test an ordering contract, make the competing input order intentionally different so the wrong driver cannot pass accidentally.
- Production follow-up: Proposed streaming with a `batch_id`. This is a useful start for lineage, checkpointing, and resumability, but the matching strategy still needs to bound state through sorted merge, consistent hash partitioning, or an external keyed store.
- Recommended next exercise: MINI-006 — tests and edge cases.

### MINI-006 — Test Loadable File Selection

- Assumption or approach: Derived table-driven valid and invalid cases from the contract and used deep copies for mutation checks.
- Main issue found: Early ordering fixtures mixed size mismatches with ordering, and one revision defined cases without executing them correctly.
- Revision: Created deliberately conflicting manifest and arrival orders with otherwise matching records, covered duplicates in both inputs, executed the case table with its loop variables, and retained exact exception and non-mutation assertions.
- One thing to remember: An ordering fixture must make every record otherwise eligible, and a table of cases provides coverage only when every row is actually passed to the function under test.
- Recommended next exercise: MINI-007 — retry, pagination, and resumability.

### MINI-007 — Resumable Paginated Loader

- Assumption or approach: Retried `TimeoutError` against the current cursor and appended records only after a successful page response.
- Main issue found: Early revisions checked exhaustion after allowing one extra call and did not initially return safely when the failed page had never been assigned; one revision also failed to reset the allowance per page.
- Revision: Counted at most `max_attempts` calls for each cursor, reset the allowance after success, and returned completed records plus the failed cursor when retries were exhausted.
- One thing to remember: Define whether a limit means total attempts or additional retries, then assert the exact call count and cursor sequence.
- Recommended next exercise: MINI-008 — streaming and memory safety, using a generator with explicitly bounded retained state.

### MINI-008 — Reconcile Sorted File Streams

- Assumption or approach: Used one iterator per sorted input, retained one current record from each, and yielded reconciliation differences incrementally.
- Main issue found: The first version advanced both streams after unequal IDs and stopped without draining the remaining stream. The production follow-up initially proposed arbitrary batches identified by `batch_id`, which did not guarantee that matching keys met.
- Revision: Advanced only the smaller key, advanced both equal keys, handled either stream ending, and used a sentinel to consume one-pass iterables with O(1) additional state. Clarified that unsorted inputs require external sorting, deterministic hash partitioning by `file_id`, or an external keyed store.
- One thing to remember: A batch label provides lineage, not matching; both sides must use the same stable key-partition function and partition count, sized so the largest partition fits safely in a worker.
- Recommended next exercise: MINI-009 — schema evolution and contracts.

### MINI-009 — Check a Schema Change

- Assumption or approach: Applied the stated pipeline policy using two dictionary passes: existing fields in current order, then additions in proposed order.
- Main issue found: The initial set-based removal phase and proposed-driven comparison loop violated ordering; the test loop evaluated equality without asserting it. The first revision fixed the implementation but omitted the requested ordering regression.
- Revision: Added executable assertions and an assisted fixture that places a proposed addition before existing-field changes and a current removal after a changed field. All four submitted tests passed; external checks covered ordering permutations, allowed changes, empty schemas, and non-mutation.
- One thing to remember: A test must assert its result, and an ordering fixture must deliberately distinguish competing input orders. Allowed changes and unchanged schemas also need explicit tests.
- Production follow-up: Identified numeric limits, downstream calculations, and consumer contracts before approving int-to-float widening. Refined numeric capacity to exact representability: a 64-bit float cannot represent `2**53 + 1` exactly, even though it is within range.
- Recommended next exercise: MINI-010 — event and orchestration state.

## Completion Standard

A topic becomes `Solid` when both are true:

- the latest relevant exercise is a `Pass`
- correctness is at least 4/5 with no critical edge-case gap

Mark a topic `Revisit` if the same issue appears in two later exercises.

## Next Session

MINI-009 is complete. When ready to continue, use the mini prompt and say:

> Start mini. Use the next priority in `progress_mini.md`. Do not give hints unless I ask.

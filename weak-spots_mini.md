# Senior Data Engineer Python Mini Practice: Weak Spots

Last updated: 2026-09-09

Use this file only for weaknesses demonstrated during mini exercises. Keep entries specific, actionable, and linked to exercise IDs. Move resolved items to the resolved table instead of deleting them.

## Stage 1 Closure

- Stage ended: 2026-08-27
- Exercise completed: `MINI-001 — Validate a Payment Record`
- Final result: Pass — C4/P4/T3/J4
- Strong improvement: type boundaries, whitespace handling, boolean-as-integer behavior, deterministic error collection, and simpler control flow
- Carry-forward focus: exact contract naming and complete boundary-test selection
- Resolution note: No item is marked resolved yet because resolution requires two clean demonstrations in separate exercises.

## Active Weak Spots

| Priority | Weak spot | Evidence | Impact | Next drill | Status |
| --- | --- | --- | --- | --- | --- |
| 2 | Parse-then-validate control flow | MINI-004 initially inspected string formatting and validated before conversion, causing inconsistent behavior for zero, negative strings, and conversion errors. | Equivalent numeric representations can receive different validation results. | In a later parsing task, create one canonical candidate and apply domain checks once. | Recheck |
| 1 | Ordering-specific test selection | MINI-005 initially lost order through set operations. MINI-006 ultimately used deliberately conflicting manifest and arrival orders, but its first fixture also included a size mismatch and therefore did not isolate ordering. | An ordering bug can pass when both fixtures happen to use compatible orders or when another condition excludes a record first. | In a later test task, make competing input orders intentionally different while holding every other condition equal. | Recheck |
| 3 | Iterable-based bounded reconciliation | In the MINI-005 production follow-up, the proposed strategy was streaming with a `batch_id`. The follow-up example introduced `Iterable` inputs, an `Iterator` result, and sorted merge, but this pattern has not yet been implemented independently. | Lazy input/output avoids eager lists, but streaming alone can still retain O(n + m) keys unless matching state is bounded; calling `list()` on the result also restores eager buffering. | In Priority 8, implement a generator over sorted iterables, consume it incrementally, and explain the maximum retained state. | New |

Status values: `New`, `Practicing`, or `Recheck`.

## Initial Watchlist

These are starting hypotheses inherited from the longer practice tracker. Confirm them through mini exercises before moving them into `Active Weak Spots`.

| Area to watch | What good performance looks like |
| --- | --- |
| Test selection | Derive normal, invalid, boundary, duplicate/conflict, and failure-path tests from the contract. |
| Validation flow | Validate before use and deliberately choose skip, collect, retry, or stop. |
| Python type details | Distinguish missing values from valid falsy values and reject `bool` when a true integer is required. |
| Collection choice | Choose list, set, or keyed dictionary based on ordering, membership, and lookup needs. |
| Complexity explanation | Describe how often pages, records, and lookup keys are processed. |
| Output contracts | Preserve exact field names and consistent error shapes. |

## Resolved Weak Spots

Move an item here after two clean demonstrations in separate exercises.

| Weak spot | First seen | Clean demonstrations | Resolution evidence |
| --- | --- | --- | --- |
| Exact output-contract handling | MINI-001 | MINI-003, MINI-004-R7 | Preserved exact result shapes in MINI-003 and exact canonical keys and exception text in MINI-004-R7. |
| Type and boundary validation | MINI-001 | MINI-001-R2, MINI-004-R7 | Correctly handled whitespace and non-string identifiers, booleans, zero, negatives, and malformed values in two separate exercises. |
| Ordered uniqueness and collection choice | MINI-002 | MINI-003, MINI-005-R2 | Used insertion-ordered keyed lookups without set conversion and preserved each specified output order with linear membership checks. |
| Exception semantics and failure-path tests | MINI-004 | MINI-004-R8, MINI-005-R2 | Used explicit no-exception failure and exact `ValueError` assertions in two separate exercises. |

## Exercise Evidence

Add a compact entry only when an exercise reveals or rechecks a weakness.

### Entry Template

```markdown
### <Exercise ID>: <short label>

- Observed:
- Why it matters:
- Better rule:
- Small next drill:
- Status: New / Practicing / Recheck / Resolved
```

### MINI-001: Payment validation boundaries

- Observed: Field checkers returned `True` for success, and the final error result retained those booleans. The ID check did not enforce string type or whitespace handling, while the amount check accepted `bool` through `isinstance(True, int)`.
- Why it matters: The function violates its `list[str]` output contract and allows malformed payment data to pass validation.
- Better rule: Validate each field against its full requirement and append only its exact error message when invalid.
- Small next drill: Revise MINI-001 and test whitespace ID, integer ID, boolean amount, zero amount, and multiple simultaneous errors.
- Status: New

### MINI-001-R1: Payment validation revision

- Observed: The revision removed successful booleans from error output and correctly rejected integer IDs and boolean amounts. Whitespace-only IDs still passed, and the supplied example messages were not preserved.
- Why it matters: One malformed identifier still bypasses validation, and exact-output contract tests still fail.
- Better rule: Check the complete string condition, including `.strip()`, and turn each shown example into an exact assertion.
- Small next drill: Complete MINI-001-R2 with whitespace, integer ID, boolean amount, zero amount, and multi-error tests.
- Status: Practicing

### MINI-001-R2: Payment validation completion

- Observed: The function now rejects whitespace IDs, returns only strings, rejects booleans as amounts, accepts zero, and reports simultaneous errors in requirement order. Final cleanup also removed the unused flag and introduced stable error codes.
- Why it matters: The functional validation boundary is now reliable; only exact message wording and two missing submitted assertions remain as cautions.
- Better rule: Convert every explicit example and boundary requirement into an exact assertion.
- Small next drill: Preserve an exact output contract during MINI-002 and recheck one falsy/type boundary later.
- Status: Recheck

### MINI-002: Deduplicate Ingestion Events

- Observed: The initial implementation treated identical repeats as conflicts and returned the wrong empty-output shape. A revision introduced keyed lookup but converted conflicts through a set, losing the ordering guarantee. The final implementation used insertion-ordered dictionaries, preserved the input, and passed exact normal, duplicate, conflict, empty, ordering, and non-mutation checks.
- Why it matters: Idempotent ingestion must distinguish safe retries from conflicting replays, while deterministic output and stable return shapes protect downstream consumers and tests.
- Better rule: Derive equality, ordering, uniqueness, and empty-output requirements separately, then choose collections that satisfy all four without post-processing that discards guarantees.
- Small next drill: In MINI-003, select the lookup/grouping structure explicitly and write exact normal and empty assertions before considering the implementation complete.
- Status: Recheck

### MINI-003: Aggregate Usage Events

- Observed: Directly leveraged nested dictionaries for two-level keyed grouping, accurately preserving encounter order and handling zero accumulation. Correctly analyzed O(N) time and space bounds.
- Why it matters: Demonstrates clean collection selection and contract adherence on first pass.
- Better rule: In mutation tests, snapshot input beforehand (`snapshot = deepcopy(events)`), call the function on `events`, and assert `events == snapshot`.
- Small next drill: In MINI-004, test transformation with malformed / dirty fields alongside happy paths.
- Status: Clean demonstration (1/2 for output contract and collection choice)

### MINI-004: Usage normalization and exception semantics

- Observed: Early revisions validated raw string forms before parsing, returned exception objects instead of raising, and used invalid-input assertions that could falsely pass. MINI-004-R8 corrected the submitted tests with table-driven cases, exact error assertions, explicit failure when no exception is raised, and mutation snapshots.
- Why it matters: A normalization boundary must either return a complete canonical record or raise a stable exception; partial values and false-positive tests allow malformed data downstream.
- Better rule: Parse allowed inputs into one candidate, validate the canonical value once, and make every exception test fail explicitly when no exception is raised.
- Small next drill: Repeat the corrected failure-path assertion in one separate exercise before marking the weakness resolved.
- Status: Recheck for exception tests and parse-then-validate flow

### MINI-005: Ordered invoice reconciliation

- Observed: The first implementation used set operations that discarded order, and the next revision populated shared IDs from target order. The final version correctly drove source-ordered results from the source dictionary and target-ordered results from the target dictionary. Duplicate failure tests correctly used `try`/`except`/`else`, but no submitted case deliberately reversed shared-ID order.
- Why it matters: Reconciliation output may be logically correct as a set while still violating a deterministic sequence contract relied on by downstream processing and tests.
- Better rule: Derive each output from the input whose order the contract names, and construct fixtures where source and target order conflict.
- Small next drill: In MINI-006, write the reversed-order assertion before reviewing the supplied implementation.
- Status: Practicing for ordering-specific test selection; resolved for collection choice and exception-test semantics

### MINI-005 Follow-up: Large-scale reconciliation

- Observed: Proposed streaming plus a `batch_id` for snapshots that do not fit in memory. The answer identifies incremental processing and run identity, but does not yet specify how records with the same `invoice_id` meet without retaining all keys.
- Why it matters: A streaming loop can still consume unbounded memory when reconciliation requires global keyed matching.
- Better rule: Pair streaming with a concrete bounded-state mechanism: sorted merge, consistent hash partitioning, or an external keyed store. Use `batch_id` for lineage, snapshot isolation, checkpointing, and restart safety.
- Iterable rule: Accept `Iterable[Record]` when callers may provide a list, generator, file reader, or database cursor. Return `Iterator[Result]` and use `yield` when each reconciliation result can be consumed immediately.
- Memory warning: `Iterable` describes how values are supplied, not how much state the algorithm retains. A generator that stores every previously seen key is still O(n) memory, and wrapping the output in `list(...)` buffers every result.
- Small next drill: In Priority 8, state the input-order assumption, matching mechanism, checkpoint, and maximum retained state.
- Status: New

### MINI-006: Loadable-file contract tests

- Observed: The final tests cover empty input, normal matching, mismatches, unexpected arrivals, duplicates in either input, non-mutation, and exact manifest order. Early revisions mixed a size mismatch into an ordering fixture and briefly defined a case table without correctly calling the function with each row.
- Why it matters: A test can appear to cover ordering while actually passing or failing because of another filter, and unexecuted table rows provide no protection.
- Better rule: For an ordering test, make all compared records otherwise eligible and deliberately reverse the competing input order; verify that each table row is passed to the function under test.
- Small next drill: Repeat the same isolation pattern once in a later task with a different order-owning input.
- Status: Recheck

## Update Rules

After every mini exercise:

1. Add at most two demonstrated weak spots.
2. Cite the exercise ID as evidence.
3. Write one concrete rule or next drill, not a broad goal.
4. Do not record a weakness merely because the exercise did not cover that topic.
5. Mark an item resolved only after two separate clean demonstrations.
6. Keep `progress_mini.md` as the complete exercise history; keep this file focused on recurring learning needs.

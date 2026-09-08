# Senior Data Engineer Python Mini Practice: Weak Spots

Last updated: 2026-09-07

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
| 3 | Ordered uniqueness and collection choice | MINI-002 began with linear list membership; MINI-002-R1 removed duplicate conflicts using `set`, which did not preserve discovery order. The final version correctly used insertion-ordered dictionaries. | The wrong collection can produce O(n²) behavior or nondeterministic ordered output. | In MINI-003, state the ordering and lookup requirements before choosing list, set, or dictionary. | Recheck |
| 1 | Exception semantics and failure-path tests | MINI-004 revisions repeatedly returned `ValueError` objects or used `assert function(invalid_record)`, which could pass when no exception was raised. MINI-004-R8 corrected the tests with `try`/`except`/`else` and table-driven cases. | Malformed records can leak into output while tests incorrectly report success. | Repeat the corrected failure-path pattern in one separate exercise before resolving. | Recheck |
| 2 | Parse-then-validate control flow | MINI-004 initially inspected string formatting and validated before conversion, causing inconsistent behavior for zero, negative strings, and conversion errors. | Equivalent numeric representations can receive different validation results. | In a later parsing task, create one canonical candidate and apply domain checks once. | Recheck |

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

## Update Rules

After every mini exercise:

1. Add at most two demonstrated weak spots.
2. Cite the exercise ID as evidence.
3. Write one concrete rule or next drill, not a broad goal.
4. Do not record a weakness merely because the exercise did not cover that topic.
5. Mark an item resolved only after two separate clean demonstrations.
6. Keep `progress_mini.md` as the complete exercise history; keep this file focused on recurring learning needs.

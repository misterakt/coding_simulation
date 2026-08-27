# Senior Data Engineer Python Mini Practice: Weak Spots

Last updated: 2026-08-27

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
| 1 | Exact output-contract handling | MINI-001-R2 now uses stable error codes, but names such as `WRONGE_DATA_TYPE_PAYMENT_ID` are inconsistent and differ from the supplied example. | Contract consumers may depend on exact, correctly named codes. | Define canonical codes and assert the full multi-error result exactly. | Practicing |
| 2 | Type and boundary validation | MINI-001-R2 correctly handles whitespace/integer IDs, boolean amounts, and zero. | A regression could reintroduce malformed values without complete boundary tests. | Recheck these boundaries in one separate exercise before resolving. | Recheck |

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
| — | — | — | None yet. |

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

## Update Rules

After every mini exercise:

1. Add at most two demonstrated weak spots.
2. Cite the exercise ID as evidence.
3. Write one concrete rule or next drill, not a broad goal.
4. Do not record a weakness merely because the exercise did not cover that topic.
5. Mark an item resolved only after two separate clean demonstrations.
6. Keep `progress_mini.md` as the complete exercise history; keep this file focused on recurring learning needs.

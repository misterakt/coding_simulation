# Senior Data Engineer SQL Practice: Weak Spots

Last updated: 2026-08-27

Use this file only for weaknesses demonstrated during exercises run with `docs/senior_data_engineer_sql_interview_practice_prompt.md`. It is not a generic list of topics still to learn.

## Current Summary

- No SQL exercises have been reviewed yet.
- No demonstrated weak spots are active.
- Start with Priority 1 and promote an item from the watchlist only when an exercise provides evidence.
- Resolve a weak spot only after two clean demonstrations in different scenarios.

## Active Weak Spots

| Priority | Weak spot | Evidence | Impact | Focused next drill | Status |
| --- | --- | --- | --- | --- | --- |
| — | — | None yet. | — | Start SQL-001. | — |

Status values: `New`, `Practicing`, or `Recheck`.

## Initial Watchlist

These are risks to observe, not assumed weaknesses.

| Area to watch | What good performance looks like |
| --- | --- |
| Output grain | States one row per what before coding and preserves it through every query stage. |
| Join cardinality | Predicts one-to-one, one-to-many, or many-to-many behavior and prevents metric amplification. |
| Null semantics | Handles three-valued logic, outer-join filters, and missing values intentionally. |
| Aggregation | Groups at the required level and distinguishes rows, entities, and distinct events. |
| Deduplication | Defines a business key, precedence rule, and deterministic tie-breaker. |
| Temporal boundaries | States time zone and uses deliberate inclusive-start/exclusive-end logic. |
| Percentages and rates | Defines numerator and denominator grain and protects against integer division and zero. |
| Window functions | Chooses partition, ordering, and frame explicitly; explains tie behavior. |
| Reconciliation | Checks missing keys and value mismatches, not only total row counts. |
| Incremental processing | Accounts for late data, retries, overlap/lookback, and idempotency. |
| SQL maintainability | Uses named stages that make grain transitions and business rules auditable. |
| Performance reasoning | Uses data volume, distribution, pruning, and query-plan evidence rather than guesswork. |

## Resolved Weak Spots

| Weak spot | First seen | Clean demonstrations | Resolution evidence |
| --- | --- | --- | --- |
| — | — | — | None yet. |

## Exercise Evidence

Add at most two entries per reviewed exercise.

### Entry Template

```markdown
### <Exercise ID>: <short label>

- Observed:
- Why it matters:
- Better rule:
- Focused next drill:
- Status: New / Practicing / Recheck / Resolved
```

## Update Rules

1. Record only behavior demonstrated by a submitted query or explanation.
2. Cite the exercise ID and the exact query pattern or reasoning that revealed the issue.
3. Describe the production impact, not merely the syntax mistake.
4. Give one small next drill that can confirm improvement.
5. Add at most two weak spots from a single exercise.
6. Keep one underlying issue as one entry even when it creates several symptoms.
7. Move an item to `Recheck` after one clean correction.
8. Move it to `Resolved` only after a second clean demonstration in a different scenario.
9. If a resolved issue returns twice, move it back to `Active Weak Spots` as `Revisit` in `progress_sql.md`.
10. Keep the complete exercise history in `progress_sql.md`; keep this file focused on recurring learning needs.

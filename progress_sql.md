# Senior Data Engineer SQL Practice Progress

Last updated: 2026-08-27

Use this file with `docs/senior_data_engineer_sql_interview_practice_prompt.md`.

## Current Status

- Practice state: Ready to start
- Topics solid: 0 of 21
- Exercises completed: 0
- Current priority: 1 — Grain, keys, filtering, and nulls
- Recommended first exercise: SQL-001 — establish grain and calculate order totals safely
- Default mode: Full Interview
- Default dialect: PostgreSQL 15+
- Next exercise ID: SQL-001
- Current no-hint streak: 0

## Priority Queue

Work from the highest priority unless an active weak spot needs a retry. A topic becomes `Solid` after two clean demonstrations in different scenarios, including one without hints.

| Priority | Topic | Status | Clean demonstrations | Best score C/G/Q/P/E | Next action |
| --- | --- | --- | --- | --- | --- |
| 1 | Grain, keys, filtering, and nulls | Not started | 0 | — | Start SQL-001. |
| 2 | Aggregation and conditional aggregation | Not started | 0 | — | Pending. |
| 3 | Join correctness and cardinality | Not started | 0 | — | Pending. |
| 4 | Deduplication and latest-state selection | Not started | 0 | — | Pending. |
| 5 | Date, timestamp, interval, and time-zone logic | Not started | 0 | — | Pending. |
| 6 | Percentages, ratios, rates, and safe arithmetic | Not started | 0 | — | Pending. |
| 7 | Core window functions | Not started | 0 | — | Pending. |
| 8 | CTEs, subqueries, and set operations | Not started | 0 | — | Pending. |
| 9 | Reconciliation and data-quality SQL | Not started | 0 | — | Pending. |
| 10 | Gaps and islands, sequences, and sessionization | Not started | 0 | — | Pending. |
| 11 | Top-N, percentiles, median, and distribution | Not started | 0 | — | Pending. |
| 12 | Incremental loads, watermarks, and late data | Not started | 0 | — | Pending. |
| 13 | CDC and slowly changing dimensions | Not started | 0 | — | Pending. |
| 14 | Cohorts, retention, funnels, and attribution | Not started | 0 | — | Pending. |
| 15 | Dimensional-model queries | Not started | 0 | — | Pending. |
| 16 | Semi-structured and nested data | Not started | 0 | — | Pending. |
| 17 | Pivoting, unpivoting, and reshaping | Not started | 0 | — | Pending. |
| 18 | Recursive SQL and hierarchies | Not started | 0 | — | Pending. |
| 19 | DML, transactions, and idempotent writes | Not started | 0 | — | Pending. |
| 20 | Query performance and physical design | Not started | 0 | — | Pending. |
| 21 | Security-aware SQL | Not started | 0 | — | Pending. |

Status values: `Not started`, `Practicing`, `Solid`, or `Revisit`.

## Exercise Log

Add one row after each reviewed exercise. If no query was submitted, use `In progress` and leave scores blank.

| Date | ID | Priority/topic | Mode | Result | Scores C/G/Q/P/E | Time | Highest hint | Main skill demonstrated | Next step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | — | — | — | — | — |

Score key: `C` correctness, `G` grain/cardinality, `Q` SQL quality, `P` production judgment, `E` explanation. Each score is out of 5.

## Session Notes

Keep only information that will improve the next attempt.

### Entry Template

```markdown
### <Exercise ID>: <title>

- Output grain:
- Approach used:
- Strongest point:
- Main issue:
- Revision made:
- Hidden case to remember:
- Recommended next exercise:
```

## Coverage Checkpoints

Use these checkpoints to ensure practice covers more than isolated syntax.

| Checkpoint | Required evidence | Status |
| --- | --- | --- |
| Foundation | Clean aggregation, null handling, and correct one-to-many join | Not started |
| Analytical SQL | Ranking, `LAG`/`LEAD`, and explicit window-frame exercise | Not started |
| Temporal SQL | Timestamp boundary plus time-zone or interval reasoning | Not started |
| Metrics | Percentage/rate with safe denominator and explicit grain | Not started |
| Pipeline SQL | Deduplication plus incremental/late-data exercise | Not started |
| Data correctness | Reconciliation and at least two data-quality checks | Not started |
| Advanced modeling | SCD/CDC, cohort/session, or dimensional-model exercise | Not started |
| Production readiness | Query-plan/physical-design and idempotent-write discussion | Not started |

## Next Session

Use the SQL prompt and say:

> Start sql. Use the next priority in `progress_sql.md`. Include executable sample data and do not give hints unless I ask.

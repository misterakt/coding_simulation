The simplest practical streaming version is a “merge reconciliation.” It reads one source record and one target record at a time instead of building two large dictionaries.

The important requirement: both inputs must be sorted by `invoice_id`.

## Mental model

Imagine two sorted lists:

```text
source: inv-1, inv-2, inv-3
target: inv-1, inv-2, inv-4
```

Compare the current record from each side:

- Same ID: compare `amount` and `status`, then advance both.
- Source ID is smaller: it exists only in source; advance source.
- Target ID is smaller: it exists only in target; advance target.

Only two records need to be held at once.

## Streaming implementation

```python
from collections.abc import Iterable, Iterator
from typing import Any


def require_sorted_unique(
    records: Iterable[dict[str, Any]],
) -> Iterator[dict[str, Any]]:
    previous_id: str | None = None

    for record in records:
        invoice_id = record["invoice_id"]

        if previous_id is not None:
            if invoice_id == previous_id:
                raise ValueError("duplicate invoice_id")

            if invoice_id < previous_id:
                raise ValueError("input must be sorted by invoice_id")

        previous_id = invoice_id
        yield record


def reconcile_invoice_streams(
    source: Iterable[dict[str, Any]],
    target: Iterable[dict[str, Any]],
    batch_id: str,
) -> Iterator[dict[str, str]]:
    source_iterator = iter(require_sorted_unique(source))
    target_iterator = iter(require_sorted_unique(target))

    source_record = next(source_iterator, None)
    target_record = next(target_iterator, None)

    while source_record is not None or target_record is not None:
        if source_record is None:
            yield {
                "batch_id": batch_id,
                "classification": "only_in_target",
                "invoice_id": target_record["invoice_id"],
            }
            target_record = next(target_iterator, None)
            continue

        if target_record is None:
            yield {
                "batch_id": batch_id,
                "classification": "only_in_source",
                "invoice_id": source_record["invoice_id"],
            }
            source_record = next(source_iterator, None)
            continue

        source_id = source_record["invoice_id"]
        target_id = target_record["invoice_id"]

        if source_id < target_id:
            yield {
                "batch_id": batch_id,
                "classification": "only_in_source",
                "invoice_id": source_id,
            }
            source_record = next(source_iterator, None)

        elif target_id < source_id:
            yield {
                "batch_id": batch_id,
                "classification": "only_in_target",
                "invoice_id": target_id,
            }
            target_record = next(target_iterator, None)

        else:
            amount_changed = (
                source_record["amount"] != target_record["amount"]
            )
            status_changed = (
                source_record["status"] != target_record["status"]
            )

            if amount_changed or status_changed:
                yield {
                    "batch_id": batch_id,
                    "classification": "changed",
                    "invoice_id": source_id,
                }

            source_record = next(source_iterator, None)
            target_record = next(target_iterator, None)
```

## Using it

```python
source = [
    {"invoice_id": "inv-1", "amount": 100, "status": "open"},
    {"invoice_id": "inv-2", "amount": 50, "status": "paid"},
    {"invoice_id": "inv-3", "amount": 0, "status": "open"},
]

target = [
    {"invoice_id": "inv-1", "amount": 100, "status": "open"},
    {"invoice_id": "inv-2", "amount": 55, "status": "paid"},
    {"invoice_id": "inv-4", "amount": 20, "status": "open"},
]

results = reconcile_invoice_streams(
    source,
    target,
    batch_id="batch-20260907-001",
)

for result in results:
    print(result)
```

Output:

```python
{
    "batch_id": "batch-20260907-001",
    "classification": "changed",
    "invoice_id": "inv-2",
}
{
    "batch_id": "batch-20260907-001",
    "classification": "only_in_source",
    "invoice_id": "inv-3",
}
{
    "batch_id": "batch-20260907-001",
    "classification": "only_in_target",
    "invoice_id": "inv-4",
}
```

In production, the loop could write each result immediately:

```python
for result in reconcile_invoice_streams(source, target, batch_id):
    write_to_database(result)
```

Avoid doing this for large data:

```python
results = list(reconcile_invoice_streams(...))
```

`list()` collects everything and removes much of the memory benefit.

## Reading from files lazily

For newline-delimited JSON files:

```python
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def read_json_lines(
    path: Path,
) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)
```

Then:

```python
source = read_json_lines(Path("source.jsonl"))
target = read_json_lines(Path("target.jsonl"))

for result in reconcile_invoice_streams(
    source,
    target,
    batch_id="batch-20260907-001",
):
    write_to_database(result)
```

The files must already be sorted by `invoice_id`.

## What `batch_id` contributes

Your `batch_id` idea is useful for:

- Identifying all results from one reconciliation run.
- Retrying the same run safely.
- Tracking checkpoints.
- Auditing which snapshots produced a result.

On retry, reuse the same `batch_id`; creating a new one would make the retry look like a separate run.

However, `batch_id` does not perform matching. The sorted merge is what bounds memory.

## Important tradeoff

Your original function preserves source and target encounter order. A sorted streaming merge produces `invoice_id` order instead. You generally cannot preserve arbitrary original order and use constant-memory sorted merging at the same time.

A concise interview explanation would be:

> I would change the function from returning accumulated lists to yielding reconciliation events. I would require both snapshots to be sorted by invoice ID and use a merge-style comparison, keeping only one record from each stream in memory. The batch ID would provide run identity and checkpoint lineage, while the sorted merge would provide bounded matching state.

# Python Interview Practice: Weak Spots And Drills

Last updated: 2026-09-07

This is a practice guide, not a list of failures. These are the areas that caused the most friction across the practice exercises and will produce the biggest improvement with repetition.

## 1. Creating Test Scenarios Before Coding

### Pattern noticed

The main difficulty has been deciding what to test, especially edge cases and failure paths. Initial tests usually covered empty input, one valid input, and the happy path. Important requirements such as malformed data, conflicts, invalid types, limits, and exceptions were often added only after review.

MINI-004 initially used invalid-input assertions that could pass when the function returned a truthy value instead of raising. In MINI-004-R8, this improved to table-driven valid and invalid cases, exact exception-message checks, explicit failure when no exception is raised, and input-mutation snapshots. This is one clean demonstration; repeat it independently before treating the pattern as resolved.

### Better mental model

Every requirement should become at least one test. Ask four questions:

1. What is the normal successful case?
2. What input is empty, missing, blank, or at a boundary?
3. What can be invalid but still not crash the function?
4. What state or count must change after this case?

### Drill

Before writing code, write a compact test list:

```text
empty input
one valid input
one rule violation per requirement
multiple violations in one record
duplicate/conflict or other special branch
external exception or malformed response
boundary value: 0, None, empty list, final page
```

Group equivalent inputs into a table and use one assertion helper per behavior. This reduces duplicated test code while keeping each contract rule visible.

## 2. Validation Order And Failure Control Flow

### Pattern noticed

There was recurring uncertainty about when to validate a value, when an exception variable exists, and whether an error path should continue or stop. This appeared in event validation and especially API-response handling.

### Rule to remember

Validate before using data. On a non-recoverable failure, record context, set the failure state, and exit that path.

```python
response = fetch_page(cursor)

if not isinstance(response, dict):
    errors.append(error_log(cursor, "response is not a dictionary"))
    failed = True
    break
```

`e` exists only inside `except Exception as e:`. A validation problem is not an exception unless code actually raised one.

For an expected-exception test, returning normally must fail the test:

```python
try:
    function(invalid_input)
except ValueError as error:
    assert str(error) == "expected message"
else:
    raise AssertionError("Expected ValueError")
```

Do not use `assert function(invalid_input)` to test raising: a truthy return value makes that assertion pass.

### Drill

For every external input, identify:

- type validation
- required fields
- value validation
- action on failure: skip, collect and continue, or stop

## 3. Python Type And Truthiness Details

### Pattern noticed

Using `not record.get(field)` initially treated valid falsy values such as `0` as missing. Schema validation also required learning that `bool` is a subclass of `int`.

### Rules to remember

```python
not record.get("age")
```

is too broad when `0` may be valid.

```python
isinstance(True, int)  # True
```

For required string fields, check for absent key, `None`, empty string, and whitespace string intentionally. For integer fields, explicitly reject booleans when the domain requires a real integer.

### Drill

Test every validator with:

```text
missing key, None, "", "   ", 0, False, expected valid value, wrong type
```

Only include values that make sense for the field, but build the habit of checking them deliberately.

## 4. Collections: Lists, Sets, And Dictionaries

### Pattern noticed

Tuple keys, set intersection/difference, dictionary key views, and `append` versus `extend` needed extra explanation during reconciliation and pagination.

### Rules to remember

```python
common_keys = source_keys & target_keys
only_source = source_keys - target_keys
```

`&` and `-` are set operations. Normal dictionaries are lookup tables, so use their key views when needed:

```python
common_keys = source_by_key.keys() & target_by_key.keys()
```

For lists:

```python
records.append(item)  # add one item
records.extend(items) # add each item from another iterable
```

### Drill

For any matching problem, say out loud:

```text
What is my key?
Do I need membership, lookup, or output order?
Should this data be a list, set, or dictionary?
```

## 5. Complexity: Understand What Is Repeated

### Pattern noticed

The `O(n + p)` pagination complexity was initially confusing because pages contain records.

### Rule to remember

Count how many times each unit of work is processed.

- Pagination: each page is fetched once (`p`) and each record is processed once total (`n`), so `O(p + n)`.
- Nested source/target scan: every source row is compared against every target row, so `O(n * m)`.
- Dictionary lookup: build each dictionary once, then look up each shared key, so `O(n + m)` on average.

The inner loop does not automatically mean multiplication. It becomes multiplication only when the full inner collection is repeated for every outer item.

## 6. Output Contracts And Consistent Error Shapes

### Pattern noticed

Early revisions occasionally used a slightly different field name or error shape from the requested contract.

### Rule to remember

Treat the return shape as an API contract. Before coding, copy the requested keys into a skeleton return value and keep error entries consistent.

```python
{
    "cursor": cursor,
    "reason": message,
}
```

### Drill

Add one assertion that checks the full empty-result contract. For special cases, assert only the fields relevant to that behavior so tests remain readable.

## 7. Streaming Does Not Automatically Bound Reconciliation State

### Pattern noticed

For the MINI-005 scale follow-up, the proposed approach was streaming with a `batch_id`. Streaming is the right direction for incremental reads, and `batch_id` is useful for lineage and resumability, but neither determines how matching state is bounded.

### Rule to remember

Two large snapshots still need a concrete matching strategy:

- sorted inputs plus a merge join, retaining only the current keys
- consistent hash partitioning by business key, processing one bounded partition at a time
- an external keyed store or database join when local state cannot fit in memory

Use `batch_id` to identify the snapshot/run, isolate retries, record checkpoints, and make outputs traceable. Do not treat it as the lookup mechanism.

### Python interface to remember

`Iterable[T]` means the function can receive values one at a time from a list, generator, file reader, or database cursor. `Iterator[T]` is the stateful object consumed with `next()`; a generator function that uses `yield` returns an iterator.

```python
from collections.abc import Iterable, Iterator
from typing import Any


def reconcile_streams(
    source: Iterable[dict[str, Any]],
    target: Iterable[dict[str, Any]],
) -> Iterator[dict[str, Any]]:
    ...
    yield reconciliation_result
```

Prefer `Iterable` for the input annotation when the function only needs to loop once. Use `Iterator` for the return annotation when results are yielded lazily.

```python
for result in reconcile_streams(source, target):
    write_result(result)  # consume immediately
```

Avoid `list(reconcile_streams(...))` for unbounded data because it collects every result in memory. Also remember that lazy iteration alone is not enough: the algorithm must avoid accumulating all previously seen keys. A sorted merge can retain only the current record from each iterator.

### Drill

For any streaming reconciliation design, state five things explicitly:

```text
input ordering or partitioning assumption
where keyed matching happens
maximum state retained in memory
checkpoint and restart boundary
whether any caller converts the iterator back into a list
```

## What Is Already Improving

- You now use keyed dictionaries instead of nested matching loops.
- You distinguish exceptions from validation errors.
- You track state clearly for ingestion: current cursor, last successful cursor, next cursor, counts, and failure flag.
- You are increasingly choosing simple, readable control flow such as `while True` with explicit `break` conditions.

## Highest-Value Next Step

For the next exercise, spend the first five minutes writing tests before implementation. Aim for one test for every stated rule, then use those tests as your build checklist.

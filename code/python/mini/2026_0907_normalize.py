"""
-- conditions
  - Strip surrounding whitespace from account_id and metric, and lowercase metric
  - Parse units from an int, float, or numeric string into an int or float
  - Reject missing, non-string, or whitespace-only identifiers.
  - Reject booleans, non-numeric units, and negative units by raising ValueError("invalid usage event")
-- 

  core logic

   0. validate the record param itself
   1. convert proper string
        

   2. validate the each attribtues 
   3. return 

   




"""
from copy import deepcopy
from typing import Any
import math

def normalize_usage_event(record: dict[str, Any]) -> dict[str, Any]:


    if record is None or not isinstance(record, dict):
        return {} 



    def convert_attributes(value, param_type):
        if value is None or (isinstance(value,str) and len(value.strip()) == 0) or not isinstance(value,str):
            raise ValueError("invalid usage event") 
        if param_type == "account_id" and isinstance(value, str):
            return value.strip()
        if param_type == "metric" and isinstance(value, str):
            return value.strip().lower()

    def parse_units(value):
        unit_cancidate = None
        if isinstance(value, bool):
            raise ValueError("invalid usage event")
        elif isinstance(value, int) or isinstance(value, float):
            unit_cancidate = value 
        elif isinstance(value,str):
            if len(value.strip()) == 0:
               raise ValueError("invalid usage event")
            try:
                unit_cancidate = int(value)
            except ValueError as e:
                try:
                    unit_cancidate = float(value)
                except ValueError as e:
                    raise ValueError("invalid usage event")
        else:
            raise ValueError("invalid usage event")

        return unit_cancidate
        

    ## validate 



    ## main functions (normalize)

    account_id_candidate = convert_attributes(record.get("account_id"), 'account_id')
    metric_candidate = convert_attributes(record.get("metric"), 'metric')
    unit_candidate = parse_units(record.get("units"))

    if math.isnan(unit_candidate) or math.isinf(unit_candidate) or unit_candidate < 0:
        raise ValueError("invalid usage event")
    
    return {
        "account_id" : account_id_candidate,
        "metric" : metric_candidate,
        "units" : unit_candidate
    }

def test_invalid_data(record: dict[str, Any]) -> None:
    before = deepcopy(record)

    try:
        normalize_usage_event(record)
    except ValueError as error:
        assert str(error) == "invalid usage event"
    else:
        raise AssertionError(
            f"Expected ValueError for record: {record!r}"
        )

    assert record == before 



if __name__ == "__main__":
    

    invalid_cases = [
        {"metric": "calls", "units": 1},  # missing account account_id
        {"account_id": "A", "units": 1},  # missing metric
        {"account_id": "   ", "metric": "calls", "units": 1},
        {"account_id": "A", "metric": 123, "units": 1},
        {"account_id": "A", "metric": "calls", "units": True},
        {"account_id": "A", "metric": "calls", "units": "unknown"},
        {"account_id": "A", "metric": "calls", "units": -1},
        {"account_id": "A", "metric": "calls", "units": "-1.5"},
    ]

    for record in invalid_cases:
        test_invalid_data(record)

valid_cases = [
    (
        {
            "account_id": " A ",
            "metric": " API_CALLS ",
            "units": "42",
        },
        {
            "account_id": "A",
            "metric": "api_calls",
            "units": 42,
        },
    ),
    (
        {
            "account_id": "A",
            "metric": "storage_gb",
            "units": "4.5",
        },
        {
            "account_id": "A",
            "metric": "storage_gb",
            "units": 4.5,
        },
    ),
    (
        {
            "account_id": "A",
            "metric": "calls",
            "units": "0",
            "source_file": "batch.json",
        },
        {
            "account_id": "A",
            "metric": "calls",
            "units": 0,
        },
    ),
]

for record, expected in valid_cases:
    before = deepcopy(record)

    assert normalize_usage_event(record) == expected
    assert record == before


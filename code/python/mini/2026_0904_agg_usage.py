"""
Requirements
Group and sum units keyed first by account_id, then by metric.
Preserve first-seen encounter order for both account_id and each metric under that account.
Accurately accumulate numeric units including 0 / 0.0.
Return {} when given an empty list.
Do not mutate the input events list or any inner dictionaries.
"""

from copy import deepcopy
from typing import Any

def aggregate_usage_by_account(events: list[dict[str, Any]]) -> dict[str, dict[str, int | float]]:
    
    if events is None:
        return {}



    accu_dict_data = {}

    # main logic

    for event in events: 
        # learning point - spelling check!! 
        # compare the previous values from dict data    
        new_event_accout_id = event.get("account_id")
        new_metric = event.get("metric")
        new_unit = event.get("units")  
        if new_event_accout_id not in accu_dict_data:
            accu_dict_data[new_event_accout_id] = { new_metric : new_unit}
            # accu_dict_data[new_event_accout_id][new_metric] = new_unit
        else:
            # keep the first-seens encounter order 
            if new_metric not in accu_dict_data[new_event_accout_id]:
                accu_dict_data[new_event_accout_id][new_metric] = new_unit
            else:
                accu_dict_data[new_event_accout_id][new_metric] += new_unit


    return accu_dict_data




if __name__ == "__main__":

    events = [
        {"account_id": "acc_101", "metric": "api_calls", "units": 150},
        {"account_id": "acc_202", "metric": "storage_gb", "units": 50},
        {"account_id": "acc_101", "metric": "api_calls", "units": 50},
        {"account_id": "acc_101", "metric": "compute_hours", "units": 4.5},
    ]

    events_with_only_one_account_id = [
        {"account_id": "acc_101", "metric": "api_calls", "units": 150},
        {"account_id": "acc_101", "metric": "api_calls", "units": 100},
        {"account_id": "acc_101", "metric": "compute_hours", "units": 6.5},
    ]

    events_order_test = [
        {"account_id": "acc_101", "metric": "api_calls", "units": 150},
        {"account_id": "acc_101", "metric": "api_calls", "units": 50},
        {"account_id": "acc_101", "metric": "compute_hours", "units": 4.5},
        {"account_id": "acc_102", "metric": "compute_hours", "units": 50},
        {"account_id": "acc_102", "metric": "compute_hours", "units": 4.5},
        {"account_id": "acc_102", "metric": "storage_gb", "units": 150},
    ]


    # test cases
    # empty case 
    assert aggregate_usage_by_account([]) == {}

    # success case
    assert aggregate_usage_by_account(events) == {'acc_101': {'api_calls': 200, 'compute_hours': 4.5}, 'acc_202': {'storage_gb': 50}}

    # only one account
    assert aggregate_usage_by_account(events_with_only_one_account_id) == {'acc_101': {'api_calls': 250, 'compute_hours': 6.5}}

    # first seen enocounter order check
    assert aggregate_usage_by_account(events_order_test) == {'acc_101': {'api_calls': 200, 'compute_hours': 4.5}, 'acc_102': {'compute_hours': 54.5, 'storage_gb': 150}}

    # input mutate check
    copied_event = deepcopy(events)
    assert aggregate_usage_by_account(copied_event) == {'acc_101': {'api_calls': 200, 'compute_hours': 4.5}, 'acc_202': {'storage_gb': 50}}
from typing import Any

def deduplicate_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    

    dedup_cnt = 0
    conflict_cnt = 0

    valid_list = []
    invalid_list = []
    seen_events = dict()
    required_fields = ["event_id","customer_id","event_type","event_time"]

    def is_missing_required_value(value: Any) -> bool:
        return value is None or (isinstance(value,str) and value.strip() == "")


    for event in events:
        
        # check the invalid event 
        # should not be the part of dedup 

        missing_fields = [
            field
            for field in required_fields
            if field not in event or is_missing_required_value(event[field])
        ]

        if missing_fields:

            wrapper_data = {"record" : event , "reason" : f"{', '.join(missing_fields)}"}
            invalid_list.append(wrapper_data)

            continue
        
        # If the same event_id appears with different content, keep the first valid event and count later conflicting records as conflicts.
        event_id = event.get("event_id")
        if event_id in seen_events:
        
            if seen_events[event_id] != event:
                conflict_cnt += 1
            elif seen_events[event_id] == event:
                dedup_cnt += 1

        else:
            seen_events[event.get("event_id")] = event
            valid_list.append(event)


    return {"valid_events" : valid_list , "duplicate_count": dedup_cnt, "conflict_count": conflict_cnt, "invalid_events": invalid_list}



if __name__ == "__main__":


    sample_data = {
        "event_id": "evt_123",
        "customer_id": "cust_1",
        "event_type": "purchase",
        "event_time": "2026-08-14T10:15:00Z",
        "payload": {"amount": 42.5, "currency": "EUR"}
    }

    print(deduplicate_events([]))
    
    # Empty input
    assert deduplicate_events([]) == {
        "valid_events": [],
        "duplicate_count" : 0,
        "conflict_count" : 0,
        "invalid_events": [],
    }

    # singe valid event
    assert deduplicate_events([sample_data]) == {
        "valid_events": [sample_data],
        "duplicate_count": 0,
        "conflict_count": 0,
        "invalid_events": []
    }

    result = deduplicate_events([sample_data, sample_data.copy()])
    assert result["valid_events"] == [sample_data]
    assert result["duplicate_count"] == 1
    assert result["conflict_count"] == 0
    assert result["invalid_events"] == []
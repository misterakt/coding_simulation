'''
1. process
- ignore later events that are exactly equal
- ignore conflicting duplicates but add their add event_id 
- preserve retained-event order and conflict discovery order
- do not touch original parameter vars

'''

from copy import deepcopy

def deduplicate_events(
    events: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[str]]:
    

    conflict_event_ids = {}
    event_dict = {}

    if events is None or events == []:
        return ([],[])

    for event in events:
        event_id = event.get("event_id")

        '''  first specify the conditions if it's complex = learning 
        1. check event_id 
             1. NO -> add event list
             2. yes -> check duplicated event itself 

        '''
        if event_id not in event_dict:
            event_dict[event_id] = event
        else:
            if event != event_dict[event_id]:
                # because dics doesn't allow to have duplicated keys  = major learning point
                conflict_event_ids[event_id] = None
            else:
                continue

    # if dict is converted to list by list(), it only returns keys = major learning point
    return list(event_dict.values()),list(conflict_event_ids)



if __name__ == "__main__":

    normal_events_only_one_event_ids = [
        {"event_id": "e1", "amount": 100},
        {"event_id": "e1", "amount": 999},
        {"event_id": "e1", "amount": 500},
    ]

    test_events_all_duplicates = [
        {"event_id": "e1", "amount": 100},
        {"event_id": "e1", "amount": 100},
        {"event_id": "e1", "amount": 100},
    ]

    test_empty_input = []

    test_events_retained_order_conoflict_discovery = [
        {"event_id": "e1", "amount": 100},
        {"event_id": "e2", "amount": 100},
        {"event_id": "e3", "amount": 100},
        {"event_id": "e3", "amount": 200},
        {"event_id": "e4", "amount": 50},
        {"event_id": "e4", "amount": 51},
    ]

    test_deep_events = [
        {"event_id": "e1", "amount": 100},
        {"event_id": "e1", "amount": 999},
    ]

    deep_copied_events = deepcopy(test_deep_events)
    deduplicate_events(test_deep_events)
    assert test_deep_events == deep_copied_events

    # one event_id case
    assert deduplicate_events(normal_events_only_one_event_ids) ==  \
        ([{'event_id': 'e1', 'amount': 100}],['e1'])

    # # # # all duplicates
    assert deduplicate_events(test_events_all_duplicates) ==  \
        ([{'event_id': 'e1', 'amount': 100}],[])

    # # # # no input case
    assert deduplicate_events(test_empty_input) == ([],[])

    # test_retained_event_order + conflict_discovery_order 
    assert deduplicate_events(test_events_retained_order_conoflict_discovery) ==  \
        ([{'event_id': 'e1', 'amount': 100},{'event_id': 'e2', 'amount': 100},{'event_id': 'e3', 'amount': 100},{'event_id': 'e4', 'amount': 50}], ['e3','e4'])


from typing import Any, Callable


def mock_fetch_page_non_data(cursor = None):
    if cursor == None: 
        return {
        }


def mock_fetch_page(cursor = None):

    if cursor == None: 
        return {
        "items": [
            {"id": "rec_1", "updated_at": "2026-08-20T10:00:00Z", "payload": {"value": 10}},
            {"id": "rec_2", "updated_at": "2026-08-20T10:05:00Z", "payload": {"value": 20}},
        ],
        "next_cursor": "cursor_2"
        }

    if cursor == 'cursor_2': 
        return {
        "items": [
            {"id": "rec_3", "updated_at": "2026-08-20T10:00:00Z", "payload": {"value": 10}},
            {"id": "rec_4", "updated_at": "2026-08-20T10:05:00Z", "payload": {"value": 20}},
        ],
        "next_cursor": "cursor_3"
        }

    if cursor == 'cursor_3': 
        return {
        "items": [
            {"id": "rec_5", "updated_at": "2026-08-20T10:00:00Z", "payload": {"value": 10}},
            {"id": "rec_6", "updated_at": "2026-08-20T10:05:00Z", "payload": {"value": 20}},
        ],
        "next_cursor": "cursor_4"
        }

    if cursor == 'cursor_4': 
        return {
        "items": [
            {"id": "rec_7", "updated_at": "2026-08-20T10:00:00Z", "payload": {"value": 10}},
            {"id": "rec_8", "updated_at": "2026-08-20T10:05:00Z", "payload": {"value": 20}},
        ],
        "next_cursor": None
        }


def mock_fetch_page_bad_1(cursor = None):

    if cursor == None: 
        return {
        "items": [
            {"id": "rec_1", "updated_at": "2026-08-20T10:00:00Z", "payload": {"value": 10}},
            {"id": "rec_2", "updated_at": "2026-08-20T10:05:00Z", "payload": {"value": 20}},
        ],
        "next_cursor": "cursor_2"
        }

    if cursor == 'cursor_2': 
        return {
        "items": [
            {"id": "rec_3", "updated_at": "2026-08-20T10:00:00Z", "payload": {"value": 10}},
            {"id": "rec_4", "updated_at": "2026-08-20T10:05:00Z", "payload": {"value": 20}},
        ],
        # "next_cursor": "cursor_3"
        }

    if cursor == 'cursor_3': 
        return {
        "items": [
            {"id": "rec_5", "updated_at": "2026-08-20T10:00:00Z", "payload": {"value": 10}},
            {"id": "rec_6", "updated_at": "2026-08-20T10:05:00Z", "payload": {"value": 20}},
        ],
        "next_cursor": "cursor_4"
        }

    if cursor == 'cursor_4': 
        return {
        # "items": [
        #     {"id": "rec_7", "updated_at": "2026-08-20T10:00:00Z", "payload": {"value": 10}},
        #     {"id": "rec_8", "updated_at": "2026-08-20T10:05:00Z", "payload": {"value": 20}},
        # ],
        "next_cursor": None
        }


def error_log(cursor, message):
    return {'cursor' : cursor , 'reason' : message}

def ingest_paginated_api(
    fetch_page: Callable[[str | None], dict[str, Any]],
    start_cursor: str | None = None,
    max_pages: int | None = None,
) -> dict[str, Any]:

    '''
        * flow
        1.  fetch from start_cursor
        2.  stop when "next_cursor = None" 

        * condition
        1. if max_pages is provided -> stop after fetching at most that many pages
        2. preserve order record
        3. validate response
            - response must be dict
            - item must exist and list
            - next_cursor must exit 
            - last cursor - cursor for the last successfully fetched page
            - next cursor - to resume after stopping 

        * complexity 
        1. time - O(N) 
        2. SPACE - O(K) where the K output's space 
    '''
    # vars
    records = list()
    errors = list()
    pages_fetched = 0
    records_fetched = 0
    failed  = False
    last_cursor = start_cursor
    next_cursor = None
    current_success_cursor = None
    # helper functions 


    # main process
    # API error hadnling + check major attributes 
    
    while True:

        if max_pages is not None:
            if pages_fetched >= max_pages or max_pages == 0:
                break
        try:
            fetched_item = fetch_page(last_cursor)
        except Exception as e:
            errors.append(error_log(last_cursor,f"error at fetch_page with message : {str(e)}"))
            failed = True
            break

        if not isinstance(fetched_item, dict):
            errors.append(error_log(last_cursor,f"fetched_page error : response is not a dictionary"))
            failed = True
            break  # easily leave, since no meaning continuing the flow without dict item

        if 'items' not in fetched_item:
            errors.append(error_log(last_cursor,f"fetched_page error : items field is missing"))
        elif not isinstance(fetched_item.get('items'),list):
            errors.append(error_log(last_cursor,f"fetched_page error : items must be a list"))

        if 'next_cursor' not in fetched_item:
            errors.append(error_log(last_cursor,f"fetched_page error : next cursor doesn't exist"))

        if len(errors) > 0:
            failed = True
            break

        if failed is not True:
            # main flow
            items = fetched_item.get("items")
            next_cursor = fetched_item.get("next_cursor")
                
            # processing the records
            for item in items:
                records.append(item) 
                records_fetched += 1 

            current_success_cursor = last_cursor
            last_cursor = next_cursor
            pages_fetched += 1

        if fetched_item.get('next_cursor') is None:
            break

            


    return {
    "records": records,
    "errors": errors,
    "summary": {
        "pages_fetched": pages_fetched,
        "records_fetched": records_fetched,
        "failed": failed,
        "last_cursor": current_success_cursor,
        "next_cursor": next_cursor
    }
}




if __name__ == "__main__":


    ## happy case
    assert len(ingest_paginated_api(mock_fetch_page,start_cursor = None, max_pages = 2)['records']) == 4, "happy case"
    assert ingest_paginated_api(mock_fetch_page,start_cursor = None, max_pages = 2)['summary'] == {
            "pages_fetched": 2,
            "records_fetched": 4,
            "failed": False,
            "last_cursor": "cursor_2",
            "next_cursor": "cursor_3"
        }
    assert len(ingest_paginated_api(mock_fetch_page,start_cursor = None, max_pages = 2)['errors']) == 0

    ## non data
    assert ingest_paginated_api(mock_fetch_page_non_data,start_cursor = None, max_pages = 4)['records'] == [] 
    assert ingest_paginated_api(mock_fetch_page_non_data,start_cursor = None, max_pages = 4)['summary'] == {'pages_fetched': 0, 'records_fetched': 0, 'failed': True, 'last_cursor': None, 'next_cursor': None}
    
    ## bad data
    assert len(ingest_paginated_api(mock_fetch_page_bad_1,start_cursor = None, max_pages = 4)['records']) == 2
    assert ingest_paginated_api(mock_fetch_page_bad_1,start_cursor = None, max_pages = 4)['errors'] == [{'cursor': 'cursor_2', 'reason': "fetched_page error : next cursor doesn't exist"}]
    assert ingest_paginated_api(mock_fetch_page_bad_1,start_cursor = 'cursor_3', max_pages = 4)['errors'] == [{'cursor': 'cursor_4', 'reason': 'fetched_page error : items field is missing'}]
    # ## track the cursor case
    assert (ingest_paginated_api(mock_fetch_page_bad_1,start_cursor = 'cursor_3', max_pages = 4))['summary']['last_cursor'] == 'cursor_3'



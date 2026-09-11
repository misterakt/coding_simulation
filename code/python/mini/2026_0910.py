from collections.abc import Callable
from typing import Any

def load_pages(
    fetch_page: Callable[[str], dict[str, Any]],
    start_cursor: str = "start",
    max_attempts: int = 3,
) -> tuple[list[dict[str, Any]], str | None]:
    records: list[dict[str,Any]] = []
    cursor: str | None = start_cursor 

    remaining_attempts = max_attempts
    while cursor is not None:
        try:
            page = fetch_page(cursor)
        except TimeoutError:
            if remaining_attempts > 0:
                remaining_attempts -= 1

            if remaining_attempts == 0:
                return records, cursor 
            continue
        else:
            remaining_attempts = max_attempts
                
        records.extend(page["records"])
        cursor = page["next_cursor"]

    return records, None

def test_fetch_page(cursor: str) -> dict:
    pages = {
        "start": {"records": [{"id": "A"}], "next_cursor": "page-2"},
        "page-2": {"records": [{"id": "B"}], "next_cursor": None},
    }
    return pages[cursor]

def test_fetch_multiple_pages(cursor: str) -> dict:
    pages = {
        "start": {"records": [{"id": "A"}], "next_cursor": "page-2"},
        "page-2": {"records": [{"id": "B"}], "next_cursor": "page-3"},
        "page-3": {"records": [{"id": "C"}], "next_cursor": "page-4"},
        "page-4": {"records": [{"id": "D"}], "next_cursor": None},
    }
    return pages[cursor]

def test_recovers_after_one_timeout():
    call_count = 0 

    def fetch_page(cursor: str) -> dict:
        nonlocal call_count
        call_count += 1 

        if call_count == 1:
            raise TimeoutError("temp error")
        
        return {
            "records": [{"id": "A"}],
            "next_cursor": None
        }

    records, resume_cursor = load_pages(
        fetch_page,
        max_attempts=2
    )

    assert records == [{"id":"A"}]
    assert resume_cursor is None
    assert call_count == 2

def test_returns_cursor_after_exhausted_retries():
    call_count = 0

    def fetch_page(cursor: str) -> dict:
        nonlocal call_count
        call_count += 1 
        raise TimeoutError("temp failure")

    assert load_pages(fetch_page, max_attempts=3) == ([], "start")
    assert call_count == 3
 

if __name__ == "__main__":

    # test for successful pagenation
    assert load_pages(test_fetch_page) == ([{'id': 'A'}, {'id': 'B'}], None)

    # test for successful pagenation 
    assert load_pages(test_fetch_multiple_pages) == ([{'id': 'A'}, {'id': 'B'}, {'id': 'C'}, {'id': 'D'}], None)

    test_recovers_after_one_timeout()
    test_returns_cursor_after_exhausted_retries()





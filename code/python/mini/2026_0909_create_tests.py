from typing import Any
from copy import deepcopy

def select_loadable_files(
    manifest: list[dict[str, Any]],
    arrivals: list[dict[str, Any]],
) -> list[str]:
    manifest_sizes = {
        record["file_name"]: record["size_bytes"]
        for record in manifest
    }

    return [
        record["file_name"]
        for record in arrivals
        if (
            record["file_name"] in manifest_sizes
            and record["size_bytes"]
            == manifest_sizes[record["file_name"]]
        )
    ]


def test_invalid_cases(
    manifest: list[dict[str, Any]],
    arrivals: list[dict[str, Any]],
) -> None:
    
    # mutation test for inputs 
    copied_manifest = deepcopy(manifest)
    copied_arrivals = deepcopy(arrivals)

    try:
        select_loadable_files(copied_manifest,copied_arrivals)
    except ValueError as e:
        assert str(e) == "duplicate file_name"
    else:
        raise AssertionError("Error not intended")

    assert copied_manifest == manifest
    assert copied_arrivals == arrivals



if __name__ == "__main__":

    manifest = []
    arrivals = []
    # empty case
    assert select_loadable_files(manifest,arrivals) == []

    invalid_test_cases = [
        (   # duplicated file names - defect part 
            [
                {"file_name": "a.csv", "size_bytes": 200},
                {"file_name": "a.csv", "size_bytes": 200},
            ],
            [
                {"file_name": "a.csv", "size_bytes": 100},
            ],
            # ["a.csv"]
        ),
        (   # duplicated file names - defect part 
            [
                {"file_name": "a.csv", "size_bytes": 200},
                {"file_name": "b.csv", "size_bytes": 200},
            ],
            [
                {"file_name": "c.csv", "size_bytes": 100},
                {"file_name": "c.csv", "size_bytes": 100},
            ],
            # ["a.csv"]
        ),
    ]

    # invalid test
    for manifest, arrivals in invalid_test_cases:
        test_invalid_cases(manifest, arrivals) 



    test_cases = [
        (   # one more matching case
            [
                {"file_name": "a.csv", "size_bytes": 100},
                {"file_name": "b.csv", "size_bytes": 200},
            ],
            [
                {"file_name": "a.csv", "size_bytes": 100},
            ],
            ["a.csv"]
        ),
        (   ## mismatch case
            [
                {"file_name": "a.csv", "size_bytes": 100},
                {"file_name": "b.csv", "size_bytes": 200},
            ],
            [
                {"file_name": "a.csv", "size_bytes": 200},
                {"file_name": "c.csv", "size_bytes": 100},
            ],
            []
        ),
        (   ## defect the order of manifest - case 1 
            [
                {"file_name": "c.csv", "size_bytes": 100},
                {"file_name": "a.csv", "size_bytes": 200},
            ],
            [
                {"file_name": "a.csv", "size_bytes": 200},
                {"file_name": "c.csv", "size_bytes": 100},
            ],
            ["c.csv", "a.csv"]
        ),
        (   ## defect the order of manifest - case 2 
            [
                {"file_name": "c.csv", "size_bytes": 100},
                {"file_name": "a.csv", "size_bytes": 200},
            ],
            [
                {"file_name": "a.csv", "size_bytes": 200},
                {"file_name": "b.csv", "size_bytes": 100},
                {"file_name": "c.csv", "size_bytes": 100},
                {"file_name": "d.csv", "size_bytes": 100},
            ],
            ["c.csv", "a.csv"]
        )
    ]


    # test cases 
    for manifest, arrivals, output in test_cases:
        assert select_loadable_files(manifest, arrivals) == output

    manifest_mutation_test = [
        {"file_name": "a.csv", "size_bytes": 100},
        {"file_name": "b.csv", "size_bytes": 200},
    ]

    arrivals_mutatin_test = [
        {"file_name": "a.csv", "size_bytes": 100},
    ]

    copied_manifest = deepcopy(manifest_mutation_test)
    copied_arrivals = deepcopy(arrivals_mutatin_test)

    select_loadable_files(copied_manifest, copied_arrivals)

    assert copied_manifest == manifest_mutation_test
    assert copied_arrivals == arrivals_mutatin_test
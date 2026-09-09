from typing import Any
from collections import defaultdict
from copy import deepcopy

"""
1.  output
    - "only_in_source": ["inv-3"]
    - "only_in_target": ["inv-4"]
    - "changed": ["inv-2"]

2. logic
    - compare records by "invoice id"  (Assume every records have the 3 required fields)
    - classify the diff on amount or status
    - perserve order for all outputs 
    - if duplicated invoice id -> raise ValueError("duplicate invoice_id")
    - always return all three lists with empty inputs 


"""

def reconcile_invoices(
    source: list[dict[str, Any]],
    target: list[dict[str, Any]],
) -> dict[str, list[str]]:

    # 1. check the params 
    #   1) invalid the source / target 
    if source is None and target is None:
        return {
            "only_in_source": [],
            "only_in_target": [],
            "changed": [],
        }

    # check the duplicated invoice_ids  (source)
    source_dict = {}
    target_dict = {}
    # overlap_keys = []

    for src in source:
        src_invoice_id = src.get("invoice_id")
        if src_invoice_id in source_dict:
            raise ValueError("duplicate invoice_id")
        else:
            source_dict[src_invoice_id] = src

    # check the duplicated invoice_ids  (target)
    for tar in target:
        tar_invoice_id = tar.get("invoice_id")
        if tar_invoice_id in target_dict:
            raise ValueError("duplicate invoice_id")
        else:
            target_dict[tar_invoice_id] = tar
        # # overlapp check
        # if tar_invoice_id in source_dict:
        #     overlap_keys.append(tar_invoice_id)



    only_in_source = [key for key in source_dict if key not in target_dict]
    only_in_target = [key for key in target_dict if key not in source_dict]
    diff_keys = [key for key in source_dict if key in target_dict if source_dict[key]['amount'] != target_dict[key]['amount'] or source_dict[key]['status'] != target_dict[key]['status'] ]


    # set operation but doesn't gurantee the order 
    # # reconcile the data
    # overlap_keys = (source_dict.keys() & target_dict.keys())

    # # only left 
    # only_left = list(source_dict.keys() - overlap_keys)
    # # only right
    # only_right = list(target_dict.keys() - overlap_keys)

    # # diff keys - sets
    # diff_keys = set()
    # # compare the overlap parts 
    # for key in overlap_keys:
    #     if source_dict[key] != target_dict[key]:
    #         diff_keys.add(key)



    return {
        "only_in_source": only_in_source,
        "only_in_target": only_in_target,
        "changed": list(diff_keys),
    }


def test_invalid(source, target):
    copied_source = deepcopy(source)
    copied_target = deepcopy(target)


    try:
        reconcile_invoices(source,target)
    except ValueError as e:
        assert str(e) == "duplicate invoice_id"
    else:
        raise AssertionError("Normal error case patterns")       

    assert copied_source == source
    assert copied_target == target


if __name__ == "__main__":


    invalid_data_list = [
        
        (
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-2", "amount": 50, "status": "paid"},
                {"invoice_id": "inv-2", "amount": 0, "status": "open"},
            ],
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-1", "amount": 55, "status": "paid"},
                {"invoice_id": "inv-4", "amount": 20, "status": "open"},
            ]
        ),
        (
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-2", "amount": 50, "status": "paid"},
                {"invoice_id": "inv-3", "amount": 0, "status": "open"},
            ],
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-1", "amount": 55, "status": "paid"},
                {"invoice_id": "inv-4", "amount": 20, "status": "open"},
            ]
        ),
    ]


    for source, target in invalid_data_list:
        test_invalid(source, target)

    
    valid_data_list = [
        
        (
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-2", "amount": 50, "status": "paid"},
                {"invoice_id": "inv-3", "amount": 0, "status": "open"},
            ],
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-3", "amount": 55, "status": "paid"},
                {"invoice_id": "inv-4", "amount": 20, "status": "open"},
            ],
                {"only_in_source": ["inv-2"], "only_in_target": ["inv-4"], "changed": ["inv-3"]},
        ),
        (
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-2", "amount": 50, "status": "paid"},
                {"invoice_id": "inv-4", "amount": 0, "status": "open"},
            ],
            [
                {"invoice_id": "inv-4", "amount": 90, "status": "open"},
                {"invoice_id": "inv-5", "amount": 55, "status": "paid"},
                {"invoice_id": "inv-6", "amount": 20, "status": "open"},
            ],
                {"only_in_source": ["inv-1","inv-2"], "only_in_target": ["inv-5","inv-6"], "changed": ["inv-4"]},  
        ),
        (
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-2", "amount": 50, "status": "paid"},
                {"invoice_id": "inv-4", "amount": 0, "status": "open"},
            ],
            [
                {"invoice_id": "inv-1", "amount": 90, "status": "open"},
                {"invoice_id": "inv-2", "amount": 55, "status": "paid"},
                {"invoice_id": "inv-4", "amount": 20, "status": "open"},
            ],
            
                {"only_in_source": [], "only_in_target": [], "changed": ["inv-1","inv-2","inv-4"]},
        ),
        (
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-2", "amount": 50, "status": "paid", "factor": 30},
            ],
            [
                {"invoice_id": "inv-1", "amount": 100, "status": "open"},
                {"invoice_id": "inv-2", "amount": 50, "status": "paid"},
            ],
            
                {"only_in_source": [], "only_in_target": [], "changed": []},
        ),
    ]

    for source, target, result in valid_data_list:
        # print(reconcile_invoices(source, target))
        # print(f"result : {result}")
        assert reconcile_invoices(source, target) == result
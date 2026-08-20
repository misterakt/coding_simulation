from typing import Any



def reconcile_order_lines(
    source_records: list[dict[str, Any]],
    target_records: list[dict[str, Any]],
) -> dict[str, Any]:
    '''
    * flow
      - use pandas to join and create a new sets 
      - join keys = order_id / line_id
         * compare customer_id / amount / currency / updated_at
        

    '''

    missing_in_target = list()
    missing_in_source = list()
    mismatched_records = list()
    duplicate_keys_source = list() 
    duplicate_keys_target = list() 
    source_count = 0
    target_count = 0
    missing_in_target_cnt = 0
    missing_in_source_cnt = 0
    mismatched_cnt = 0
    matched_cnt = 0
    duplicate_keys_source_cnt = 0
    duplicate_keys_target_cnt = 0

    ## source duplication check
    dedup_src_list = list()
    dedup_src_keys = set()
    # duplicated_src_keys = set()
    for record in source_records:
        source_count += 1
        # only sum up the duplicated count for source (not adding rows)
        key = (record.get('order_id'), record.get('line_id'))
        if key in dedup_src_keys:
            duplicate_keys_source_cnt += 1
            # duplicated_src_keys.add(key)
            duplicate_keys_source.append(record)
        else:
            dedup_src_keys.add(key)
            dedup_src_list.append(record)

    # # create duplicates source key sets
    # for record in source_records:
    #     if (record.get('order_id'), record.get('line_id')) in duplicated_src_keys:
    #         duplicate_keys_source.append(record)

    ## target duplication check
    dedup_trg_list = list()
    dedup_trg_keys = set()
    # duplicated_trg_keys = set()
    for record in target_records:
        target_count += 1
        # only sum up the duplicated count for source (not adding rows)
        key = (record.get('order_id'), record.get('line_id'))
        if key in dedup_trg_keys:
            duplicate_keys_target_cnt += 1
            # duplicated_trg_keys.add(key)
            duplicate_keys_target.append(record)
        else:
            dedup_trg_keys.add(key)
            dedup_trg_list.append(record)

    # # create duplicates target key sets
    # for record in target_records:
    #     if (record.get('order_id'), record.get('line_id')) in duplicated_trg_keys:
    #         duplicate_keys_target.append(record)

    # compare the keys between source and target

    only_source_exist_keys = dedup_src_keys - dedup_trg_keys
    for record in source_records:
        if (record.get('order_id'), record.get('line_id')) in only_source_exist_keys:
            missing_in_target.append(record)
            missing_in_target_cnt += 1

    only_target_exist_keys = dedup_trg_keys - dedup_src_keys
    for record in target_records:
        if (record.get('order_id'), record.get('line_id')) in only_target_exist_keys:
            missing_in_source.append(record)
            missing_in_source_cnt += 1


    src_dict = {
        (record.get("order_id"), record.get("line_id")) : record
        for record in dedup_src_list
    }

    trg_dict = {
        (record.get("order_id"), record.get("line_id")) : record
        for record in dedup_trg_list
    }

    # get the intersect by set comparision 
    common_keys = src_dict.keys() & trg_dict.keys()
    
    for key in common_keys:

        src_rec = src_dict[key]
        trg_rec = trg_dict[key]

        differences = {}

        for field in ["customer_id","amount","currency","updated_at"]:
            if src_rec.get(field) != trg_rec.get(field):
                differences[field] = {"source": src_rec.get(field), "target": trg_rec.get(field)} 

        if differences != {}:
            mismatched_records.append(
                {
                    "key": (src_rec.get('order_id'), src_rec.get('line_id')),
                    "source": src_rec,
                    "target": trg_rec,
                    "differences": differences
                }
            ) 
            mismatched_cnt += 1
        else:
            matched_cnt += 1


    return {
        "matched_count": matched_cnt,
        "missing_in_target": missing_in_target,
        "missing_in_source": missing_in_source,
        "mismatched_records": mismatched_records,
        "duplicate_keys": {
            "source": duplicate_keys_source,
            "target": duplicate_keys_target
    },
        "summary": {
            "source_count": source_count,
            "target_count": target_count,
            "matched": matched_cnt,
            "missing_in_target": missing_in_target_cnt,
            "missing_in_source": missing_in_source_cnt,
            "mismatched": mismatched_cnt,
            "duplicate_keys_source": duplicate_keys_source_cnt,
            "duplicate_keys_target": duplicate_keys_target_cnt
        }
    }





if __name__ == "__main__":



    source_sample= [
    {
    "order_id": "ord_1001",
    "line_id": "1",
    "customer_id": "cust_123",
    "amount": 42.50,
    "currency": "EUR",
    "updated_at": "2026-08-19T10:15:00Z"
    },
    {
    "order_id": "ord_1002",
    "line_id": "2",
    "customer_id": "cust_124",
    "amount": 50.50,
    "currency": "EUR",
    "updated_at": "2026-08-19T10:15:00Z"
    },
    {
    "order_id": "ord_1002",
    "line_id": "2",
    "customer_id": "cust_124",
    "amount": 50.50,
    "currency": "USD",
    "updated_at": "2026-08-19T10:15:00Z"
    }

    ]

    target_sample= [
    {
    "order_id": "ord_1001",
    "line_id": "1",
    "customer_id": "cust_123",
    "amount": 42.50,
    "currency": "EUR",
    "updated_at": "2026-08-19T10:15:00Z"
    },
    {
    "order_id": "ord_1001",
    "line_id": "1",
    "customer_id": "cust_123",
    "amount": 42.50,
    "currency": "EUR",
    "updated_at": "2026-08-19T10:15:00Z"
    },
    {
    "order_id": "ord_1002",
    "line_id": "2",
    "customer_id": "cust_125",
    "amount": 40.50,
    "currency": "EUR",
    "updated_at": "2026-08-19T10:15:00Z"
    },
    {
    "order_id": "ord_1003",
    "line_id": "3",
    "customer_id": "cust_125",
    "amount": 41.50,
    "currency": "EUR",
    "updated_at": "2026-08-19T10:15:00Z"
    },
    {
    "order_id": "ord_1004",
    "line_id": "4",
    "customer_id": "cust_126",
    "amount": 41.10,
    "currency": "EUR",
    "updated_at": "2026-08-20T10:15:00Z"
    }
    ]

    # no data case
    assert reconcile_order_lines([],[]) == {
        "matched_count": 0,
        "missing_in_target": [],
        "missing_in_source": [],
        "mismatched_records": [],
        "duplicate_keys": {
            "source": [],
            "target": []
    },
        "summary": {
            "source_count": 0,
            "target_count": 0,
            "matched": 0,
            "missing_in_target": 0,
            "missing_in_source": 0,
            "mismatched": 0,
            "duplicate_keys_source": 0,
            "duplicate_keys_target": 0
        }
    }

    # # same data case
    # 
    assert reconcile_order_lines([source_sample[0]],[target_sample[0]]) == {
        "matched_count": 1,
        "missing_in_target": [],
        "missing_in_source": [],
        "mismatched_records": [],
        "duplicate_keys": {
            "source": [],
            "target": []
    },
        "summary": {
            "source_count": 1,
            "target_count": 1,
            "matched": 1,
            "missing_in_target": 0,
            "missing_in_source": 0,
            "mismatched": 0,
            "duplicate_keys_source": 0,
            "duplicate_keys_target": 0
        }
    }
    
    print(reconcile_order_lines(source_sample,target_sample))

    # matching but customer_id is different and amount is different (summary)
    assert reconcile_order_lines([source_sample[1]],[target_sample[2]])["summary"] == \
        {
            "source_count": 1,
            "target_count": 1,
            "matched": 0,
            "missing_in_target": 0,
            "missing_in_source": 0,
            "mismatched": 1,
            "duplicate_keys_source": 0,
            "duplicate_keys_target": 0
        }

    # check missing parts of sources 
    assert reconcile_order_lines(source_sample,target_sample)["missing_in_source"] == \
                [
                    {
                    "order_id": "ord_1003",
                    "line_id": "3",
                    "customer_id": "cust_125",
                    "amount": 41.5,
                    "currency": "EUR",
                    "updated_at": "2026-08-19T10:15:00Z"
                    },
                    {
                    "order_id": "ord_1004",
                    "line_id": "4",
                    "customer_id": "cust_126",
                    "amount": 41.1,
                    "currency": "EUR",
                    "updated_at": "2026-08-20T10:15:00Z"
                    }
                ]
    # check summary - for N * M comparision          
    assert reconcile_order_lines(source_sample,target_sample)["summary"] == \
                {
                    "source_count": 3,
                    "target_count": 5,
                    "matched": 1,
                    "missing_in_target": 0,
                    "missing_in_source": 2,
                    "mismatched": 1,
                    "duplicate_keys_source": 1,
                    "duplicate_keys_target": 1
                }
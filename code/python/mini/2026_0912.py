

"""
 flow   
    1. create an empty dict to represent the output
    2. compare the attributes one by one based on the proposed 
    3. check 
        1) field existence 
             -> field_removed:<name>
        2) type check (type_changed:<name>) / nullable check (true -> false) (nullability_tightened:<name>)
        3) adding a non-nullable field produces "required_field_added:<name>"
           - Adding nullable fields and relaxing nullability are allowed.
    4. return 
"""



def check_schema_change(
    current: dict[str, dict[str, str | bool]],
    proposed: dict[str, dict[str, str | bool]],
) -> list[str]:

    output = list()

    for ckey in current.keys():
        # check type & nullable
        if ckey not in proposed:
            output.append(f"field_removed:{ckey}")
        else:
            if proposed[ckey]["type"] != current[ckey]["type"]:
                output.append(f"type_changed:{ckey}")
            if proposed[ckey]["nullable"] != current[ckey]["nullable"]: 
                if proposed[ckey]["nullable"] == False and current[ckey]["nullable"] == True:
                    output.append(f"nullability_tightened:{ckey}")
                else:
                    continue
  
    for pkey in proposed.keys():
        # add a required field
        if pkey not in current and proposed[pkey]["nullable"] == False:
            output.append(f"required_field_added:{pkey}")

    return output

if __name__ == "__main__":


    test_cases = [
        (  ##  normal case
             {
                "event_id": {"type": "string", "nullable": False},
                "amount": {"type": "int", "nullable": True},
            },
            {
                "event_id": {"type": "string", "nullable": False},
                "amount": {"type": "float", "nullable": False},
                "region": {"type": "string", "nullable": True},
                "sector": {"type": "string", "nullable": True},
            },
            [
                "type_changed:amount",
                "nullability_tightened:amount",
            ]
        ),
        (  ##  normal case (with empty input-current)
            {
            },
            {
                "event_id": {"type": "string", "nullable": False},
            },
            [
                "required_field_added:event_id",
            ]
        ),
        (  ##  normal case (removed)
             {
                "event_id": {"type": "string", "nullable": False},
                "amount": {"type": "float", "nullable": False},
            },
            {
                "amount": {"type": "float", "nullable": False},
            },
            [
                "field_removed:event_id",
            ]
        ),
        (
            {
                "amount": {"type": "int", "nullable": True},
                "retired": {"type": "string", "nullable": True},
            },
            {
                "region": {"type": "string", "nullable": False},
                "amount": {"type": "float", "nullable": False},
            },
            [
                "type_changed:amount",
                "nullability_tightened:amount",
                "field_removed:retired",
                "required_field_added:region",
            ],
        )

    ]

    for current, proposed, output in test_cases:
        assert check_schema_change(current, proposed) == output



    # assert check_schema_change(current, proposed) == [
    #     "type_changed:amount",
    #     "nullability_tightened:amount",
    # ]


from collections.abc import Iterable, Iterator

def reconcile_file_streams(
    source: Iterable[dict[str, str]],
    target: Iterable[dict[str, str]]
) -> Iterator[dict[str,str]]:

    end = object()

    iter_src = iter(source)
    iter_trg = iter(target)
    src_record = next(iter_src, end) 
    trg_record = next(iter_trg, end)


    def advance_iter(iter_src,iter_trg):
        return next(iter_src, end) ,  next(iter_trg, end)

    while True:

        if src_record is end and trg_record is end:
            break
        elif src_record is not end and trg_record is not end:
            if src_record["file_id"] == trg_record["file_id"]:
                if src_record["checksum"] == trg_record["checksum"]:
                    src_record,trg_record = advance_iter(iter_src,iter_trg)
                    continue
                else:
                    yield {"file_id": src_record["file_id"], "status": "checksum_mismatch"}
                    src_record,trg_record = advance_iter(iter_src,iter_trg)
                    continue

        if src_record is end and trg_record is not end:
            yield {"file_id": trg_record["file_id"], "status": "missing_in_source"}
            trg_record = next(iter_trg, end)

        elif trg_record is end and src_record is not end:
            yield {"file_id": src_record["file_id"], "status": "missing_in_target"}
            src_record = next(iter_src, end)

        elif (src_record["file_id"] < trg_record["file_id"]):
            yield {"file_id": src_record["file_id"], "status": "missing_in_target"}
            src_record = next(iter_src, end) 

        elif (src_record["file_id"] > trg_record["file_id"]):
            yield {"file_id": trg_record["file_id"], "status": "missing_in_source"}
            trg_record = next(iter_trg, end) 




if __name__ == "__main__":

    source = iter([
        {"file_id": "a", "checksum": "111"},
        {"file_id": "b", "checksum": "222"},
        {"file_id": "d", "checksum": "444"},
    ])

    target = iter([
        {"file_id": "a", "checksum": "111"},
        {"file_id": "c", "checksum": "333"},
        {"file_id": "d", "checksum": "999"},
    ])


    source_case2 = iter([
        {"file_id": "a", "checksum": "111"},
        {"file_id": "b", "checksum": "222"},
        {"file_id": "d", "checksum": "444"},
    ])

    target_case2 = iter([
        {"file_id": "a", "checksum": "111"},
        {"file_id": "d", "checksum": "999"},
    ])

    source_case3 = iter([
        {"file_id": "a", "checksum": "111"},
    ])

    target_case3 = iter([
        {"file_id": "a", "checksum": "112"},
        {"file_id": "b", "checksum": "999"},
        {"file_id": "c", "checksum": "999"},
        {"file_id": "d", "checksum": "999"},
    ])

    source_case4 = iter([])

    target_case4 = iter([
        {"file_id": "a", "checksum": "112"},
        {"file_id": "b", "checksum": "999"},
        {"file_id": "c", "checksum": "999"},
        {"file_id": "d", "checksum": "999"},
    ])


    # print(list(reconcile_file_streams(source_case3, target_case3)))

    # print(list(reconcile_file_streams(source, target)))

    # print(list(reconcile_file_streams(source_case4, target_case4)))

    assert list(reconcile_file_streams(source, target)) == [
        {"file_id": "b", "status": "missing_in_target"},
        {"file_id": "c", "status": "missing_in_source"},
        {"file_id": "d", "status": "checksum_mismatch"},
    ]

    assert list(reconcile_file_streams(iter([]), iter([]))) == []

    assert list(reconcile_file_streams(source_case2, target_case2)) == [{'file_id': 'b', 'status': 'missing_in_target'}, {'file_id': 'd', 'status': 'checksum_mismatch'}]
  
    assert list(reconcile_file_streams(source_case4, target_case4)) == [{'file_id': 'a', 'status': 'missing_in_source'}, {'file_id': 'b', 'status': 'missing_in_source'}, {'file_id': 'c', 'status': 'missing_in_source'}, {'file_id': 'd', 'status': 'missing_in_source'}]

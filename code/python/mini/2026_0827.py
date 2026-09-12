def validate_payment(record: dict[str, object]) -> list[str]:
    
    result = []

    def check_payment_id(payment_id):
        if payment_id is None:
            return "NON_EXIST_PAYMENT_ID"
        if not isinstance(payment_id,str):
            return "WRONGE_DATA_TYPE_PAYMENT_ID"
        if (payment_id is not None and (isinstance(payment_id,str) and payment_id.strip() == "")):
            return "EMPTY_STRING"

        return True

    def check_amount(amount):
        if amount is None:
            return "AMOUNT_DOESNT_EXIST"
        if not isinstance(amount,(int,float)):
            return "INVALID_AMOUNT_TYPE"
        if isinstance(amount,bool):
            return "AMOUNT_TYPE_IS_BOOLEAN"
        if amount < 0:
            return "NEGATIVE_VALUE"
        return True

    def check_currency(currency):
        if currency is None:
            return "CURRENCY_DOESNT_EXIST"
        if currency not in ("EUR","GBP","USD"):
            return "NOT_CURRENCY_TYPES"
        return True

    payment_id = record.get("payment_id")
    amount = record.get("amount")
    currency = record.get("currency")

    for rs in [ 
        check_payment_id(payment_id),
        check_amount(amount),
        check_currency(currency)
    ]:
        if rs is not True:
           result.append(rs)


    return result


if __name__ == "__main__":

    
    assert validate_payment({
        "payment_id": "pay-101",
        "amount": 25.50,
        "currency": "EUR",
    }) == []

    assert validate_payment({
        "payment_id": "pay-101",
        "amount": "25.50",
        "currency": "EUR",
    }) == ['INVALID_AMOUNT_TYPE']

    assert validate_payment({
        "payment_id": "pay-101",
        "amount": "25.50",
        "currency": "eur",
    }) == ['INVALID_AMOUNT_TYPE', 'NOT_CURRENCY_TYPES']

    assert validate_payment({
        "payment_id": "",
        "amount": 25.50,
        "currency": "EUR",
    }) == ['EMPTY_STRING']

    assert validate_payment({
        "payment_id": "   ",
        "amount": 25.50,
        "currency": "EUR",
    }) == ["EMPTY_STRING"]
    
    assert validate_payment({
        "payment_id": 500,
        "amount": 25.50,
        "currency": "EUR",
    }) == ["WRONGE_DATA_TYPE_PAYMENT_ID"]

    assert validate_payment({
        "payment_id": "500",
        "amount": True,
        "currency": "EUR",
    }) == ["AMOUNT_TYPE_IS_BOOLEAN"]
    
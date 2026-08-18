from typing import Any
from datetime import datetime
# from collections import Counter
import re

def validate_customer_records(records: list[dict[str, Any]]) -> dict[str, Any]:

    

    required_fields = ['customer_id', 'email', 'status', 'signup_date']
    valid_records = list() 
    invalid_records = list()
    total = 0
    valid = 0 
    invalid = 0
    DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def validate_dateformat(value: Any):
        

        if value is None or not isinstance(value,str) or len(value) != 10:
            return 'date_format_mismatch - non string or length problem' 
        
        if not DATE_RE.fullmatch(value):
            return 'date_format_mismatch - non match format'

        try:
            datetime.strptime(value,"%Y-%m-%d")
            return None
        except Exception:
            return 'date_format_mismatch - date format unfit'

    def validate_age(value: Any):
        if isinstance(value,int) and not isinstance(value,bool) and value >= 0: 
            return None
        return 'age type mismatch'

    def validate_country(value: Any):
        if isinstance(value, str) and len(value) == 2 and value.isupper():
            return None
        return 'invalid_country'

    def required_valid_column(value: Any, col_name: str):


        if col_name == 'customer_id':
            if value is None or not isinstance(value,str) or (isinstance(value,str) and value.strip() == ''):
                return "customer id doesn't have the proper value or doesn't exist"
        
        if col_name == 'email':
            if value is not None and isinstance(value,str) and value.count("@") == 1:
                return None
            return 'email_format is wrong'
        
        if col_name == 'status':
            if value is None or value not in ('active','inactive','suspended'):
                return f'status is wrong'

        if col_name == 'signup_date':
            return validate_dateformat(value)

        
        return None


    ## main flow



    for record in records:

        # print(f"record = {record}")

        error_logs = []

        valid_flag = True 
        # check if whether is any missing keys based on required_fields 
        for must_field in required_fields:
            if must_field not in record: # key existience check
                error_logs.append(f"key columns({must_field}) doesn't exist")
                valid_flag = False
                continue
            else:   # at least they have all keys 
                valid_column_log = required_valid_column(record.get(must_field),must_field)
                if valid_column_log is not None:
                    valid_flag = False
                    error_logs.append(valid_column_log)

        if 'age' in record:
            age_log = validate_age(record.get('age'))
            if age_log is not None:
                valid_flag = False
                error_logs.append(age_log)
        
        if 'country' in record:
            country_log = validate_country(record.get('country'))
            if country_log is not None:
                valid_flag = False
                error_logs.append(country_log)

        if valid_flag is False:
            # create invalid sets
            invalid += 1
            invalid_record_with_error = {
                "record" : record,
                "errors"  : error_logs
            }
            # print(f"invalid_record_with_error = {invalid_record_with_error}")
            invalid_records.append(invalid_record_with_error)

        else:
            # create valid sets
            valid_records.append(record)
            valid += 1
            
        total += 1
         
    return {
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "summary": {
            "total": total,
            "valid": valid,
            "invalid": invalid
        }
}




if __name__ == "__main__":


    sample_data = [{
        "customer_id": "cust_001",
        "email": "alice@example.com",
        "status": "active",
        "signup_date": "2026-08-14",
        "age": 34,
        "country": "DE"
    },  # normal case
    {
        "customer_id": "cust_001",
        "email": "alice@example.com",
        "status": "active",
        "signup_date": "2026-08-14",
        "age": -34,
        "country": "DE"
    },  # wrong age case
    {
        "customer_id": "cust_001",
        "email": "alice@example.com",
        "status": "active",
        "signup_date": "2026-08-14",
        "age": -1,
        "country": "DE"
    },  # wrong age case-2
    {
        "customer_id": "cust_002",
        "email": "aliceexample.com",
        "status": "active",
        "signup_date": "2026-08-14",
        "age": 34,
        "country": "DE"
    },  # wrong email case - 1
    {
        "customer_id": "cust_002",
        "email": "alice@example.com",
        "status": "active",
        "signup_date": "2026-08-14",
        "age": 34,
        "country": "de"
    },  # wrong country case - 1
    {
        "customer_id": "cust_002",
        "email": "alice@example.com",
        "status": "active",
        "signup_date": "2026-08-14",
        "age": 34,
        "country": "des"
    },  # wrong country case - 2
    {
        "customer_id": "cust_002",
        "email": "alice@example.com",
        "status": "lunch",
        "signup_date": "2026-08-14",
        "age": 34,
        "country": "DE"
    },  # wrong status case - 1
    {
        "customer_id": "cust_002",
        "email": "alice@example.com",
        "status": "active",
        "signup_date": "00081-08-14",
        "age": 34,
        "country": "DE"
    }  # wrong date case - 1
    ]

    print(validate_customer_records([sample_data[0]]))

    # normal case
    assert validate_customer_records([sample_data[0]]) == {
        'valid_records': [{'customer_id': 'cust_001', 'email': 'alice@example.com', 'status': 'active', 'signup_date': '2026-08-14', 'age': 34, 'country': 'DE'}], 
        'invalid_records': [], 
        'summary': {'total': 1, 'valid': 1, 'invalid': 0}
    }

    # wrong age case
    assert validate_customer_records([sample_data[1]]) == {
        'valid_records': [], 
        'invalid_records': [ 
            {
            'record' : {'customer_id': 'cust_001', 'email': 'alice@example.com', 'status': 'active', 'signup_date': '2026-08-14', 'age': -34, 'country': 'DE'}, 
            'errors': ['age type mismatch']}
        ], 
        'summary': {'total': 1, 'valid': 0, 'invalid': 1}
    }

    # wrong age case-2
    assert validate_customer_records([sample_data[2]]) == {
        'valid_records': [], 
        'invalid_records': [ 
            {
            'record' : {'customer_id': 'cust_001', 'email': 'alice@example.com', 'status': 'active', 'signup_date': '2026-08-14', 'age': -1, 'country': 'DE'} , 
             'errors' : ['age type mismatch']}
        ], 
        'summary': {'total': 1, 'valid': 0, 'invalid': 1}
    }

    # wrong email case
    assert validate_customer_records([sample_data[3]]) == {
        'valid_records': [], 
        'invalid_records': [ 
            {
            'record' : {'customer_id': 'cust_002', 'email': 'aliceexample.com', 'status': 'active', 'signup_date': '2026-08-14', 'age': 34, 'country': 'DE'} , 
             'errors' : ['email_format is wrong']
            }
        ], 
        'summary': {'total': 1, 'valid': 0, 'invalid': 1}
    }
    # invalid country case
    assert validate_customer_records([sample_data[4]]) == {
        'valid_records': [], 
        'invalid_records': [ 
            {
            'record' : {'customer_id': 'cust_002', 'email': 'alice@example.com', 'status': 'active', 'signup_date': '2026-08-14', 'age': 34, 'country': 'de'} , 
             'errors' : ['invalid_country']
            }
        ], 
        'summary': {'total': 1, 'valid': 0, 'invalid': 1}
    }

    # invalid country case-2
    assert validate_customer_records([sample_data[5]]) == {
        'valid_records': [], 
        'invalid_records': [ 
            {
            'record' : {'customer_id': 'cust_002', 'email': 'alice@example.com', 'status': 'active', 'signup_date': '2026-08-14', 'age': 34, 'country': 'des'} , 
             'errors' : ['invalid_country']
            }
        ], 
        'summary': {'total': 1, 'valid': 0, 'invalid': 1}
    }

    # invalid status case
    assert validate_customer_records([sample_data[6]]) == {
        'valid_records': [], 
        'invalid_records': [ 
            {
            'record' : {'customer_id': 'cust_002', 'email': 'alice@example.com', 'status': 'lunch', 'signup_date': '2026-08-14', 'age': 34, 'country': 'DE'} , 
            'errors' : ['status is wrong']
            }
        ], 
        'summary': {'total': 1, 'valid': 0, 'invalid': 1}
    }, f"invalid_status"

    # invalid signup_date case
    assert validate_customer_records([sample_data[7]]) == {
        'valid_records': [], 
        'invalid_records': [ 
            {
            'record' : {'customer_id': 'cust_002', 'email': 'alice@example.com', 'status': 'active', 'signup_date': '00081-08-14', 'age': 34, 'country': 'DE'} , 
            'errors' : ['date_format_mismatch - non string or length problem']
            }
        ], 
        'summary': {'total': 1, 'valid': 0, 'invalid': 1}
    }


# print(validate_customer_records(sample_data))


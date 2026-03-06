from pydantic import ValidationError
from .validate_call import calculate


def test_validate_call():
    try:
        calculate(2.8)
        calculate("slovo")
    except ValidationError as e:
        print(e)
    finally:
        print("The function is working")

test_validate_call()
from pydantic import validate_call


@validate_call
def calculate(number: float):
    return number + 2  
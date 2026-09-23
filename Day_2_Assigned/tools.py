
SERVICES = {
    "GENERAL": {
        "name": "General Consultation",
        "fee": 500
    },
    "CARDIO": {
        "name": "Cardiology Consultation",
        "fee": 800
    },
    "DERMA": {
        "name": "Dermatology Consultation",
        "fee": 700
    },
    "LAB001": {
        "name": "Blood Test",
        "fee": 300
    }
}


def get_service_fee(service_code):
    """
    Return the fee of a hospital service.
    """

    service = SERVICES.get(service_code.upper())

    if service is None:
        return f"Service {service_code} was not found."

    return service["fee"]


def get_service_details(service_code):
    """
    Return complete information about a hospital service.
    """

    service = SERVICES.get(service_code.upper())

    if service is None:
        return f"Service {service_code} was not found."

    return service


def calculator(expression):
    """
    Simple calculator tool used by the ReAct agent.
    """

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )
        return result

    except Exception as error:
        return f"Calculation error: {error}"
import random


def generate_business_id(prefix: str):
    number = random.randint(1000, 9999)
    return f"{prefix}-{number}"

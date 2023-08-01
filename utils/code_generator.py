import random
import string


def generator():
    return "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=7))

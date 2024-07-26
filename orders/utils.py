import random
from datetime import datetime

def generate_orderid():
    random_number = random.randint(100000,999999)
    unique_code = "order_" + str(datetime.now().day) + str(datetime.now().month) + str(random_number)

    return unique_code
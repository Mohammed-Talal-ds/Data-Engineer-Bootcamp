import json
import random
import time
import os
from faker import Faker
from datetime import datetime

fake = Faker()

output_folder = "../raw_data/orders"

os.makedirs(output_folder, exist_ok=True)

order_count = 1

while True:

    order = {
        "order_id": f"ORD{order_count}",
        "customer_id": random.randint(1, 5),
        "product_id": random.randint(1, 5),

        # Intentionally messy values
        "quantity": random.choice([1, 2, 3, None]),
        "price": random.choice(["20$", "100$", "invalid", 50]),

        "payment_method": random.choice([
            "Cash",
            "Credit Card",
            "PayPal"
        ]),

        "status": random.choice([
            "Completed",
            "Pending",
            "Canceled"
        ]),

        "email": random.choice([
            fake.email(),
            "",
            None
        ]),

        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Duplicate records intentionally
    if random.random() < 0.2:
        order["order_id"] = "ORD_DUPLICATE"

    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_folder}/transaction_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(order, f, indent=4)

    print(f"Generated: {filename}")

    order_count += 1

    time.sleep(3)
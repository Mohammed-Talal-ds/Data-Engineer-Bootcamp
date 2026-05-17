import csv
import random
import time
import uuid
import os
from datetime import datetime
from faker import Faker

fake = Faker()

OUTPUT_DIR = r"M:\M\Data Science\nifi-real-time-project\project\raw_data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

call_types = ["VOICE", "SMS", "DATA"]

def random_timestamp():
    formats = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
    ]
    return random.choice(formats)

def generate_record():
    return {
        "call_id": random.randint(100000, 999999),
        "customer_id": f"CUST{random.randint(1000,9999)}",
        "tower_id": f"TWR{random.randint(1,99)}",
        "duration": random.randint(1, 5000),
        "cost": round(random.uniform(0.1, 100.0), 2),
        "call_type": random.choice(call_types),
        "timestamp": random_timestamp()
    }

def inject_errors(record):
    error_type = random.choice([
        "none",
        "missing",
        "duplicate",
        "negative",
        "corrupted"
    ])

    if error_type == "missing":
        record["customer_id"] = ""

    elif error_type == "negative":
        record["cost"] = -50

    elif error_type == "corrupted":
        return "BAD_ROW_@@@@"

    return record

while True:

    file_name = f"telecom_{int(time.time())}.csv"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    records = []

    for _ in range(random.randint(100, 300)):
        record = generate_record()
        record = inject_errors(record)
        records.append(record)

    with open(file_path, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "call_id",
            "customer_id",
            "tower_id",
            "duration",
            "cost",
            "call_type",
            "timestamp"
        ])

        for row in records:

            if isinstance(row, str):
                file.write(row + "\n")
            else:
                writer.writerow(row.values())

    print(f"Generated: {file_name}")

    time.sleep(3)
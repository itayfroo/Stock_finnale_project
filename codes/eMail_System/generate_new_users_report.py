import json
import os
import csv
from datetime import datetime, timedelta

USERS_PATH = r"texts/users.json"
OUTPUT_DIR = "reports"
OUTPUT_FILE = "new_users_weekly.csv"
DAYS_BACK = 7


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        return None


def generate_new_users_report():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(USERS_PATH, encoding="utf-8") as f:
        users = json.load(f)

    cutoff = datetime.now() - timedelta(days=DAYS_BACK)
    rows = []

    for key, info in users.items():
        if not key.endswith("_info"):
            continue

        signup_date = parse_date(info.get("date", ""))
        if not signup_date or signup_date < cutoff:
            continue

        username = key.replace("_info", "")

        rows.append([
            username,
            info.get("Age", ""),
            info.get("City", ""),
            info.get("Stock_investment", ""),
            info.get("Amount_invested", ""),
            signup_date.strftime("%Y-%m-%d %H:%M:%S")
        ])

    path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([
            ["Username", "Age", "City", "Stock Investment", "Amount Invested", "Signup Date"],
            *rows
        ])

    print(f"✅ New users report created: {path}")
    return path


if __name__ == "__main__":
    generate_new_users_report()

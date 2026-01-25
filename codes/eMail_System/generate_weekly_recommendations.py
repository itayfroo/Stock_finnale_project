import json
import os
import csv
from datetime import datetime, timedelta

# 🔹 project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# 🔹 input
RECOMMENDATIONS_PATH = os.path.join(BASE_DIR, "texts", "recommendations.json")

# 🔹 output → codes/eMail_System/reports
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "reports")
OUTPUT_FILE = "weekly_recommendations.csv"

DAYS_BACK = 7


def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        return None


def generate_weekly_recommendations_report():
    if not os.path.exists(RECOMMENDATIONS_PATH):
        raise FileNotFoundError(f"File not found: {RECOMMENDATIONS_PATH}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(RECOMMENDATIONS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    cutoff = datetime.now() - timedelta(days=DAYS_BACK)
    rows = []

    for key, value in data.items():
        if len(value) < 2:
            continue

        stock = value[0]
        comment = value[1].strip()
        if not comment:
            continue

        rating = value[2] if len(value) >= 3 else ""
        date_str = value[3] if len(value) >= 4 else None
        if not date_str:
            continue

        dt = parse_datetime(date_str)
        if not dt or dt < cutoff:
            continue

        username = key.split("_")[0]

        rows.append([
            username,
            stock,
            comment,
            rating,
            dt.strftime("%Y-%m-%d %H:%M:%S")
        ])

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([
            ["User", "Stock", "Comment", "Rating", "Date"],
            *rows
        ])

    print(f"✅ Weekly recommendations report created: {output_path}")
    print(f"📊 Recommendations in last {DAYS_BACK} days: {len(rows)}")

    return output_path


if __name__ == "__main__":
    generate_weekly_recommendations_report()

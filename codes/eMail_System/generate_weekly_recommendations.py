import json
import os
from datetime import datetime, timedelta
import csv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RECOMMENDATIONS_PATH = os.path.join(BASE_DIR, "texts", "recommendations.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_DIR = "reports"
OUTPUT_FILE = "weekly_recommendations.csv"

DAYS_BACK = 7

def parse_datetime(dt_str):
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        return None

def generate_weekly_recommendations_report():
    if not os.path.exists(RECOMMENDATIONS_PATH):
        raise FileNotFoundError("recommendations.json not found")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(RECOMMENDATIONS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    now = datetime.now()
    cutoff = now - timedelta(days=DAYS_BACK)

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
        if not dt:
            continue

        if dt < cutoff:
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

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Stock", "Comment", "Rating", "Date"])
        writer.writerows(rows)

    print(f"✅ Weekly recommendations report created: {output_path}")
    print(f"📊 Total recommendations in last {DAYS_BACK} days: {len(rows)}")

    return output_path

if __name__ == "__main__":
    generate_weekly_recommendations_report()

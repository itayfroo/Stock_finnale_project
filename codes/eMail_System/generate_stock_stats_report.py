import os
import csv
import json
from codes.handleReport import Reports

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RECOMMENDATIONS_PATH = os.path.join(BASE_DIR, "texts", "recommendations.json")
STOCKS_PATH = os.path.join(BASE_DIR, "texts", "stocks.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "codes", "eMail_System", "reports")
OUTPUT_FILE = "stock_recommendation_stats.csv"


def generate_weekly_recommendations():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(RECOMMENDATIONS_PATH, encoding="utf-8") as f:
        recommendations = json.load(f)

    with open(STOCKS_PATH, encoding="utf-8") as f:
        stocks_map = json.load(f)

    symbol_to_name = {v: k for k, v in stocks_map.items()}

    symbols = {
        v[0]
        for v in recommendations.values()
        if len(v) > 1 and v[1].strip()
    }

    rows = []
    for symbol in sorted(symbols):
        rec = Reports(symbol, base_dir=BASE_DIR)

        if rec.counter == 0:
            continue

        stock_name = symbol_to_name.get(symbol, symbol)

        rows.append([
            stock_name,
            symbol,
            rec.counter,
            rec.avg_numeric,
            rec.average_text
        ])

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Stock Name",
            "Symbol",
            "Recommendations",
            "Average (Numeric)",
            "Average (Stars)"
        ])
        writer.writerows(rows)

    print("Saved:", output_path)


if __name__ == "__main__":
    generate_weekly_recommendations()

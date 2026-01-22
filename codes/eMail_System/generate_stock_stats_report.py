from codes.handleRecom import Recommendations
import os, csv, json

# 🔹 project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

RECOMMENDATIONS_PATH = os.path.join(BASE_DIR, "texts", "recommendations.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_FILE = "stock_recommendation_stats.csv"


class BackendRecommendations(Recommendations):
    def __init__(self, stock):
        self.stock_name = stock
        self.sum = 0
        self.counter = 0
        self.avg_numeric = None
        self.average_text = None
        self.load_recom()

    def printAverage(self):
        if self.counter == 0:
            return

        stars = ['⭐☆☆☆☆', '⭐⭐☆☆☆', '⭐⭐⭐☆☆', '⭐⭐⭐⭐☆', '⭐⭐⭐⭐⭐']
        avg = self.sum / self.counter
        self.avg_numeric = round(avg, 2)
        self.average_text = stars[max(0, min(4, int(avg) - 1))]

    @staticmethod
    def MarkDownCode(*_, **__):
        pass


def generate_stock_stats_report():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(RECOMMENDATIONS_PATH, encoding="utf-8") as f:
        stocks = {v[0] for v in json.load(f).values() if len(v) > 1 and v[1].strip()}

    rows = []
    for stock in sorted(stocks):
        rec = BackendRecommendations(stock)
        if rec.counter:
            rows.append([
                stock,
                rec.counter,
                rec.avg_numeric,
                rec.average_text
            ])

    path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([
            ["Stock", "Number of Recommendations", "Average Rating", "Stars"],
            *rows
        ])

    print(f"✅ Stock statistics report created: {path}")
    return path


if __name__ == "__main__":
    generate_stock_stats_report()

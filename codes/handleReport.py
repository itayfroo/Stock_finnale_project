import os
import json


class Reports:
    def __init__(self, stock: str, base_dir: str = None):
        self.stock_name = (stock or "").upper()
        self.sum = 0
        self.counter = 0
        self.avg_numeric = None
        self.average_text = None

        if base_dir is None:
            self.base_dir = os.getcwd()
        else:
            self.base_dir = base_dir

        self.stocks_path = os.path.join(self.base_dir, "texts", "stocks.json")
        self.recommendations_path = os.path.join(self.base_dir, "texts", "recommendations.json")

        self.load_recom()
        self.printAverage()

    def on_recommendation(self, name, comment, rate, date):
        pass

    def on_no_recommendations(self):
        pass

    def on_count(self, count):
        pass

    def on_average(self, stars_text):
        pass

    def on_warning(self, e):
        pass

    def printAverage(self):
        stars = ['⭐☆☆☆☆', '⭐⭐☆☆☆', '⭐⭐⭐☆☆', '⭐⭐⭐⭐☆', '⭐⭐⭐⭐⭐']
        try:
            avg = self.sum / self.counter
            self.avg_numeric = round(avg, 2)
            average_int = int(avg)
            if 1 <= average_int <= 5:
                self.average_text = stars[average_int - 1]
                self.on_average(self.average_text)
        except Exception:
            pass

    def average(self, rate):
        stars = ['⭐☆☆☆☆', '⭐⭐☆☆☆', '⭐⭐⭐☆☆', '⭐⭐⭐⭐☆', '⭐⭐⭐⭐⭐']
        if rate == stars[0]:
            self.sum += 1
        if rate == stars[1]:
            self.sum += 2
        if rate == stars[2]:
            self.sum += 3
        if rate == stars[3]:
            self.sum += 4
        if rate == stars[4]:
            self.sum += 5

    def load_recom(self):
        try:
            counter = 0

            with open(self.stocks_path, "r", encoding="utf-8") as f:
                stocks_data = json.load(f)

            if self.stock_name in stocks_data:
                stock_symbol = stocks_data[self.stock_name]
            else:
                stock_symbol = self.stock_name

            with open(self.recommendations_path, "r", encoding="utf-8") as f:
                recom_data = json.load(f)

                for key, value in recom_data.items():
                    if value[0] == stock_symbol and value[1].strip():
                        counter += 1

                        name = key.split('_', 1)[0]
                        comment = value[1]

                        try:
                            rating = value[2]
                        except Exception:
                            rating = '⭐⭐⭐⭐☆'

                        self.average(rating)

                        words = comment.split()
                        try:
                            date = value[3][:10]
                        except Exception:
                            date = 'Two years ago'

                        wrapped = '\n'.join(
                            [' '.join(words[i:i + 8]) for i in range(0, len(words), 8)]
                        )

                        self.on_recommendation(name, wrapped, rating, date)
                        self.counter += 1

                if counter == 0:
                    self.on_no_recommendations()
                else:
                    self.on_count(counter)

        except Exception as e:
            self.on_warning(e)

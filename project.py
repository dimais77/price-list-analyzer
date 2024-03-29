import csv
import os
import re

from tabulate import tabulate


def display_results(results):
    headers = ['№', 'Наименование', 'цена', 'вес', 'цена за кг.', 'файл']
    numbered_results = [[i + 1] + result[1:] + [result[0]] for i, result in enumerate(results)]
    print(tabulate(numbered_results, headers=headers, tablefmt='grid'))


def export_to_html(results, filename):
    headers = ['№', 'Наименование', 'цена', 'вес', 'цена за кг.', 'файл']
    numbered_results = [[i + 1] + result[1:] + [result[0]] for i, result in enumerate(results)]
    table = tabulate(numbered_results, headers=headers, tablefmt='html')
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(table)


class PriceMachine:
    def __init__(self):
        self.data = []
        self.name_length = 0

    def load_prices(self, directory):
        self.data = []
        for filename in os.listdir(directory):
            if filename.endswith('.csv') and 'price' in filename.lower():
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        product_name = None
                        price = None
                        weight = None
                        for column_name in row:
                            if re.search(r'(название|продукт|товар|наименование)', column_name, re.IGNORECASE):
                                product_name = row[column_name].strip()
                            elif re.search(r'(цена|розница)', column_name, re.IGNORECASE):
                                price = float(row[column_name].replace(',', '.').strip())
                            elif re.search(r'(фасовка|масса|вес)', column_name, re.IGNORECASE):
                                weight = float(row[column_name].replace(',', '.').strip())

                        if product_name and price is not None and weight is not None:
                            self.data.append([filename, product_name, price, weight, round(price / weight, 2)])

    def search_items(self, query):
        results = []
        for row in self.data:
            if re.search(query, row[1], re.IGNORECASE):
                results.append(row)
        return sorted(results, key=lambda x: x[2] / x[3])

    def find_text(self, query):
        results = self.search_items(query)
        display_results(results)
        html_filename = 'search_results.html'
        export_to_html(results, html_filename)
        print(f"Результаты поиска сохранены в файле: {html_filename}")

    def main(self, directory):
        self.load_prices(directory)

        while True:
            query = input("Введите текст для поиска (или 'exit' для завершения): ")
            if query.lower() == 'exit' or query.lower() == 'учше':
                print("Работа завершена.")
                break
            self.find_text(query)


if __name__ == "__main__":
    pm = PriceMachine()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    pm.main(current_directory)

import requests


class ExchangeRatesService:
    def __init__(self):
        self.api_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.currencies = ["USD", "EUR", "JPY", "GBP", "CNY", "THB"]
        self.rates = []

    def get_data(self) -> list:
        response = requests.get(self.api_url)
        currencies = response.json()["Valute"]

        for currency in self.currencies:
            self.rates.append(currencies[currency]["Nominal"])
            self.rates.append(currencies[currency]["CharCode"])
            self.rates.append(currencies[currency]["Value"])

        return self.rates

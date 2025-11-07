import requests


class YandexWeatherService:
    conditions = {
        "clear": "ясно",
        "partly-cloudy": "малооблачно",
        "cloudy": "облачно с прояснениями",
        "overcast": "пасмурно",
        "light-rain": "небольшой дождь",
        "rain": "дождь",
        "heavy-rain": "сильный дождь",
        "showers": "ливень",
        "wet-snow": "дождь со снегом",
        "light-snow": "небольшой снег",
        "snow": "снег",
        "snow-showers": "снегопад",
        "hail": "град",
        "thunderstorm": "гроза",
        "thunderstorm-with-rain": "дождь с грозой",
        "thunderstorm-with-hail": "гроза с градом",
    }

    phenom_conditions = {
        "fog": "туман",
        "mist": "дымка",
        "smoke": "смог",
        "dust": "пыль",
        "dust-suspension": "пылевая взвесь",
        "duststorm": "пыльная буря",
        "thunderstorm-with-duststorm": "пыльная буря с грозой",
        "drifting-snow": "слабая метель",
        "blowing-snow": "метель",
        "ice-pellets": "ледяная крупа",
        "freezing-rain": "ледяной дождь",
        "tornado": "торнадо",
        "volcanic-ash": "вулканический пепел",
    }

    cloudness = {
        0: "ясно",
        0.25: "малооблачно",
        0.5: "облачно с прояснениями",
        0.75: "облачно с прояснениями",
        1: "пасмурно",
    }

    def __init__(self):
        self.api_key = '***REMOVED***'
        self.api_url = 'https://api.weather.yandex.ru/v2/forecast?lat=48.480223&lon=135.071917'
        self.forecasts = None

    def get_data(self) -> str:
        self.get_today_forecasts()
        return self.get_forecast_text()

    def get_today_forecasts(self):
        headers = {
            'X-Yandex-Weather-Key': self.api_key
        }
        response = requests.get(self.api_url, headers=headers)
        self.forecasts = response.json()["forecasts"][0]["parts"]

    def get_forecast_text(self) -> list:
        morning_forecast = self.forecasts["morning"]
        day_forecast = self.forecasts["day"]
        evening_forecast = self.forecasts["evening"]

        forecast_args = [
            morning_forecast['temp_avg'], morning_forecast["feels_like"],
            self.conditions[morning_forecast["condition"]],
            day_forecast['temp_avg'], day_forecast["feels_like"],
            self.conditions[day_forecast["condition"]],
            evening_forecast['temp_avg'], evening_forecast["feels_like"],
            self.conditions[evening_forecast["condition"]]]
        return forecast_args
        # total_text = ("Утро:\n{}°C, ощущается как {}°C, {}\n\n"
        #               "День:\n{}°C, ощущается как {}°C, {}\n\n"
        #               "Вечер:\n{}°C, ощущается как {}°C, {}").format(*forecast_args)
        # return total_text

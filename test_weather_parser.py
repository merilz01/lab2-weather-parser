import json
import unittest
from pathlib import Path

from weather_parser import WeatherParser


class TestWeatherParser(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = WeatherParser()

    def test_find_temperature_positive(self) -> None:
        text = "Сегодня в Москве +15.5°C, легкий ветер."
        result = self.parser.parse_text(text)
        self.assertEqual(result.temperature, 15.5)

    def test_find_temperature_negative(self) -> None:
        text = "На улице -10 °C."
        result = self.parser.parse_text(text)
        self.assertEqual(result.temperature, -10.0)

    def test_find_temperature_no_data(self) -> None:
        text = "Просто текст без погоды."
        result = self.parser.parse_text(text)
        self.assertIsNone(result.temperature)

    def test_find_wind_speed(self) -> None:
        text = "Ветер 5.5 м/с, порывы до 10."
        result = self.parser.parse_text(text)
        self.assertEqual(result.wind_speed, 5.5)

    def test_find_humidity(self) -> None:
        text = "Влажность воздуха: 85%."
        result = self.parser.parse_text(text)
        self.assertEqual(result.humidity, 85)

    def test_parse_text_full(self) -> None:
        text = "Температура: +20°C, ветер 3 м/с, влажность 60%, давление 745 мм рт. ст."
        result = self.parser.parse_text(text)
        
        self.assertEqual(result.temperature, 20.0)
        self.assertEqual(result.wind_speed, 3.0)
        self.assertEqual(result.humidity, 60)
        self.assertEqual(result.pressure, 745)

    def test_save_to_json(self) -> None:
        data = self.parser.parse_text("+20°C, ветер 3 м/с")
        test_file = "test_output.json"
        
        self.parser.save_to_json(data, test_file)
        
        # Проверяем, что файл создался и в нем правильные данные
        self.assertTrue(Path(test_file).exists())
        
        with open(test_file, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data["temperature"], 20.0)
        self.assertEqual(saved_data["wind_speed"], 3.0)
        
        # Удаляем тестовый файл после проверки
        Path(test_file).unlink()


if __name__ == "__main__":
    unittest.main()
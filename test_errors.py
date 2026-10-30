import unittest
from weather_parser import WeatherParser


class TestWeatherParserErrors(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = WeatherParser()

    def test_parse_temperature_empty_string(self) -> None:
        """Тест: пустая строка не вызывает ошибок."""
        result = self.parser.parse_text("")
        self.assertIsNone(result.temperature)

    def test_parse_temperature_wrong_format(self) -> None:
        """Тест: если вместо температуры просто текст."""
        result = self.parser.parse_text("Сегодня отличная погода!")
        self.assertIsNone(result.temperature)

    def test_parse_file_not_found(self) -> None:
        """Тест: ошибка FileNotFoundError при чтении несуществующего файла."""
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_file("no_such_file.txt")

    def test_parse_url_invalid(self) -> None:
        """Тест: ошибка ConnectionError при неверном URL."""
        with self.assertRaises(ConnectionError):
            self.parser.parse_url("https://this-domain-does-not-exist-12345.com")

    def test_parse_wind_speed_no_data(self) -> None:
        """Тест: если в тексте нет данных о ветре."""
        result = self.parser.parse_text("Тихо и спокойно.")
        self.assertIsNone(result.wind_speed)

    def test_parse_humidity_no_data(self) -> None:
        """Тест: если в тексте нет данных о влажности."""
        result = self.parser.parse_text("Просто текст.")
        self.assertIsNone(result.humidity)


if __name__ == "__main__":
    unittest.main()
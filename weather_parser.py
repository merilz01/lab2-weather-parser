import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import requests


@dataclass
class WeatherData:
    temperature: Optional[float] = None
    wind_speed: Optional[float] = None
    humidity: Optional[int] = None
    pressure: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)


class WeatherParser:

    # Температура (например: +15.5°C, -10 C)
    TEMP_PATTERN = re.compile(r"(-?\d+(?:\.\d+)?)\s*°?C", re.IGNORECASE)
    
    # Ветер (3 м/с, 10 км/ч, 5 m/s)
    WIND_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(?:м/с|км/ч|m/s|km/h)", re.IGNORECASE)
    
    # Влажность (60%, 45 %)
    HUMIDITY_PATTERN = re.compile(r"(\d+)\s*%", re.IGNORECASE)

    # Давление (745 мм рт. ст., 1013 гПа)
    PRESSURE_PATTERN = re.compile(r"(\d+)\s*(?:мм\s*рт\.?\s*ст\.?|гПа|hPa)", re.IGNORECASE)

    def _find_value(self, pattern: re.Pattern, text: str, cast_to: type) -> Optional:
        match = pattern.search(text)
        if match:
            return cast_to(match.group(1))
        return None

    def parse_text(self, text: str) -> WeatherData:
        return WeatherData(
            temperature=self._find_value(self.TEMP_PATTERN, text, float),
            wind_speed=self._find_value(self.WIND_PATTERN, text, float),
            humidity=self._find_value(self.HUMIDITY_PATTERN, text, int),
            pressure=self._find_value(self.PRESSURE_PATTERN, text, int),
        )

    def parse_file(self, file_path: str) -> WeatherData:
        try:
            path = Path(file_path)
            content = path.read_text(encoding="utf-8")
            return self.parse_text(content)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не найден")
        except Exception as e:
            raise ValueError(f"Ошибка при чтении файла: {e}")

    def parse_url(self, url: str) -> WeatherData:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return self.parse_text(response.text)
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка при загрузке URL: {e}")

    def save_to_json(self, data: WeatherData, file_path: str) -> None:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data.to_dict(), f, ensure_ascii=False, indent=4)
        except OSError as e:
            raise IOError(f"Не удалось сохранить JSON: {e}")
from weather_parser import WeatherParser


def main() -> None:
    parser = WeatherParser()
    
    print("=" * 50)
    print("ПАРСЕР ПОГОДЫ (Вариант 22)")
    print("=" * 50)
    
    while True:
        print("\nВыберите режим работы:")
        print("1. Поиск в тексте")
        print("2. Поиск в файле")
        print("3. Поиск по URL")
        print("4. Сохранить последний результат в JSON")
        print("0. Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "1":
            text = input("Введите текст с данными о погоде: ")
            last_result = parser.parse_text(text)
            print(f"\nРезультат: {last_result}")
            
        elif choice == "2":
            path = input("Введите путь к файлу: ").strip()
            try:
                last_result = parser.parse_file(path)
                print(f"\nРезультат: {last_result}")
            except FileNotFoundError as e:
                print(f"\nОшибка: {e}")
            except Exception as e:
                print(f"\nОшибка чтения: {e}")
                
        elif choice == "3":
            url = input("Введите URL страницы: ").strip()
            try:
                last_result = parser.parse_url(url)
                print(f"\nРезультат: {last_result}")
            except ConnectionError as e:
                print(f"\nОшибка сети: {e}")
            except Exception as e:
                print(f"\nОшибка: {e}")
        
        elif choice == "4":
            if 'last_result' in locals() and last_result:
                try:
                    parser.save_to_json(last_result, "weather_result.json")
                    print("\nДанные сохранены в weather_result.json")
                except Exception as e:
                    print(f"\nОшибка сохранения: {e}")
            else:
                print("\nСначала получите данные о погоде (пункты 1-3).")
                
        elif choice == "0":
            print("Выход из программы. До встречи!")
            break
        else:
            print("\nНеверный ввод. Пожалуйста, выберите 1, 2, 3, 4 или 0.")


if __name__ == "__main__":
    main()
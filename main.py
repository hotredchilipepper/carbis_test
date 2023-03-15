from traceback import print_exc
import time
import requests
import json
import crud


def get_options(query):
    # Получаем настройки из БД
    settings = crud.select_settings()
    url = settings["base_url"]
    api_key = settings["api_key"]
    language = settings["language"]
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Token " + api_key,
    }
    data = {
        "query": query,
        "count": 10,
        "language": language
    }
    result = requests.post(url, data=json.dumps(data), headers=headers)

    return result


def bad_command() -> None:
    # Функция заглушка для ответа на не существующий запрос
    print("Запрашиваемого действия не существует!")
    time.sleep(2)


def get_address():
    """ Непосредственно функция для получения координат,
    по запросу пользователя.
    
    """

    print("Чтобы получить точные координаты введите адрес и нажмите Enter\n")
    inp = input(">>> ")
    
    crit_error="""
============================================
Возникли критические ошибки найстройки ПО!!!
Установлены настройки по умолчанию, 
пожалуйста установите повторно ваш API-ключ.
============================================
"""
    try:
        result = get_options(inp)
    except Exception:
        print(crit_error)
        crud.reset_settings()
        time.sleep(3)
        return 'error'

    if result.status_code == 404:
        print("Возникла ошибка базового URL, изменяю на настройки по умолчанию.")
        url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
        crud.update_settings("base_url", url)
        time.sleep(2)
        return 'error'
    elif result.status_code == 403:
        print("Некорректный API-ключ, попробуйте в меню настроек ввести его заново.")
        time.sleep(2)
        return 'error'
    elif result.status_code == 400:
        print("Некорректно указан язык для ответа от сервиса DaData, изменяю на базовый русский(ru).")
        crud.update_settings("language", "ru")
        time.sleep(2)
        return 'error'
    
    try:
        counter = 1
        array_addresses = "\nВыбирите более подходящее из списка:\n"
        dict_addresses = {}
        for dat in result.json()["suggestions"]:
            array_addresses += f"[{counter}] {dat['value']}\n"
            dict_addresses[str(counter)] = dat
            counter += 1

    except:
        print("Ошибка запроса, проверьте себя и попробуйте снова")
    
    
    while True:
        print(array_addresses)
        choice = input(">>> ")
        try:
            print("Ваш выбор: [%s] %s"%(choice, dict_addresses[choice]["value"]))
            #data_coordinates = dadata.suggest(name="address", query=dict_addresses[choice], count=1)
            lat = dict_addresses[choice]["data"]["geo_lat"]
            lon = dict_addresses[choice]["data"]["geo_lon"]
            result = f"\nТочные координаты:\nШирота: {lat}\nДолгота: {lon}"
            print(result)

            break
        except Exception:
            print("Ваш выбор не корректный, попробуйте снова")
            time.sleep(2)
    
    time.sleep(2)
    return 1

def settings():
    """ Функция для добавления/изменения настроек,
    Для корректной работы необходимо перед началом 
    работы с ПО задать API-key.
    
    """
    menu_settings = """
============================================
Чтобы полноценно пользоваться данным ПО,
вам нужно обязательно ввести свой API ключ
без которого данное ПО не будет корректно 
работать, остальные настройки изменять можно 
по желанию(главное быть внимательными)
============================================
[1] Базовый URL сервиса DaData
[2] API ключ для сервиса DaData
[3] Язык ответа от сервиса DaData
[0] Вернуться в главное меню
"""
    
    while True:
        print(menu_settings)
        echo = input(">>> ")
        if echo == "0":
            break
        try:
            if echo == "1":
                print("Введите полный URL-адрес\n(сейчас установлен адресс по умолчанию, меняете на свой страх и риск):\n")
                echo = input(">>> ")
                if 0 < len(echo) <= 256:
                    crud.update_settings("base_url", echo)
                    print("\nБазовый URL успешно изменен.")
                else:
                    print("Неудалось изменить базовый URL, попробуйте снова..")
                time.sleep(2)

            elif echo == "2":
                print("Введите свой API-ключ от сервиса DaData\n(без ключа невозможна корректная работа ПО):\n")
                echo = input(">>> ")
                if 0 < len(echo) <= 64:
                    crud.update_settings("api_key", echo)
                    print("\nAPI-ключ добавлен.")
                else:
                    print("Неудалось добавить API-ключ, попробуйте снова..")
                time.sleep(2)

            elif echo == "3":
                print("Введите код языка(en/ru) на котором хотели бы получать ответ от сервиса DaData\n(по умолчанию стоит русский(ru)):\n")
                echo = input(">>> ")
                if 0 < len(echo) <= 4:
                    crud.update_settings("language", echo)
                    print("\nЯзык ответа изменен.")
                else:
                    print("Неудалось изменить язык ответа, попробуйте снова..")
                time.sleep(2)
            else:
                bad_command()

        except Exception:

            print("Ошибка действия %s"%(echo))
            print_exc()
            time.sleep(3)
            input("Нажмиет Enter для продолжения...")
            continue


def menu():
    """ Функция реализующая главное меню
    текущей программы.
    
    """
    menu_str = """
============================================
Главное меню:
============================================
[1] Получить координаты 
[2] Настроить ПО
[0] Завершить работу
    
    Введите номер команды:
"""
    warning = """
######################################
# Перед началом работы настройте ПО! #
######################################"""
    print(warning)

    while True:
        print(menu_str)
        
        echo = input(">>> ")

        if echo == "0":
            break
            
        try:
            if echo == "1":
                # Вызов функции получения координат.
                get_address()

            elif echo == "2":
                # Вызов функции изменения настроек.
                settings()

            else:
                # Вызвана не коррекатная команда.
                bad_command()
        
        except Exception:

            print("Ошибка действия %s"%(echo))
            print_exc()
            time.sleep(3)
            input("Нажмиет Enter для продолжения...")
            continue
    
    print("Отлично поработали! До скорой встречи!")


if __name__ == "__main__":
    check_settings = crud.select_settings()
    if check_settings is None:
        crud.insert_settings()
    menu()
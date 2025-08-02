import requests
import bs4
import tabulate

# Если бы не ограничения по библам в ТЗ я бы поместил эти данные в .env 
auth_url = "http://185.244.219.162/phpmyadmin/index.php"
auth_login = "test"
auth_password = "JHFBdsyf2eg8*"

db_url = "http://185.244.219.162/phpmyadmin/index.php?route=/sql&db=testDB&table=users&pos=0"
params = {
    "route": "/sql",
    "server": 1,
    "db": "testDB",
    "table": "users",
    "pos": 0
}

def is_target_td(tag):
    if tag.name != "td":
        return False

    cls = tag.get("class", [])
    data_type = tag.get("data-type")

    return (
        "grid_edit" in cls and
        data_type in {"blob", "int"}  # искомые типы
    )



# Функция для регистрации в pma
def auth():
    with requests.Session() as session:
        # Вытаскиваем страницу логина
        auth_response = session.get(auth_url)
        soup = bs4.BeautifulSoup(auth_response.text, "html.parser")

        # Извлекаем token из скрытого поля формы
        token = soup.find("input", {"name": "token"}).get("value")

        # Формируем данные для POST-запроса
        login_data = {
            "pma_username": auth_login,
            "pma_password": auth_password,
            "server": "1",
            "route": "/",
            "token": token,
            "set_session": soup.find("input", {"name": "set_session"}).get("value"),
        }

        # POST-запрос для авторизации
        post_response = session.post(auth_url, data=login_data)

        if "phpMyAdmin" in post_response.text:
            print("Авторизация успешна!")
            # Тут можно дальше делать запросы к phpMyAdmin через session
        else:
            print("Ошибка авторизации")
        
        # Вытаскиваем страницу с БД
        db_response = session.get(db_url, params=params)
        
        html = db_response.text
        soup = bs4.BeautifulSoup(html, "html.parser")

        # Вытаскиваем нужную таблицу
        tds = soup.find_all(is_target_td)
        pairs = []

        # Проходим по всем <td> по 2 штуки за раз
        for i in range(0, len(tds), 2):
            id_td = tds[i]
            name_td = tds[i + 1] if i + 1 < len(tds) else None

            if id_td and name_td:
                id_val = id_td.get_text(strip=True)
                name_val = name_td.get_text(strip=True)
                pairs.append((id_val, name_val))

        # Красиво выводим
        print(tabulate.tabulate(pairs, headers=["ID", "Имя"], tablefmt="github"))

        

        

if __name__ == "__main__":
    auth()
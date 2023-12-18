![Логотип](https://github.com/Conqerorior/razkhodka_bot/blob/main/razhodka.jpg?width=100?Razkhodka)
<div id="header" align="center">
  <h1>Razkhodka Bot</h1>
  <img src="https://img.shields.io/badge/Python-3.9-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/aiogram-2.14.3-F8F8FF?style=for-the-badge&logo=aiogram&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/MongoDB-4.6.1-F8F8FF?style=for-the-badge&logo=mongodb&logoColor=F5F5DC">
  <img src="https://img.shields.io/badge/httpx-0.25.0-F8F8FF?style=for-the-badge&logo=httpx&logoColor=F5F5DC">
</div>

## Описание

Этот телеграм-бот позволяет пользователям отслеживать статус своих заявлений на
официальном сайте Болгарии. Бот использует асинхронный парсер **HTTPX** для
обращения к сайту и извлечения информации о статусе заявления.

## Функции

* **Добавление нового пользователя:** Пользователь может добавить свои данные в
  базу данных, указав номер заявки и ПИН-код.
* **Удаление пользователя:** Пользователь может удалить свои данные из базы
  данных.
* **Проверка данных:** Бот проверяет, правильно ли пользователь ввел номер
  заявки и ПИН-код.
* **Проверка статуса заявления:** Бот проверяет статус заявления на официальном
  сайте Болгарии и отправляет пользователю уведомление.

## Технологии

* HTTPX для асинхронных запросов
* MongoDB и библиотека Motor для работы с базой данных
* Асинхронная библиотека aiogram для управления ботом


## Установка

Чтобы установить бот, выполните следующие действия:

* Клонируйте репозиторий.
```bash
   git clone <название репозитория>
```

* Установите и активируйте виртуальное окружение Для Windows:
```bash
   python -m venv venv
   source venv/Scripts/activate
```

* Для Mac OS и Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

* Установить зависимости из файла **requirements.txt**:

```bash
   pip install requirements.txt
```


* Создайте файл **.env** и введите в него следующие переменные:
    ```
    BOT_TOKEN=YOUR_BOT_TOKEN
    MONGO_URI=mongodb://localhost:27017/
   ``` 


* Запустите бот:
  * **python main.py**

## Чтобы использовать бота, выполните следующие действия:

* Откройте Telegram и найдите бота по имени [@razkhodka_bot](https://t.me/razkhodka_bot)
* Нажмите кнопку Старт `/start`.
* Введите номер заявки и ПИН-код.
* Бот будет отправлять вам уведомление с текущим статусом заявления каждые 3 дня.
* Нажмите кнопку Проверить статус `/check`.

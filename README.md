# Проект ELibrary - платформа для начинающих авторов

![Python test](https://github.com/Inteshil/ELibary-YandexProject/actions/workflows/python-package.yml/badge.svg)
![Django test](https://github.com/Inteshil/ELibary-YandexProject/actions/workflows/django.yml/badge.svg)

Буква R в названии репозитория пропущена не просто так! В этом есть огромный скрытый смысл, который нам, смертным, не понять.

## Инструкция по установке
- Загрузите проект
  ```
  git clone https://github.com/Inteshil/ELibary-YandexProject
  ```
- Перейдите в в папку проекта
  ```
  cd ELibary-YandexProject
  ```
- Создайте виртуальное окружение
  ```
  python -m venv venv
  ```
- Зайдите в него, **работает для Windows**
  ```
  venv\Scripts\activate
  ```
- Загрузите внешние зависимости
  ```
  pip install -r requirements.txt
  ```
- Примените миграции
  ```
  python site/manage.py migrate
  ```
- Запустите проект
  ```
  python site/manage.py runserver
  ```
## Настройка:
- Вы можете создать файл .env в папке config и определить переменные окружения. Пример такого файла - .env-example (в той же папке)
- Загрузить тестовые данные в базу можно прописав команду:
  ```
  python manage.py loaddata fixtures/default.json
  ```

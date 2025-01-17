# Movies

### Тестовое задание
Таблица с данными находится на ручке `/movies`.

Ручка для загрузки таблицы в БД `/from_csv`. CSV файл лежит в директории files.

---

## Установка

1. Клонируйте репозиторий.
   ```bash
   git clone https://github.com/Slava140/Movies.git
   ```

2. Измените файл `.env.example` и переименуйте в `.env`.

3. Поднимите docker-compose.
   ```bash
   docker-compose up -d --build
   ```

4. Выполните **после первого запуска**. При последующих **не нужно**, данные сохраняются в `pg_data`.
   - Подключитесь к контейнеру `postgres`.
     ```bash
     docker exec -it postgres psql -U postgres
     ```
   - Создайте базу данных с названием, которое указали в `DB_NAME` в `.env`.
     ```sql
     CREATE DATABASE name;
     ```
   - Выйдите из контейнера
     ```bash
     exit
     ```
5. Завершите работу контейнера и запустите его снова.
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```
   


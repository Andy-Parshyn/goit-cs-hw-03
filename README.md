# goit-cs-hw-03

Домашня робота: PostgreSQL (система управління завданнями) і MongoDB (CRUD через PyMongo).

## Підготовка

```bash
docker compose up -d
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Compose піднімає PostgreSQL 16 (`localhost:5432`, база `task_manager`, логін/пароль `postgres`) і MongoDB 7 (`localhost:27017`).

## Завдання 1. PostgreSQL

Файли в `task1/`:

- `create_tables.sql` - створення таблиць `users`, `status`, `tasks` і базових статусів
- `seed.py` - заповнення випадковими даними через Faker
- `queries.sql` - 14 запитів із завдання

Запуск:

```bash
docker exec -i hw03_postgres psql -U postgres -d task_manager < task1/create_tables.sql
python task1/seed.py
docker exec -i hw03_postgres psql -U postgres -d task_manager < task1/queries.sql
```

Структура:

- `users.email` і `status.name` унікальні
- `tasks.user_id` має `ON DELETE CASCADE`, тому при видаленні користувача зникають і його завдання
- `description` може бути `NULL`, seed лишає порожнім приблизно 20% завдань, щоб було що вибрати запитом на "без опису"

Перевірка каскаду:

```sql
DELETE FROM users WHERE id = 3;
SELECT COUNT(*) FROM tasks WHERE user_id = 3;  -- 0
```

## Завдання 2. MongoDB

Файли в `task2/`:

- `seed.py` - додає кілька котів у колекцію `cats_db.cats`
- `main.py` - консольне меню з операціями

Запуск:

```bash
python task2/seed.py
python task2/main.py
```

Операції в меню:

1. вивести всі записи
2. знайти кота за ім'ям
3. оновити вік за ім'ям
4. додати характеристику в `features` за ім'ям
5. видалити кота за ім'ям
6. видалити всі записи
7. додати нового кота

Усі звернення до бази обгорнуті в `try/except PyMongoError`, при старті скрипт робить `ping` і завершується, якщо MongoDB недоступна. Для додавання характеристики використано `$addToSet`, щоб не плодити дублікати в масиві.

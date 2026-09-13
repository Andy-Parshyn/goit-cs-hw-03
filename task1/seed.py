import random

import psycopg2
from faker import Faker

DSN = "dbname=task_manager user=postgres password=postgres host=localhost port=5432"

USERS_COUNT = 10
TASKS_COUNT = 30

fake = Faker()


def seed(conn):
    cur = conn.cursor()

    cur.execute("TRUNCATE tasks, users RESTART IDENTITY CASCADE")

    users = [(fake.name(), fake.unique.email()) for _ in range(USERS_COUNT)]
    cur.executemany("INSERT INTO users (fullname, email) VALUES (%s, %s)", users)

    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]

    tasks = [
        (
            fake.sentence(nb_words=4).rstrip("."),
            fake.text(max_nb_chars=200) if random.random() > 0.2 else None,
            random.choice(status_ids),
            random.choice(user_ids),
        )
        for _ in range(TASKS_COUNT)
    ]
    cur.executemany(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
        tasks,
    )

    conn.commit()
    cur.close()


if __name__ == "__main__":
    try:
        with psycopg2.connect(DSN) as conn:
            seed(conn)
        print(f"Seeded {USERS_COUNT} users and {TASKS_COUNT} tasks")
    except psycopg2.Error as e:
        print(f"Database error: {e}")

from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
db = client["cats_db"]
cats = db["cats"]


def create_cat(name: str, age: int, features: list[str]):
    try:
        result = cats.insert_one({"name": name, "age": age, "features": features})
        print(f"Додано кота з _id={result.inserted_id}")
    except PyMongoError as e:
        print(f"Помилка при додаванні: {e}")


def read_all():
    try:
        docs = list(cats.find())
        if not docs:
            print("Колекція порожня")
        for doc in docs:
            print(doc)
    except PyMongoError as e:
        print(f"Помилка при читанні: {e}")


def read_by_name(name: str):
    try:
        doc = cats.find_one({"name": name})
        print(doc if doc else f"Кота з ім'ям '{name}' не знайдено")
    except PyMongoError as e:
        print(f"Помилка при читанні: {e}")


def update_age(name: str, age: int):
    try:
        result = cats.update_one({"name": name}, {"$set": {"age": age}})
        if result.matched_count:
            print(f"Вік кота '{name}' оновлено на {age}")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено")
    except PyMongoError as e:
        print(f"Помилка при оновленні: {e}")


def add_feature(name: str, feature: str):
    # $addToSet щоб не дублювати однакові характеристики
    try:
        result = cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.matched_count:
            print(f"Коту '{name}' додано характеристику '{feature}'")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено")
    except PyMongoError as e:
        print(f"Помилка при оновленні: {e}")


def delete_by_name(name: str):
    try:
        result = cats.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кота '{name}' видалено")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено")
    except PyMongoError as e:
        print(f"Помилка при видаленні: {e}")


def delete_all():
    try:
        result = cats.delete_many({})
        print(f"Видалено записів: {result.deleted_count}")
    except PyMongoError as e:
        print(f"Помилка при видаленні: {e}")


def ask_int(prompt: str) -> int | None:
    value = input(prompt).strip()
    if not value.isdigit():
        print("Потрібно ввести ціле число")
        return None
    return int(value)


MENU = """
1 - Показати всіх котів
2 - Знайти кота за ім'ям
3 - Оновити вік кота
4 - Додати характеристику коту
5 - Видалити кота за ім'ям
6 - Видалити всіх котів
7 - Додати кота
0 - Вихід
"""


def main():
    try:
        client.admin.command("ping")
    except PyMongoError as e:
        print(f"Не вдалося підключитися до MongoDB: {e}")
        return

    while True:
        print(MENU)
        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            read_all()
        elif choice == "2":
            read_by_name(input("Ім'я кота: ").strip())
        elif choice == "3":
            name = input("Ім'я кота: ").strip()
            age = ask_int("Новий вік: ")
            if age is not None:
                update_age(name, age)
        elif choice == "4":
            name = input("Ім'я кота: ").strip()
            add_feature(name, input("Нова характеристика: ").strip())
        elif choice == "5":
            delete_by_name(input("Ім'я кота: ").strip())
        elif choice == "6":
            if input("Точно видалити всіх? (y/n): ").strip().lower() == "y":
                delete_all()
        elif choice == "7":
            name = input("Ім'я кота: ").strip()
            age = ask_int("Вік: ")
            if age is None:
                continue
            features = [f.strip() for f in input("Характеристики через кому: ").split(",") if f.strip()]
            create_cat(name, age, features)
        elif choice == "0":
            break
        else:
            print("Невідома команда")

    client.close()


if __name__ == "__main__":
    main()

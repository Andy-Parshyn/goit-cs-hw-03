from pymongo import MongoClient
from pymongo.errors import PyMongoError

CATS = [
    {"name": "barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
    {"name": "murzik", "age": 5, "features": ["любить спати", "сірий"]},
    {"name": "lama", "age": 2, "features": ["ходить в лоток", "не дає себе гладити"]},
]

if __name__ == "__main__":
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        cats = client["cats_db"]["cats"]
        cats.delete_many({})
        result = cats.insert_many(CATS)
        print(f"Додано котів: {len(result.inserted_ids)}")
    except PyMongoError as e:
        print(f"Помилка: {e}")

import pymongo
import json

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = db_client["justdial"]
apartments_col = db["classes"]


def insert(apartment_data: dict) -> None:
    apartments_col.insert_one(apartment_data)
    print('Inserted: ', apartment_data)


def dump():
    return [list(doc.values())[1::] for doc in apartments_col.find({})]


def dump_json():
    data = [list(doc.values())[1::] for doc in apartments_col.find({})]
    result = []
    for item in data:
        result.append(dict(title=item[0], address=item[1], phone=item[2]))

    with open('classes.json', 'w') as file:
        file.write(json.dumps(result))
    print(result)

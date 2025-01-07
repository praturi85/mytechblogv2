# config/db.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.techblog
articles_collection = db.articles
comments_collection = db.comments

# utils/helper.py
def object_id_str(obj):
    return str(obj)
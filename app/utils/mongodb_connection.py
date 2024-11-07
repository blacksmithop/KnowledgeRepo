from pymongo import MongoClient
import urllib.parse
from json import load
from app.utils.models import Category, CategoryExample
from bson import ObjectId

DATABASE_NAME = "knowledge_repo"
COLLECTION_NAME = "domain_specific"

username = urllib.parse.quote_plus('abhi')
password = urllib.parse.quote_plus('supersecretpassword')

class MongoDB:
    def __init__(
        self,
        uri="mongodb://%s:%s@localhost:27018/" % (username, password),
    ):
        self.client = MongoClient(uri)
        self.database = self.client[DATABASE_NAME]
        collection_exists = self._check_if_collection_exists()
        print(f"Collection exists: {collection_exists}")
        if not collection_exists:
            self._populate_collection()
        
    def _check_if_collection_exists(self):
        collections = self.database.list_collection_names()
        if COLLECTION_NAME not in collections:
            self.collection = self.database[COLLECTION_NAME]
            return False
        self.collection = self.database[COLLECTION_NAME]
        return True
    
    def _populate_collection(self):
        with open("./static/reference/knowledge_base_data.json") as f:
            data = load(f)
        print(f"Loaded sample collection data ({len(data)})")
        self.collection.insert_many(data)
        print("Inserted sample collection data")
    
    def _fetch_data(self, exclude_id: bool = True):
        if exclude_id:
            return self.collection.find({}, {'_id': False})
        return self.collection.find()
    
    def get_domain_knowledge(self):
        data = self._fetch_data()
        return list(data) # use next for processing
    
    def add_category(self, data: Category):
        self.collection.insert_one(dict(data))
        
    def delete_category(self, category_id: str):
        object_id = ObjectId(category_id)
        self.collection.delete_one({"_id": ObjectId(object_id)})
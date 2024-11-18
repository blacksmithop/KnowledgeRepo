import urllib.parse
from json import load
from os import getenv
from app import embeddings
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.documents import Document
from app.utils.models import Category

load_dotenv()

deployment_mode = getenv("DEPLOYMENT_MODE") or "dev"

DATABASE_NAME = "knowledge_repo"
COLLECTION_NAME = "domain_specific"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"


user, pwd, uri, port = (
    getenv("MONGO_USER"),
    getenv("MONGO_PWD"),
    getenv("MONGO_URI"),
    getenv("MONGO_PORT"),
)
username = urllib.parse.quote_plus(user)
password = urllib.parse.quote_plus(pwd)
uri = uri or "mongodb"
port = port or 27018


class MongoDB:
    def __init__(
        self
    ):
        if deployment_mode == "production":
            uri="mongodb://%s:%s@mongodb:27017/" % (username, password)
        elif deployment_mode == "dev":
            uri="mongodb://%s:%s@localhost:27017/" % (username, password)
        try:
            self.client = MongoClient(uri)
        except Exception as e:
            print(f"Failed to connect to MongoDB due to {e}")
            exit(0)
            
        self.database = self.client[DATABASE_NAME]
        try:
            collection_exists = self._check_if_collection_exists()
        except Exception as e:
            print(e)
            exit(0)
            
        print(f"Collection exists: {collection_exists}")
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.collection,
            embedding=embeddings,
            index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
            relevance_score_fn="cosine",
        )
        
        # if not collection_exists:
            # self._populate_collection()

    def _check_if_collection_exists(self):
        collections = self.database.list_collection_names()
        if COLLECTION_NAME not in collections:
            self.collection = self.database[COLLECTION_NAME]
            return False
        self.collection = self.database[COLLECTION_NAME]
        return True

    def _populate_with_vector_store(self, data: dict):
        documents = []
        dataset = []

        for item in data:
            try:
                entry = Category(**item)
                dataset.append(entry)
            except Exception as e:
                print(f"Ingoring {item} due to {e}")
        for item in dataset:
            page_content = item.description
            entry = dict(item)
            try:
                del entry['description']
                del entry['_id']
            except:
                ...
            doc = Document(page_content=page_content, metadata=entry)
            documents.append(doc)
        self.vector_store.add_documents(documents=documents)
            


    def _populate_collection(self):
        with open("./static/reference/knowledge_base_data.json") as f:
            data = load(f)
        print(f"Loaded sample collection data ({len(data)})")
        self._populate_with_vector_store(data=data)
        # self.collection.insert_many(data)
        print("Inserted sample collection data")

    def _fetch_data(self, exclude_id: bool = True):
        if exclude_id:
            return self.collection.find({}, {"_id": False})
        return self.collection.find()

    def get_domain_knowledge(self):
        data = self._fetch_data()
        return list(data)  # use next for processing

    def add_category(self, data: Category):
        self.collection.insert_one(dict(data))

    def delete_category(self, category_id: str):
        object_id = ObjectId(category_id)
        self.collection.delete_one({"_id": ObjectId(object_id)})

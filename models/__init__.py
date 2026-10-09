from pymongo import MongoClient
import pymongo
from bson import ObjectId
import os
import sys

_client = None
_db = None
_use_mock = False

class MockCollection:
    def __init__(self, name):
        self.name = name
        self.docs = []

    def find(self, query=None, sort=None):
        query = query or {}
        results = []
        for doc in self.docs:
            match = True
            for k, v in query.items():
                if k == '_id':
                    if str(doc.get('_id')) != str(v):
                        match = False
                        break
                elif doc.get(k) != v:
                    match = False
                    break
            if match:
                results.append(dict(doc))
        if sort:
            key, direction = sort[0]
            results.sort(key=lambda x: x.get(key, ''), reverse=(direction == -1 or direction == pymongo.DESCENDING))
        return results

    def find_one(self, query=None):
        res = self.find(query)
        return res[0] if res else None

    def insert_one(self, doc):
        if '_id' not in doc or not doc['_id']:
            doc['_id'] = ObjectId()
        elif isinstance(doc['_id'], str):
            doc['_id'] = ObjectId(doc['_id'])
        self.docs.append(dict(doc))
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc['_id'])

    def update_one(self, query, update):
        target = self.find_one(query)
        if target:
            target_real = next((d for d in self.docs if str(d.get('_id')) == str(target.get('_id'))), None)
            if target_real and '$set' in update:
                for k, v in update['$set'].items():
                    target_real[k] = v
                class UpdateResult:
                    modified_count = 1
                return UpdateResult()
        class UpdateResult:
            modified_count = 0
        return UpdateResult()

    def delete_one(self, query):
        target = self.find_one(query)
        if target:
            self.docs = [d for d in self.docs if str(d.get('_id')) != str(target.get('_id'))]
            class DeleteResult:
                deleted_count = 1
            return DeleteResult()
        class DeleteResult:
            deleted_count = 0
        return DeleteResult()

    def count_documents(self, query=None):
        return len(self.find(query or {}))

class MockDatabase:
    def __init__(self):
        self.collections = {}

    def __getitem__(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollection(name)
        return self.collections[name]

    def __getattr__(self, name):
        return self[name]

_mock_db_instance = MockDatabase()

def init_db(app):
    global _client, _db, _use_mock
    mongo_uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/travel_booking')
    db_name = app.config.get('DB_NAME', 'travel_booking')

    try:
        # Server selection timeout (5000ms recommended for cloud Atlas clusters)
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        _client.admin.command('ping')
        _db = _client[db_name]
        _use_mock = False
        print(f"[MongoDB] Connected successfully to MongoDB database: {db_name}")
    except Exception as e:
        print(f"[MongoDB Warning] Could not connect to MongoDB server ({e}). Operating in memory/fallback mode for development.")
        _use_mock = True
        _db = _mock_db_instance

def get_db():
    global _db
    if _db is None:
        return _mock_db_instance
    return _db

def to_object_id(id_str):
    if not id_str:
        return None
    if isinstance(id_str, ObjectId):
        return id_str
    try:
        return ObjectId(str(id_str))
    except Exception:
        return None

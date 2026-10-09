from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import get_db, to_object_id

class User:
    collection_name = 'users'

    @classmethod
    def get_collection(cls):
        return get_db()[cls.collection_name]

    @classmethod
    def create(cls, name, email, password, phone='', role='user'):
        hashed_password = generate_password_hash(password)
        user_doc = {
            'name': name,
            'email': email.lower().strip(),
            'password': hashed_password,
            'phone': phone,
            'role': role,  # 'user' or 'admin'
            'created_at': datetime.utcnow()
        }
        res = cls.get_collection().insert_one(user_doc)
        user_doc['_id'] = str(res.inserted_id)
        return user_doc

    @classmethod
    def find_by_email(cls, email):
        user = cls.get_collection().find_one({'email': email.lower().strip()})
        if user:
            user['_id'] = str(user['_id'])
        return user

    @classmethod
    def find_by_id(cls, user_id):
        obj_id = to_object_id(user_id)
        if not obj_id:
            return None
        user = cls.get_collection().find_one({'_id': obj_id})
        if user:
            user['_id'] = str(user['_id'])
        return user

    @classmethod
    def verify_password(cls, stored_password_hash, password):
        return check_password_hash(stored_password_hash, password)

    @classmethod
    def get_all(cls):
        users = list(cls.get_collection().find())
        for u in users:
            u['_id'] = str(u['_id'])
        return users

    @classmethod
    def count(cls):
        return cls.get_collection().count_documents({})

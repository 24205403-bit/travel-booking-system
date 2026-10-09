from datetime import datetime
from models import get_db, to_object_id

class Destination:
    collection_name = 'destinations'

    @classmethod
    def get_collection(cls):
        return get_db()[cls.collection_name]

    @classmethod
    def create(cls, title, location, price, duration, description, category, image_url, highlights=None, included=None, rating=4.5):
        dest_doc = {
            'title': title,
            'location': location,
            'price': float(price),
            'duration': duration,
            'description': description,
            'category': category,  # e.g., Hill Station, Beach, Cultural, Nature
            'image_url': image_url,
            'highlights': highlights or [],
            'included': included or [],
            'rating': float(rating),
            'created_at': datetime.utcnow()
        }
        res = cls.get_collection().insert_one(dest_doc)
        dest_doc['_id'] = str(res.inserted_id)
        return dest_doc

    @classmethod
    def find_all(cls, query_dict=None, sort_by=None):
        query_dict = query_dict or {}
        coll = cls.get_collection()
        if sort_by == 'price_low':
            items = list(coll.find(query_dict, sort=[('price', 1)]))
        elif sort_by == 'price_high':
            items = list(coll.find(query_dict, sort=[('price', -1)]))
        elif sort_by == 'rating':
            items = list(coll.find(query_dict, sort=[('rating', -1)]))
        else:
            items = list(coll.find(query_dict))

        for item in items:
            item['_id'] = str(item['_id'])
        return items

    @classmethod
    def find_by_id(cls, dest_id):
        obj_id = to_object_id(dest_id)
        if not obj_id:
            return None
        dest = cls.get_collection().find_one({'_id': obj_id})
        if dest:
            dest['_id'] = str(dest['_id'])
        return dest

    @classmethod
    def update(cls, dest_id, data):
        obj_id = to_object_id(dest_id)
        if not obj_id:
            return False
        data['updated_at'] = datetime.utcnow()
        if 'price' in data:
            data['price'] = float(data['price'])
        if 'rating' in data:
            data['rating'] = float(data['rating'])
        res = cls.get_collection().update_one({'_id': obj_id}, {'$set': data})
        return res.modified_count > 0

    @classmethod
    def delete(cls, dest_id):
        obj_id = to_object_id(dest_id)
        if not obj_id:
            return False
        res = cls.get_collection().delete_one({'_id': obj_id})
        return res.deleted_count > 0

    @classmethod
    def count(cls):
        return cls.get_collection().count_documents({})

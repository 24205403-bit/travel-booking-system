from datetime import datetime
from models import get_db, to_object_id


class PackageType:
    collection_name = 'package_types'

    @classmethod
    def get_collection(cls):
        return get_db()[cls.collection_name]

    @classmethod
    def create(cls, name, icon='fa-map-marker-alt', description='', color='#6366f1'):
        """Create a new package type / category."""
        # Prevent duplicates (case-insensitive)
        existing = cls.get_collection().find_one({'name_lower': name.strip().lower()})
        if existing:
            return None

        doc = {
            'name': name.strip(),
            'name_lower': name.strip().lower(),
            'icon': icon.strip(),
            'description': description.strip(),
            'color': color.strip(),
            'created_at': datetime.utcnow()
        }
        res = cls.get_collection().insert_one(doc)
        doc['_id'] = str(res.inserted_id)
        return doc

    @classmethod
    def find_all(cls):
        items = list(cls.get_collection().find())
        for item in items:
            item['_id'] = str(item['_id'])
        return items

    @classmethod
    def find_by_id(cls, type_id):
        obj_id = to_object_id(type_id)
        if not obj_id:
            return None
        item = cls.get_collection().find_one({'_id': obj_id})
        if item:
            item['_id'] = str(item['_id'])
        return item

    @classmethod
    def find_by_name(cls, name):
        item = cls.get_collection().find_one({'name_lower': name.strip().lower()})
        if item:
            item['_id'] = str(item['_id'])
        return item

    @classmethod
    def update(cls, type_id, data):
        obj_id = to_object_id(type_id)
        if not obj_id:
            return False
        data['updated_at'] = datetime.utcnow()
        if 'name' in data:
            data['name_lower'] = data['name'].strip().lower()
        res = cls.get_collection().update_one({'_id': obj_id}, {'$set': data})
        return res.modified_count > 0

    @classmethod
    def delete(cls, type_id):
        obj_id = to_object_id(type_id)
        if not obj_id:
            return False
        res = cls.get_collection().delete_one({'_id': obj_id})
        return res.deleted_count > 0

    @classmethod
    def count(cls):
        return cls.get_collection().count_documents({})

    @classmethod
    def seed_defaults(cls):
        """Seed default package types if none exist."""
        if cls.count() > 0:
            return
        defaults = [
            {'name': 'Hill Station', 'icon': 'fa-mountain', 'description': 'Misty mountains, cool climate & scenic views', 'color': '#10b981'},
            {'name': 'Beach', 'icon': 'fa-umbrella-beach', 'description': 'Sun, sand & sea adventures', 'color': '#f59e0b'},
            {'name': 'Nature', 'icon': 'fa-leaf', 'description': 'Wildlife, forests & natural wonders', 'color': '#22c55e'},
            {'name': 'Cultural', 'icon': 'fa-landmark', 'description': 'Heritage sites, temples & historical tours', 'color': '#8b5cf6'},
            {'name': 'Adventure', 'icon': 'fa-person-hiking', 'description': 'Trekking, rafting & extreme sports', 'color': '#ef4444'},
        ]
        for d in defaults:
            cls.create(**d)

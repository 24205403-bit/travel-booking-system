from datetime import datetime
from models import get_db, to_object_id

class Review:
    collection_name = 'reviews'

    @classmethod
    def get_collection(cls):
        return get_db()[cls.collection_name]

    @classmethod
    def create(cls, destination_id, user_id, user_name, rating, comment):
        rev_doc = {
            'destination_id': str(destination_id),
            'user_id': str(user_id),
            'user_name': user_name,
            'rating': int(rating),
            'comment': comment,
            'created_at': datetime.utcnow()
        }
        res = cls.get_collection().insert_one(rev_doc)
        rev_doc['_id'] = str(res.inserted_id)

        # Update average rating of destination
        cls.recalculate_destination_rating(destination_id)
        return rev_doc

    @classmethod
    def find_by_destination(cls, destination_id):
        items = list(cls.get_collection().find({'destination_id': str(destination_id)}))
        for item in items:
            item['_id'] = str(item['_id'])
        return items

    @classmethod
    def recalculate_destination_rating(cls, destination_id):
        from models.destination import Destination
        reviews = cls.find_by_destination(destination_id)
        if reviews:
            avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
            Destination.update(destination_id, {'rating': round(avg_rating, 1)})

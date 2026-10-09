from datetime import datetime
import random
import string
from models import get_db, to_object_id

class Booking:
    collection_name = 'bookings'

    @classmethod
    def get_collection(cls):
        return get_db()[cls.collection_name]

    @classmethod
    def generate_booking_ref(cls):
        return 'BK-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    @classmethod
    def create(cls, user_id, destination_id, travel_date, guests, total_price, special_requests=''):
        ref_code = cls.generate_booking_ref()
        booking_doc = {
            'user_id': str(user_id),
            'destination_id': str(destination_id),
            'travel_date': travel_date,
            'guests': int(guests),
            'total_price': float(total_price),
            'special_requests': special_requests,
            'status': 'Pending',  # Pending, Confirmed, Cancelled
            'payment_status': 'Unpaid',  # Unpaid, Paid, Refunded
            'booking_ref': ref_code,
            'created_at': datetime.utcnow()
        }
        res = cls.get_collection().insert_one(booking_doc)
        booking_doc['_id'] = str(res.inserted_id)
        return booking_doc

    @classmethod
    def find_by_user(cls, user_id):
        items = list(cls.get_collection().find({'user_id': str(user_id)}))
        for item in items:
            item['_id'] = str(item['_id'])
        return items

    @classmethod
    def find_all(cls):
        items = list(cls.get_collection().find())
        for item in items:
            item['_id'] = str(item['_id'])
        return items

    @classmethod
    def find_by_id(cls, booking_id):
        obj_id = to_object_id(booking_id)
        if not obj_id:
            return None
        item = cls.get_collection().find_one({'_id': obj_id})
        if item:
            item['_id'] = str(item['_id'])
        return item

    @classmethod
    def update_status(cls, booking_id, status=None, payment_status=None):
        obj_id = to_object_id(booking_id)
        if not obj_id:
            return False
        update_data = {}
        if status:
            update_data['status'] = status
        if payment_status:
            update_data['payment_status'] = payment_status
        if update_data:
            update_data['updated_at'] = datetime.utcnow()
            cls.get_collection().update_one({'_id': obj_id}, {'$set': update_data})
            return True
        return False

    @classmethod
    def count(cls):
        return cls.get_collection().count_documents({})

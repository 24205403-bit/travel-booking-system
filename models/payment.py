from datetime import datetime
import random
import string
from models import get_db, to_object_id

class Payment:
    collection_name = 'payments'

    @classmethod
    def get_collection(cls):
        return get_db()[cls.collection_name]

    @classmethod
    def generate_tx_id(cls):
        return 'TXN-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    @classmethod
    def create(cls, booking_id, user_id, amount, method, status='Success'):
        tx_id = cls.generate_tx_id()
        pay_doc = {
            'booking_id': str(booking_id),
            'user_id': str(user_id),
            'amount': float(amount),
            'method': method,  # Credit Card, UPI, NetBanking, PayPal
            'transaction_id': tx_id,
            'status': status,
            'created_at': datetime.utcnow()
        }
        res = cls.get_collection().insert_one(pay_doc)
        pay_doc['_id'] = str(res.inserted_id)
        return pay_doc

    @classmethod
    def find_by_booking(cls, booking_id):
        item = cls.get_collection().find_one({'booking_id': str(booking_id)})
        if item:
            item['_id'] = str(item['_id'])
        return item

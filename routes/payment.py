from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.booking import Booking
from models.destination import Destination
from models.payment import Payment

payment_bp = Blueprint('payment', __name__)

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@payment_bp.route('/checkout/<booking_id>', methods=['GET', 'POST'])
@login_required
def checkout(booking_id):
    booking = Booking.find_by_id(booking_id)
    if not booking or (booking['user_id'] != session['user_id'] and session.get('user_role') != 'admin'):
        flash('Booking not found.', 'danger')
        return redirect(url_for('booking.my_bookings'))

    destination = Destination.find_by_id(booking['destination_id'])

    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'Credit Card')

        # Create payment record
        payment = Payment.create(
            booking_id=booking_id,
            user_id=session['user_id'],
            amount=booking['total_price'],
            method=payment_method,
            status='Success'
        )

        # Update booking status
        Booking.update_status(booking_id, status='Confirmed', payment_status='Paid')

        flash('Payment successful! Your trip is confirmed.', 'success')
        return redirect(url_for('booking.booking_details', booking_id=booking_id))

    existing_payment = Payment.find_by_booking(booking_id)

    return render_template('payments/payment.html',
                           booking=booking,
                           destination=destination,
                           existing_payment=existing_payment)

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.booking import Booking
from models.destination import Destination
from models.payment import Payment

booking_bp = Blueprint('booking', __name__)

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@booking_bp.route('/create/<dest_id>', methods=['GET', 'POST'])
@login_required
def create_booking(dest_id):
    destination = Destination.find_by_id(dest_id)
    if not destination:
        flash('Destination not found.', 'danger')
        return redirect(url_for('destination.list_destinations'))

    if request.method == 'POST':
        travel_date = request.form.get('travel_date')
        guests = int(request.form.get('guests', 1))
        special_requests = request.form.get('special_requests', '').strip()

        if not travel_date or guests < 1:
            flash('Please select a valid travel date and guest count.', 'danger')
            return render_template('bookings/booking.html', destination=destination)

        total_price = destination['price'] * guests
        user_id = session['user_id']

        booking = Booking.create(
            user_id=user_id,
            destination_id=dest_id,
            travel_date=travel_date,
            guests=guests,
            total_price=total_price,
            special_requests=special_requests
        )

        flash('Booking initiated! Proceed to payment to confirm.', 'success')
        return redirect(url_for('payment.checkout', booking_id=booking['_id']))

    return render_template('bookings/booking.html', destination=destination)

@booking_bp.route('/my_bookings')
@login_required
def my_bookings():
    user_id = session['user_id']
    user_bookings = Booking.find_by_user(user_id)

    # Attach destination details to each booking
    detailed_bookings = []
    for b in user_bookings:
        dest = Destination.find_by_id(b['destination_id'])
        payment = Payment.find_by_booking(b['_id'])
        b['destination'] = dest or {'title': 'Unknown Package', 'image_url': '', 'location': 'N/A'}
        b['payment'] = payment
        detailed_bookings.append(b)

    return render_template('bookings/my_bookings.html', bookings=detailed_bookings)

@booking_bp.route('/details/<booking_id>')
@login_required
def booking_details(booking_id):
    booking = Booking.find_by_id(booking_id)
    if not booking or (booking['user_id'] != session['user_id'] and session.get('user_role') != 'admin'):
        flash('Booking record not found or access denied.', 'danger')
        return redirect(url_for('booking.my_bookings'))

    destination = Destination.find_by_id(booking['destination_id'])
    payment = Payment.find_by_booking(booking_id)

    return render_template('bookings/booking_details.html',
                           booking=booking,
                           destination=destination,
                           payment=payment)

@booking_bp.route('/cancel/<booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.find_by_id(booking_id)
    if booking and (booking['user_id'] == session['user_id'] or session.get('user_role') == 'admin'):
        Booking.update_status(booking_id, status='Cancelled')
        flash('Booking has been cancelled.', 'info')
    else:
        flash('Permission denied.', 'danger')
    return redirect(url_for('booking.my_bookings'))

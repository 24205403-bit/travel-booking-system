from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.destination import Destination
from models.booking import Booking
from models.payment import Payment
from models.package_type import PackageType

admin_bp = Blueprint('admin', __name__)

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            flash('Access denied. Admin authorization required.', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_users = User.count()
    total_destinations = Destination.count()
    total_bookings = Booking.count()
    total_package_types = PackageType.count()
    all_bookings = Booking.find_all()

    total_revenue = sum(b['total_price'] for b in all_bookings if b.get('payment_status') == 'Paid')
    recent_bookings = sorted(all_bookings, key=lambda x: str(x.get('created_at', '')), reverse=True)[:5]

    for b in recent_bookings:
        dest = Destination.find_by_id(b['destination_id'])
        usr = User.find_by_id(b['user_id'])
        b['destination_title'] = dest['title'] if dest else 'N/A'
        b['user_name'] = usr['name'] if usr else 'N/A'

    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_destinations=total_destinations,
                           total_bookings=total_bookings,
                           total_revenue=total_revenue,
                           total_package_types=total_package_types,
                           recent_bookings=recent_bookings)

@admin_bp.route('/destinations')
@admin_required
def list_destinations():
    destinations = Destination.find_all()
    return render_template('admin/destinations.html', destinations=destinations)

@admin_bp.route('/destinations/add', methods=['GET', 'POST'])
@admin_required
def add_destination():
    package_types = PackageType.find_all()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        location = request.form.get('location', '').strip()
        price = request.form.get('price', 0)
        duration = request.form.get('duration', '').strip()
        category = request.form.get('category', 'Hill Station').strip()
        image_url = request.form.get('image_url', '').strip()
        description = request.form.get('description', '').strip()
        highlights_raw = request.form.get('highlights', '')
        included_raw = request.form.get('included', '')

        highlights = [h.strip() for h in highlights_raw.split(',') if h.strip()]
        included = [i.strip() for i in included_raw.split(',') if i.strip()]

        if not title or not location or not price:
            flash('Title, Location, and Price are required.', 'danger')
            return render_template('admin/add_destination.html', package_types=package_types)

        if not image_url:
            image_url = '/static/images/ooty.jpg'

        Destination.create(
            title=title,
            location=location,
            price=price,
            duration=duration,
            description=description,
            category=category,
            image_url=image_url,
            highlights=highlights,
            included=included
        )

        flash('Destination package added successfully!', 'success')
        return redirect(url_for('admin.list_destinations'))

    return render_template('admin/add_destination.html', package_types=package_types)

@admin_bp.route('/destinations/edit/<dest_id>', methods=['GET', 'POST'])
@admin_required
def edit_destination(dest_id):
    destination = Destination.find_by_id(dest_id)
    if not destination:
        flash('Destination not found.', 'danger')
        return redirect(url_for('admin.list_destinations'))

    package_types = PackageType.find_all()

    if request.method == 'POST':
        highlights_raw = request.form.get('highlights', '')
        included_raw = request.form.get('included', '')

        highlights = [h.strip() for h in highlights_raw.split(',') if h.strip()]
        included = [i.strip() for i in included_raw.split(',') if i.strip()]

        data = {
            'title': request.form.get('title', '').strip(),
            'location': request.form.get('location', '').strip(),
            'price': float(request.form.get('price', 0)),
            'duration': request.form.get('duration', '').strip(),
            'category': request.form.get('category', '').strip(),
            'image_url': request.form.get('image_url', '').strip(),
            'description': request.form.get('description', '').strip(),
            'highlights': highlights,
            'included': included
        }

        Destination.update(dest_id, data)
        flash('Destination updated successfully!', 'success')
        return redirect(url_for('admin.list_destinations'))

    destination['highlights_str'] = ', '.join(destination.get('highlights', []))
    destination['included_str'] = ', '.join(destination.get('included', []))
    return render_template('admin/edit_destination.html', destination=destination, package_types=package_types)

@admin_bp.route('/destinations/delete/<dest_id>', methods=['POST'])
@admin_required
def delete_destination(dest_id):
    Destination.delete(dest_id)
    flash('Destination deleted.', 'info')
    return redirect(url_for('admin.list_destinations'))

# ─── Package Type Management ─────────────────────────────────────────────────

@admin_bp.route('/package-types')
@admin_required
def list_package_types():
    package_types = PackageType.find_all()
    # Count destinations per package type
    all_destinations = Destination.find_all()
    for pt in package_types:
        pt['dest_count'] = sum(1 for d in all_destinations if d.get('category', '').lower() == pt['name'].lower())
    return render_template('admin/package_types.html', package_types=package_types)

@admin_bp.route('/package-types/add', methods=['GET', 'POST'])
@admin_required
def add_package_type():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        icon = request.form.get('icon', 'fa-map-marker-alt').strip()
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '#6366f1').strip()

        if not name:
            flash('Package type name is required.', 'danger')
            return render_template('admin/add_package_type.html')

        result = PackageType.create(name=name, icon=icon, description=description, color=color)
        if result is None:
            flash(f'Package type "{name}" already exists.', 'warning')
            return render_template('admin/add_package_type.html')

        flash(f'Package type "{name}" created successfully!', 'success')
        return redirect(url_for('admin.list_package_types'))

    return render_template('admin/add_package_type.html')

@admin_bp.route('/package-types/edit/<type_id>', methods=['GET', 'POST'])
@admin_required
def edit_package_type(type_id):
    pkg_type = PackageType.find_by_id(type_id)
    if not pkg_type:
        flash('Package type not found.', 'danger')
        return redirect(url_for('admin.list_package_types'))

    if request.method == 'POST':
        data = {
            'name': request.form.get('name', '').strip(),
            'icon': request.form.get('icon', 'fa-map-marker-alt').strip(),
            'description': request.form.get('description', '').strip(),
            'color': request.form.get('color', '#6366f1').strip(),
        }
        if not data['name']:
            flash('Package type name is required.', 'danger')
            return render_template('admin/edit_package_type.html', package_type=pkg_type)

        PackageType.update(type_id, data)
        flash(f'Package type "{data["name"]}" updated successfully!', 'success')
        return redirect(url_for('admin.list_package_types'))

    return render_template('admin/edit_package_type.html', package_type=pkg_type)

@admin_bp.route('/package-types/delete/<type_id>', methods=['POST'])
@admin_required
def delete_package_type(type_id):
    pkg_type = PackageType.find_by_id(type_id)
    name = pkg_type['name'] if pkg_type else 'Unknown'
    PackageType.delete(type_id)
    flash(f'Package type "{name}" deleted.', 'info')
    return redirect(url_for('admin.list_package_types'))

# ─── Booking Management ──────────────────────────────────────────────────────

@admin_bp.route('/bookings')
@admin_required
def manage_bookings():
    bookings = Booking.find_all()
    for b in bookings:
        dest = Destination.find_by_id(b['destination_id'])
        usr = User.find_by_id(b['user_id'])
        b['destination_title'] = dest['title'] if dest else 'N/A'
        b['user_name'] = usr['name'] if usr else 'N/A'
        b['user_email'] = usr['email'] if usr else 'N/A'

    return render_template('admin/bookings.html', bookings=bookings)

@admin_bp.route('/bookings/update_status/<booking_id>', methods=['POST'])
@admin_required
def update_booking_status(booking_id):
    new_status = request.form.get('status')
    payment_status = request.form.get('payment_status')
    Booking.update_status(booking_id, status=new_status, payment_status=payment_status)
    flash('Booking status updated.', 'success')
    return redirect(url_for('admin.manage_bookings'))

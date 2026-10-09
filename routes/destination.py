from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.destination import Destination
from models.review import Review

dest_bp = Blueprint('destination', __name__)

@dest_bp.route('/')
def list_destinations():
    search_query = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', '').strip()

    all_items = Destination.find_all(sort_by=sort_by)
    categories = list(set([d.get('category', 'General') for d in all_items if d.get('category')]))

    # Apply filters
    filtered_items = []
    for item in all_items:
        match = True
        if search_query:
            q = search_query.lower()
            if q not in item['title'].lower() and q not in item['location'].lower() and q not in item['description'].lower():
                match = False
        if category and category.lower() != 'all':
            if item.get('category', '').lower() != category.lower():
                match = False
        if match:
            filtered_items.append(item)

    return render_template('destinations/destinations.html',
                           destinations=filtered_items,
                           categories=categories,
                           selected_category=category,
                           search_query=search_query,
                           sort_by=sort_by)

@dest_bp.route('/<dest_id>')
def details(dest_id):
    destination = Destination.find_by_id(dest_id)
    if not destination:
        flash('Destination not found.', 'danger')
        return redirect(url_for('destination.list_destinations'))

    reviews = Review.find_by_destination(dest_id)
    return render_template('destinations/details.html', destination=destination, reviews=reviews)

from flask import Blueprint, render_template, request, session
from models.destination import Destination

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_destinations = Destination.find_all(sort_by='rating')[:4]
    all_destinations = Destination.find_all()
    categories = list(set([d.get('category', 'General') for d in all_destinations if d.get('category')]))
    return render_template('home/index.html', featured=featured_destinations, categories=categories)

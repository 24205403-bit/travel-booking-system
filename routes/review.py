from flask import Blueprint, request, redirect, url_for, flash, session
from models.review import Review

review_bp = Blueprint('review', __name__)

@review_bp.route('/add/<dest_id>', methods=['POST'])
def add_review(dest_id):
    if 'user_id' not in session:
        flash('You must be logged in to leave a review.', 'warning')
        return redirect(url_for('auth.login'))

    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '').strip()

    if not comment:
        flash('Review comment cannot be empty.', 'danger')
        return redirect(url_for('destination.details', dest_id=dest_id))

    Review.create(
        destination_id=dest_id,
        user_id=session['user_id'],
        user_name=session.get('user_name', 'Anonymous Traveler'),
        rating=rating,
        comment=comment
    )

    flash('Thank you! Your review has been added.', 'success')
    return redirect(url_for('destination.details', dest_id=dest_id))

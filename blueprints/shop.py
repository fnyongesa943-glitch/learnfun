"""
Shop Blueprint - Avatar and item customization.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, ShopItem, UserOwnedItem
from blueprints.auth import login_required

shop_bp = Blueprint('shop', __name__)


@shop_bp.route('/')
@login_required
def index():
    """Shop home page."""
    user = User.query.get(session['user_id'])
    items = ShopItem.query.all()
    owned = UserOwnedItem.query.filter_by(user_id=user.id).all()
    owned_ids = [o.item_id for o in owned]
    return render_template('shop.html', user=user, items=items, owned_ids=owned_ids)


@shop_bp.route('/buy/<int:item_id>', methods=['POST'])
@login_required
def buy_item(item_id):
    """Purchase an item."""
    user = User.query.get(session['user_id'])
    item = ShopItem.query.get_or_404(item_id)

    # Check if already owned
    existing = UserOwnedItem.query.filter_by(user_id=user.id, item_id=item_id).first()
    if existing:
        flash('You already own this!', 'warning')
        return redirect(url_for('shop.index'))

    if user.coins < item.price:
        flash(f'Not enough coins! Need {item.price} but you have {user.coins}.', 'error')
        return redirect(url_for('shop.index'))

    # Buy it
    user.coins -= item.price
    new_item = UserOwnedItem(user_id=user.id, item_id=item_id, is_active=(item.item_type == 'hat' or item.item_type == 'frame'))
    db.session.add(new_item)
    db.session.commit()

    flash(f'Bought {item.name} for {item.price} coins! 🎉', 'success')
    return redirect(url_for('shop.index'))


@shop_bp.route('/equip/<int:item_id>', methods=['POST'])
@login_required
def equip_item(item_id):
    """Equip an owned item."""
    user = User.query.get(session['user_id'])
    owned = UserOwnedItem.query.filter_by(user_id=user.id, item_id=item_id).first()

    if not owned:
        flash('You don\'t own this item!', 'error')
        return redirect(url_for('shop.index'))

    # Deactivate others of same type
    item = ShopItem.query.get(item_id)
    if item.item_type in ['hat', 'frame']:
        UserOwnedItem.query.filter_by(user_id=user.id).update({UserOwnedItem.is_active: False})
    
    owned.is_active = True
    
    # Update user profile if it's an avatar change
    if item.item_type == 'avatar':
        user.avatar = item.icon
    elif item.item_type == 'hat':
        user.avatar_frame = item.icon
    elif item.item_type == 'frame':
        user.avatar_frame = item.icon
    
    db.session.commit()
    flash(f'Equipped {item.name}! ✨', 'success')
    return redirect(url_for('shop.index'))

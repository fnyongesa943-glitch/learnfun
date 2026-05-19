from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Payment, DigitalProduct, UserDownload
from functools import wraps
from datetime import datetime, timedelta
from daraja import stk_push, query_status

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


def premium_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access premium content!', 'warning')
            return redirect(url_for('auth.login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_premium:
            flash('This content requires a Premium subscription. Upgrade now!', 'warning')
            return redirect(url_for('payments.upgrade'))
        if user.subscription_expiry and user.subscription_expiry < datetime.utcnow():
            user.is_premium = False
            db.session.commit()
            flash('Your subscription has expired. Renew to continue accessing premium content!', 'warning')
            return redirect(url_for('payments.upgrade'))
        return f(*args, **kwargs)
    return decorated_function


def check_premium():
    if 'user_id' not in session:
        return False
    user = User.query.get(session['user_id'])
    if not user:
        return False
    if not user.is_premium:
        return False
    if user.subscription_expiry and user.subscription_expiry < datetime.utcnow():
        user.is_premium = False
        db.session.commit()
        return False
    return True


@payments_bp.route('/upgrade')
def upgrade():
    plan = {
        'name': 'Premium Learning Plan',
        'price': 200,
        'currency': 'KES',
        'duration_days': 30,
        'features': [
            'Full access to all lessons',
            'Interactive quizzes and exercises',
            'Advanced phonics lessons',
            'Progress tracking dashboard',
            'Ad-free experience',
            'Printable worksheets',
            'Priority support'
        ]
    }
    digital_products = DigitalProduct.query.filter_by(is_active=True).all()
    return render_template('upgrade.html', plan=plan, digital_products=digital_products)


@payments_bp.route('/initiate', methods=['POST'])
def initiate_payment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user = User.query.get(session['user_id'])
    phone = request.form.get('phone_number', '').strip()
    amount = request.form.get('amount', '200').strip()
    product_type = request.form.get('type', 'subscription')

    if not phone:
        return jsonify({'success': False, 'error': 'Phone number is required'}), 400

    if not phone.startswith('254'):
        phone = '254' + phone.lstrip('0')
    if len(phone) != 12 or not phone.isdigit():
        return jsonify({'success': False, 'error': 'Invalid phone number. Use 2547XXXXXXXX'}), 400

    try:
        amount = int(amount)
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid amount'}), 400

    if product_type == 'product':
        product_id = request.form.get('product_id')
        product = DigitalProduct.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        amount = product.price

    account_ref = f"UPGRADE-{user.id}" if product_type == 'subscription' else f"PROD-{product.id}-{user.id}"
    transaction_desc = 'Premium Subscription' if product_type == 'subscription' else f'{product.name}'

    payment = Payment(
        user_id=user.id,
        amount=amount,
        phone_number=phone,
        status='pending'
    )
    db.session.add(payment)
    db.session.commit()

    result = stk_push(phone, amount, account_ref, transaction_desc)

    if result.get('error'):
        payment.status = 'failed'
        payment.result_desc = result['error']
        db.session.commit()
        return jsonify({'success': False, 'error': result['error']}), 500

    if result.get('ResponseCode') == '0':
        payment.merchant_request_id = result.get('MerchantRequestID')
        payment.checkout_request_id = result.get('CheckoutRequestID')
        payment.transaction_id = account_ref
        user.phone_number = phone
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'STK Push sent! Check your phone to complete payment.',
            'checkout_request_id': payment.checkout_request_id
        })
    else:
        payment.status = 'failed'
        payment.result_desc = result.get('ResponseDescription', 'Payment initiation failed')
        db.session.commit()
        return jsonify({'success': False, 'error': result.get('ResponseDescription', 'Payment failed')}), 400


@payments_bp.route('/mpesa-callback', methods=['POST'])
def mpesa_callback():
    data = request.json

    if not data or 'Body' not in data:
        return jsonify({'ResultCode': 1, 'ResultDesc': 'Invalid request'}), 400

    stk_callback = data['Body']['stkCallback']
    checkout_request_id = stk_callback.get('CheckoutRequestID')
    result_code = stk_callback.get('ResultCode')
    result_desc = stk_callback.get('ResultDesc', '')

    payment = Payment.query.filter_by(checkout_request_id=checkout_request_id).first()
    if not payment:
        return jsonify({'ResultCode': 1, 'ResultDesc': 'Payment not found'}), 404

    payment.result_code = result_code
    payment.result_desc = result_desc

    if result_code == 0:
        payment.status = 'success'
        payment.transaction_id = checkout_request_id

        if 'CallbackMetadata' in stk_callback:
            metadata = {item['Name']: item.get('Value') for item in stk_callback['CallbackMetadata']['Item']}
            if 'MpesaReceiptNumber' in metadata:
                payment.transaction_id = metadata['MpesaReceiptNumber']

        user = User.query.get(payment.user_id)
        if user:
            user.is_premium = True
            user.subscription_expiry = datetime.utcnow() + timedelta(days=30)
            user.phone_number = payment.phone_number
            db.session.commit()
    else:
        payment.status = 'failed'

    db.session.commit()
    return jsonify({'ResultCode': 0, 'ResultDesc': 'Success'})


@payments_bp.route('/payment-status/<checkout_request_id>')
def payment_status(checkout_request_id):
    payment = Payment.query.filter_by(checkout_request_id=checkout_request_id).first()
    if not payment:
        return jsonify({'status': 'not_found'})

    if payment.status == 'pending':
        result = query_status(checkout_request_id)
        if result.get('ResultCode') == 0:
            payment.status = 'success'
            user = User.query.get(payment.user_id)
            if user:
                user.is_premium = True
                user.subscription_expiry = datetime.utcnow() + timedelta(days=30)
            db.session.commit()
        elif result.get('ResultCode') is not None and result.get('ResultCode') != 0:
            payment.status = 'failed'
            db.session.commit()

    return jsonify({'status': payment.status})


@payments_bp.route('/success')
def payment_success():
    return render_template('payment_status.html', success=True,
                           message='Payment successful! Welcome to Premium! Your premium access is now active.')


@payments_bp.route('/failed')
def payment_failed():
    return render_template('payment_status.html', success=False,
                           message='Payment was not completed. Please try again.')


@payments_bp.route('/buy-product/<int:product_id>', methods=['POST'])
def buy_product(product_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    product = DigitalProduct.query.get_or_404(product_id)
    if not product.is_active:
        return jsonify({'success': False, 'error': 'Product not available'}), 404

    existing = UserDownload.query.join(Payment).filter(
        UserDownload.user_id == session['user_id'],
        UserDownload.product_id == product_id,
        Payment.status == 'success'
    ).first()
    if existing:
        return jsonify({'success': False, 'error': 'You already own this product'}), 400

    phone = request.form.get('phone_number', '').strip()
    if not phone:
        return redirect(url_for('payments.upgrade'))

    if not phone.startswith('254'):
        phone = '254' + phone.lstrip('0')

    payment = Payment(
        user_id=session['user_id'],
        amount=product.price,
        phone_number=phone,
        status='pending'
    )
    db.session.add(payment)
    db.session.commit()

    result = stk_push(phone, product.price, f"PROD-{product.id}-{session['user_id']}", product.name)

    if result.get('error'):
        payment.status = 'failed'
        db.session.commit()
        return jsonify({'success': False, 'error': result['error']}), 500

    if result.get('ResponseCode') == '0':
        payment.merchant_request_id = result.get('MerchantRequestID')
        payment.checkout_request_id = result.get('CheckoutRequestID')
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'STK Push sent! Check your phone to complete payment.',
            'checkout_request_id': payment.checkout_request_id
        })

    payment.status = 'failed'
    db.session.commit()
    return jsonify({'success': False, 'error': 'Payment initiation failed'}), 400


@payments_bp.route('/download/<int:product_id>')
def download_product(product_id):
    if 'user_id' not in session:
        flash('Please log in to download products!', 'warning')
        return redirect(url_for('auth.login'))

    product = DigitalProduct.query.get_or_404(product_id)
    if not product.file_path:
        flash('File not available', 'error')
        return redirect(url_for('payments.upgrade'))

    download = UserDownload.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()

    if not download:
        flash('Please purchase this product first!', 'warning')
        return redirect(url_for('payments.upgrade'))

    return redirect(url_for('static', filename=product.file_path))

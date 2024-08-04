from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, Order, OrderItem
from app.forms import RegistrationForm, LoginForm
from app.utils import hash_password, check_password
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = hash_password(form.password.data)
        user = User(name=form.name.data, phone=form.phone.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        logger.info(f'New user registered: {user.name}')
        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and check_password(user.password_hash, form.password.data):
            login_user(user)
            logger.info(f'User logged in: {user.name}')
            return redirect(url_for('home'))
        else:
            flash('Неправильное имя или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    logger.info('User logged out')
    return redirect(url_for('home'))

@app.route('/menu')
def menu():
    # Пример списка блюд
    menu_items = [
        {"name": "Шашлык", "price": 200, "image": "kebab.jpg"},
        {"name": "Картофель жареный с грибами", "price": 110, "image": "tasty1.jpg"},
        {"name": "Плов", "price": 150, "image": "uzbek-cuisine.jpg"},
        {"name": "Суши и сеты", "price": 180, "image": "sushi-rolls-maki.jpg"},
        {"name": "Вареники с вишней", "price": 135, "image": "cherries-black.jpg"},
    ]
    return render_template('menu.html', menu_items=menu_items)

@app.route('/add_to_order', methods=['POST'])
@login_required
def add_to_order():
    item_name = request.form.get('item_name')
    quantity = int(request.form.get('quantity', 1))
    price = float(request.form.get('price'))

    order_item = OrderItem(name=item_name, quantity=quantity, price=price, order=current_user.id)
    db.session.add(order_item)
    db.session.commit()
    logger.info(f'Item added to order: {item_name}, quantity: {quantity}')

    flash(f'{item_name} добавлен в ваш заказ.', 'success')
    return redirect(url_for('menu'))

@app.route('/order')
@login_required
def order():
    order_items = OrderItem.query.filter_by(order=current_user.id).all()
    total = sum(item.quantity * item.price for item in order_items)
    return render_template('order.html', order_items=order_items, total=total)
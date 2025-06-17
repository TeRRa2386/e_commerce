from flask import Flask, render_template, session, request, redirect, url_for, flash
from dotenv import load_dotenv
from inventory import *
from models import *
import json
import os


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SK')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():

    return render_template('index.html', products=products)


@app.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):

    cart = session.get('cart', [])
    quantity = int(request.form.get('quantity',1))
    cart.append({'product_id': product_id, 'quantity': quantity})
    session['cart'] = cart
    return redirect(url_for('index'))


@app.route('/cart/fragment')
def cart_fragment():

    cart = session.get('cart', [])
    detailed_cart = {}
    subtotal = 0
    for item in cart:
        product = products.get(item['product_id'])
        if not product:
            continue

        product_id = item['product_id']
        quantity = item['quantity']
        product_price = round(product['price'] * (1 - product['disc_amount']) if product['disc'] else product['price'], 2)
        item_subtotal = round(product_price * quantity, 2)
        subtotal += item_subtotal

        if product_id in detailed_cart:
            detailed_cart[product_id]['quantity'] += quantity
            detailed_cart[product_id]['subtotal'] += item_subtotal
        else:
            detailed_cart[product_id] = {
                'product_id': product_id,
                'name': product['name'],
                'price': product_price,
                'quantity': quantity,
                'subtotal': item_subtotal
            }

    session['subtotal'] = subtotal

    return render_template('partials/cart_fragment.html', cart=detailed_cart.values(), total=subtotal)


@app.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]
    session['cart'] = cart
    return '', 204


@app.route('/checkout/fragment', methods=['GET', 'POST'])
def checkout():

    subtotal = session.get('subtotal',0)
    tax = round(subtotal * 0.067, 2)
    total = round(subtotal + tax, 2)

    if request.method == 'POST':
        customer_info = [{'firstName': request.form.get('firstName'), 'lastName': request.form.get('lastName'), 'email': request.form.get('email'),
                          'address': request.form.get('address'), 'country': request.form.get('country'), 'state': request.form.get('state'),
                          'zip': request.form.get('zip')}]
        payment_info = [{'paymentMethod': request.form.get('paymentMethod'), 'cardName': request.form.get('cardName'),
                         'cardNumber': request.form.get('cardNumber'), 'cardExpiration': request.form.get('cardExpiration'),
                         'cardCVV': request.form.get('cardCVV'), 'total': total}]
        cart = session.get('cart',[])
        order = Order(customer_info=json.dumps(customer_info), payment_info=json.dumps(payment_info), items=json.dumps(cart))
        db.session.add(order)
        db.session.commit()
        session['cart'] = []
        session['total'] = 0
        flash('Your order was created successfully!', 'success')
        return redirect(url_for('index'))


    return render_template('partials/checkout_fragment.html', total=total, subtotal=subtotal, tax=tax)



# if __name__ == '__main__':
#     app.run(debug=True)


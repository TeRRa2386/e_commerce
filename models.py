from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_info = db.Column(db.Text)
    payment_info = db.Column(db.Text)
    items = db.Column(db.Text)

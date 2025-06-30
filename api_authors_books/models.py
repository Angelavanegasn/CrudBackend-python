import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
   
#Modelo de la tabla producto
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    orders = db.relationship("Order")
 

#Modelo de la tabla pedido
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cant_product = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


    
from flask import Flask, request, jsonify
from models import db, Product,Order
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost:5433/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Esta línea es clave
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello world!'


#End point de productoS
#Metodo POST crear product
@app.route('/product', methods=['POST'])
def add_product():
    try:
        data = request.json
        name = data.get('name')
        price = data.get('price')
        if not name or not price:
            return jsonify({'message': 'Bad request, name or age not found'}), 400
        new_product = Product(name=name, price=price)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'product': {'id': new_product.id, 'name': new_product.name, 'price': new_product.price}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
   
#Metodo GET consultar product
@app.route('/product', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        products_data = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'orders': []
            }
            for order in product.orders:
                order_data = {
                    'id': order.id,
                    'name': order.name,
                    'cant_product': order.cant_product,
                    'total': order.total,
                    'createdAt': order.created_at
                }
                product_data['orders'].append(order_data)
            products_data.append(product_data)
        return jsonify({'products': products_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    

#Consultar por id un producto
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': f'product with id {product_id} not found'}), 404

        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'orders': []
        }
        for order in product.orders:
            order_data = {
                'id': order.id,
                'name': order.name,
                'cant_product': order.cant_product,
                'total': order.total,
                'createdAt': order.created_at
            }
            product_data['orders'].append(order_data)

        return jsonify({'product': product_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    

#Actualizar product
@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'messprice': f'product with id {product_id} not found'}), 404

        data = request.json
        name = data.get('name')
        price = data.get('price')

        if name:
            product.name = name
        if price:
            product.price = price

        db.session.commit()

        return jsonify({
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price
            }
        })
    except Exception as error:
        print('Error', error)
        return jsonify({'messprice': 'Internal server error'}), 500

#Metodo DELETE para eliminar un product
@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': f'product with id {product_id} not found'}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': f'product with id {product_id} deleted successfully'})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


#End point de pedidos
#Metodo POST crear order
@app.route('/orders', methods=['POST'])
def add_order():
    try:
        data = request.json
        name = data.get('name')
        cant_product = data.get('cant_product')
        total = data.get('total')
        product_id = data.get('product_id')
        if not cant_product or not total or not product_id or not name:
            return jsonify({'message': 'Bad request, name or cant_product or total or product not found'}), 400
        new_order = Order(name=name, cant_product=cant_product, total=total, product_id=product_id)
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'order': {'id': new_order.id, 'name': new_order.name, 'cant_product': new_order.cant_product, 'total': new_order.total}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


#Metodo GET consultar precios
@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        orders_data = []
        for order in orders:
            order_data = {
                'id': order.id,
                'name': order.name,
                'cant_product': order.cant_product,
                'total': order.total
            }
            orders_data.append(order_data)
        return jsonify({'orders': orders_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    
 
#Consultar precios por id 
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'message': f'order with id {order_id} not found'}), 404

        order_data = {
            'id': order.id,
            'name': order.name,
            'cant_product': order.cant_product,
            'total': order.total,
            'createdAt': order.created_at,
            'product_id': order.product_id
        }
        return jsonify({'order': order_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    

#Actualizar precios
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'message': f'order with id {order_id} not found'}), 404

        data = request.json
        name = data.get('name')
        cant_product = data.get('cant_product')
        total = data.get('total')
        product_id = data.get('product_id')

        if name:
            order.name = name
        if cant_product:
            order.cant_product = cant_product
        if total:
            order.total = total
        if product_id:
            order.product_id = product_id

        db.session.commit()

        return jsonify({
            'order': {
                'id': order.id,
                'name': order.name,
                'cant_product': order.cant_product,
                'total': order.total,
                'product_id': order.product_id
            }
        })
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

#Metodo DELETE para eliminar un producto por id
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'message': f'order with id {order_id} not found'}), 404

        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': f'order with id {order_id} deleted successfully'})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Esto crea las tablas si no existen
    app.run(port=3000, debug=True)

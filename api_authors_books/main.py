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

@app.route('/order', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    data = []
    for order in orders:
        data.append({
            "id": order.id,
            "name": order.name,
            "cant_product": order.cant_product,
            "total": order.total,
            "product_id": order.product_id
        })
    return jsonify({"orders": data})


@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    product = Product.query.filter_by(name=data['name']).first()
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    total = int(data['cant_product']) * product.price
    new_order = Order(
        name=data['name'],
        cant_product=data['cant_product'],
        total=total,
        product_id=product.id
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Pedido creado correctamente"}), 201


@app.route('/order/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.json
    order = Order.query.get_or_404(id)
    product = Product.query.filter_by(name=data['name']).first()
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    order.name = data['name']
    order.cant_product = data['cant_product']
    order.total = int(data['cant_product']) * product.price
    order.product_id = product.id
    db.session.commit()
    return jsonify({"message": "Pedido actualizado"})


@app.route('/order/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Pedido eliminado correctamente"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Esto crea las tablas si no existen
    app.run(port=3000, debug=True)
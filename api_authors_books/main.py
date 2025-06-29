from flask import Flask, request, jsonify
from models import db, Author, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost:5433/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Esta línea es clave
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/authors', methods=['GET'])
def get_authors():
    try:
        authors = Author.query.all()
        authors_data = []
        for author in authors:
            author_data = {
                'id': author.id,
                'name': author.name,
                'age': author.age,
                'books': []
            }
            for book in author.books:
                book_data = {
                    'id': book.id,
                    'isbn': book.isbn,
                    'name': book.name,
                    'cant_pages': book.cant_pages,
                    'createdAt': book.created_at
                }
                author_data['books'].append(book_data)
            authors_data.append(author_data)
        return jsonify({'authors': authors_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/authors', methods=['POST'])
def add_author():
    try:
        data = request.json
        name = data.get('name')
        age = data.get('age')
        if not name or not age:
            return jsonify({'message': 'Bad request, name or age not found'}), 400
        new_author = Author(name=name, age=age)
        db.session.add(new_author)
        db.session.commit()
        return jsonify({'author': {'id': new_author.id, 'name': new_author.name, 'age': new_author.age}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        books_data = []
        for book in books:
            book_data = {
                'id': book.id,
                'isbn': book.isbn,
                'name': book.name,
                'cant_pages': book.cant_pages
            }
            books_data.append(book_data)
        return jsonify({'books': books_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        isbn = data.get('isbn')
        name = data.get('name')
        cant_pages = data.get('cant_pages')
        author_id = data.get('author_id')
        if not name or not cant_pages or not author_id or not isbn:
            return jsonify({'message': 'Bad request, isbn or name or cantPages or author not found'}), 400
        new_book = Book(isbn=isbn, name=name, cant_pages=cant_pages, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'book': {'id': new_book.id, 'isbn': new_book.isbn, 'name': new_book.name, 'cant_pages': new_book.cant_pages}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    

    ##nuevo

@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author_by_id(author_id):
    try:
        author = Author.query.get(author_id)
        if not author:
            return jsonify({'message': f'Author with id {author_id} not found'}), 404

        author_data = {
            'id': author.id,
            'name': author.name,
            'age': author.age,
            'books': []
        }
        for book in author.books:
            book_data = {
                'id': book.id,
                'isbn': book.isbn,
                'name': book.name,
                'cant_pages': book.cant_pages,
                'createdAt': book.created_at
            }
            author_data['books'].append(book_data)

        return jsonify({'author': author_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
##segundo nuevo
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': f'Book with id {book_id} not found'}), 404

        book_data = {
            'id': book.id,
            'isbn': book.isbn,
            'name': book.name,
            'cant_pages': book.cant_pages,
            'createdAt': book.created_at,
            'author_id': book.author_id
        }
        return jsonify({'book': book_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
##✅ 1. Endpoint para actualizar un author
@app.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    try:
        author = Author.query.get(author_id)
        if not author:
            return jsonify({'message': f'Author with id {author_id} not found'}), 404

        data = request.json
        name = data.get('name')
        age = data.get('age')

        if name:
            author.name = name
        if age:
            author.age = age

        db.session.commit()

        return jsonify({
            'author': {
                'id': author.id,
                'name': author.name,
                'age': author.age
            }
        })
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

## 2. Endpoint para actualizar un book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': f'Book with id {book_id} not found'}), 404

        data = request.json
        isbn = data.get('isbn')
        name = data.get('name')
        cant_pages = data.get('cant_pages')
        author_id = data.get('author_id')

        if isbn:
            book.isbn = isbn
        if name:
            book.name = name
        if cant_pages:
            book.cant_pages = cant_pages
        if author_id:
            book.author_id = author_id

        db.session.commit()

        return jsonify({
            'book': {
                'id': book.id,
                'isbn': book.isbn,
                'name': book.name,
                'cant_pages': book.cant_pages,
                'author_id': book.author_id
            }
        })
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

##Endpoint para eliminar un autor
@app.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    try:
        author = Author.query.get(author_id)
        if not author:
            return jsonify({'message': f'Author with id {author_id} not found'}), 404

        db.session.delete(author)
        db.session.commit()

        return jsonify({'message': f'Author with id {author_id} deleted successfully'})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

##Endpoint para eliminar un book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': f'Book with id {book_id} not found'}), 404

        db.session.delete(book)
        db.session.commit()

        return jsonify({'message': f'Book with id {book_id} deleted successfully'})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Esto crea las tablas si no existen
    app.run(port=3000, debug=True)

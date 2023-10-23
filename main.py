from bson import json_util
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from jsonschema import validate, ValidationError
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
import bcrypt
import json
import secrets

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/data"

app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
jwt = JWTManager(app)

mongo = PyMongo(app)

USER_ROLES = ['new', 'standard', 'banned', 'admin']

ALLOWED_EXTENSIONS = {'pdf', 'txt'}

with open('user-schema.json', 'r') as user_schema:
    schema = json.load(user_schema)

with open('book-schema.json', 'r') as book_schema:
    b_schema = json.load(book_schema)

with open('image-schema.json', 'r') as image_schema:
    i_schema = json.load(image_schema)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def next_book_id():
    last_book = mongo.db.books.find_one(sort=[("_id", -1)])
    if last_book is not None:
        next_id = last_book["_id"] + 1
    else:
        next_id = 1
    return next_id


def next_user_id():
    last_user = mongo.db.users.find_one(sort=[("_id", -1)])
    if last_user is not None:
        next_id = last_user["id"] + 1
    else:
        next_id = 1
    return next_id


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    fullname = data.get("fullname")
    email = data.get("email")
    password = data.get("password")

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'error': e.message}), 400

    existing_user = mongo.db.users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User with this email already registered"}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = next_user_id()

    new_user = {
        "id": user_id,
        "fullname": fullname,
        "email": email,
        "password": hashed_password,
        "role": 'new'
    }

    mongo.db.users.insert_one(new_user)

    return jsonify({"message": "User successfully registered"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = mongo.db.users.find_one({'email': email})

    if user is not None and 'password' in user:
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            access_token = create_access_token(identity=user['email'])
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user_data': {
                    'fullname': user['fullname'],
                    'email': user['email'],
                    'role': user['role']
                }
            }), 200

    return jsonify({'error': 'Invalid email or password'}), 401


@app.route('/change_user_role', methods=['POST'])
def change_user_role():
    data = request.get_json()
    email = data.get('email')
    new_role = data.get('role')

    user = mongo.db.users.find_one({'email': email})
    if user:
        mongo.db.users.update_one({'email': email}, {'$set': {'role': new_role}})
        return jsonify({'message': 'User role updated successfully'}), 200
    else:
        return jsonify({'error': 'Permission denied'}), 403


@app.route('/books', methods=['GET'])
def get_all_books():
    books = list(mongo.db.books.find({}, projection={'file': False}))

    for book in books:
        book['_id'] = str(book['_id'])

    return json_util.dumps({'books': books}), 200, {'Content-Type': 'application/json'}


@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book = mongo.db.books.find_one({"id": int(book_id)}, projection={'file': False})
    if book:
        return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404


@app.route("/add_book", methods=["POST"])
def add_book():
    data = request.form.to_dict()
    file = request.files['file']
    if file and allowed_file(file.filename):
        try:
            validate(data, b_schema)
        except ValidationError as e:
            return jsonify({'error': e.message}), 400

        book_id = mongo.db.books.count_documents({}) + 1

        book = {
            "id": book_id,
            "name": data['name'],
            "author_name": data['author_name'],
            "tag": data['tag'],
            "file": {
                "filename": request.files['file'].filename,
                "originalName": request.files['file'].filename,
                "contentType": request.files['file'].content_type,
                "data": request.files['file'].read(),
            }
        }

        mongo.db.books.insert_one(book)
        return jsonify({"message": "Book added successfully"}), 201
    else:
        return jsonify({"error": "Invalid file format"}), 400


@app.route('/books/<book_id>', methods=['PATCH'])
def update_book(book_id):
    data = request.get_json()
    book = mongo.db.books.find_one({"id": int(book_id)})
    if book:
        if "name" in data:
            book["name"] = data["name"]
        if "author_name" in data:
            book["author_name"] = data["author_name"]
        if "tag" in data:
            book["tag"] = data["tag"]

        mongo.db.books.update_one({"id": int(book_id)}, {"$set": book})
        return jsonify({"message": "Book updated successfully"}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404


@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = mongo.db.books.find_one({"id": int(book_id)})
    if book:
        mongo.db.books.delete_one({"id": int(book_id)})
        return jsonify({"message": "Book deleted successfully"}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404


if __name__ == "__main__":
    app.run(debug=True)

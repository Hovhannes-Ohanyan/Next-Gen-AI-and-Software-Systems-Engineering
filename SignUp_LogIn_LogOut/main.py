
from flask import Flask, request, jsonify, render_template
import bcrypt
import json

app = Flask(__name__)

auto_increment_id = 1


def load_users():
    try:
        with open('users.json', 'r') as users_data:
            return json.load(users_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def authorized_users():
    try:
        with open('authorized.json', 'r') as auth_file:
            return json.load(auth_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_users(users):
    with open('users.json', 'w') as users_file:
        json.dump(users, users_file)


def save_authorized_users(users):
    with open('authorized.json', 'w') as auth_file:
        json.dump(users, auth_file)


def hash_password(password):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')
    except Exception as e:
        print(f"Error hashing password: {str(e)}")
        return None


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    global auto_increment_id
    users_information = load_users()

    if request.method == "POST":
        data = request.form
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not name or not email or not password:
            return jsonify({"message": "Name, email, and password are required"}), 400

        for user in users_information:
            if user["email"] == email:
                return jsonify({"status_code": 409, "message": "Email already used"})

        h_password = hash_password(password)
        if h_password is None:
            return jsonify({"message": "Error hashing password"}), 500

        new_user = {"id": auto_increment_id, "name": name, "email": email, "password": h_password}
        auto_increment_id += 1
        users_information.append(new_user)
        save_users(users_information)

        return render_template("signup.html")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        for user in load_users():
            if user['email'] == email and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                save_authorized_users(user)
                return jsonify(
                    {'message': 'Login successful',
                     'user': {'id': user['id'], 'name': user['name'], 'email': email}}), 200

        return jsonify({'message': 'Unauthorized'}), 401

    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        data = request.form
        email = data.get('email')

        try:
            authorized_users_data = json.loads(open('authorized.json', 'r').read())
        except FileNotFoundError:
            authorized_users_data = []

        if not authorized_users_data:
            return jsonify({'message': 'No authorized users found'}), 404

        updated_authorized_users = []

        for user in authorized_users_data:
            if isinstance(user, dict) and user.get('email') == email:
                continue
            updated_authorized_users.append(user)

        with open('authorized.json', 'w') as auth_file:
            auth_file.write(json.dumps(updated_authorized_users))

        return jsonify({'message': 'Logout successful'}), 200

    return render_template("logout.html")


if __name__ == "__main__":
    app.run(debug=True)

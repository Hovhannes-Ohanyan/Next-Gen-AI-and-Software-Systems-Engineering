from flask import Flask, render_template, request, redirect, url_for
from database import (get_db, close_db, insert_product, update_product, delete_product, insert_category,
                      update_category, delete_category, find_user_by_username, insert_user)

import bcrypt

app = Flask(__name__)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return "Please provide a username and password"
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        close_db(conn)

        if existing_user:
            return "Username is already taken. Please choose another one"

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        insert_user(username, hashed_password)

        return "Registration successful! You can now log in."

    return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = find_user_by_username(username)

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
            return "Login successful!"
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')


@app.route('/products')
def list_products():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, stock, category_id FROM products")
        products = cursor.fetchall()
        close_db(conn)
        print(products)
        return render_template('products.html', products=products)
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/products/add", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        category_id = request.form.get("category_id")

        if not name or not price or not stock or not category_id:
            return "please provide all product details"

        insert_product(name, price, stock, category_id)
        return redirect(url_for("list_products"))
    return render_template("add_product.html")


@app.route('/products/edit/<int:product_id>', methods=["GET", "POST"])
def edit_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, stock, category_id FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    close_db(conn)

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        category_id = request.form.get("category_id")

        if not name or not price or not stock or not category_id:
            return "Please provide all product details"

        update_product(product_id, name, price, stock, category_id)
        return redirect(url_for('list_products'))

    return render_template('edit_product.html', product=product)


@app.route('/products/delete/<int:product_id>', methods=["POST"])
def delete_product(product_id):
    delete_product(product_id)
    return redirect(url_for('list_products'))


@app.route('/categories')
def list_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    close_db(conn)
    return render_template('categories.html', categories=categories)


@app.route('/categories/add', methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return "Please provide a category name"
        insert_category(name)
        return redirect(url_for('list_categories'))
    return render_template('add_category.html')


@app.route('/categories/edit/<int:category_id>', methods=["GET", "POST"])
def edit_category(category_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories WHERE id = ?", (category_id,))
    category = cursor.fetchone()
    close_db(conn)

    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return "Please provide a category name"
        update_category(category_id, name)
        return redirect(url_for('list_categories'))
    return render_template('edit_category.html', category=category)


@app.route('/categories/delete/<int:category_id>', methods=["DELETE"])
def delete_category(category_id):
    delete_category(category_id)
    return redirect(url_for('list_categories'))


if __name__ == "__main__":
    app.run(debug=True)

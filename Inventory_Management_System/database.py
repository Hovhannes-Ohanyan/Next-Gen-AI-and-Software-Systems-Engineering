import sqlite3

DATABASE = 'inventory.db'


def get_db():
    return sqlite3.connect(DATABASE)


def close_db(conn):
    conn.close()


def insert_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        close_db(conn)


def find_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    close_db(conn)
    return user


def insert_product(name, price, stock, category_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, price, stock, category_id) VALUES (?, ?, ?, ?)",
                       (name, price, stock, category_id))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        close_db(conn)


def update_product(product_id, name, price, stock, category_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE products SET name = ?, price = ?, stock = ?, category_id = ? WHERE id = ?",
                       (name, price, stock, category_id, product_id))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        close_db(conn)


def delete_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        close_db(conn)


def insert_category(name):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        close_db(conn)


def update_category(category_id, name):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (name, category_id))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        close_db(conn)


def delete_category(category_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        close_db(conn)

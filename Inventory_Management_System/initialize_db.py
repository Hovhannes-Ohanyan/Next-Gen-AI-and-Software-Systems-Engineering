import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

with open('schema.sql', 'r') as schema_file:
    schema_sql = schema_file.read()
    cursor.executescript(schema_sql)

conn.commit()
conn.close()

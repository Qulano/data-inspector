import sqlite3
from rich import print
def read_dataset(file_path):
    dataset = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            dataset.append(line.strip().split(","))
    return dataset

def transform(raw_data):
    header = raw_data[0]
    rows = raw_data[1:]
    seen_ids = []
    clean_rows = []
    for index, row in enumerate(rows, start =1):
        if len(row) == len(header) and "" not in row and row[0] not in seen_ids and row[1].isalpha() and row[2].isdigit() and "@" in row[3] and "." in row[3]:
            clean_rows.append((int(row[0]), row[1], int(row[2]), row[3]))
            seen_ids.append(row[0])
    return clean_rows

def load_to_db(clean_records, db_name = "warehouse.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS clients")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER,
            name TEXT,
            age INTEGER,
            email TEXT
        ) 
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    products = [
        ("Ноутбук", 9000, 1),
        ("Мышка", 3000, 1),
        ("Монитор", 25000, 10)
    ]
    cursor.executemany('''
        INSERT INTO orders (item, price, client_id)
        VALUES (?, ?, ?)
    ''', products)

    cursor.executemany('''
        INSERT INTO clients (id, name, age, email)
        VALUES (?, ?, ?, ?)
    ''', clean_records)
    connection.commit()
    connection.close()
    print(f"[bold green]Успешно загружено в базу: {len(clean_records)} записей![/bold green]")
    
raw_records = read_dataset("dirty_data.csv")
clean = transform(raw_records)
load_to_db(clean)

conn = sqlite3.connect("warehouse.db")
cur = conn.cursor()

cur.execute("SELECT * FROM  clients")
for row in cur.fetchall():
    print(row)

cur.execute("SELECT clients.name, orders.item, orders.price FROM clients JOIN orders ON clients.id = orders.client_id")
report_data = cur.fetchall()
for row in report_data:
    print(row)
    
cur.execute("SELECT clients.name, COUNT(orders.item), SUM(orders.price) FROM clients JOIN orders ON clients.id = orders.client_id GROUP BY clients.name")
analytics_data = cur.fetchall()
for row in analytics_data:
    print(row)


conn.close()





    
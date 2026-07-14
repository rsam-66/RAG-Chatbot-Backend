import sqlite3
import os

db_path = os.path.join(os.environ['LOCALAPPDATA'], 'Ollama', 'db.sqlite')
print(f"DB path: {db_path}")
print(f"DB exists: {os.path.exists(db_path)}")
print(f"DB size: {os.path.getsize(db_path)} bytes")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# List tables
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f"\nTables: {[t[0] for t in tables]}")

# Check each table
for table in tables:
    name = table[0]
    rows = cur.execute(f"SELECT * FROM [{name}] LIMIT 10").fetchall()
    cols = [desc[0] for desc in cur.description]
    print(f"\n--- {name} ({len(rows)} rows) ---")
    print(f"Columns: {cols}")
    for row in rows:
        print(f"  {row}")

conn.close()

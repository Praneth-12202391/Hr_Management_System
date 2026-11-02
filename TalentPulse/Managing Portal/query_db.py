import sys
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "backend" / "data" / "talentpulse.db"

def run_query(sql: str):
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        return
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        if cursor.description:
            cols = [d[0] for d in cursor.description]
            rows = cursor.fetchall()
            print(" | ".join(cols))
            print("-" * 80)
            for r in rows:
                print(" | ".join(str(v) for v in r))
            print(f"\n({len(rows)} rows)")
        else:
            conn.commit()
            print("Query executed successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        run_query(query)
    else:
        print("Usage: python query_db.py \"SELECT * FROM employees LIMIT 5\"")
        print("\nDefault: Listing all tables:")
        run_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")

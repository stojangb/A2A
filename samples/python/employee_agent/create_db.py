import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("employees.db")

EMPLOYEES = [
    ("Ana", "España", "Ingeniera"),
    ("Luis", "España", "Gerente"),
    ("Marie", "Francia", "Analista"),
    ("Pierre", "Francia", "Desarrollador"),
]


def create_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            pais TEXT,
            cargo TEXT
        )
        """
    )
    cur.execute("SELECT COUNT(*) FROM employees")
    count = cur.fetchone()[0]
    if count == 0:
        cur.executemany(
            "INSERT INTO employees (nombre, pais, cargo) VALUES (?, ?, ?)", EMPLOYEES
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()

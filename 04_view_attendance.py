import sqlite3
from tabulate import tabulate


conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        status TEXT
    )
""")
conn.commit()


cursor.execute("SELECT * FROM attendance ORDER BY date DESC, time DESC")
rows = cursor.fetchall()


if not rows:
    print("⚠️  No attendance records found.")
else:
    
    try:
        from tabulate import tabulate
        print(tabulate(rows, headers=["ID", "Name", "Roll No", "Date", "Time", "Status"], tablefmt="fancy_grid"))
    except:
        
        print("ID | Name | Roll No | Date | Time | Status")
        print("-" * 60)
        for row in rows:
            print(row)

conn.close()

import sqlite3
import pandas as pd

conn = sqlite3.connect('attendance.db')
df = pd.read_sql_query("SELECT * FROM attendance", conn)
df.to_csv("attendance_report.csv", index=False)
conn.close()

print("✅ Attendance exported successfully as attendance_report.csv")

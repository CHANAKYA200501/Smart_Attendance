import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd

def show_records():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute("SELECT * FROM attendance ORDER BY date DESC, time DESC")
    rows = c.fetchall()
    conn.close()
    text_box.delete('1.0', tk.END)
    if rows:
        for row in rows:
            text_box.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} {row[3]}\n")
    else:
        text_box.insert(tk.END, "No attendance records found.")

def export_csv():
    conn = sqlite3.connect('attendance.db')
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    df.to_csv("attendance_report.csv", index=False)
    conn.close()
    messagebox.showinfo("Export", "Attendance exported successfully!")

root = tk.Tk()
root.title("Smart Attendance Viewer")
root.geometry("600x400")

tk.Button(root, text="View Attendance", command=show_records, bg="lightblue").pack(pady=10)
tk.Button(root, text="Export to CSV", command=export_csv, bg="lightgreen").pack(pady=10)

text_box = tk.Text(root, height=15, width=70)
text_box.pack(pady=10)

root.mainloop()

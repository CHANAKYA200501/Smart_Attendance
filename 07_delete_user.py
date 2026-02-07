import os
import shutil
import sqlite3

def delete_user(username):
   
    dataset_path = os.path.join("dataset", username)
    
    if os.path.exists(dataset_path):
        shutil.rmtree(dataset_path)
        print(f"🗑️ Deleted face dataset for '{username}'")
    else:
        print(f"⚠️ No dataset found for '{username}'")

    
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance WHERE name = ?", (username,))
    conn.commit()
    conn.close()
    print(f"🗑️ Deleted all attendance records for '{username}'")

    print(f"✅ Successfully removed user '{username}'")


if __name__ == "__main__":
    user_to_delete = input("Enter the username to delete: ")
    delete_user(user_to_delete)

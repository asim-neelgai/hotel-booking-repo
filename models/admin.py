import pandas as pd
import os
from models.user import User

class Admin(User):
    def __init__(self, username, password, email):
        super().__init__(username, password, email, is_admin=True)

    def add_room(self, room_id, room_type, price):
        rooms_file = os.path.join('data', 'rooms.xlsx')
        if os.path.exists(rooms_file):
            df = pd.read_excel(rooms_file)
        else:
            df = pd.DataFrame(columns=['room_id', 'room_type', 'price'])

        room_id = str(room_id)    

        if room_id in df['room_id'].values:
            print("Room ID already exists.")
            return

        new_room = {
            'room_id': room_id,
            'room_type': room_type,
            'price': price
        }
        df.loc[len(df)] = new_room
        df.to_excel(rooms_file, index=False)
        print(f"Room {room_id} added successfully.")

    def remove_room(self, room_id):
       rooms_file = os.path.join('data', 'rooms.xlsx')
       if not os.path.exists(rooms_file):
        print("No rooms file found.")
        return

       room_id = str(room_id).strip()
       df = pd.read_excel(rooms_file, dtype={'room_id': str})
       df['room_id'] = df['room_id'].astype(str).str.strip()

       new_df = df[df['room_id'] != room_id]
       new_df.to_excel(rooms_file, index=False)
       print(f"Room {room_id} removed successfully.")



    def modify_room(self, room_id, new_type=None, new_price=None):
        rooms_file = os.path.join('data', 'rooms.xlsx')
        if not os.path.exists(rooms_file):
            print("No rooms file found.")
            return
        
        room_id = str(room_id)
        df = pd.read_excel(rooms_file)
        idx = df.index[df['room_id'] == room_id]

        if len(idx) == 0:
            print("Room not found.")
            return

        if new_type:
            df.at[idx[0], 'room_type'] = new_type
        if new_price is not None:
            df.at[idx[0], 'price'] = new_price

        df.to_excel(rooms_file, index=False)
        print(f"Room {room_id} modified successfully.")

    def view_all_bookings(self):
        from pandas import read_excel
        import os
        import tkinter as tk
        from tkinter import messagebox

        bookings_file = os.path.join('data', 'bookings.xlsx')
        if not os.path.exists(bookings_file):
            messagebox.showinfo("No Bookings", "No bookings found.")
            return

        df = read_excel(bookings_file)
        text = df.to_string(index=False)

        # Create a new window
        win = tk.Toplevel()
        win.title("All Bookings")
        win.geometry("400x300")
        win.configure(padx=20, pady=20)

        text_widget = tk.Text(win, wrap="none", font=("Arial", 12))
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        text_widget.pack(expand=True, fill="both")

        df = pd.read_excel(bookings_file)
        print("All Bookings:")
        print(df)

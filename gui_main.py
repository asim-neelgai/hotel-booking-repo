import os
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import User
from models.admin import Admin
from models.booking import Booking

def main_window():
    """ The initial window with 'Login' and 'Exit' buttons. """
    root = tk.Tk()
    root.title("Western Hotel Booking System")

    # Set a default size and padding
    root.geometry("400x250")
    root.configure(padx=20, pady=20)

    label = tk.Label(root, text="Welcome to Western Hotel Booking System", 
                     font=("Arial", 16, "bold"))
    label.pack(pady=(0, 20))

    login_button = tk.Button(root, text="Login", width=12, 
                             font=("Arial", 12),
                             command=lambda: open_login_window(root))
    login_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", width=12, 
                            font=("Arial", 12),
                            command=root.quit)
    exit_button.pack(pady=5)

    root.mainloop()

def open_login_window(parent):
    """ Opens a separate window to input username and password. """
    login_window = tk.Toplevel(parent)
    login_window.title("Login")
    login_window.geometry("320x200")
    login_window.resizable(False, False)

    frame = ttk.Frame(login_window, padding="20 20 20 20")
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Username:", style="TLabel").grid(row=0, column=0, pady=5, sticky="e")
    username_entry = ttk.Entry(frame, width=20)
    username_entry.grid(row=0, column=1, pady=5, sticky="w")

    ttk.Label(frame, text="Password:", style="TLabel").grid(row=1, column=0, pady=5, sticky="e")
    password_entry = ttk.Entry(frame, width=20, show='*')
    password_entry.grid(row=1, column=1, pady=5, sticky="w")

    login_btn = ttk.Button(frame, text="Login",
                           command=lambda: handle_login(username_entry.get(),
                                                        password_entry.get(),
                                                        login_window))
    login_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Let columns expand proportionally
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)

def handle_login(username, password, login_window):
    user_obj = User.login(username, password)
    if user_obj:
        login_window.destroy()
        if user_obj.is_admin:
            # Manually create an Admin object from the user's credentials
            admin_obj = Admin(user_obj.username, user_obj.password, user_obj.email)
            messagebox.showinfo("Login Success", "Welcome Admin!")
            open_admin_dashboard(admin_obj)
        else:
            messagebox.showinfo("Login Success", f"Welcome, {user_obj.username}!")
            open_user_dashboard(user_obj)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

def open_admin_dashboard(admin_user):
    """ A new window for admin actions. """
    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")

    admin_window.geometry("300x300")
    admin_window.configure(padx=20, pady=20)

    tk.Button(admin_window, text="Add Room", width=15, 
              font=("Arial", 12),
              command=lambda: add_room_ui(admin_window, admin_user)).pack(pady=5)

    tk.Button(admin_window, text="Remove Room", width=15, 
              font=("Arial", 12),
              command=lambda: remove_room_ui(admin_window, admin_user)).pack(pady=5)

    tk.Button(admin_window, text="Modify Room", width=15,
              font=("Arial", 12),
              command=lambda: modify_room_ui(admin_window, admin_user)).pack(pady=5)

    tk.Button(admin_window, text="View Bookings", width=15,
              font=("Arial", 12),
              command=lambda: admin_user.view_all_bookings()).pack(pady=5)

    tk.Button(admin_window, text="Logout", width=15, 
              font=("Arial", 12),
              command=admin_window.destroy).pack(pady=20)

    admin_window.mainloop()

def add_room_ui(parent, admin_user):
    """ Simple pop-up window to add a new room. """
    room_win = tk.Toplevel(parent)
    room_win.title("Add Room")

    room_win.geometry("300x200")
    room_win.configure(padx=20, pady=20)

    tk.Label(room_win, text="Room ID:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    room_id_entry = tk.Entry(room_win, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(room_win, text="Room Type:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    room_type_entry = tk.Entry(room_win, font=("Arial", 12))
    room_type_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(room_win, text="Price:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    price_entry = tk.Entry(room_win, font=("Arial", 12))
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    def on_add():
        room_id = room_id_entry.get().strip()
        room_type = room_type_entry.get().strip()
        try:
            price = float(price_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid price.")
            return

        admin_user.add_room(room_id, room_type, price)
        messagebox.showinfo("Success", f"Room {room_id} added.")
        room_win.destroy()

    tk.Button(room_win, text="Add", font=("Arial", 12), command=on_add).grid(row=3, column=0, columnspan=2, pady=10)

def remove_room_ui(parent, admin_user):
    """ Simple pop-up window to remove a room. """
    remove_win = tk.Toplevel(parent)
    remove_win.title("Remove Room")

    remove_win.geometry("300x150")
    remove_win.configure(padx=20, pady=20)

    tk.Label(remove_win, text="Room ID:", font=("Arial", 12)).pack(pady=(0, 5))
    room_id_entry = tk.Entry(remove_win, font=("Arial", 12))
    room_id_entry.pack(pady=5)

    def on_remove():
        r_id = room_id_entry.get().strip()
        admin_user.remove_room(r_id)
        messagebox.showinfo("Success", f"Room {r_id} removed.")
        remove_win.destroy()

    tk.Button(remove_win, text="Remove", font=("Arial", 12), command=on_remove).pack(pady=5)

def modify_room_ui(parent, admin_user):
    """ Simple pop-up to modify an existing room's type/price. """
    mod_win = tk.Toplevel(parent)
    mod_win.title("Modify Room")

    mod_win.geometry("300x200")
    mod_win.configure(padx=20, pady=20)

    tk.Label(mod_win, text="Room ID:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    room_id_entry = tk.Entry(mod_win, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(mod_win, text="New Type:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    new_type_entry = tk.Entry(mod_win, font=("Arial", 12))
    new_type_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(mod_win, text="New Price:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    new_price_entry = tk.Entry(mod_win, font=("Arial", 12))
    new_price_entry.grid(row=2, column=1, padx=5, pady=5)

    def on_modify():
        r_id = room_id_entry.get().strip()
        new_type = new_type_entry.get().strip() or None
        price_str = new_price_entry.get().strip()
        new_price = float(price_str) if price_str else None

        admin_user.modify_room(r_id, new_type, new_price)
        messagebox.showinfo("Success", f"Room {r_id} modified.")
        mod_win.destroy()

    tk.Button(mod_win, text="Modify", font=("Arial", 12), command=on_modify).grid(row=3, column=0, columnspan=2, pady=10)

def open_user_dashboard(user_obj):
    """ A new window for normal user actions: view rooms, book a room, etc. """
    user_window = tk.Tk()
    user_window.title("User Dashboard")

    user_window.geometry("300x250")
    user_window.configure(padx=20, pady=20)

    tk.Button(user_window, text="View Rooms", width=15,
              font=("Arial", 12),
              command=lambda: view_rooms_ui(user_window)).pack(pady=10)

    tk.Button(user_window, text="Book a Room", width=15,
              font=("Arial", 12),
              command=lambda: book_room_ui(user_window, user_obj)).pack(pady=10)

    tk.Button(user_window, text="Logout", width=15,
              font=("Arial", 12),
              command=user_window.destroy).pack(pady=20)

    user_window.mainloop()

def view_rooms_ui(parent):
    """ Display the rooms in a simple text box or labels. """
    # For example, load the 'rooms.xlsx' via Admin or direct Pandas
    from pandas import read_excel
    import os

    rooms_file = os.path.join('data', 'rooms.xlsx')
    text = ""
    if not os.path.exists(rooms_file):
        text = "No rooms found."
    else:
        df = read_excel(rooms_file)
        text = df.to_string(index=False)

    room_win = tk.Toplevel(parent)
    room_win.title("Available Rooms")

    room_win.geometry("400x300")
    room_win.configure(padx=20, pady=20)

    text_widget = tk.Text(room_win, wrap="none", font=("Arial", 12))
    text_widget.insert("1.0", text)
    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both")

def book_room_ui(parent, user_obj):
    """ Pop-up for booking a room. """
    book_win = tk.Toplevel(parent)
    book_win.title("Book a Room")

    book_win.geometry("320x200")
    book_win.configure(padx=20, pady=20)

    tk.Label(book_win, text="Room ID:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    room_id_entry = tk.Entry(book_win, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(book_win, text="Check-in (YYYY-MM-DD):", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    checkin_entry = tk.Entry(book_win, font=("Arial", 12))
    checkin_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(book_win, text="Check-out (YYYY-MM-DD):", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    checkout_entry = tk.Entry(book_win, font=("Arial", 12))
    checkout_entry.grid(row=2, column=1, padx=5, pady=5)

    def on_book():
        room_id = room_id_entry.get().strip()
        ci = checkin_entry.get().strip()
        co = checkout_entry.get().strip()

        if is_room_available(room_id, ci, co):
            b = Booking(user_obj.username, room_id, ci, co)
            b.save_booking()
            messagebox.showinfo("Success", "Booking saved.")
            book_win.destroy()
        else:
            messagebox.showerror("Error", "Room not available for these dates.")

    tk.Button(book_win, text="Book", font=("Arial", 12), 
              command=on_book).grid(row=3, column=0, columnspan=2, pady=10)

def is_room_available(room_id, check_in, check_out):
    """ Reuse your existing logic or replicate it here. """
    import pandas as pd
    import os

    bookings_file = os.path.join('data', 'bookings.xlsx')
    if not os.path.exists(bookings_file):
        return True

    df = pd.read_excel(bookings_file)
    same_room_bookings = df[df['room_id'] == room_id]

    new_check_in = pd.to_datetime(check_in)
    new_check_out = pd.to_datetime(check_out)

    for _, row in same_room_bookings.iterrows():
        existing_check_in = pd.to_datetime(row['check_in'])
        existing_check_out = pd.to_datetime(row['check_out'])
        # If there's an overlap, return False
        if not (new_check_out <= existing_check_in or new_check_in >= existing_check_out):
            return False

    return True

if __name__ == "__main__":
    # Ensure data folder exists and create admin if needed
    os.makedirs('data', exist_ok=True)
    main_window()

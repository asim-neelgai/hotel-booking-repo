import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from models.user import User
from models.admin import Admin
from models.booking import Booking

def main_window():
    """ The initial window with 'Login', 'Register', and 'Exit' buttons. """
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

    # ----------- NEW: Register Button -----------
    register_button = tk.Button(root, text="Register", width=12, 
                                font=("Arial", 12),
                                command=lambda: open_register_window(root))
    register_button.pack(pady=5)
    # --------------------------------------------

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

# ----------- NEW: Register Window -----------
def open_register_window(parent):
    """ Opens a separate window for user registration. """
    reg_window = tk.Toplevel(parent)
    reg_window.title("Register")
    reg_window.geometry("350x250")
    reg_window.resizable(False, False)

    frame = ttk.Frame(reg_window, padding="20 20 20 20")
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Username:").grid(row=0, column=0, pady=5, sticky="e")
    username_entry = ttk.Entry(frame, width=25)
    username_entry.grid(row=0, column=1, pady=5, sticky="w")

    ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5, sticky="e")
    password_entry = ttk.Entry(frame, width=25, show='*')
    password_entry.grid(row=1, column=1, pady=5, sticky="w")

    ttk.Label(frame, text="Email:").grid(row=2, column=0, pady=5, sticky="e")
    email_entry = ttk.Entry(frame, width=25)
    email_entry.grid(row=2, column=1, pady=5, sticky="w")

    register_btn = ttk.Button(frame, text="Register", 
                    command=lambda: handle_register(username_entry.get(),
                                                    password_entry.get(),
                                                    email_entry.get(),
                                                    reg_window))
    register_btn.grid(row=3, column=0, columnspan=2, pady=15)

    # Let columns expand proportionally
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)


import re

def handle_register(username, password, email, reg_window):
    """ Handles user registration via user.py -> User.register """
    # Basic input validation
    if not username or not password or not email:
        messagebox.showerror("Error", "All fields are required.")
        return
    
    # Optional email format check (very basic regex for demonstration)
    email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
    if not re.match(email_pattern, email):
        messagebox.showerror("Error", "Please enter a valid email address.")
        return

    new_user = User.register(username, password, email)
    if new_user is None:
        # Registration failed (username taken or other reason).
        messagebox.showerror("Error", "Registration failed. Username may be taken.")
    else:
        # Registration succeeded
        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        reg_window.destroy()

# -----------------------------------------------------

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
    """ Pop-up window to add a new room (with a dropdown for room type). """
    room_win = tk.Toplevel(parent)
    room_win.title("Add Room")

    # Increase window size & padding
    room_win.geometry("400x250")
    room_win.configure(padx=20, pady=20)

    # Create a Frame for the form
    form_frame = tk.Frame(room_win)
    form_frame.pack(expand=True, fill="both")

    tk.Label(form_frame, text="Room ID:", font=("Arial", 12)).grid(
        row=0, column=0, padx=5, pady=5, sticky="e"
    )
    room_id_entry = tk.Entry(form_frame, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="Room Type:", font=("Arial", 12)).grid(
        row=1, column=0, padx=5, pady=5, sticky="e"
    )

    # Use a Combobox for the room type
    room_types = ["Single", "Double", "Suite"]
    room_type_var = tk.StringVar(value=room_types[0])  # default to "Single"
    
    # Note: If you want them to have to select something,
    # you could do: tk.StringVar(value="Select Type")
    # and then check for that in on_add().

    room_type_combo = ttk.Combobox(
        form_frame, textvariable=room_type_var,
        values=room_types, state="readonly",
        font=("Arial", 12)
    )
    room_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="Price:", font=("Arial", 12)).grid(
        row=2, column=0, padx=5, pady=5, sticky="e"
    )
    price_entry = tk.Entry(form_frame, font=("Arial", 12))
    price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def on_add():
        room_id = room_id_entry.get().strip()
        # Now grab the selected room type from the Combobox
        room_type = room_type_var.get().strip()
        try:
            price = float(price_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid price.")
            return

        admin_user.add_room(room_id, room_type, price)
        messagebox.showinfo("Success", f"Room {room_id} added.")
        room_win.destroy()

    # "Add" button on a new row
    tk.Button(
        form_frame, text="Add", font=("Arial", 12), command=on_add
    ).grid(row=3, column=0, columnspan=2, pady=15)

    # Let columns expand proportionally
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)

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
    """ Pop-up to modify an existing room's type/price (with a dropdown for new type). """
    mod_win = tk.Toplevel(parent)
    mod_win.title("Modify Room")

    mod_win.geometry("400x250")
    mod_win.configure(padx=20, pady=20)

    form_frame = tk.Frame(mod_win)
    form_frame.pack(expand=True, fill="both")

    tk.Label(form_frame, text="Room ID:", font=("Arial", 12)).grid(
        row=0, column=0, padx=5, pady=5, sticky="e"
    )
    room_id_entry = tk.Entry(form_frame, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="New Type:", font=("Arial", 12)).grid(
        row=1, column=0, padx=5, pady=5, sticky="e"
    )

    # Combobox for new room type
    room_types = ["Single", "Double", "Suite"]
    new_type_var = tk.StringVar(value="")  # can be empty if user only wants to change price
    new_type_combo = ttk.Combobox(
        form_frame, textvariable=new_type_var,
        values=room_types, state="readonly",
        font=("Arial", 12)
    )
    new_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="New Price:", font=("Arial", 12)).grid(
        row=2, column=0, padx=5, pady=5, sticky="e"
    )
    new_price_entry = tk.Entry(form_frame, font=("Arial", 12))
    new_price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def on_modify():
        r_id = room_id_entry.get().strip()

        # If user leaves "New Type" empty, we won't change it
        # (like your current code: `new_type = new_type_entry.get().strip() or None`)
        chosen_type = new_type_var.get().strip()
        new_type = chosen_type if chosen_type else None

        price_str = new_price_entry.get().strip()
        new_price = float(price_str) if price_str else None

        admin_user.modify_room(r_id, new_type, new_price)
        messagebox.showinfo("Success", f"Room {r_id} modified.")
        mod_win.destroy()

    tk.Button(form_frame, text="Modify", font=("Arial", 12), command=on_modify).grid(
        row=3, column=0, columnspan=2, pady=15
    )

    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)

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
    """ Pop-up for booking a room with more spacious layout. """
    book_win = tk.Toplevel(parent)
    book_win.title("Book a Room")

    # Increase window size a bit and add padding around edges
    book_win.geometry("400x250")
    book_win.configure(padx=20, pady=20)

    # Create a Frame to hold the form controls
    form_frame = tk.Frame(book_win)
    form_frame.pack(expand=True, fill="both")

    # Labels and entries in a grid
    tk.Label(form_frame, text="Room ID:", font=("Arial", 12)).grid(row=0, column=0, 
                                                                   padx=5, pady=5, 
                                                                   sticky="e")
    room_id_entry = tk.Entry(form_frame, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="Check-in (YYYY-MM-DD):", font=("Arial", 12)).grid(row=1, column=0, 
                                                                                padx=5, pady=5, 
                                                                                sticky="e")
    checkin_entry = tk.Entry(form_frame, font=("Arial", 12))
    checkin_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="Check-out (YYYY-MM-DD):", font=("Arial", 12)).grid(row=2, column=0, 
                                                                                 padx=5, pady=5, 
                                                                                 sticky="e")
    checkout_entry = tk.Entry(form_frame, font=("Arial", 12))
    checkout_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

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

    # Place the "Book" button on its own row
    tk.Button(form_frame, text="Book", font=("Arial", 12), command=on_book).grid(row=3, column=0, 
                                                                                columnspan=2, 
                                                                                pady=15)

    # Let columns expand proportionally
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)


def is_room_available(room_id, check_in, check_out):
    """ Checking for room availability by scanning the bookings file. """
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
    os.makedirs('data', exist_ok=True)
    main_window()

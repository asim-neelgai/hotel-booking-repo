import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from models.user import User
from models.admin import Admin
from models.booking import Booking
from tkcalendar import DateEntry
from datetime import timedelta
import re

def launch_main_interface():
    root = tk.Tk()
    root.title("Western Hotel Booking System")
    root.geometry("400x250")
    root.configure(padx=20, pady=20, bg="lightgrey")

    style = ttk.Style(root)
    style.configure("TFrame", background="lightgrey")
    style.configure("TLabel", background="lightgrey")

    label = tk.Label(root, text="Welcome to Western Hotel Booking System", 
                     font=("Arial", 16, "bold"),
                     bg="lightgrey")
    label.pack(pady=(0, 20))

    login_button = tk.Button(root, text="Sign In", width=12, font=("Arial", 12),
                             command=lambda: show_login_popup(root), bg="lightgrey")
    login_button.pack(pady=5)

    register_button = tk.Button(root, text="Sign Up", width=12, font=("Arial", 12),
                                command=lambda: show_register_popup(root), bg="lightgrey")
    register_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", width=12, font=("Arial", 12),
                            command=root.quit, bg="lightgrey")
    exit_button.pack(pady=5)

    root.mainloop()

def show_login_popup(parent):
    login_window = tk.Toplevel(parent)
    login_window.title("Login")
    login_window.geometry("320x200")
    login_window.resizable(False, False)
    login_window.configure(bg="lightgrey")

    frame = ttk.Frame(login_window, padding="20 20 20 20")
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Username:").grid(row=0, column=0, pady=5, sticky="e")
    username_entry = ttk.Entry(frame, width=20)
    username_entry.grid(row=0, column=1, pady=5, sticky="w")

    ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5, sticky="e")
    password_entry = ttk.Entry(frame, width=20, show='*')
    password_entry.grid(row=1, column=1, pady=5, sticky="w")

    login_btn = ttk.Button(frame, text="Sign In",
                           command=lambda: process_login(username_entry.get(),
                                                         password_entry.get(),
                                                         login_window))
    login_btn.grid(row=2, column=0, columnspan=2, pady=10)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)

def show_register_popup(parent):
    reg_window = tk.Toplevel(parent)
    reg_window.title("Register")
    reg_window.geometry("350x250")
    reg_window.resizable(False, False)
    reg_window.configure(bg="lightgrey")

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

    register_btn = ttk.Button(frame, text="Sign Up", 
                              command=lambda: process_registration(username_entry.get(),
                                                                   password_entry.get(),
                                                                   email_entry.get(),
                                                                   reg_window))
    register_btn.grid(row=3, column=0, columnspan=2, pady=15)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)

def process_registration(username, password, email, reg_window):
    if not username or not password or not email:
        messagebox.showerror("Error", "Please provide a username, password, and email.")
        return

    email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
    if not re.match(email_pattern, email):
        messagebox.showerror("Error", "The email address format is invalid. Please re-enter.")
        return

    new_user = User.register(username, password, email)
    if new_user is None:
        messagebox.showerror("Registration Unsuccessful", 
                             "Registration failed. This username might already be in use. Please choose another.")
    else:
        messagebox.showinfo("Registration Complete", 
                            "Your account has been created! Please log in using your new credentials.")
        reg_window.destroy()

def process_login(username, password, login_window):
    user_obj = User.login(username, password)
    if user_obj:
        login_window.destroy()
        if user_obj.is_admin:
            admin_obj = Admin(user_obj.username, user_obj.password, user_obj.email)
            messagebox.showinfo("Login Successful", "Welcome, esteemed Admin!")
            display_admin_dashboard(admin_obj)
        else:
            messagebox.showinfo("Login Successful", f"Welcome {user_obj.username}, enjoy your stay!")
            display_user_dashboard(user_obj)
    else:
        messagebox.showerror("Login Failed", 
                             "Login unsuccessful. Please check your username and password, then try again.")

def display_admin_dashboard(admin_user):
    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("300x300")
    admin_window.configure(padx=20, pady=20, bg="lightgrey")

    tk.Button(admin_window, text="Add Room", width=15, font=("Arial", 12),
              command=lambda: add_room_popup(admin_window, admin_user), bg="lightgrey").pack(pady=5)

    tk.Button(admin_window, text="Delete Room", width=15, font=("Arial", 12),
              command=lambda: remove_room_popup(admin_window, admin_user), bg="lightgrey").pack(pady=5)

    tk.Button(admin_window, text="Update Room", width=15, font=("Arial", 12),
              command=lambda: modify_room_popup(admin_window, admin_user), bg="lightgrey").pack(pady=5)

    tk.Button(admin_window, text="Show Bookings", width=15, font=("Arial", 12),
              command=lambda: admin_user.view_all_bookings(), bg="lightgrey").pack(pady=5)

    tk.Button(admin_window, text="Sign Out", width=15, font=("Arial", 12),
              command=admin_window.destroy, bg="lightgrey").pack(pady=20)

def add_room_popup(parent, admin_user):
    room_win = tk.Toplevel(parent)
    room_win.title("Add Room")
    room_win.geometry("400x250")
    room_win.configure(padx=20, pady=20, bg="lightgrey")
    form_frame = tk.Frame(room_win, bg="lightgrey")
    form_frame.pack(expand=True, fill="both")

    tk.Label(form_frame, text="Room ID:", font=("Arial", 12), bg="lightgrey").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    room_id_entry = tk.Entry(form_frame, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="Room Type:", font=("Arial", 12), bg="lightgrey").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    room_types = ["Single", "Double", "Suite"]
    room_type_var = tk.StringVar(value=room_types[0])
    room_type_combo = ttk.Combobox(form_frame, textvariable=room_type_var, values=room_types, state="readonly", font=("Arial", 12))
    room_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="Price:", font=("Arial", 12), bg="lightgrey").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    price_entry = tk.Entry(form_frame, font=("Arial", 12))
    price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def on_add():
        room_id = room_id_entry.get().strip()
        room_type = room_type_var.get().strip()
        try:
            price = float(price_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "The price entered is not valid. Please enter a number.")
            return

        admin_user.add_room(room_id, room_type, price)
        messagebox.showinfo("Room Added", f"Room '{room_id}' has been successfully added!")
        room_win.destroy()

    tk.Button(form_frame, text="Add Room", font=("Arial", 12), command=on_add, bg="lightgrey").grid(row=3, column=0, columnspan=2, pady=15)
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)

def remove_room_popup(parent, admin_user):
    remove_win = tk.Toplevel(parent)
    remove_win.title("Delete Room")
    remove_win.geometry("300x150")
    remove_win.configure(padx=20, pady=20, bg="lightgrey")

    tk.Label(remove_win, text="Room ID:", font=("Arial", 12), bg="lightgrey").pack(pady=(0, 5))
    room_id_entry = tk.Entry(remove_win, font=("Arial", 12))
    room_id_entry.pack(pady=5)

    def on_remove():
        r_id = room_id_entry.get().strip()
        admin_user.remove_room(r_id)
        messagebox.showinfo("Room Removed", f"Room '{r_id}' was successfully removed.")
        remove_win.destroy()

    tk.Button(remove_win, text="Delete", font=("Arial", 12), command=on_remove, bg="lightgrey").pack(pady=5)

def modify_room_popup(parent, admin_user):
    mod_win = tk.Toplevel(parent)
    mod_win.title("Update Room")
    mod_win.geometry("400x250")
    mod_win.configure(padx=20, pady=20, bg="lightgrey")
    form_frame = tk.Frame(mod_win, bg="lightgrey")
    form_frame.pack(expand=True, fill="both")

    tk.Label(form_frame, text="Room ID:", font=("Arial", 12), bg="lightgrey").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    room_id_entry = tk.Entry(form_frame, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="New Type:", font=("Arial", 12), bg="lightgrey").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    room_types = ["Single", "Double", "Suite"]
    new_type_var = tk.StringVar(value="")
    new_type_combo = ttk.Combobox(form_frame, textvariable=new_type_var, values=room_types, state="readonly", font=("Arial", 12))
    new_type_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="New Price:", font=("Arial", 12), bg="lightgrey").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    new_price_entry = tk.Entry(form_frame, font=("Arial", 12))
    new_price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def on_modify():
        r_id = room_id_entry.get().strip()
        chosen_type = new_type_var.get().strip()
        new_type = chosen_type if chosen_type else None
        price_str = new_price_entry.get().strip()
        new_price = float(price_str) if price_str else None

        admin_user.modify_room(r_id, new_type, new_price)
        messagebox.showinfo("Room Updated", f"Room '{r_id}' has been updated successfully.")
        mod_win.destroy()

    tk.Button(form_frame, text="Update Room", font=("Arial", 12), command=on_modify, bg="lightgrey").grid(row=3, column=0, columnspan=2, pady=15)
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)

def display_user_dashboard(user_obj):
    user_window = tk.Toplevel()
    user_window.title("User Dashboard")
    user_window.geometry("300x250")
    user_window.configure(padx=20, pady=20, bg="lightgrey")

    tk.Button(user_window, text="Browse Rooms", width=15, font=("Arial", 12),
              command=lambda: view_rooms_ui(user_window), bg="lightgrey").pack(pady=10)

    tk.Button(user_window, text="Reserve Room", width=15, font=("Arial", 12),
              command=lambda: book_room_ui(user_window, user_obj), bg="lightgrey").pack(pady=10)

    tk.Button(user_window, text="Sign Out", width=15, font=("Arial", 12),
              command=user_window.destroy, bg="lightgrey").pack(pady=20)

def view_rooms_ui(parent):
    """Display available rooms by reading from the Excel file."""
    from pandas import read_excel
    rooms_file = os.path.join('data', 'rooms.xlsx')
    if not os.path.exists(rooms_file):
        text = "No rooms available at the moment."
    else:
        df = read_excel(rooms_file)
        text = df.to_string(index=False)

    room_win = tk.Toplevel(parent)
    room_win.title("Available Rooms")
    room_win.geometry("400x300")
    room_win.configure(padx=20, pady=20, bg="lightgrey")

    text_widget = tk.Text(room_win, wrap="none", font=("Arial", 12), bg="lightgrey")
    text_widget.insert("1.0", text)
    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both")

def book_room_ui(parent, user_obj):
    """Pop-up for booking a room with date selection."""
    book_win = tk.Toplevel(parent)
    book_win.title("Book a Room")
    book_win.geometry("400x250")
    book_win.configure(padx=20, pady=20, bg="lightgrey")

    form_frame = tk.Frame(book_win, bg="lightgrey")
    form_frame.pack(expand=True, fill="both")

    tk.Label(form_frame, text="Room ID:", font=("Arial", 12), bg="lightgrey").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    room_id_entry = tk.Entry(form_frame, font=("Arial", 12))
    room_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="Check-in (YYYY-MM-DD):", font=("Arial", 12), bg="lightgrey").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    checkin_entry = DateEntry(form_frame, font=("Arial", 12), date_pattern="yyyy-mm-dd")
    checkin_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(form_frame, text="Check-out (YYYY-MM-DD):", font=("Arial", 12), bg="lightgrey").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    checkout_entry = DateEntry(form_frame, font=("Arial", 12), date_pattern="yyyy-mm-dd")
    checkout_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def on_book():
        room_id = room_id_entry.get().strip()
        check_in = checkin_entry.get().strip()
        check_out = checkout_entry.get().strip()

        if is_room_available(room_id, check_in, check_out):
            b = Booking(user_obj.username, room_id, check_in, check_out)
            b.save_booking()
            messagebox.showinfo("Booking Confirmed", "Your booking has been successfully confirmed!")
            book_win.destroy()
        else:
            messagebox.showerror("Booking Error", "The room isn't available on the chosen dates. Please select different dates.")

    tk.Button(form_frame, text="Book", font=("Arial", 12), command=on_book, bg="lightgrey").grid(row=3, column=0, columnspan=2, pady=15)
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=2)

def is_room_available(room_id, check_in, check_out):
    """Check if a room is available for the given date range."""
    bookings_file = os.path.join('data', 'bookings.xlsx')
    if not os.path.exists(bookings_file):
        return True

    df = pd.read_excel(bookings_file)
    same_room_bookings = df[df['room_id'].astype(str) == str(room_id)]
    new_check_in = pd.to_datetime(check_in)
    new_check_out = pd.to_datetime(check_out)

    if new_check_in == new_check_out:
        new_check_out += timedelta(days=1)

    for _, row in same_room_bookings.iterrows():
        existing_check_in = pd.to_datetime(row['check_in'])
        existing_check_out = pd.to_datetime(row['check_out'])
        if existing_check_in == existing_check_out:
            existing_check_out += timedelta(days=1)
        if not (new_check_out <= existing_check_in or new_check_in >= existing_check_out):
            return False

    return True

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    launch_main_interface()

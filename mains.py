import os
import pandas as pd
from models.user import User
from models.admin import Admin
from models.booking import Booking

def create_admin_if_not_exists():
    users_file = os.path.join('data', 'users.xlsx')
    if not os.path.exists(users_file):
        # create empty DataFrame
        df = pd.DataFrame(columns=['username', 'password', 'email', 'is_admin'])
        df.to_excel(users_file, index=False)

    df = pd.read_excel(users_file)
    admins = df[df['is_admin'] == True]

    if admins.empty:
        print("No admin account found. Creating a default admin account...")
        new_row = {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@example.com',
            'is_admin': True
        }
        new_df = pd.DataFrame([new_row])  # convert the dict to a DataFrame
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel(users_file, index=False)
        print("Default admin created. Username: admin, Password: admin123")


def main_menu():
    while True:
        print("\n--- Hotel Room Booking System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            User.register(username, password, email)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            logged_in_user = User.login(username, password)
            if logged_in_user:
                if logged_in_user.is_admin:
                    admin_menu(logged_in_user)
                else:
                    user_menu(logged_in_user)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

def admin_menu(admin_user):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Room")
        print("2. Remove Room")
        print("3. Modify Room")
        print("4. View All Bookings")
        print("5. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            room_id = input("Enter Room ID: ")
            room_type = input("Enter Room Type (Single, Double, Suite): ")
            price = float(input("Enter Room Price: "))
            admin_user.add_room(room_id, room_type, price)
        elif choice == "2":
            room_id = input("Enter Room ID to remove: ")
            admin_user.remove_room(room_id)
        elif choice == "3":
            room_id = input("Enter Room ID to modify: ")
            new_type = input("Enter new room type (leave blank for no change): ")
            new_price_str = input("Enter new price (leave blank for no change): ")
            new_price = float(new_price_str) if new_price_str else None
            admin_user.modify_room(room_id, new_type if new_type else None, new_price)
        elif choice == "4":
            admin_user.view_all_bookings()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

def user_menu(user):
    while True:
        print("\n--- User Menu ---")
        print("1. View Available Rooms")
        print("2. Book a Room")
        print("3. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            list_available_rooms()
        elif choice == "2":
            room_id = input("Enter Room ID to book: ")
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            check_out = input("Enter check-out date (YYYY-MM-DD): ")
            if is_room_available(room_id, check_in, check_out):
                booking = Booking(user.username, room_id, check_in, check_out)
                booking.save_booking()
            else:
                print("Room not available for these dates.")
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

def list_available_rooms():
    rooms_file = os.path.join('data', 'rooms.xlsx')
    if not os.path.exists(rooms_file):
        print("No rooms found.")
        return

    df = pd.read_excel(rooms_file)
    print("Available Rooms:")
    print(df)

def is_room_available(room_id, new_check_in, new_check_out):
    bookings_file = os.path.join('data', 'bookings.xlsx')
    if not os.path.exists(bookings_file):
        # No bookings file -> everything is available
        return True

    df = pd.read_excel(bookings_file)
    same_room_bookings = df[df['room_id'] == room_id]

    new_check_in = pd.to_datetime(new_check_in)
    new_check_out = pd.to_datetime(new_check_out)

    for _, booking in same_room_bookings.iterrows():
        existing_check_in = pd.to_datetime(booking['check_in'])
        existing_check_out = pd.to_datetime(booking['check_out'])
        # If there's an overlap
        if not (new_check_out <= existing_check_in or new_check_in >= existing_check_out):
            return False

    return True

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    create_admin_if_not_exists()
    main_menu()

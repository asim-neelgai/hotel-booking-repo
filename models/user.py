import pandas as pd
import os

class User:
    def __init__(self, username, password, email, is_admin=False):
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = is_admin

    @staticmethod
    def register(username, password, email):
        users_file = os.path.join('data', 'users.xlsx')

        # If file exists, load it
        if os.path.exists(users_file):
            df = pd.read_excel(users_file)
        else:
            # Otherwise create a new DataFrame
            df = pd.DataFrame(columns=['username', 'password', 'email', 'is_admin'])

        # Check if the username already exists
        if username in df['username'].values:
            print("Username already taken.")
            return None

        new_row = {
            'username': username,
            'password': password,
            'email': email,
            'is_admin': False
        }
        df = df.append(new_row, ignore_index=True)
        df.to_excel(users_file, index=False)
        print("Registration successful!")
        return User(username, password, email)

    @staticmethod
    def login(username, password):
        users_file = os.path.join('data', 'users.xlsx')
        if not os.path.exists(users_file):
            print("No users file found. Please register an account.")
            return None

        df = pd.read_excel(users_file)
        user_row = df.loc[(df['username'] == username) & (df['password'] == password)]
        if not user_row.empty:
            is_admin_val = user_row['is_admin'].values[0]
            email_val = user_row['email'].values[0]
            print(f"Login successful. Welcome, {username}!")
            return User(username, password, email_val, is_admin_val)
        else:
            print("Invalid username or password.")
            return None

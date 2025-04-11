import pandas as pd
import os

class Booking:
    def __init__(self, username, room_id, check_in, check_out):
        self.username = username
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out

    def save_booking(self):
        bookings_file = os.path.join('data', 'bookings.xlsx')
        if os.path.exists(bookings_file):
            df = pd.read_excel(bookings_file)
        else:
            df = pd.DataFrame(columns=['username', 'room_id', 'check_in', 'check_out'])

        new_row = {
            'username': self.username,
            'room_id': self.room_id,
            'check_in': self.check_in,
            'check_out': self.check_out
        }
        df = df.append(new_row, ignore_index=True)
        df.to_excel(bookings_file, index=False)
        print("Booking saved successfully.")

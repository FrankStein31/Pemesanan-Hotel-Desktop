import sys
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow
from PyQt5 import QtWidgets

class DatabaseManager:
    def __init__(self, host='localhost', user='root', password='', database='hotel_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("Database connection successful")
        except Error as e:
            print(f"Error: {e}")
            QMessageBox.critical(None, "Database Error", str(e))

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")

    # Room Type CRUD Operations
    def add_room_type(self, type_name, description, price):
        try:
            # Ensure price is converted to integer
            price = int(price)
            query = "INSERT INTO room_types (type_name, description, price) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (type_name, description, price))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return None

    def get_room_types(self):
        try:
            query = "SELECT * FROM room_types"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            QMessageBox.critical(None, "Database Error", str(e))
            return []

    def update_room_type(self, type_id, type_name, description, price):
        try:
            query = """
            UPDATE room_types 
            SET type_name = %s, description = %s, price = %s 
            WHERE id = %s
            """
            self.cursor.execute(query, (type_name, description, price, type_id))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return False

    def delete_room_type(self, type_id):
        try:
            query = "DELETE FROM room_types WHERE id = %s"
            self.cursor.execute(query, (type_id,))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return False

    # Room CRUD Operations
    def add_room(self, room_number, room_type_id, status='Tersedia'):
        try:
            query = "INSERT INTO rooms (room_number, room_type_id, status) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (room_number, room_type_id, status))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return None

    def get_rooms(self):
        try:
            query = """
            SELECT rooms.id, rooms.room_number, room_types.type_name, 
                room_types.price, rooms.status, room_types.description
            FROM rooms 
            JOIN room_types ON rooms.room_type_id = room_types.id
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            QMessageBox.critical(None, "Database Error", str(e))
            return []

    def update_room(self, room_id, room_number, room_type_id, status):
        try:
            query = """
            UPDATE rooms 
            SET room_number = %s, room_type_id = %s, status = %s 
            WHERE id = %s
            """
            self.cursor.execute(query, (room_number, room_type_id, status, room_id))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return False

    def delete_room(self, room_id):
        try:
            query = "DELETE FROM rooms WHERE id = %s"
            self.cursor.execute(query, (room_id,))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return False

    # Facility CRUD Operations
    def add_facility(self, facility_name, description, price):
        try:
            # Convert price to an integer, removing any formatting
            price = int(str(price).replace('.', ''))
            
            query = "INSERT INTO facilities (facility_name, description, price) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (facility_name, description, price))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", f"Failed to add facility: {str(e)}")
            return None
        
    def update_reservation_status(self, reservation_id, status):
        """
        Update the status of a specific reservation
        
        Parameters:
        - reservation_id (int): ID of the reservation to update
        - status (str): New status for the reservation
        
        Returns:
        - bool: True if update successful, False otherwise
        """
        try:
            # Validate that the status is a valid enum value
            valid_statuses = ['Pending', 'Confirmed', 'Completed', 'Cancelled', 'Paid']
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

            # SQL query to update reservation status
            query = """
            UPDATE reservations 
            SET status = %s 
            WHERE id = %s
            """
            
            # Execute the update
            self.cursor.execute(query, (status, reservation_id))
            
            # Commit the transaction
            self.connection.commit()
            
            # Log the status update
            print(f"Reservation {reservation_id} status updated to {status}")
            
            return True
        
        except Error as e:
            # Rollback the transaction in case of error
            self.connection.rollback()
            
            # Show error message
            QMessageBox.critical(None, "Database Error", 
                                f"Failed to update reservation status: {str(e)}")
            
            return False
        except ValueError as ve:
            # Handle invalid status
            QMessageBox.warning(None, "Invalid Status", str(ve))
            return False
        
    def get_facilities(self):
        try:
            query = "SELECT * FROM facilities"
            self.cursor.execute(query)
            facilities = self.cursor.fetchall()
            
            # Ensure price is an integer without converting to float
            for facility in facilities:
                facility['price'] = int(facility['price'])
            
            return facilities
        except Error as e:
            QMessageBox.critical(None, "Database Error", f"Failed to retrieve facilities: {str(e)}")
            return []
        
    def update_facility(self, facility_id, facility_name, description, price):
        try:
            # Convert price to an integer, removing any formatting
            price = int(str(price).replace('.', ''))
            
            query = """
            UPDATE facilities 
            SET facility_name = %s, description = %s, price = %s 
            WHERE id = %s
            """
            self.cursor.execute(query, (facility_name, description, price, facility_id))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", f"Failed to update facility: {str(e)}")
            return False

    def delete_facility(self, facility_id):
        try:
            query = "DELETE FROM facilities WHERE id = %s"
            self.cursor.execute(query, (facility_id,))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", f"Failed to delete facility: {str(e)}")
            return False

    # Helper method to search facilities
    def search_facilities(self, search_term):
        try:
            query = """
            SELECT * FROM facilities 
            WHERE facility_name LIKE %s OR description LIKE %s
            """
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern))
            facilities = self.cursor.fetchall()
            
            # Format price back to string with dot separators
            for facility in facilities:
                facility['price'] = f"{facility['price']:,}".replace(',', '.')
            
            return facilities
        except Error as e:
            QMessageBox.critical(None, "Database Error", f"Failed to search facilities: {str(e)}")
            return []

    # Customer CRUD Operations
    def add_customer(self, name, email, phone, address):
        try:
            query = "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (name, email, phone, address))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return None

    def get_customers(self):
        try:
            query = "SELECT * FROM customers"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            QMessageBox.critical(None, "Database Error", str(e))
            return []

    def update_customer(self, customer_id, name, email, phone, address):
        try:
            query = """
            UPDATE customers 
            SET name = %s, email = %s, phone = %s, address = %s 
            WHERE id = %s
            """
            self.cursor.execute(query, (name, email, phone, address, customer_id))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return False

    def delete_customer(self, customer_id):
        try:
            query = "DELETE FROM customers WHERE id = %s"
            self.cursor.execute(query, (customer_id,))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Database Error", str(e))
            return False
        
    # Reservation CRUD Operations
    def create_reservation(self, customer_id, check_in_date, check_out_date, total_people, total_price, room_ids, facility_ids, voucher_code=None):
        try:
            # Pastikan tidak ada transaksi yang sedang berlangsung
            if self.connection.is_connected():
                if self.connection.in_transaction:
                    self.connection.rollback()  # Batalkan transaksi sebelumnya jika ada

            # Mulai transaksi baru
            self.connection.start_transaction()

            # Insert reservation dengan total harga sebagai integer
            reservation_query = """
            INSERT INTO reservations 
            (customer_id, check_in_date, check_out_date, total_people, total_price, status) 
            VALUES (%s, %s, %s, %s, %s, 'Pending')
            """
            self.cursor.execute(reservation_query, (customer_id, check_in_date, check_out_date, total_people, int(total_price)))
            reservation_id = self.cursor.lastrowid

            # Insert reservation rooms
            room_query = "INSERT INTO reservation_rooms (reservation_id, room_id) VALUES (%s, %s)"
            for room_id in room_ids:
                self.cursor.execute(room_query, (reservation_id, room_id))

            # Insert reservation facilities
            facility_query = "INSERT INTO reservation_facilities (reservation_id, facility_id) VALUES (%s, %s)"
            for facility_id in facility_ids:
                self.cursor.execute(facility_query, (reservation_id, facility_id))

            # Commit the transaction
            self.connection.commit()
            return reservation_id
        except Error as e:
            # Rollback in case of error
            self.connection.rollback()
            QMessageBox.critical(None, "Reservation Error", str(e))
            return None

    def get_available_rooms(self, check_in_date, check_out_date, room_type_id=None):
        try:
            # Query to find rooms that are available and not reserved during a specific period
            query = """
            SELECT rooms.id, rooms.room_number, room_types.type_name, room_types.price
            FROM rooms
            JOIN room_types ON rooms.room_type_id = room_types.id
            WHERE rooms.status = 'Tersedia' AND rooms.id NOT IN (
                SELECT DISTINCT reservation_rooms.room_id
                FROM reservation_rooms
                JOIN reservations ON reservation_rooms.reservation_id = reservations.id
                WHERE (
                    (%s BETWEEN check_in_date AND check_out_date) OR
                    (%s BETWEEN check_in_date AND check_out_date) OR
                    (check_in_date BETWEEN %s AND %s)
                )
                AND reservations.status != 'Cancelled'
            )
            """
            params = [check_in_date, check_out_date, check_in_date, check_out_date]

            # Add room type filter if specified
            if room_type_id:
                query += " AND rooms.room_type_id = %s"
                params.append(room_type_id)

            self.cursor.execute(query, params)
            available_rooms = self.cursor.fetchall()

            # If no rooms are available, show all rooms of the type
            if not available_rooms and room_type_id:
                query = """
                SELECT rooms.id, rooms.room_number, room_types.type_name, room_types.price
                FROM rooms
                JOIN room_types ON rooms.room_type_id = room_types.id
                WHERE rooms.room_type_id = %s AND rooms.status = 'Tersedia'
                """
                self.cursor.execute(query, (room_type_id,))
                available_rooms = self.cursor.fetchall()

            return available_rooms
        except Error as e:
            QMessageBox.critical(None, "Room Availability Error", str(e))
            return []

    def update_room_status_after_checkout(self):
        try:
            # Query to update room status to 'Tersedia' for rooms in completed reservations
            query = """
            UPDATE rooms r
            JOIN reservation_rooms rr ON r.id = rr.room_id
            JOIN reservations res ON rr.reservation_id = res.id
            SET r.status = 'Tersedia'
            WHERE res.check_out_date < CURRENT_DATE 
            AND res.status = 'Completed'
            """
            
            self.cursor.execute(query)
            self.connection.commit()
            
            print("Room statuses updated successfully")
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Room Status Update Error", str(e))

    def ensure_transaction_closed(self):
        """
        Memastikan transaksi ditutup dengan benar
        Panggil method ini sebelum operasi database yang memerlukan transaksi baru
        """
        try:
            if self.connection.is_connected() and self.connection.in_transaction:
                print("Warning: Closing an ongoing transaction")
                self.connection.rollback()
        except Exception as e:
            print(f"Error closing transaction: {e}")

    def get_reservation_details(self, reservation_id):
        try:
            # Get reservation details with customer info
            reservation_query = """
            SELECT r.*, c.name AS customer_name, c.email, c.phone
            FROM reservations r
            JOIN customers c ON r.customer_id = c.id
            WHERE r.id = %s
            """
            self.cursor.execute(reservation_query, (reservation_id,))
            reservation = self.cursor.fetchone()

            # Get reserved rooms
            rooms_query = """
            SELECT rr.room_id, rm.room_number, rt.type_name, rt.price
            FROM reservation_rooms rr
            JOIN rooms rm ON rr.room_id = rm.id
            JOIN room_types rt ON rm.room_type_id = rt.id
            WHERE rr.reservation_id = %s
            """
            self.cursor.execute(rooms_query, (reservation_id,))
            reservation['rooms'] = self.cursor.fetchall()

            # Get reserved facilities
            facilities_query = """
            SELECT rf.facility_id, f.facility_name, f.price
            FROM reservation_facilities rf
            JOIN facilities f ON rf.facility_id = f.id
            WHERE rf.reservation_id = %s
            """
            self.cursor.execute(facilities_query, (reservation_id,))
            reservation['facilities'] = self.cursor.fetchall()

            return reservation
        except Error as e:
            QMessageBox.critical(None, "Reservation Details Error", str(e))
            return None

    def cancel_reservation(self, reservation_id):
        try:
            query = "UPDATE reservations SET status = 'Cancelled' WHERE id = %s"
            self.cursor.execute(query, (reservation_id,))
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            QMessageBox.critical(None, "Reservation Cancellation Error", str(e))
            return False

    def verify_voucher(self, voucher_code):
        try:
            query = """
            SELECT * FROM vouchers 
            WHERE CODE = %s 
            AND is_active = TRUE 
            AND CURRENT_DATE BETWEEN valid_from AND valid_to
            """
            self.cursor.execute(query, (voucher_code,))
            return self.cursor.fetchone()
        except Error as e:
            QMessageBox.critical(None, "Voucher Verification Error", str(e))
            return None
        
    def check_voucher_discount(self, voucher_code):
        try:
            # Query untuk memeriksa voucher di database
            query = "SELECT discount_percentage FROM vouchers WHERE code = ? AND is_active = 1"
            self.cursor.execute(query, (voucher_code,))
            result = self.cursor.fetchone()

            if result:
                return result[0]  # Kembalikan persentase diskon
            else:
                return 0  # Voucher tidak valid
        except Exception as e:
            print(f"Error checking voucher: {e}")
            return 0
        
    def save_payment(self, reservation_id, payment_date, amount, payment_method):
        try:
            query = """
                INSERT INTO payments (reservation_id, payment_date, amount, payment_method)
                VALUES (%s, %s, %s, %s)
            """
            values = (reservation_id, payment_date, amount, payment_method)
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving payment: {e}")
            self.connection.rollback()
            return False


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

    # def get_rooms(self):
    #     try:
    #         query = """
    #         SELECT rooms.id, rooms.room_number, room_types.type_name, 
    #                room_types.price, rooms.status, room_types.description
    #         FROM rooms 
    #         JOIN room_types ON rooms.room_type_id = room_types.id
    #         """
    #         self.cursor.execute(query)
    #         return self.cursor.fetchall()
    #     except Error as e:
    #         QMessageBox.critical(None, "Database Error", str(e))
    #         return []
        
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

    def get_facilities(self):
        try:
            query = "SELECT * FROM facilities"
            self.cursor.execute(query)
            facilities = self.cursor.fetchall()
            
            # Format price back to string with dot separators
            for facility in facilities:
                facility['price'] = f"{facility['price']:,}".replace(',', '.')
            
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
import sys
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from databasemanager import DatabaseManager

class Ui_MainWindow(object):
    def __init__(self):
        self.db_manager = DatabaseManager()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Title Label
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setText("Tipe Kamar di Hotel Acumalaka")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(QtGui.QFont("Comic Sans MS", 24, QtGui.QFont.Bold))
        self.title_label.setStyleSheet("""
            color: #3f6ad8;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        """)
        self.main_layout.addWidget(self.title_label)

        # Search Layout
        self.search_layout = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setPlaceholderText("Cari Tipe Kamar...")
        self.search_input.setFont(QtGui.QFont("Arial", 14))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 12px;
                border: 2px solid #3f6ad8;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #28a745;
                background-color: #f1f1f1;
            }
        """)
        self.search_input.textChanged.connect(self.search_rooms)
        self.search_layout.addWidget(self.search_input)
        self.main_layout.addLayout(self.search_layout)

        # Table Widget
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(4)  # Added ID column
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Tipe Kamar", "Harga", "Deskripsi"])
        
        # Hide ID column
        self.tableWidget.setColumnHidden(0, True)

        # Styling for table
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # Room Type
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  # Price
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)  # Description

        self.tableWidget.setStyleSheet(""" 
            QTableWidget {
                border: 2px solid #ddd;
                background-color: #f9f9f9;
                font-size: 16px;
                color: #333;
                font-family: "Arial";
            }
        """)

        self.main_layout.addWidget(self.tableWidget)

        # Form Layout for Input
        self.form_layout = QtWidgets.QFormLayout()
        
        # ID input (hidden)
        self.room_id_input = QtWidgets.QLineEdit(self.centralwidget)
        self.room_id_input.setVisible(False)
        
        # Room Type input
        self.room_name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.room_name_input.setPlaceholderText("Masukkan nama tipe kamar")
        self.room_name_input.setFont(QtGui.QFont("Arial", 14))
        self.form_layout.addRow("Nama Tipe Kamar:", self.room_name_input)

        # Price input
        self.room_price_input = QtWidgets.QLineEdit(self.centralwidget)
        self.room_price_input.setPlaceholderText("Masukkan harga kamar")
        self.room_price_input.setFont(QtGui.QFont("Arial", 14))
        self.form_layout.addRow("Harga:", self.room_price_input)

        # Description input
        self.room_desc_input = QtWidgets.QLineEdit(self.centralwidget)
        self.room_desc_input.setPlaceholderText("Masukkan deskripsi kamar")
        self.room_desc_input.setFont(QtGui.QFont("Arial", 14))
        self.form_layout.addRow("Deskripsi:", self.room_desc_input)

        self.main_layout.addLayout(self.form_layout)

        # Button Layout
        self.button_layout = QtWidgets.QHBoxLayout()

        # Buttons with consistent styling and connected methods
        buttons = [
            ("Tambah Kamar", self.add_room, "#28a745"),
            ("Perbarui Kamar", self.update_room, "#ffc107"),
            ("Hapus Kamar", self.delete_room, "#dc3545"),
            ("Kosongkan Form", self.clear_fields, "#6c757d"),
            ("Kembali", self.back_action, "#007bff")
        ]

        for label, method, color in buttons:
            btn = QtWidgets.QPushButton(label, self.centralwidget)
            btn.setStyleSheet(f""" 
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-weight: bold;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background-color: {color}CC;
                }}
            """)
            btn.clicked.connect(method)
            self.button_layout.addWidget(btn)

        self.main_layout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        # Populate table on startup
        self.populate_table()

        # Connect table row selection to fill form
        self.tableWidget.itemSelectionChanged.connect(self.fill_form_from_selection)

    def populate_table(self):
        # Clear existing rows
        self.tableWidget.setRowCount(0)

        # Fetch room types from database
        room_types = self.db_manager.get_room_types()
        
        for room_type in room_types:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            
            # Insert data in order: ID, Type Name, Price, Description
            self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(room_type['id'])))
            self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(room_type['type_name']))
            self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(f"Rp {room_type['price']:,.0f}"))
            self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(room_type['description']))

    def fill_form_from_selection(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            self.room_id_input.setText(self.tableWidget.item(row, 0).text())
            self.room_name_input.setText(self.tableWidget.item(row, 1).text())
            
            # Remove 'Rp' and thousand separators before setting price
            price_text = self.tableWidget.item(row, 2).text().replace('Rp ', '').replace(',', '')
            self.room_price_input.setText(price_text)
            
            self.room_desc_input.setText(self.tableWidget.item(row, 3).text())

    def add_room(self):
        room_name = self.room_name_input.text()
        room_price = self.room_price_input.text()
        room_desc = self.room_desc_input.text()

        if room_name and room_price and room_desc:
            try:
                # Convert price to numeric
                price = float(room_price.replace(',', ''))
                
                # Add to database
                new_id = self.db_manager.add_room_type(room_name, room_desc, price)
                
                if new_id:
                    # Refresh table
                    self.populate_table()
                    self.clear_fields()
                    QtWidgets.QMessageBox.information(None, "Sukses", "Tipe Kamar Berhasil Ditambahkan!")
            except ValueError:
                QtWidgets.QMessageBox.warning(None, "Error", "Harga harus berupa angka!")
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "Harap isi semua kolom!")

    def update_room(self):
        room_id = self.room_id_input.text()
        room_name = self.room_name_input.text()
        room_price = self.room_price_input.text()
        room_desc = self.room_desc_input.text()

        if room_id and room_name and room_price and room_desc:
            try:
                # Convert price to numeric
                price = float(room_price.replace(',', ''))
                
                # Update in database
                success = self.db_manager.update_room_type(int(room_id), room_name, room_desc, price)
                
                if success:
                    # Refresh table
                    self.populate_table()
                    self.clear_fields()
                    QtWidgets.QMessageBox.information(None, "Sukses", "Tipe Kamar Berhasil Diperbarui!")
            except ValueError:
                QtWidgets.QMessageBox.warning(None, "Error", "Harga harus berupa angka!")
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "Harap pilih kamar dan isi semua kolom!")

    def delete_room(self):
        room_id = self.room_id_input.text()

        if room_id:
            confirm = QtWidgets.QMessageBox.question(
                None, 
                "Konfirmasi Hapus", 
                "Apakah Anda yakin ingin menghapus tipe kamar ini?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if confirm == QtWidgets.QMessageBox.Yes:
                # Delete from database
                success = self.db_manager.delete_room_type(int(room_id))
                
                if success:
                    # Refresh table
                    self.populate_table()
                    self.clear_fields()
                    QtWidgets.QMessageBox.information(None, "Sukses", "Tipe Kamar Berhasil Dihapus!")
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "Harap pilih kamar yang akan dihapus!")

    def search_rooms(self):
        search_text = self.search_input.text().lower()
        
        # Loop through all rows
        for row in range(self.tableWidget.rowCount()):
            # Ambil teks dari setiap kolom
            type_name = self.tableWidget.item(row, 1).text().lower() if self.tableWidget.item(row, 1) else ""
            price = self.tableWidget.item(row, 2).text().lower() if self.tableWidget.item(row, 2) else ""
            description = self.tableWidget.item(row, 3).text().lower() if self.tableWidget.item(row, 3) else ""
            
            # Tentukan apakah baris harus disembunyikan
            if (search_text in type_name or 
                search_text in price or 
                search_text in description):
                self.tableWidget.setRowHidden(row, False)  # Tampilkan baris
            else:
                self.tableWidget.setRowHidden(row, True)  # Sembunyikan baris

    def clear_fields(self):
        self.room_id_input.clear()
        self.room_name_input.clear()
        self.room_price_input.clear()
        self.room_desc_input.clear()

    def back_action(self):
        QtWidgets.QApplication.quit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
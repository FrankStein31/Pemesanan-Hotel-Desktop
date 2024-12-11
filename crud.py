from PyQt5 import QtCore, QtGui, QtWidgets
from databasemanager import DatabaseManager

class Ui_MainWindow(object):
    def __init__(self):
        self.db_manager = DatabaseManager()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 650)

        # Set Background Gradient for the Main Window
        MainWindow.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F5F5F5, stop:1 #D0E2F1);
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main Layout to Center the Form
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        
        # Title Label
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setText("Stok Kamar Hotel Acumalaka")
        self.label_title.setFont(QtGui.QFont("Helvetica", 26, QtGui.QFont.Bold))
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("color: #4B0082; padding: 20px;")
        main_layout.addWidget(self.label_title)

        # Search Bar
        self.search_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.search_bar.setFont(QtGui.QFont("Arial", 12))
        self.search_bar.setPlaceholderText("Cari Kamar (Nomor, Tipe, atau Status)...")
        self.search_bar.setStyleSheet("border: 2px solid #B8D1E8; border-radius: 10px; padding: 12px; background-color: #ffffff;")
        self.search_bar.textChanged.connect(self.filter_rooms)
        main_layout.addWidget(self.search_bar)

        # Form Group Box without the title
        self.form_groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.form_groupbox.setFont(QtGui.QFont("Arial", 12))
        self.form_groupbox.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border-radius: 15px;
                border: 2px solid #cccccc;
                margin-top: 20px;
                padding: 20px;
            }
        """)
        
        form_layout = QtWidgets.QVBoxLayout(self.form_groupbox)
        self.add_input(form_layout, "Nomor Kamar:", "input_room_number")
        
        # Modified room type input to use database
        self.add_combobox(form_layout, "Tipe Kamar:", "input_room_type", 
                          [rt['type_name'] for rt in self.db_manager.get_room_types()])
        
        self.add_input(form_layout, "Harga Kamar:", "input_room_price")
        self.add_combobox(form_layout, "Status Kamar:", "input_room_status", ["Tersedia", "Terisi"])

        button_layout = QtWidgets.QHBoxLayout()
        for label, method in [
            ("Tambah Kamar", self.add_room),
            ("Perbarui Kamar", self.update_room),
            ("Hapus Kamar", self.delete_room),
            ("Kosongkan Form", self.clear_form),
        ]:
            self.add_button(button_layout, label, method)

        # Adding the "Kembali" button
        self.back_button = QtWidgets.QPushButton("Kembali", self.centralwidget)
        self.back_button.setFont(QtGui.QFont("Arial", 12))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6347;
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF4500;
            }
        """)
        self.back_button.clicked.connect(self.back_action)
        button_layout.addWidget(self.back_button)

        form_layout.addLayout(button_layout)

        main_layout.addWidget(self.form_groupbox)

        # Room Table
        self.room_table = QtWidgets.QTableWidget(self.centralwidget)
        self.room_table.setColumnCount(5)  # Added column for room ID
        self.room_table.setHorizontalHeaderLabels(["ID", "Nomor Kamar", "Tipe Kamar", "Harga", "Status"])
        self.room_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.room_table.hideColumn(0)  # Hide ID column
        
        # Connect table row selection to form filling
        self.room_table.itemSelectionChanged.connect(self.fill_form_from_table)
        
        # Set Table and Header Styles
        self.room_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border-radius: 15px;
                border: 2px solid #B8D1E8;
                font-family: 'Arial', sans-serif;
                font-size: 12pt;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #4B0082;
                color: white;
                font-size: 10pt;
                padding: 10px;
                font-family: 'Arial', sans-serif;
            }
            QTableWidget::item {
                padding: 12px;
                font-family: 'Arial', sans-serif;
                font-size: 12pt;
                border: 1px solid #B8D1E8;
                background-color: #F9F9F9;
            }
            QTableWidget::item:hover {
                background-color: #E8E8E8;
            }
            QTableWidget::item:selected {
                background-color: #D0D0D0;
            }
        """)
        
        main_layout.addWidget(self.room_table)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)

        # Load rooms from database
        self.load_rooms_from_database()

    def load_rooms_from_database(self):
        # Clear existing rows
        self.room_table.setRowCount(0)
        
        # Get rooms from database
        rooms = self.db_manager.get_rooms()
        
        for room in rooms:
            row_position = self.room_table.rowCount()
            self.room_table.insertRow(row_position)
            
            # Add room details to table
            self.room_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(room['id'])))
            self.room_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(room['room_number']))
            self.room_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(room['type_name']))
            self.room_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(room['price'])))
            self.room_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(room['status']))

    def fill_form_from_table(self):
        # Get current selected row
        row = self.room_table.currentRow()
        if row != -1:
            # Fill input fields from table row
            self.input_room_number.setText(self.room_table.item(row, 1).text())
            room_type = self.room_table.item(row, 2).text()
            self.input_room_type.setCurrentText(room_type)
            self.input_room_price.setText(self.room_table.item(row, 3).text())
            self.input_room_status.setCurrentText(self.room_table.item(row, 4).text())

    def add_input(self, layout, label_text, input_name):
        layout_widget = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        label.setFont(QtGui.QFont("Arial", 11))
        input_field = QtWidgets.QLineEdit()
        input_field.setFont(QtGui.QFont("Arial", 11))
        input_field.setStyleSheet("border: 2px solid #B8D1E8; border-radius: 10px; padding: 12px; background-color: #ffffff;")
        setattr(self, input_name, input_field)
        layout_widget.addWidget(label)
        layout_widget.addWidget(input_field)
        layout.addLayout(layout_widget)

    def add_combobox(self, layout, label_text, combo_name, options):
        layout_widget = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        label.setFont(QtGui.QFont("Arial", 11))
        combo_box = QtWidgets.QComboBox()
        combo_box.setFont(QtGui.QFont("Arial", 11))
        combo_box.addItems(options)
        combo_box.setStyleSheet("border: 2px solid #B8D1E8; border-radius: 10px; padding: 12px; background-color: #ffffff;")
        setattr(self, combo_name, combo_box)
        layout_widget.addWidget(label)
        layout_widget.addWidget(combo_box)
        layout.addLayout(layout_widget)

    def add_button(self, layout, label, method):
        button = QtWidgets.QPushButton(label)
        button.setFont(QtGui.QFont("Arial", 12))
        button.setStyleSheet("""
            QPushButton {
                background-color: #4B0082;
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #836FFF;
            }
        """)
        button.clicked.connect(method)
        layout.addWidget(button)

    def add_room(self):
        room_number = self.input_room_number.text()
        room_type = self.input_room_type.currentText()
        room_price = self.input_room_price.text()
        room_status = self.input_room_status.currentText()

        # Find room type ID
        room_types = self.db_manager.get_room_types()
        room_type_id = next((rt['id'] for rt in room_types if rt['type_name'] == room_type), None)

        if room_number and room_type_id and room_price:
            # Add room to database
            room_id = self.db_manager.add_room(room_number, room_type_id, room_status)
            
            if room_id:
                # Reload rooms from database to reflect changes
                self.load_rooms_from_database()
                self.statusbar.showMessage("Kamar berhasil ditambahkan!", 2000)
                self.clear_form()
            else:
                self.statusbar.showMessage("Gagal menambahkan kamar!", 2000)
        else:
            self.statusbar.showMessage("Isi semua data!", 2000)

    def update_room(self):
        row = self.room_table.currentRow()
        if row != -1:
            # Get room ID from hidden column
            room_id = int(self.room_table.item(row, 0).text())
            room_number = self.input_room_number.text()
            room_type = self.input_room_type.currentText()
            room_status = self.input_room_status.currentText()

            # Find room type ID
            room_types = self.db_manager.get_room_types()
            room_type_id = next((rt['id'] for rt in room_types if rt['type_name'] == room_type), None)

            if room_type_id:
                # Update room in database
                if self.db_manager.update_room(room_id, room_number, room_type_id, room_status):
                    # Reload rooms from database to reflect changes
                    self.load_rooms_from_database()
                    self.statusbar.showMessage("Kamar berhasil diperbarui!", 2000)
                else:
                    self.statusbar.showMessage("Gagal memperbarui kamar!", 2000)

    def delete_room(self):
        row = self.room_table.currentRow()
        if row != -1:
            # Get room ID from hidden column
            room_id = int(self.room_table.item(row, 0).text())
            
            # Delete room from database
            if self.db_manager.delete_room(room_id):
                # Reload rooms from database to reflect changes
                self.load_rooms_from_database()
                self.statusbar.showMessage("Kamar berhasil dihapus!", 2000)
                self.clear_form()
            else:
                self.statusbar.showMessage("Gagal menghapus kamar!", 2000)

    def __del__(self):
        # Close database connection when UI is destroyed
        if hasattr(self, 'db_manager'):
            self.db_manager.close()

    def clear_form(self):
        self.input_room_number.clear()
        self.input_room_price.clear()
        self.input_room_type.setCurrentIndex(0)
        self.input_room_status.setCurrentIndex(0)
        self.statusbar.showMessage("Form telah dikosongkan", 2000)

    def add_predefined_rooms(self):
        rooms = [
            ("101", "Standart", "500.000", "Tersedia"),
            ("102", "Executive", "1.500.000", "Terisi"),
            ("103", "Deluxe", "2.500.000", "Tersedia"),
            ("104", "Suite", "3.000.000", "Terisi"),
            ("105", "Presidential", "5.000.000", "Tersedia")
        ]
        for room in rooms:
            row_position = self.room_table.rowCount()
            self.room_table.insertRow(row_position)
            self.room_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(room[0]))
            self.room_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(room[1]))
            self.room_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(room[2]))
            self.room_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(room[3]))

    def filter_rooms(self):
        search_text = self.search_bar.text().lower()
        for row in range(self.room_table.rowCount()):
            # Sesuaikan index kolom berdasarkan struktur tabel terbaru
            room_number = self.room_table.item(row, 1).text().lower()  # Kolom 1 adalah Nomor Kamar
            room_type = self.room_table.item(row, 2).text().lower()    # Kolom 2 adalah Tipe Kamar
            room_status = self.room_table.item(row, 4).text().lower()  # Kolom 4 adalah Status

            # Show row if any cell contains the search text
            match = (search_text in room_number or 
                    search_text in room_type or 
                    search_text in room_status)
            self.room_table.setRowHidden(row, not match)

    def back_action(self):
        QtWidgets.QApplication.quit()  # Closes the application

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()  # Fullscreen display
    sys.exit(app.exec_())

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import subprocess
from databasemanager import DatabaseManager
from datetime import datetime, timedelta

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.db_manager = DatabaseManager()  # Initialize database manager early
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Set theme (keeping the existing styling)
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #d4f1f4;
                font-family: 'Arial', sans-serif;
            }
            QLabel {
                font-size: 18px;
                color: #2a9df4;
                font-weight: bold;
                padding: 5px 0;
            }
            QLineEdit, QComboBox, QDateTimeEdit {
                background-color: #ffffff;
                border: 2px solid #2a9df4;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #ff007f;
                color: white;
                border-radius: 10px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout utama
        self.titleLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.titleLayout.setContentsMargins(20, 20, 20, 10)

        # Judul
        self.label = QtWidgets.QLabel("Form Reservasi Hotel Acumalaka", self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ff007f;")
        self.titleLayout.addWidget(self.label)

        # Scroll Area
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_content_widget)

        # Layout di dalam scroll area
        self.scroll_layout = QtWidgets.QFormLayout(self.scroll_content_widget)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setHorizontalSpacing(20)
        self.scroll_layout.setVerticalSpacing(15)

        # Tambahkan form
        self.name_input = self.create_line_edit("Nama Lengkap")
        self.add_form_field("Nama Lengkap:", self.name_input)
        
        self.ktp_input = self.create_line_edit("Nomor KTP")
        self.add_form_field("No KTP:", self.ktp_input)
        
        self.check_in_date = self.create_date_edit()
        self.add_form_field("Tanggal Check-in:", self.check_in_date)
        
        self.check_out_date = self.create_date_edit()
        self.add_form_field("Tanggal Check-out:", self.check_out_date)

        # Fasilitas - Dynamically populated from database
        self.fasilitas_combo = self.create_facility_combo()
        self.add_form_field("Fasilitas:", self.fasilitas_combo)

        # Gender 
        self.gender_combo = self.create_combo(["Laki-Laki", "Perempuan"])
        self.add_form_field("Jenis Kelamin:", self.gender_combo)

        # People Count
        self.people_count_input = self.create_line_edit("Jumlah Orang")
        self.people_count_input.setValidator(QtGui.QIntValidator(1, 10))
        self.add_form_field("Jumlah Orang:", self.people_count_input)

        # Optional Voucher
        # self.voucher_input = self.create_line_edit("Kode Voucher (Optional)")
        # self.add_form_field("Kode Voucher:", self.voucher_input)

        # Room Type Layout
        self.room_layout = QtWidgets.QVBoxLayout()
        self.room_widgets = []
        self.add_room_type_field()

        # Calculate Price Button
        self.calculate_price_button = QtWidgets.QPushButton("Hitung Total Harga")
        self.calculate_price_button.clicked.connect(self.calculate_total_price)
        self.room_layout.addWidget(self.calculate_price_button)

        # Total Price Label
        self.total_price_label = QtWidgets.QLabel("Total Harga: Rp 0")
        self.room_layout.addWidget(self.total_price_label)

        self.scroll_layout.addRow(QtWidgets.QLabel("Jenis Kamar:"), self.room_layout)

        # Tambahkan scroll area ke layout utama
        self.titleLayout.addWidget(self.scroll_area)

        # Tombol navigasi
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.backButton = self.create_button("Kembali")
        self.backButton.clicked.connect(self.go_back_to_pet)
        self.reserveButton = self.create_button("Reservasi")
        self.reserveButton.clicked.connect(self.go_to_bayar)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.reserveButton)

        self.titleLayout.addLayout(self.buttonLayout)
        MainWindow.setCentralWidget(self.centralwidget)

    def create_line_edit(self, placeholder):
        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        return line_edit

    def create_facility_combo(self):
        # Dynamically populate facilities from database
        facilities = self.db_manager.get_facilities()
        facility_combo = QtWidgets.QComboBox()
        
        for facility in facilities:
            facility_text = f"{facility['facility_name']} - Rp {facility['price']}"
            facility_combo.addItem(facility_text, facility['id'])
        
        return facility_combo

    def add_room_type_field(self):
        # Clear any previously added room type fields to avoid duplicates
        for widget in self.room_widgets:
            widget[0].clear()
            widget[1].clear()

        # Get available room types from the database
        room_types = self.db_manager.get_room_types()

        # Create a new room type combobox and input field for room quantity
        room_type_combobox = QtWidgets.QComboBox()
        for room_type in room_types:
            room_type_text = f"{room_type['type_name']} - Rp {room_type['price']:,}"
            room_type_combobox.addItem(room_type_text, room_type['id'])

        room_quantity_input = self.create_line_edit("Jumlah Kamar")
        room_quantity_input.setValidator(QtGui.QIntValidator(0, 10))

        # Save references to the room widgets
        self.room_widgets.append((room_type_combobox, room_quantity_input))

        # Create a widget to hold the room type combobox and quantity input
        room_layout_item = QtWidgets.QWidget()
        room_layout_item.setLayout(QtWidgets.QVBoxLayout())
        room_layout_item.layout().addWidget(QtWidgets.QLabel("Jenis Kamar:"))
        room_layout_item.layout().addWidget(room_type_combobox)
        room_layout_item.layout().addWidget(QtWidgets.QLabel("Jumlah Kamar:"))
        room_layout_item.layout().addWidget(room_quantity_input)

        # Add the room layout item to the room layout
        self.room_layout.addWidget(room_layout_item)


    def calculate_total_price(self):
        total_price = 0

        # Mengambil jumlah orang
        try:
            num_people = int(self.people_count_input.text())
        except ValueError:
            num_people = 1  # Default 1 orang jika input tidak valid

        # Mengambil harga fasilitas
        fasilitas_text = self.fasilitas_combo.currentText()
        facility_price = int(float(fasilitas_text.split(" - Rp ")[1].replace(".", "").replace(",", "")))
        total_price += facility_price * num_people  # Fasilitas dihitung per orang

        # Mengambil harga kamar dan jumlah kamar
        for room_type_combobox, room_quantity_input in self.room_widgets:
            room_type_text = room_type_combobox.currentText()
            room_price = int(float(room_type_text.split(" - Rp ")[1].replace(".", "").replace(",", "")))
            
            try:
                room_quantity = int(room_quantity_input.text())
                if room_quantity > 0:  # Pastikan jumlah kamar lebih besar dari 0
                    total_price += room_price * room_quantity * num_people  # Harga kamar per orang
            except ValueError:
                pass  # Jika input tidak valid, abaikan

        # Update total price label
        self.total_price_label.setText(f"Total Harga: Rp {total_price:,}")
        return total_price


    def go_back_to_pet(self):
        subprocess.Popen(["python", "pet.py"])

    def go_to_bayar(self):
        try:
            # Create reservation
            reservation_id = self.create_reservation()
            
            if reservation_id:
                # Get reservation details
                reservation = self.db_manager.get_reservation_details(reservation_id)
                
                # Show success message with reservation details
                message = f"""
                Reservasi berhasil!
                Nomor Pesanan: {reservation_id}
                Nama: {reservation['customer_name']}
                Check-in: {reservation['check_in_date']}
                Check-out: {reservation['check_out_date']}
                Total Orang: {reservation['total_people']}
                Total Harga: Rp {reservation['total_price']:,.2f}
                """
                
                QtWidgets.QMessageBox.information(None, "Reservasi Sukses", message)
                
                # Proceed to payment
                subprocess.Popen(["python", "bayar.py"])
            else:
                QtWidgets.QMessageBox.warning(None, "Reservasi Gagal", "Gagal membuat reservasi. Silakan coba lagi.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", str(e))
        
    def create_reservation(self):
        # Validate inputs
        if not self.name_input.text():
            raise ValueError("Nama harus diisi")
        
        if not self.ktp_input.text():
            raise ValueError("Nomor KTP harus diisi")

        # Collect form data
        name = self.name_input.text()
        ktp = self.ktp_input.text()
        check_in_date = self.check_in_date.date().toString("yyyy-MM-dd")
        check_out_date = self.check_out_date.date().toString("yyyy-MM-dd")
        
        # Facility selection
        facility_id = self.fasilitas_combo.currentData()
        
        # Room selection
        room_type_combobox, room_quantity_input = self.room_widgets[0]
        room_type_id = room_type_combobox.currentData()
        room_quantity = int(room_quantity_input.text())
        
        # Get available rooms
        available_rooms = self.db_manager.get_available_rooms(
            check_in_date, 
            check_out_date, 
            room_type_id
        )
        
        # Select rooms
        room_ids = [room['id'] for room in available_rooms[:room_quantity]]
        
        # People count
        try:
            total_people = int(self.people_count_input.text())
        except ValueError:
            total_people = 1
        
        # Calculate total price
        total_price = self.calculate_total_price()
        
        # Voucher code (optional)
        # voucher_code = self.voucher_input.text().strip()
        
        # Add customer
        customer_id = self.db_manager.add_customer(
            name, 
            "N/A", 
            ktp, 
            "N/A"
        )
        
        # Create reservation
        reservation_id = self.db_manager.create_reservation(
            customer_id, 
            check_in_date, 
            check_out_date, 
            total_people, 
            total_price, 
            room_ids, 
            [facility_id]
            # voucher_code
        )
        
        return reservation_id

    def add_form_field(self, label_text, widget):
        label = QtWidgets.QLabel(label_text)
        self.scroll_layout.addRow(label, widget)

    def create_combo(self, items):
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        return combo

    def create_date_edit(self):
        date_edit = QtWidgets.QDateTimeEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDisplayFormat("dd/MM/yyyy")
        date_edit.setDate(QtCore.QDate.currentDate())
        return date_edit

    def create_button(self, text):
        button = QtWidgets.QPushButton(text)
        button.setFixedHeight(40)
        return button

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import subprocess
import schedule
import threading
import time
from databasemanager import DatabaseManager
from invo import Ui_MainWindow as InvoiceWindow

class Ui_MainWindow(object):
    def __init__(self, reservation_data=None):
        self.reservation_data = reservation_data
        self.db_manager = DatabaseManager()
        self.invoice_window = None 
        self.original_total = 0
        self.discounted_total = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Pembayaran Reservasi Hotel")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: #1e1e2f;")  # Dark background

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create a QScrollArea
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidgetResizable(True)

        # Create a container widget for the layout
        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        # Layout utama
        self.layout = QtWidgets.QVBoxLayout(self.scroll_area_widget)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        # Judul
        self.title_label = QtWidgets.QLabel("FORM PEMBAYARAN")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #e0e0e0; text-shadow: 2px 2px 4px #000000;")
        self.layout.addWidget(self.title_label)

        # Customer Dropdown
        self.customer_label = QtWidgets.QLabel("Nama Pemesan:")
        self.customer_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.customer_combo = QtWidgets.QComboBox()
        self.customer_combo.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        self.layout.addWidget(self.customer_label)
        self.layout.addWidget(self.customer_combo)

        # Reservation Dropdown
        self.reservation_label = QtWidgets.QLabel("Nomor Pemesanan:")
        self.reservation_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.reservation_combo = QtWidgets.QComboBox()
        self.reservation_combo.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        self.layout.addWidget(self.reservation_label)
        self.layout.addWidget(self.reservation_combo)

        # Voucher Input
        self.voucher_label = QtWidgets.QLabel("Kode Voucher (Optional):")
        self.voucher_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.voucher_input = QtWidgets.QLineEdit()
        self.voucher_input.setPlaceholderText("Masukkan kode voucher jika ada")
        self.voucher_input.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        self.voucher_button = QtWidgets.QPushButton("Verifikasi Voucher")
        self.voucher_button.setStyleSheet("""
            background-color: #4285f4; 
            color: white; 
            font-weight: bold; 
            padding: 10px; 
            border-radius: 10px;
            font-size: 14px;
            text-shadow: 1px 1px 3px #000000;
        """)
        self.voucher_button.clicked.connect(self.verify_voucher)
        
        # Voucher layout
        self.voucher_layout = QtWidgets.QHBoxLayout()
        self.voucher_layout.addWidget(self.voucher_input)
        self.voucher_layout.addWidget(self.voucher_button)
        
        self.layout.addWidget(self.voucher_label)
        self.layout.addLayout(self.voucher_layout)

        # Metode Pembayaran
        self.payment_label = QtWidgets.QLabel("Metode Pembayaran:")
        self.payment_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.payment_combo = QtWidgets.QComboBox()
        self.payment_combo.addItems(["Pilih Metode", "Cash", "Kartu Kredit", "Transfer Bank", "e-Wallet"])
        self.payment_combo.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        self.layout.addWidget(self.payment_label)
        self.layout.addWidget(self.payment_combo)

        # Total Pembayaran
        self.total_label = QtWidgets.QLabel("Total Pembayaran (Rp):")
        self.total_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.total_input = QtWidgets.QLineEdit()
        self.total_input.setReadOnly(True)  # Make read-only to prevent manual editing
        self.total_input.setPlaceholderText("Total akan ditampilkan otomatis")
        self.total_input.setValidator(QtGui.QIntValidator(0, 999999999))
        self.total_input.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        
        # Discount Label
        self.discount_label = QtWidgets.QLabel("Diskon:")
        self.discount_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.discount_input = QtWidgets.QLineEdit()
        self.discount_input.setReadOnly(True)
        self.discount_input.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        
        # Total layout
        self.total_detail_layout = QtWidgets.QHBoxLayout()
        self.total_detail_layout.addWidget(self.total_label)
        self.total_detail_layout.addWidget(self.discount_label)
        
        self.total_input_layout = QtWidgets.QHBoxLayout()
        self.total_input_layout.addWidget(self.total_input)
        self.total_input_layout.addWidget(self.discount_input)
        
        self.layout.addLayout(self.total_detail_layout)
        self.layout.addLayout(self.total_input_layout)

        # Add a stretch to push the buttons to the bottom
        self.layout.addStretch(1)

        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        self.confirm_button = QtWidgets.QPushButton("Konfirmasi")
        self.confirm_button.setStyleSheet("""
            background-color: #ff77ff; 
            color: white; 
            font-weight: bold; 
            padding: 20px; 
            border-radius: 15px;
            font-size: 18px;
            text-shadow: 1px 1px 3px #000000;
        """)
        self.confirm_button.clicked.connect(self.confirm_payment)
        self.button_layout.addWidget(self.confirm_button)

        self.cancel_button = QtWidgets.QPushButton("Batal")
        self.cancel_button.setStyleSheet("""
            background-color: #ff416c; 
            color: white; 
            font-weight: bold; 
            padding: 20px; 
            border-radius: 15px;
            font-size: 18px;
            text-shadow: 1px 1px 3px #000000;
        """)
        self.cancel_button.clicked.connect(MainWindow.close)
        self.button_layout.addWidget(self.cancel_button)

        self.back_button = QtWidgets.QPushButton("Kembali")
        self.back_button.setStyleSheet("""
            background-color: #4285f4; 
            color: white; 
            font-weight: bold; 
            padding: 20px; 
            border-radius: 15px;
            font-size: 18px;
            text-shadow: 1px 1px 3px #000000;
        """)
        self.back_button.clicked.connect(self.go_back)
        self.button_layout.addWidget(self.back_button)

        self.layout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.scroll_area)

        # Connect signals after UI setup
        self.customer_combo.currentIndexChanged.connect(self.load_customer_reservations)
        self.reservation_combo.currentIndexChanged.connect(self.load_reservation_total)

        # Populate customers
        self.start_room_status_scheduler()
        self.populate_customers()

    def update_rooms(self):
        """Update room status after checkout times"""
        try:
            self.db_manager.update_room_status_after_checkout()
            print("Room status updated successfully")
        except Exception as e:
            print(f"Error updating room status: {e}")

    def start_room_status_scheduler(self):
        """Start a background thread for room status scheduling"""
        def schedule_thread():
            schedule.every().day.at("00:00").do(self.update_rooms)
            while True:
                schedule.run_pending()
                time.sleep(1)

        # Start scheduler in a background thread
        scheduler_thread = threading.Thread(target=schedule_thread, daemon=True)
        scheduler_thread.start()

    def populate_customers(self):
        # Clear existing items
        self.customer_combo.clear()
        self.customer_combo.addItem("Pilih Pelanggan")
        
        # Get customers with active reservations from database
        query = """
        SELECT DISTINCT c.id, c.name, c.email, c.phone
        FROM customers c
        JOIN reservations r ON c.id = r.customer_id
        WHERE r.status != 'Cancelled'
        ORDER BY c.name
        """
        
        # Execute the query
        self.db_manager.cursor.execute(query)
        customers = self.db_manager.cursor.fetchall()
        
        # Populate customer dropdown
        for customer in customers:
            # Fallback to phone or some other unique identifier if email not available
            identifier = customer.get('email', customer.get('phone', 'No Contact'))
            self.customer_combo.addItem(
                f"{customer['name']} - {identifier}", 
                customer['id']
            )

    def load_customer_reservations(self):
        # Clear previous reservations
        self.reservation_combo.clear()
        self.reservation_combo.addItem("Pilih Reservasi")
        
        # Get current selected customer
        customer_index = self.customer_combo.currentIndex()
        if customer_index > 0:
            customer_id = self.customer_combo.currentData()
            
            try:
                # Fetch reservations for the customer with status not cancelled
                query = """
                SELECT r.id, r.check_in_date, r.check_out_date, r.total_price, r.status, 
                    c.name AS customer_name
                FROM reservations r
                JOIN customers c ON r.customer_id = c.id
                WHERE r.customer_id = %s AND r.status != 'Cancelled'
                ORDER BY r.check_in_date DESC
                """
                
                # Using the database manager's cursor to execute the query
                self.db_manager.cursor.execute(query, (customer_id,))
                reservations = self.db_manager.cursor.fetchall()
                    
                # Populate reservation dropdown
                for reservation in reservations:
                    display_text = (
                        f"Reservasi {reservation['id']} - "
                        f"Check-in: {reservation['check_in_date']} - "
                        f"Status: {reservation['status']} - "
                        f"Total: Rp {reservation['total_price']:,}"
                    )
                    self.reservation_combo.addItem(display_text, reservation['id'])
                
                # If no reservations found, show a message
                if len(reservations) == 0:
                    QtWidgets.QMessageBox.information(
                        None, 
                        "Informasi", 
                        "Pelanggan tidak memiliki reservasi aktif."
                    )
            
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "Error", f"Gagal memuat reservasi: {str(e)}")

    def load_reservation_total(self):
        # Reset voucher and discount
        self.voucher_input.clear()
        self.discount_input.setText("0")
        
        # Get current selected reservation
        reservation_index = self.reservation_combo.currentIndex()
        if reservation_index > 0:
            reservation_id = self.reservation_combo.currentData()
            
            # Get reservation details
            try:
                reservation = self.db_manager.get_reservation_details(reservation_id)
                
                if reservation:
                    # Store original total
                    self.original_total = int(reservation['total_price'])
                    self.discounted_total = self.original_total
                    
                    # Set total in the input field
                    self.total_input.setText(f"{self.original_total:,}")
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "Error", f"Gagal memuat detail reservasi: {str(e)}")

    def verify_voucher(self):
        # Get voucher code
        voucher_code = self.voucher_input.text().strip()
        
        if not voucher_code:
            QtWidgets.QMessageBox.warning(None, "Peringatan", "Masukkan kode voucher!")
            return
        
        # Verify voucher
        voucher = self.db_manager.verify_voucher(voucher_code)
        
        if voucher:
            # Calculate discount
            discount_percentage = voucher['discount_percentage']
            discount_amount = int(self.original_total * (discount_percentage / 100))
            
            # Apply discount
            self.discounted_total = self.original_total - discount_amount
            
            # Update UI
            self.total_input.setText(f"{self.discounted_total:,}")
            self.discount_input.setText(f"{discount_amount:,}")
            
            QtWidgets.QMessageBox.information(
                None, 
                "Voucher Berhasil", 
                f"Voucher berhasil digunakan! Diskon {discount_percentage}%"
            )
        else:
            # Reset to original total
            self.discounted_total = self.original_total
            self.total_input.setText(f"{self.original_total:,}")
            self.discount_input.setText("0")
            
            QtWidgets.QMessageBox.warning(
                None, 
                "Voucher Tidak Valid", 
                "Kode voucher tidak valid atau sudah tidak berlaku."
            )

    def confirm_payment(self):
        # Validasi input
        if (self.customer_combo.currentIndex() <= 0 or 
            self.reservation_combo.currentIndex() <= 0 or 
            self.payment_combo.currentText() == "Pilih Metode"):
            QtWidgets.QMessageBox.warning(None, "Peringatan", "Semua kolom harus diisi!")
            return

        try:
            # Ambil semua detail pembayaran
            customer_name = self.customer_combo.currentText().split(' - ')[0]
            reservation_id = self.reservation_combo.currentData()
            payment_method = self.payment_combo.currentText()
            payment_date = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
            total = int(self.total_input.text().replace('.', '').replace(',', ''))

            # Validasi total pembayaran
            if total < 1:
                QtWidgets.QMessageBox.warning(
                    None, "Peringatan", 
                    "Total pembayaran harus minimal Rp 10,000!"
                )
                return

            # Simpan detail pembayaran ke database
            success = self.db_manager.save_payment(
                reservation_id=reservation_id,
                payment_date=payment_date,
                amount=total,
                payment_method=payment_method
            )

            if success:
                # Update reservation status
                self.db_manager.update_reservation_status(reservation_id, 'Confirmed')

                # Open Invoice Window
                self.open_invoice_window(reservation_id)

                QtWidgets.QMessageBox.information(
                    None, "Sukses", 
                    "Pembayaran berhasil disimpan!"
                )
            else:
                QtWidgets.QMessageBox.warning(
                    None, "Gagal", 
                    "Gagal menyimpan pembayaran. Silakan coba lagi!"
                )
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                None, "Error", f"Terjadi kesalahan: {str(e)}"
            )
            
    def open_invoice_window(self, reservation_id):
        # Buat jendela invoice baru
        self.invoice_window = QtWidgets.QMainWindow()
        ui_invoice = InvoiceWindow()
        ui_invoice.setupUi(self.invoice_window, reservation_id)
        QtWidgets.QApplication.activeWindow().close()
        # Tampilkan jendela invoice
        self.invoice_window.show()  # Ganti dari showMaximized()

    def go_back(self):
        # Open previous reservation window
        subprocess.Popen(["python", "reser.py"])
        # Close current window
        QtWidgets.QApplication.activeWindow().close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
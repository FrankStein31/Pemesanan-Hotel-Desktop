from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import subprocess
from databasemanager import DatabaseManager
from invo import Ui_MainWindow as InvoiceWindow

class Ui_MainWindow(object):
    def __init__(self, reservation_data=None):
        self.reservation_data = reservation_data
        self.db_manager = DatabaseManager()
        self.invoice_window = None 

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
        self.total_input.setValidator(QtGui.QDoubleValidator(0, 999999999, 2))
        self.total_input.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        self.layout.addWidget(self.total_label)
        self.layout.addWidget(self.total_input)

        # Voucher Code
        # self.voucher_label = QtWidgets.QLabel("Voucher Code (Optional):")
        # self.voucher_label.setStyleSheet("""
        #     color: #ffffff;
        #     font-family: 'Roboto', sans-serif;
        #     font-size: 16px;
        # """)
        # self.voucher_input = QtWidgets.QLineEdit()
        # self.voucher_input.setPlaceholderText("Masukkan kode voucher (jika ada)")
        # self.voucher_input.setStyleSheet("""
        #     padding: 12px; 
        #     font-size: 14px; 
        #     border: 2px solid #ff77ff; 
        #     border-radius: 12px; 
        #     background-color: #2e2e3e; 
        #     color: #ffffff;
        #     font-family: 'Roboto', sans-serif;
        # """)
        # self.layout.addWidget(self.voucher_label)
        # self.layout.addWidget(self.voucher_input)

        # Verify Voucher Button
        # self.verify_voucher_button = QtWidgets.QPushButton("Verify Voucher")
        # self.verify_voucher_button.setStyleSheet("""
        #     background-color: #4285f4; 
        #     color: white; 
        #     font-weight: bold; 
        #     padding: 10px; 
        #     border-radius: 10px;
        #     font-size: 14px;
        #     text-shadow: 1px 1px 3px #000000;
        # """)
        # self.verify_voucher_button.clicked.connect(self.verify_voucher)
        # self.layout.addWidget(self.verify_voucher_button)

        # Discounted Total Label
        # self.discounted_total_label = QtWidgets.QLabel("Total (Rp):")
        # self.discounted_total_label.setStyleSheet("""
        #     color: #ffffff;
        #     font-family: 'Roboto', sans-serif;
        #     font-size: 16px;
        # """)
        # self.discounted_total_value = QtWidgets.QLabel("Rp 0")
        # self.discounted_total_value.setStyleSheet("""
        #     color: #ff77ff;
        #     font-family: 'Roboto', sans-serif;
        #     font-size: 16px;
        #     font-weight: bold;
        # """)
        # self.layout.addWidget(self.discounted_total_label)
        # self.layout.addWidget(self.discounted_total_value)

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
        self.populate_customers()

    def populate_customers(self):
        # Clear existing items
        self.customer_combo.clear()
        self.customer_combo.addItem("Pilih Pelanggan")
        
        # Get customers from database
        customers = self.db_manager.get_customers()
        
        # Populate customer dropdown
        for customer in customers:
            self.customer_combo.addItem(
                f"{customer['name']} - {customer['email']}", 
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
            
            # Query reservations for this customer (you might need to add this method to DatabaseManager)
            try:
                query = """
                SELECT id, check_in_date, check_out_date, total_price 
                FROM reservations 
                WHERE customer_id = %s AND status != 'Cancelled'
                """
                self.db_manager.cursor.execute(query, (customer_id,))
                reservations = self.db_manager.cursor.fetchall()
                
                # Populate reservation dropdown
                for reservation in reservations:
                    display_text = (
                        f"Reservasi {reservation['id']} - "
                        f"Check-in: {reservation['check_in_date']} - "
                        f"Total: Rp {reservation['total_price']:,.2f}"
                    )
                    self.reservation_combo.addItem(display_text, reservation['id'])
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "Error", f"Gagal memuat reservasi: {str(e)}")

    def load_reservation_total(self):
        # Get current selected reservation
        reservation_index = self.reservation_combo.currentIndex()
        if reservation_index > 0:
            reservation_id = self.reservation_combo.currentData()
            
            # Get reservation details
            reservation = self.db_manager.get_reservation_details(reservation_id)
            
            if reservation:
                # Set total in the input field
                self.total_input.setText(f"{reservation['total_price']:,.2f}")

    # def verify_voucher(self):
    #     voucher_code = self.voucher_input.text()
    #     if not voucher_code:
    #         QtWidgets.QMessageBox.warning(None, "Peringatan", "Masukkan kode voucher!")
    #         return

    #     # Use database method to verify voucher
    #     voucher = self.db_manager.verify_voucher(voucher_code)
    #     if voucher:
    #         # Get total price from input
    #         try:
    #             total_price = float(self.total_input.text().replace('.', '').replace(',', ''))
    #             discount_percentage = voucher['discount_percentage']
                
    #             # Calculate discounted total
    #             discount_amount = total_price * (discount_percentage / 100)
    #             discounted_total = total_price - discount_amount

    #             QtWidgets.QMessageBox.information(
    #                 None, 
    #                 "Voucher Valid", 
    #                 f"Voucher berhasil diverifikasi!\nDiskon: {discount_percentage}%\nPotongan: Rp {discount_amount:.2f}"
    #             )

    #             # Update total with discount
    #             self.discounted_total_value.setText(f"Rp {discounted_total:,.2f}")
    #             self.total_input.setText(f"{discounted_total:,.2f}")
    #         except ValueError:
    #             QtWidgets.QMessageBox.warning(None, "Error", "Pilih reservasi terlebih dahulu!")
    #     else:
    #         QtWidgets.QMessageBox.warning(None, "Voucher Invalid", "Voucher tidak valid atau sudah kadaluarsa!")

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
            reservation_id = self.reservation_combo.currentData()  # ID reservasi
            payment_method = self.payment_combo.currentText()
            payment_date = QtCore.QDate.currentDate().toString("yyyy-MM-dd")  # Ambil tanggal hari ini
            total = float(self.total_input.text().replace('.', '').replace(',', ''))

            # Validasi total pembayaran
            if total < 10000:
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
                # Open Invoice Window
                self.open_invoice_window()

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

    def open_invoice_window(self):
        # Buat jendela invoice baru
        self.invoice_window = QtWidgets.QMainWindow()
        ui_invoice = InvoiceWindow()
        ui_invoice.setupUi(self.invoice_window)
        
        # Tampilkan jendela invoice dalam mode maksimum
        self.invoice_window.showMaximized()

    def go_back(self):
        subprocess.Popen(["python", "reser.py"])  # Open reser.py when "Kembali" is clicked
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

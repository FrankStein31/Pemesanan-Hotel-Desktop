# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess  # Untuk menjalankan file eksternal
from databasemanager import DatabaseManager
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime, timedelta

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, reservation_id):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 900)  # Optional resize before maximizing
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #ffffff, stop:1 #d7f0f4
            );
        """)

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)

        # Title with gradient background
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setText("BUKTI PEMBAYARAN")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #00c6ff, stop:1 #0072ff
            );
            border-radius: 10px;
            padding: 20px;
        """)
        self.mainLayout.addWidget(self.titleLabel)

        # Hotel Name
        self.hotelNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.hotelNameLabel.setText("Hotel Acumalaka")
        self.hotelNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hotelNameLabel.setStyleSheet("font-size: 20px; color: #005073; font-weight: bold;")
        self.mainLayout.addWidget(self.hotelNameLabel)

        # Decorative Line
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setStyleSheet("background-color: #005073; height: 2px;")
        self.mainLayout.addWidget(self.line)

        # Reservation Details
        self.detailsLayout = QtWidgets.QFormLayout()
        self.detailsLayout.setHorizontalSpacing(30)
        self.detailsLayout.setVerticalSpacing(10)

        self.add_detail("Nama Pelanggan:", "")
        self.add_detail("Nomor Pemesanan:", "")
        self.add_detail("Nomor Kamar:", "")
        self.add_detail("Jenis Kamar:", "")
        self.add_detail("Jumlah Kamar:", "")
        self.add_detail("Tanggal Check-In:", "")
        self.add_detail("Tanggal Check-Out:", "")
        self.add_detail("Total Hari:", "")
        self.add_detail("Jumlah Orang Menginap:", "")
        self.add_detail("Fasilitas:", "")
        self.add_detail("Metode Pembayaran:", "")
        self.add_detail("Total Pembayaran:", "")

        self.mainLayout.addLayout(self.detailsLayout)

        # Footer Section
        self.thankYouLabel = QtWidgets.QLabel("Terima kasih telah memilih Hotel Acumalaka!")
        self.thankYouLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.thankYouLabel.setStyleSheet("font-size: 16px; font-style: italic; color: #0072ff;")
        self.mainLayout.addWidget(self.thankYouLabel)

        self.signatureLabel = QtWidgets.QLabel("Tertanda,\nManajer Hotel Acumalaka")
        self.signatureLabel.setAlignment(QtCore.Qt.AlignRight)
        self.signatureLabel.setStyleSheet("font-size: 14px; color: #333;")
        self.mainLayout.addWidget(self.signatureLabel)

        # Buttons Layout (Back and Finish)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # Back Button
        self.backButton = QtWidgets.QPushButton("Kembali")
        self.backButton.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px;
            font-family: 'Helvetica', sans-serif;
            transition: background-color 0.3s ease;
        """)
        self.backButton.clicked.connect(self.go_back)
        self.buttonLayout.addWidget(self.backButton)

        # Finish Button
        self.finishButton = QtWidgets.QPushButton("Selesai")
        self.finishButton.setStyleSheet("""
            background-color: #FF6347;
            color: white;
            font-weight: bold;
            border-radius: 15px;
            padding: 10px;
            font-family: 'Helvetica', sans-serif;
            transition: background-color 0.3s ease;
        """)
        self.finishButton.clicked.connect(self.finish_action)
        self.buttonLayout.addWidget(self.finishButton)

        self.mainLayout.addLayout(self.buttonLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.reservation_id = reservation_id
        # self.load_latest_payment_details()
        self.load_latest_payment_details(self.reservation_id)

    def add_detail(self, label_text, value_text):
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #005073;")
        value = QtWidgets.QLabel(value_text)
        value.setStyleSheet("font-size: 16px; color: #333;")
        self.detailsLayout.addRow(label, value)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Invoice Pembayaran"))

    def go_back(self):
        try:
            # Tutup jendela saat ini terlebih dahulu
            MainWindow = self.centralwidget.window()
            MainWindow.close()
            
            # Buka jendela pembayaran
            subprocess.Popen(["python", "bayar.py"])
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Gagal kembali ke halaman pembayaran: {e}")

    def finish_action(self):
        try:
            # Tutup jendela saat ini terlebih dahulu
            MainWindow = self.centralwidget.window()
            MainWindow.close()
            
            # Buka halaman logout
            subprocess.Popen(["python", "logout.py"])
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Gagal menyelesaikan proses: {e}")

    def load_latest_payment_details(self, reservation_id=None):
        # Use DatabaseManager to get the latest payment details
        db_manager = DatabaseManager()
        
        try:
            # Modifikasi query untuk mendapatkan reservasi spesifik jika reservation_id diberikan
            if reservation_id:
                query = """
                SELECT reservation_id, payment_date, amount, payment_method
                FROM payments
                WHERE reservation_id = %s
                ORDER BY payment_date DESC
                LIMIT 1
                """
                db_manager.cursor.execute(query, (reservation_id,))
            else:
                query = """
                SELECT reservation_id, payment_date, amount, payment_method
                FROM payments
                ORDER BY payment_date DESC
                LIMIT 1
                """
                db_manager.cursor.execute(query)
            
            payment_details = db_manager.cursor.fetchone()
            
            if payment_details:
                # Get full reservation details using the reservation ID
                reservation_details = db_manager.get_reservation_details(payment_details['reservation_id'])
                
                if reservation_details:
                    # Combine payment and reservation details
                    merged_details = {**payment_details, **reservation_details}
                    self.update_invoice_details(merged_details)
        except Exception as e:
            print(f"Error loading payment details: {e}")
            QMessageBox.critical(None, "Error", f"Could not load payment details: {e}")
        finally:
            db_manager.close()

    def update_invoice_details(self, details):
        # Convert datetime objects to formatted date strings
        check_in_date = details['check_in_date'].strftime("%Y-%m-%d") if details['check_in_date'] else "N/A"
        check_out_date = details['check_out_date'].strftime("%Y-%m-%d") if details['check_out_date'] else "N/A"
        
        # Calculate total days
        total_days = (details['check_out_date'] - details['check_in_date']).days if details['check_in_date'] and details['check_out_date'] else 0
        
        # Format room details
        room_details = ", ".join([f"{room['room_number']} ({room['type_name']})" for room in details.get('rooms', [])])
        
        # Format facilities details
        facility_details = ", ".join([f"{facility['facility_name']}" for facility in details.get('facilities', [])])
        
        # Prepare details for form
        amount = details.get('amount', 0)

        invoice_details = [
            ("Nama Pelanggan:", details.get('customer_name', 'N/A')),
            ("Nomor Pemesanan:", str(details.get('id', 'N/A'))),
            ("Nomor Kamar:", room_details),
            ("Jenis Kamar:", room_details),
            ("Jumlah Kamar:", str(len(details.get('rooms', [])))),
            ("Tanggal Check-In:", check_in_date),
            ("Tanggal Check-Out:", check_out_date),
            ("Total Hari:", str(total_days)),
            ("Jumlah Orang Menginap:", str(details.get('total_people', 0))),
            ("Fasilitas:", facility_details),
            ("Metode Pembayaran:", details.get('payment_method', 'N/A')),
            ("Total Pembayaran:", f"Rp {int(amount):,}")
        ]
        
        # Clear existing details
        while self.detailsLayout.rowCount() > 0:
            self.detailsLayout.removeRow(0)
        
        # Add new details
        for label_text, value_text in invoice_details:
            self.add_detail(label_text, str(value_text))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    
    # Use a default reservation ID for testing, or use the first argument if provided
    reservation_id = sys.argv[1] if len(sys.argv) > 1 else 1  # Default to 1 if no argument
    
    ui.setupUi(MainWindow, reservation_id)
    
    # Open the window maximized (full-screen size)
    MainWindow.showMaximized()

    sys.exit(app.exec_())

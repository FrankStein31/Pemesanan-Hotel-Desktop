from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess  # To run reser.py when back is clicked

class Ui_MainWindow(object):
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

        # Nama Pemesan
        self.name_label = QtWidgets.QLabel("Nama Pemesan:")
        self.name_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Masukkan nama pemesan")
        self.name_input.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        # Nomor Pemesanan
        self.booking_label = QtWidgets.QLabel("Nomor Pemesanan:")
        self.booking_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.booking_input = QtWidgets.QLineEdit()
        self.booking_input.setPlaceholderText("Masukkan nomor pemesanan")
        self.booking_input.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        self.layout.addWidget(self.booking_label)
        self.layout.addWidget(self.booking_input)

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
        self.total_input.setPlaceholderText("Masukkan total pembayaran")
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
        self.voucher_label = QtWidgets.QLabel("Voucher Code (Optional):")
        self.voucher_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.voucher_input = QtWidgets.QLineEdit()
        self.voucher_input.setPlaceholderText("Masukkan kode voucher (jika ada)")
        self.voucher_input.setStyleSheet("""
            padding: 12px; 
            font-size: 14px; 
            border: 2px solid #ff77ff; 
            border-radius: 12px; 
            background-color: #2e2e3e; 
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
        """)
        self.layout.addWidget(self.voucher_label)
        self.layout.addWidget(self.voucher_input)

        # New label to display the discounted total
        self.discounted_total_label = QtWidgets.QLabel("Total Setelah Diskon (Rp):")
        self.discounted_total_label.setStyleSheet("""
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
        """)
        self.discounted_total_value = QtWidgets.QLabel("Rp 0")
        self.discounted_total_value.setStyleSheet("""
            color: #ff77ff;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            font-weight: bold;
        """)
        self.layout.addWidget(self.discounted_total_label)
        self.layout.addWidget(self.discounted_total_value)

        # Add a stretch to push the buttons to the bottom
        self.layout.addStretch(1)

        # Tombol Konfirmasi Pembayaran
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

    def confirm_payment(self):
        nama = self.name_input.text()
        nomor = self.booking_input.text()
        metode = self.payment_combo.currentText()
        total = self.total_input.text()
        voucher = self.voucher_input.text()

        # Pastikan semua kolom sudah diisi
        if not nama or not nomor or metode == "Pilih Metode" or not total:
            QtWidgets.QMessageBox.warning(None, "Peringatan", "Semua kolom harus diisi!")
        else:
            try:
                total = float(total)  # Pastikan total adalah angka
                discount = 0
                if voucher == "SAY5":  # Kode voucher yang memberikan potongan 5%
                    discount = 0.05 * total
                elif voucher == "SAY10":  # Kode voucher yang memberikan potongan 10%
                    discount = 0.10 * total
                total -= discount  # Mengurangi diskon dari total
                total = round(total, 2)  # Membulatkan hasil total ke dua desimal

                # Update label total setelah diskon
                self.discounted_total_value.setText(f"Rp {total}")

                # Cek apakah total pembayaran lebih dari 10 juta
                if total >= 10000000:
                    # Status menunggu konfirmasi admin
                    QtWidgets.QMessageBox.information(
                        None,
                        "Pembayaran Tertunda",
                        f"Pembayaran Anda sedang menunggu konfirmasi admin.\nTotal Pembayaran: Rp {total}",
                    )
                else:
                    # Jika pembayaran kurang dari 10 juta, langsung konfirmasi
                    QtWidgets.QMessageBox.information(
                        None,
                        "Pembayaran Berhasil",
                        f"Terima kasih, {nama}!\n\nDetail Pembayaran:\nNomor Pemesanan: {nomor}\nMetode: {metode}\nTotal: Rp {total}\nVoucher Discount: Rp {discount}",
                    )
                    subprocess.Popen(["python", "invo.py"])  # Menjalankan invo.py jika konfirmasi berhasil

            except ValueError:
                QtWidgets.QMessageBox.warning(None, "Error", "Total pembayaran tidak valid!")

    def go_back(self):
        subprocess.Popen(["python", "reser.py"])  # Open reser.py when "Kembali" is clicked


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

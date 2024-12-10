# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess  # Untuk menjalankan file eksternal

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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

        self.add_detail("Nama Pelanggan:", "Bima Sakti")
        self.add_detail("Nomor Pemesanan:", "IP778")
        self.add_detail("Nomor Kamar:", "305, 306")
        self.add_detail("Jenis Kamar:", "Deluxe Room")
        self.add_detail("Jumlah Kamar:", "2")
        self.add_detail("Tanggal Check-In:", "2024-12-01")
        self.add_detail("Tanggal Check-Out:", "2024-12-05")
        self.add_detail("Total Hari:", "4")
        self.add_detail("Jumlah Orang Menginap:", "2 Orang")
        self.add_detail("Fasilitas:", "Gym")
        self.add_detail("Metode Pembayaran:", "Cash")
        self.add_detail("Total Pembayaran:", "Rp 4,000,000")

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
        """Action for 'Back' button"""
        print("Kembali ke menu utama")
        subprocess.Popen(["python", "pet.py"])  # Open pet.py
        QtWidgets.QApplication.quit()  # Close current window

    def finish_action(self):
        """Action for 'Finish' button"""
        print("Selesai - Anda telah selesai dengan pembayaran.")
        subprocess.Popen(["python", "logout.py"])  # Open logout.py
        QtWidgets.QApplication.quit()  # Close current window


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    # Open the window maximized (full-screen size)
    MainWindow.showMaximized()

    sys.exit(app.exec_())

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

# Import window-window lain
from reser import Ui_MainWindow as ReservationWindow
from riwa import Ui_MainWindow as HistoryWindow
from gale import Ui_MainWindow as GalleryWindow
from logout import Ui_MainWindow as LogoutWindow

class BimaProfileWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set up the profile window for Bima
        self.setWindowTitle("Staff Profile - Bima")
        self.setFixedSize(400, 300)

        # Layout for the profile window
        layout = QtWidgets.QVBoxLayout(self)

        # Profile Picture (Placeholder)
        self.profile_pic = QtWidgets.QLabel(self)
        self.profile_pic.setPixmap(QtGui.QPixmap("bima_profile.jpg"))  # Placeholder image for Bima's profile
        self.profile_pic.setAlignment(QtCore.Qt.AlignCenter)
        self.profile_pic.setScaledContents(True)
        layout.addWidget(self.profile_pic)

        # Bima's Info
        self.bima_name = QtWidgets.QLabel("Staff Name: Bima", self)
        self.bima_name.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.bima_name)

        self.bima_role = QtWidgets.QLabel("Role: Receptionist", self)
        self.bima_role.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.bima_role)

        self.bima_email = QtWidgets.QLabel("Email: bima@hotel.com", self)
        self.bima_email.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.bima_email)

        # Close Button
        self.close_button = QtWidgets.QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Hotel Acumalaka")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout utama
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Background dengan gambar
        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setPixmap(QtGui.QPixmap("hol.jpg"))  # Pastikan path benar
        self.background_label.setScaledContents(True)
        self.main_layout.addWidget(self.background_label)

        # Container untuk elemen-elemen
        self.overlay_widget = QtWidgets.QWidget(self.centralwidget)
        self.overlay_layout = QtWidgets.QVBoxLayout(self.overlay_widget)
        self.overlay_layout.setContentsMargins(50, 50, 50, 50)

        # Title label dengan font mewah
        self.label = QtWidgets.QLabel(self.overlay_widget)
        font = QtGui.QFont()
        font.setFamily("Lora")
        font.setPointSize(26)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("SELAMAT DATANG DI HOTEL ACUMALAKA")
        self.label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            font-size: 30px;
        """)
        self.overlay_layout.addWidget(self.label)

        # ComboBox untuk memilih jenis kamar
        self.comboBox = QtWidgets.QComboBox(self.overlay_widget)
        self.comboBox.setStyleSheet("""
            background-color: #ffffff;
            color: #333333;
            font-size: 16px;
            padding: 8px;
            border-radius: 10px;
            font-family: 'Lora', serif;
            border: 2px solid #888888;
        """)
        self.comboBox.addItem("ROOM AND SUITES")
        self.comboBox.addItem("Standart Room")
        self.comboBox.addItem("Executive Room")
        self.comboBox.addItem("Deluxe Room")
        self.comboBox.addItem("Suite Room")
        self.comboBox.addItem("Presidential Room")
        self.comboBox.currentIndexChanged.connect(self.show_rooms)
        self.overlay_layout.addWidget(self.comboBox)

        # Button layout untuk tombol-tombol lainnya
        self.button_layout = QtWidgets.QHBoxLayout()

        # Tombol Reservation
        self.pushButton_2 = QtWidgets.QPushButton("RESERVATION", self.overlay_widget)
        self.pushButton_2.setStyleSheet("""
            background-color: #d4af37;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px;
            font-family: 'Lora', serif;
            border: none;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        """)
        self.pushButton_2.clicked.connect(lambda: self.open_reservation_window(MainWindow))
        self.button_layout.addWidget(self.pushButton_2)

        # Tombol History
        self.pushButton_3 = QtWidgets.QPushButton("HISTORY", self.overlay_widget)
        self.pushButton_3.setStyleSheet("""
            background-color: #8a2be2;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px;
            font-family: 'Lora', serif;
            border: none;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        """)
        self.pushButton_3.clicked.connect(lambda: self.open_history_window(MainWindow))
        self.button_layout.addWidget(self.pushButton_3)

        # Tombol Gallery
        self.pushButton_7 = QtWidgets.QPushButton("GALLERY", self.overlay_widget)
        self.pushButton_7.setStyleSheet("""
            background-color: #2a4d8f;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px;
            font-family: 'Lora', serif;
            border: none;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        """)
        self.pushButton_7.clicked.connect(lambda: self.open_gallery_window(MainWindow))
        self.button_layout.addWidget(self.pushButton_7)

        # Tombol Staff Profile for Bima
        self.profile_button = QtWidgets.QPushButton("STAFF PROFILE", self.overlay_widget)
        self.profile_button.setStyleSheet("""
            background-color: #FF6347;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px;
            font-family: 'Lora', serif;
            border: none;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        """)
        self.profile_button.clicked.connect(self.open_bima_profile)
        self.button_layout.addWidget(self.profile_button)

        # Tombol Logout
        self.logout_button = QtWidgets.QPushButton("LOGOUT", self.overlay_widget)
        self.logout_button.setStyleSheet("""
            background-color: #e60000;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px;
            font-family: 'Lora', serif;
            border: none;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        """)
        self.logout_button.clicked.connect(lambda: self.open_logout_window(MainWindow))
        self.button_layout.addWidget(self.logout_button)

        self.overlay_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.overlay_widget)

        MainWindow.setCentralWidget(self.centralwidget)

    def show_rooms(self):
        selected = self.comboBox.currentText()
        room_details = {
            "Deluxe Room": "Harga: Rp 1.200.000/malam\nFasilitas: TV, Wi-Fi, AC, Kamar Mandi",
            "Suite Room": "Harga: Rp 2.000.000/malam\nFasilitas: TV, Wi-Fi, AC, Balkon, Kamar Mandi",
            "Presidential Room": "Harga: Rp 10.000.000/malam\nFasilitas: TV, Wi-Fi, AC, Kolam Renang Pribadi, Dua Kamar Tidur",
        }

        if selected in room_details:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(f"Detail {selected}")
            msg.setInformativeText(room_details[selected])
            msg.setWindowTitle("Room Details")
            msg.exec_()

    def open_bima_profile(self):
        self.bima_profile_window = BimaProfileWindow()
        self.bima_profile_window.show()

    def open_reservation_window(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = ReservationWindow()
        self.ui.setupUi(self.window)
        MainWindow.close()
        self.window.showMaximized()

    def open_history_window(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = HistoryWindow()
        self.ui.setupUi(self.window)
        MainWindow.close()
        self.window.showMaximized()

    def open_gallery_window(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = GalleryWindow()
        self.ui.setupUi(self.window)
        MainWindow.close()
        self.window.showMaximized()

    def open_logout_window(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = LogoutWindow()
        self.ui.setupUi(self.window)
        MainWindow.close()
        self.window.showMaximized()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
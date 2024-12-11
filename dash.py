from PyQt5 import QtCore, QtGui, QtWidgets
from gale import Ui_MainWindow as GalleryWindow
from inicr import Ui_MainWindow as MenuWindow
from riwa import Ui_MainWindow as HistoryWindow
from logout import Ui_MainWindow as LogoutWindow

class AdminProfileWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Set up the admin profile window
        self.setWindowTitle("Admin Profile - Nata")
        self.setFixedSize(400, 300)

        # Layout for the profile window
        layout = QtWidgets.QVBoxLayout(self)

        # Profile Picture (Placeholder)
        self.profile_pic = QtWidgets.QLabel(self)
        self.profile_pic.setPixmap(QtGui.QPixmap("nata_profile.jpg"))  # Placeholder image for admin profile
        self.profile_pic.setAlignment(QtCore.Qt.AlignCenter)
        self.profile_pic.setScaledContents(True)
        layout.addWidget(self.profile_pic)

        # Admin Info
        self.admin_name = QtWidgets.QLabel("Admin Name: Nata", self)
        self.admin_name.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.admin_name)

        self.admin_role = QtWidgets.QLabel("Role: Administrator", self)
        self.admin_role.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.admin_role)

        self.admin_email = QtWidgets.QLabel("Email: nata@hotel.com", self)
        self.admin_email.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.admin_email)

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

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Background Image
        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setPixmap(QtGui.QPixmap("hotel-room.jpg"))
        self.background_label.setScaledContents(True)
        self.main_layout.addWidget(self.background_label)

        # Overlay Container
        self.overlay_widget = QtWidgets.QWidget(self.centralwidget)
        self.overlay_layout = QtWidgets.QVBoxLayout(self.overlay_widget)
        self.overlay_layout.setContentsMargins(50, 50, 50, 50)

        # Title Label
        self.label = QtWidgets.QLabel(self.overlay_widget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(26)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("SELAMAT DATANG DI HOTEL ACUMALAKA")
        self.label.setStyleSheet("""
            color: white;
            background-color: rgba(255, 105, 180, 0.8);
            padding: 20px;
            border-radius: 15px;
            font-size: 28px;
        """)
        self.overlay_layout.addWidget(self.label)

        # ComboBox
        # self.comboBox = QtWidgets.QComboBox(self.overlay_widget)
        # self.comboBox.setStyleSheet("""
        #     background-color: rgba(173, 216, 230, 0.8);
        #     color: #333;
        #     font-size: 16px;
        #     padding: 12px;
        #     border-radius: 20px;
        # """)
        # self.comboBox.addItems([
        #     "ROOM AND SUITES", "Standard Room",
        #     "Executive Room", "Deluxe Room",
        #     "Suite Room", "Presidential Room"
        # ])
        # self.comboBox.currentIndexChanged.connect(self.show_rooms)
        # self.overlay_layout.addWidget(self.comboBox)

        # Button Layout
        self.button_layout = QtWidgets.QHBoxLayout()

        # MENU Button
        self.pushButton_2 = QtWidgets.QPushButton("MENU", self.overlay_widget)
        self.pushButton_2.setStyleSheet("""
            background-color: #FF7F50;
            color: white;
            font-weight: bold;
            border-radius: 20px;
            padding: 15px 20px;
        """)
        self.pushButton_2.clicked.connect(lambda: self.open_menu_window(MainWindow))
        self.button_layout.addWidget(self.pushButton_2)

        # HISTORY Button
        self.pushButton_3 = QtWidgets.QPushButton("HISTORY", self.overlay_widget)
        self.pushButton_3.setStyleSheet("""
            background-color: #DA70D6;
            color: white;
            font-weight: bold;
            border-radius: 20px;
            padding: 15px 20px;
        """)
        self.pushButton_3.clicked.connect(lambda: self.open_history_window(MainWindow))
        self.button_layout.addWidget(self.pushButton_3)

        # GALLERY Button
        self.pushButton_7 = QtWidgets.QPushButton("GALLERY", self.overlay_widget)
        self.pushButton_7.setStyleSheet("""
            background-color: #1E90FF;
            color: white;
            font-weight: bold;
            border-radius: 20px;
            padding: 15px 20px;
        """)
        self.pushButton_7.clicked.connect(lambda: self.open_gallery_window(MainWindow))
        self.button_layout.addWidget(self.pushButton_7)

        # PROFILE Button for Admin
        self.profile_button = QtWidgets.QPushButton("ADMIN PROFILE", self.overlay_widget)
        self.profile_button.setStyleSheet("""
            background-color: #FFD700;
            color: white;
            font-weight: bold;
            border-radius: 20px;
            padding: 15px 20px;
        """)
        self.profile_button.clicked.connect(self.open_profile_window)
        self.button_layout.addWidget(self.profile_button)

        # Logout Button
        self.logout_button = QtWidgets.QPushButton("LOGOUT", self.overlay_widget)
        self.logout_button.setStyleSheet("""
            background-color: #32CD32;
            color: white;
            font-weight: bold;
            border-radius: 20px;
            padding: 15px 20px;
        """)
        self.logout_button.clicked.connect(lambda: self.open_logout_window(MainWindow))
        self.button_layout.addWidget(self.logout_button)

        self.overlay_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.overlay_widget)

        MainWindow.setCentralWidget(self.centralwidget)

    def open_profile_window(self):
        self.profile_window = AdminProfileWindow()
        self.profile_window.show()

    # def show_rooms(self):
    #     room_details = {
    #         "Deluxe Room": "Harga: Rp 1.200.000/malam\nFasilitas: TV, Wi-Fi, AC, Kamar Mandi",
    #         "Suite Room": "Harga: Rp 2.000.000/malam\nFasilitas: TV, Wi-Fi, AC, Balkon, Kamar Mandi",
    #         "Presidential Room": "Harga: Rp 10.000.000/malam\nFasilitas: TV, Wi-Fi, AC, Kolam Renang Pribadi",
    #     }
    #     selected = self.comboBox.currentText()
    #     if selected in room_details:
    #         QtWidgets.QMessageBox.information(
    #             None, f"Detail {selected}", room_details[selected]
    #         )

    def show_rooms(self):
        try:
            from databasemanager import DatabaseManager
            db_manager = DatabaseManager()

            # Ambil tipe kamar yang dipilih dari comboBox
            selected_type = self.comboBox.currentText()

            # Query untuk mengambil kamar berdasarkan tipe
            query = """
                SELECT r.room_number, rt.type_name, rt.price, r.status, rt.description
                FROM rooms r
                JOIN room_types rt ON r.room_type_id = rt.id
                WHERE rt.type_name = %s
            """
            
            # Menjalankan query untuk mendapatkan kamar berdasarkan tipe
            rooms = db_manager.cursor.execute(query, (selected_type,))
            
            if rooms:
                # Menampilkan detail kamar
                room_details = "\n\n".join(
                    [f"Kamar: {room['room_number']}\nHarga: Rp {room['price']:.0f}\nStatus: {room['status']}\nDeskripsi: {room['description'] or 'Tidak ada deskripsi'}"
                    for room in rooms]
                )
                QtWidgets.QMessageBox.information(None, f"Detail Kamar {selected_type}", room_details)
            else:
                QtWidgets.QMessageBox.information(None, "Informasi", "Tidak ada kamar untuk tipe ini.")

            # Tutup koneksi database
            db_manager.close()

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Gagal mengambil detail kamar: {str(e)}")

    def open_menu_window(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = MenuWindow(self)
        self.ui.setupUi(self.window)
        MainWindow.close()
        self.window.showMaximized()

    def open_gallery_window(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = GalleryWindow()
        self.ui.setupUi(self.window)
        MainWindow.close()
        self.window.showMaximized()

    def open_history_window(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = HistoryWindow()
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
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

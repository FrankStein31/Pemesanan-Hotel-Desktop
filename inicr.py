from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from crud import Ui_MainWindow as CrudWindow  # Mengimpor CRUD dari crud.py
from kmr import Ui_MainWindow as KmrWindow  # Mengimpor kelas dari kmr.py
from fas import Ui_MainWindow as FasilitasWindow  # Mengimpor kelas Fasilitas dari fas.py
from dp import Ui_MainWindow as DpWindow  # Mengimpor Data Pelanggan dari dp.py
from logout import Ui_MainWindow as LogoutWindow  # Mengimpor kelas dari logout.py

class Ui_MainWindow(object):
    def __init__(self, previous_window=None):
        self.previous_window = previous_window

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow  # Menyimpan referensi untuk MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Hotel Acumalaka")
        MainWindow.resize(800, 600)  # Atur ukuran awal jika dibutuhkan, namun kita akan full screen
        MainWindow.setStyleSheet("""
            background-color: #2c3e50;
            font-family: 'Roboto', sans-serif;
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout utama
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Background image
        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setPixmap(QtGui.QPixmap("mw.jpg"))  # Ensure correct path
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 800, 600)
        self.background_label.lower()  # Set background behind all elements
        self.main_layout.addWidget(self.background_label)

        # Container for elements
        self.overlay_widget = QtWidgets.QWidget(self.centralwidget)
        self.overlay_layout = QtWidgets.QVBoxLayout(self.overlay_widget)
        self.overlay_layout.setContentsMargins(50, 50, 50, 50)

        # Title label with modern font
        self.label = QtWidgets.QLabel(self.overlay_widget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(24)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("SELAMAT DATANG DI HOTEL ACUMALAKA")
        self.label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 0.6);
            padding: 20px;
            border-radius: 12px;
            font-size: 26px;
        """)
        self.overlay_layout.addWidget(self.label)

        # ComboBox with modern style
        self.comboBox = QtWidgets.QComboBox(self.overlay_widget)
        self.comboBox.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.9);
            color: #34495e;
            font-size: 16px;
            padding: 10px;
            border-radius: 12px;
            border: 1px solid #bdc3c7;
            margin-top: 20px;
        """)
        self.comboBox.addItem("Pilih Menu")
        self.comboBox.addItem("Stok Kamar")
        self.comboBox.addItem("Kamar")
        self.comboBox.addItem("Fasilitas")
        self.comboBox.addItem("Data Pelanggan")  # Opsi baru
        self.comboBox.currentIndexChanged.connect(self.show_crud_form)
        self.overlay_layout.addWidget(self.comboBox)

        # Add space between combo box and buttons
        self.overlay_layout.addSpacing(20)

        # Button layout for action buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        # Back button
        self.back_button = QtWidgets.QPushButton("Kembali", self.overlay_widget)
        self.back_button.setStyleSheet("""
            background-color: #3498db;
            color: white;
            font-weight: bold;
            border-radius: 25px;
            padding: 15px;
            font-family: 'Roboto', sans-serif;
            transition: background-color 0.3s ease;
        """)
        self.back_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.go_back)
        self.button_layout.addWidget(self.back_button)

        # Add some spacing between the buttons
        self.button_layout.addSpacing(20)

        # Logout button
        self.logout_button = QtWidgets.QPushButton("Logout", self.overlay_widget)
        self.logout_button.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            font-weight: bold;
            border-radius: 25px;
            padding: 15px;
            font-family: 'Roboto', sans-serif;
            transition: background-color 0.3s ease;
        """)
        self.logout_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.logout_button.clicked.connect(self.logout)
        self.button_layout.addWidget(self.logout_button)

        # Add spacing after the buttons as well
        self.button_layout.addSpacing(20)

        self.overlay_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.overlay_widget)

        MainWindow.setCentralWidget(self.centralwidget)

    def show_crud_form(self):
        selected = self.comboBox.currentText()
        
        if selected == "Stok Kamar":
            self.show_stok_kamar_crud()
        elif selected == "Kamar":
            self.show_kamar_window()  # Show the room management window
        elif selected == "Fasilitas":
            self.show_fasilitas_crud()  # Show Fasilitas window
        elif selected == "Data Pelanggan":
            self.show_pelanggan_crud()  # This line calls the new method for Data Pelanggan

    def show_stok_kamar_crud(self):
        """Show Stok Kamar form"""
        self.window = QtWidgets.QMainWindow()
        self.ui = CrudWindow()
        self.ui.setupUi(self.window)
        self.window.showMaximized()  # Full screen for Stok Kamar

    def show_kamar_window(self):
        """Show the Kamar management window"""
        self.window = QtWidgets.QMainWindow()
        self.ui = KmrWindow()  # Create the KmrWindow instance
        self.ui.setupUi(self.window)
        self.window.showMaximized()  # Full screen for Kamar management

    def show_fasilitas_crud(self):
        """Show Fasilitas form from fas.py"""
        self.window = QtWidgets.QMainWindow()
        self.ui = FasilitasWindow()  # Create the FasilitasWindow instance
        self.ui.setupUi(self.window)
        self.window.showMaximized()  # Full screen for Fasilitas window

    def show_pelanggan_crud(self):
        """Show Data Pelanggan form from dp.py"""
        self.window = QtWidgets.QMainWindow()
        self.ui = DpWindow()  # Create the DpWindow instance (from dp.py)
        self.ui.setupUi(self.window)
        self.window.showMaximized()  # Full screen for Data Pelanggan window

    def go_back(self):
        """Go back to the main menu"""
        print("Returning to main menu")
        if self.previous_window:
            self.previous_window.show()
        self.MainWindow.close()

    def logout(self):
        """Logout and navigate to logout.py"""
        print("Logging out")
        self.window = QtWidgets.QMainWindow()
        self.ui = LogoutWindow()  # Instance of the logout window
        self.ui.setupUi(self.window)
        self.window.showMaximized()  # Full screen for logout window
        self.window.raise_()  # Bring the logout window to the front
        MainWindow.close()  # Close the current window

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()  # Fullscreen mode for the main window
    sys.exit(app.exec_())

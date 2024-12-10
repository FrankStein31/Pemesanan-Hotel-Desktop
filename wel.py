from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
import sys
import os
from login import LoginWindow

class AcumalakaHotelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acumalaka Hotel")
        self.setGeometry(100, 100, 800, 600)

        # Setup background
        self.setAutoFillBackground(True)
        palette = QPalette()

        # Load background image
        background_path = "q.jpg"  # Path gambar
        if os.path.exists(background_path):  # Validasi keberadaan gambar
            pixmap = QPixmap(background_path)
            palette.setBrush(QPalette.Window, QBrush(pixmap))
        else:
            print(f"Warning: Background image '{background_path}' not found!")
            self.setStyleSheet("background-color: gray;")  # Default background jika gambar tidak ada

        self.setPalette(palette)

        # Main layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Welcome label
        welcome_label = QLabel("WELCOME TO")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))  # Ukuran font lebih besar
        welcome_label.setStyleSheet("color: white;")  # Warna teks putih

        # Hotel name label
        hotel_name_label = QLabel("Acumalaka Hotel")
        hotel_name_label.setAlignment(Qt.AlignCenter)
        hotel_name_label.setFont(QFont("Times New Roman", 60, QFont.Bold))  # Ukuran font lebih besar
        hotel_name_label.setStyleSheet("color: white;")

        # Subtitle label
        subtitle_label = QLabel("The best hotel!")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 25))
        subtitle_label.setStyleSheet("color: white; font-style: italic;")

        # Login button (Biru transparan)
        login_button = QPushButton("LOGIN")
        login_button.setFont(QFont("Arial", 15))
        login_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 123, 255, 0.5);  /* Biru transparan */
                color: white;               /* Warna teks */
                padding: 10px 20px;
                border-radius: 10px;
                border: 2px solid rgba(0, 123, 255, 0.7);  /* Biru transparan dengan opacity lebih solid */
            }
            QPushButton:hover {
                background-color: rgba(0, 123, 255, 0.7);  /* Biru lebih solid saat di-hover */
            }
            QPushButton:pressed {
                background-color: rgba(0, 123, 255, 0.9);  /* Hampir solid saat ditekan */
            }
        """)
        login_button.setFixedSize(150, 50)

        # Connect button to slot
        login_button.clicked.connect(self.open_login_page)

        # Add widgets to layout
        layout.addWidget(welcome_label)
        layout.addWidget(hotel_name_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

        # Set layout to central widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def open_login_page(self):
        """Handler for login button click"""
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()  # Close current window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AcumalakaHotelApp()
    window.showMaximized()  # Membuka jendela dalam mode fullscreen
    sys.exit(app.exec_())

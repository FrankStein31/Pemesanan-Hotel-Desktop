from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Scroll area setup
        scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("border: none;")

        scrollContent = QtWidgets.QWidget()
        scrollArea.setWidget(scrollContent)

        mainLayout = QtWidgets.QVBoxLayout(scrollContent)
        mainLayout.setContentsMargins(40, 40, 40, 40)
        mainLayout.setSpacing(20)

        # Background gradient (dark, elegant tones)
        scrollContent.setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #3a4e77, stop:1 #62799a);
        """)

        # Title label with elegant style
        self.label = QtWidgets.QLabel(scrollContent)
        self.label.setText("Hotel Acumalaka")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 48px;
            font-weight: 800;
            color: #f4d03f;
            font-family: 'Georgia', serif;
            text-transform: uppercase;
            text-shadow: 3px 3px 15px rgba(0, 0, 0, 0.5);
        """)
        mainLayout.addWidget(self.label)

        # Description label with elegant background and subtle shadow
        self.descriptionLabel = QtWidgets.QLabel(scrollContent)
        self.descriptionLabel.setText(
            "Selamat datang di Hotel Acumalaka, tempat Anda dapat menikmati kenyamanan, "
            "kemewahan, dan pelayanan terbaik dengan suasana yang hangat dan ramah. "
            "Terletak di pusat kota, hotel ini menawarkan akses mudah ke berbagai destinasi menarik."
        )
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setStyleSheet("""
            font-size: 18px;
            color: #000000;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            font-family: 'Georgia', serif;
        """)
        mainLayout.addWidget(self.descriptionLabel)

        # Room types section with bold modern style
        self.roomLabel = QtWidgets.QLabel(scrollContent)
        self.roomLabel.setText("ROOMS:")
        self.roomLabel.setStyleSheet("""
            font-size: 24px;
            color: #f4d03f;
            font-weight: 700;
            font-family: 'Georgia', serif;
            text-transform: uppercase;
        """)
        mainLayout.addWidget(self.roomLabel)

        roomLayout = QtWidgets.QVBoxLayout()
        roomLayout.setSpacing(25)

        rooms = [
            ("Kamar Standard", "Fasilitas dasar dengan kenyamanan sempurna.", "Rp 500.000", "ys.jpg"),
            ("Kamar Executive", "Fasilitas premium dengan pemandangan spektakuler.", "Rp 1.500.000", "suite.jpg"),
            ("Kamar Deluxe", "Dilengkapi dengan fasilitas mewah.", "Rp 2.500.000", "sui.jpg"),
            ("Kamar Suite", "Fasilitas premium dengan pemandangan spektakuler.", "Rp 3.000.000", "ss.jpeg"),
            ("Kamar Presidential", "Fasilitas premium dengan pemandangan spektakuler.", "Rp 5.000.000", "suite.jpg"),
        ]

        for room_name, room_desc, room_price, image_path in rooms:
            roomHBox = QtWidgets.QHBoxLayout()
            roomHBox.setSpacing(20)

            roomImage = QtWidgets.QLabel(scrollContent)
            roomImage.setPixmap(QtGui.QPixmap(image_path).scaled(300, 300, QtCore.Qt.KeepAspectRatio))
            roomImage.setStyleSheet("border-radius: 12px; border: 2px solid #f4d03f;")
            roomHBox.addWidget(roomImage)

            # Add extra space between description and price by using <p> tag
            roomLabel = QtWidgets.QLabel(scrollContent)
            roomLabel.setText(f"<b>{room_name}</b>: {room_desc}<p><b>Harga:</b> {room_price}</p>")
            roomLabel.setWordWrap(True)
            roomLabel.setStyleSheet("""
                font-size: 18px;
                color: #000000;
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                font-family: 'Georgia', serif;
            """)
            roomHBox.addWidget(roomLabel)

            roomLayout.addLayout(roomHBox)

        mainLayout.addLayout(roomLayout)

        # Facilities section with dynamic modern style
        self.facilityLabel = QtWidgets.QLabel(scrollContent)
        self.facilityLabel.setText("FACILITIES:")
        self.facilityLabel.setStyleSheet("""
            font-size: 24px;
            color: #f4d03f;
            font-weight: 700;
            font-family: 'Georgia', serif;
            text-transform: uppercase;
        """)
        mainLayout.addWidget(self.facilityLabel)

        facilityLayout = QtWidgets.QVBoxLayout()
        facilityLayout.setSpacing(25)

        facilities = [
            ("Spa", "Relaksasi dengan layanan spa berkualitas tinggi.", "Rp 200.000", "spa.jpg"),
            ("Game Center", "Pusat hiburan dengan berbagai permainan seru.", "Rp 150.000", "gc.jpg"),
            ("Bioskop", "Nikmati film favorit dengan layar besar.", "Rp 200.000", "bio.jpg"),
            ("Kolam Renang", "Kolam renang outdoor dengan pemandangan indah.", "Rp 100.000", "pool.jpg"),
            ("Gym", "Fasilitas gym lengkap untuk menjaga kebugaran Anda.", "Rp 75.000", "gym.jpg"),
        ]

        for facility_name, facility_desc, facility_price, image_path in facilities:
            facilityHBox = QtWidgets.QHBoxLayout()
            facilityHBox.setSpacing(20)

            facilityImage = QtWidgets.QLabel(scrollContent)
            facilityImage.setPixmap(QtGui.QPixmap(image_path).scaled(300, 300, QtCore.Qt.KeepAspectRatio))
            facilityImage.setStyleSheet("border-radius: 12px; border: 2px solid #000000;")
            facilityHBox.addWidget(facilityImage)

            facilityLabel = QtWidgets.QLabel(scrollContent)
            # Add extra space between description and price by using <p> tag
            facilityLabel.setText(f"<b>{facility_name}</b>: {facility_desc}<p><b>Harga:</b> {facility_price}</p>")
            facilityLabel.setWordWrap(True)
            facilityLabel.setStyleSheet("""
                font-size: 18px;
                color: #000000;
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                font-family: 'Georgia', serif;
            """)
            facilityHBox.addWidget(facilityLabel)

            facilityLayout.addLayout(facilityHBox)

        mainLayout.addLayout(facilityLayout)

        # Back button with elegant hover effect
        self.backButton = QtWidgets.QPushButton(scrollContent)
        self.backButton.setText("Kembali")
        self.backButton.setStyleSheet("""
            background-color: #f4d03f;
            color: #2d4059;
            font-size: 20px;
            font-weight: bold;
            padding: 15px;
            border-radius: 30px;
            font-family: 'Georgia', serif;
        """)
        self.backButton.clicked.connect(self.goBack)
        mainLayout.addWidget(self.backButton)

        # Add scroll area to the main window
        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.addWidget(scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Hotel Acumalaka - Elegant UI")

    def goBack(self):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()  # Fullscreen display
    sys.exit(app.exec_())

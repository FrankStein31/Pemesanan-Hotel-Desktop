from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Menghapus border untuk efek modern

        # Menampilkan window di tengah layar
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - MainWindow.width()) // 2
        y = (screen_geometry.height() - MainWindow.height()) // 2
        MainWindow.move(x, y)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Background gradasi pastel futuristik
        self.centralwidget.setStyleSheet(""" 
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #ff9ff3, stop:0.5 #feca57, stop:1 #48dbfb);
            border-radius: 20px;
        """)

        # Label dengan efek neon glow
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet("""
            font-size: 36px;
            font-family: 'Comic Sans MS', sans-serif;
            font-weight: bold;
            color: white;
            padding: 20px;
            text-transform: uppercase;
            text-shadow: 0 0 20px #f368e0, 0 0 30px #f368e0;
            border: 4px dashed rgba(255, 255, 255, 0.5);
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 25px;
        """)

        self.label.setText("Terima kasih, have a nice day!")
        self.label.adjustSize()  # Menyesuaikan ukuran label dengan panjang teks

        # Menambahkan label pada layout atau grid
        label_layout = QtWidgets.QVBoxLayout()
        label_layout.addWidget(self.label)
        label_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Menambahkan logo atau ikon dengan style retro
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setPixmap(QtGui.QPixmap("path_to_logo.png").scaled(200, 100, QtCore.Qt.KeepAspectRatio))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setObjectName("imageLabel")

        # Tombol dengan efek hover dan transformasi
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 420, 150, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Selesai")
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #ff6b81;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 3px solid white;
                border-radius: 15px;
                padding: 10px;
                transition: 0.3s;
            }
            QPushButton:hover {
                background-color: #f368e0;
                transform: scale(1.1);
            }
        """)

        # Membuat tombol bisa menutup aplikasi
        # self.pushButton.clicked.connect(MainWindow.close)
        self.pushButton.clicked.connect(self.go_back_welcome)


        # Menambahkan tombol ke layout
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.addLayout(label_layout)  # Add label layout first
        main_layout.addWidget(self.imageLabel)
        main_layout.addWidget(self.pushButton)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Set the layout for centralwidget
        self.centralwidget.setLayout(main_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Terimakasih"))

    def go_back_welcome(self):
        """
        Close current window and return to main dashboard
        """
        from wel import AcumalakaHotelApp as WelcomePage  # Impor halaman utama

        # Membuat jendela utama
        self.window = WelcomePage()  # Buat instance langsung
        QtWidgets.QApplication.activeWindow().close()  # Tutup jendela saat ini
        self.window.showMaximized()  # Tampilkan halaman utama dalam mode fullscreen

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()  # Fullscreen display
    sys.exit(app.exec_())

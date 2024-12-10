# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow


class LoginWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Label untuk menampilkan latar belakang
        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.background_label.setScaledContents(True)
        self.set_background("kw.jpg")  # Set background 

        # Tombol kembali
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(30, 20, 120, 30))
        self.back_button.setText("Kembali")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 128, 128, 200);
                font: bold 12px;
                border-radius: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 128, 128, 255);
            }
        """)
        self.back_button.clicked.connect(self.handle_back)

        # Label judul
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(200, 50, 400, 100))
        self.title_label.setText("LOGIN")
        self.title_label.setStyleSheet("""
            QLabel {
                font: 48px "Comic Sans MS";
                color: white;
                text-align: center;
            }
        """)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)

        # Input username
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        self.username_label.setGeometry(QtCore.QRect(200, 200, 100, 30))
        self.username_label.setText("Username:")
        self.username_label.setStyleSheet("color: white; font: bold 16px;")
        
        self.username_input = QtWidgets.QLineEdit(self.centralwidget)
        self.username_input.setGeometry(QtCore.QRect(300, 200, 300, 30))
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid white;
                border-radius: 10px;
                padding: 5px;
                font: 14px;
                color: white;
                background-color: rgba(0, 0, 0, 200);
            }
        """)

        # Input password
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setGeometry(QtCore.QRect(200, 250, 100, 30))
        self.password_label.setText("Password:")
        self.password_label.setStyleSheet("color: white; font: bold 16px;")
        
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(QtCore.QRect(300, 250, 300, 30))
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid white;
                border-radius: 10px;
                padding: 5px;
                font: 14px;
                color: white;
                background-color: rgba(0, 0, 0, 200);
            }
        """)

        # Tombol login
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(350, 320, 100, 40))
        self.login_button.setText("LOGIN")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 128, 200);
                font: bold 16px;
                border-radius: 20px;
                color: black; /* Warna teks diubah menjadi hitam */
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 128, 255);
            }
        """)
        self.login_button.clicked.connect(self.handle_login)

        # Tombol ubah background
        self.change_bg_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_bg_button.setGeometry(QtCore.QRect(650, 20, 120, 30))
        self.change_bg_button.setText("Change BG")
        self.change_bg_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(128, 0, 128, 200); /* Warna tombol diubah menjadi ungu */
                font: bold 12px;
                border-radius: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(128, 0, 128, 255); /* Warna hover menjadi ungu lebih terang */
            }
        """)
        self.change_bg_button.clicked.connect(self.change_background)
        
        MainWindow.setCentralWidget(self.centralwidget)

        # Menubar dan statusbar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Login"))

    def handle_login(self):

        users = {"petugas": {"password": "123", "role": "Petugas"}, 
                "admin": {"password": "123", "role": "Admin"}}
        
        username = self.username_input.text()
        password = self.password_input.text()

        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            QtWidgets.QMessageBox.information(None, "Login", f"Login berhasil sebagai {role}!")
        else:
            QtWidgets.QMessageBox.warning(None, "Login", "Username atau password salah!")

    def handle_back(self):
        QtWidgets.QMessageBox.information(None, "Kembali", "Anda menekan tombol Kembali.")

    def set_background(self, file_path):
        try:
            self.background_label.setPixmap(QtGui.QPixmap(file_path))
        except Exception as e:
            print(f"Error loading background: {e}")

    def change_background(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Pilih Background", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            self.set_background(file_path)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = LoginWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()  # Layar penuh
    sys.exit(app.exec_())

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet("""
            background: qradialgradient(cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5, stop: 0 #dff9fb, stop: 1 #f4f5f7);
        """)
        MainWindow.setWindowState(QtCore.Qt.WindowMaximized)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Title Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Stok Kamar Hotel Acumalaka")
        self.label.setFont(QtGui.QFont("Montserrat", 28, QtGui.QFont.Bold))
        self.label.setStyleSheet("color: #2c3e50;")
        self.main_layout.addWidget(self.label)

        # Search Bar
        self.search_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.search_bar.setPlaceholderText("Cari berdasarkan Nomor Kamar, Tipe Kamar, atau Status...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px 20px;
                border: 2px solid #3498db;
                border-radius: 10px;
                font-family: Roboto;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #1abc9c;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_data)
        self.main_layout.addWidget(self.search_bar)

        # Room Table
        self.room_table = QtWidgets.QTableWidget(self.centralwidget)
        self.room_table.setColumnCount(4)
        self.room_table.setHorizontalHeaderLabels(["Nomor Kamar", "Tipe Kamar", "Harga", "Status"])
        self.room_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.room_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        # Table Styling with Gradient Header
        self.room_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border-radius: 10px;
                font-family: Roboto;
                font-size: 18px;
                color: #34495e;
                border: 2px solid #3498db;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
            QTableWidget::item:selected {
                background-color: #eaf2f8;
                color: #2980b9;
            }
            QHeaderView::section {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #1abc9c);
                color: white;
                font-size: 13px;
                font-family: Roboto;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
        """)

        header = self.room_table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.main_layout.addWidget(self.room_table)

        # Available rooms label
        self.label_available_rooms = QtWidgets.QLabel(self.centralwidget)
        self.label_available_rooms.setFont(QtGui.QFont("Roboto", 20))
        self.label_available_rooms.setAlignment(QtCore.Qt.AlignLeft)
        self.label_available_rooms.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.main_layout.addWidget(self.label_available_rooms)

        # Refresh button
        self.btn_refresh = QtWidgets.QPushButton("Refresh Data", self.centralwidget)
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 16pt;
                font-family: Roboto;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #1e8449;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            }
        """)
        self.main_layout.addWidget(self.btn_refresh)

        # Back button
        self.btn_back = QtWidgets.QPushButton("Kembali", self.centralwidget)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16pt;
                font-family: Roboto;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #c0392b;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            }
        """)
        self.btn_back.clicked.connect(self.back_action)
        self.main_layout.addWidget(self.btn_back)

        # Load data
        self.load_data()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stok Kamar Hotel"))

    def load_data(self):
        """ Load sample room data into the table and count available rooms. """
        self.rooms = [
            {"nomor": "101", "tipe": "Deluxe", "harga": "1,500,000", "status": "Tersedia"},
            {"nomor": "102", "tipe": "Presidential", "harga": "5,000,000", "status": "Terisi"},
            {"nomor": "103", "tipe": "Standar", "harga": "800,000", "status": "Tersedia"},
            {"nomor": "104", "tipe": "Deluxe", "harga": "1,500,000", "status": "Terisi"},
            {"nomor": "105", "tipe": "Standar", "harga": "800,000", "status": "Tersedia"},
        ]

        self.update_table(self.rooms)

    def update_table(self, rooms):
        """ Update table with the provided rooms data. """
        self.room_table.setRowCount(len(rooms))
        available_count = 0

        for row_idx, room in enumerate(rooms):
            nomor_item = QtWidgets.QTableWidgetItem(room["nomor"])
            nomor_item.setTextAlignment(QtCore.Qt.AlignCenter)

            # Set smaller font size for "Nomor Kamar"
            font = nomor_item.font()
            font.setPointSize(12)  # Adjust font size as needed
            nomor_item.setFont(font)

            self.room_table.setItem(row_idx, 0, nomor_item)
            self.room_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(room["tipe"]))
            self.room_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(room["harga"]))
            self.room_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(room["status"]))

            if room["status"] == "Tersedia":
                available_count += 1

        self.label_available_rooms.setText(f"Jumlah kamar yang tersedia: {available_count}")

    def filter_data(self):
        """ Filter rooms based on the text entered in the search bar. """
        query = self.search_bar.text().lower()
        filtered_rooms = [
            room for room in self.rooms
            if query in room["nomor"].lower() or query in room["tipe"].lower() or query in room["status"].lower()
        ]
        self.update_table(filtered_rooms)

    def back_action(self):
        """ Action to perform when the 'Back' button is clicked. """
        reply = QtWidgets.QMessageBox.question(
            None,
            "Kembali",
            "Apakah Anda yakin ingin kembali?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QApplication.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

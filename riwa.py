from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout utama
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Search Bar
        self.search_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.search_bar.setPlaceholderText("Cari berdasarkan Nama, Jenis Kamar, atau Status...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px 20px;
                border: 2px solid #2980b9;
                border-radius: 10px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit:focus {
                border: 2px solid #1abc9c;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_table)  # Hubungkan pencarian dengan logika filter
        main_layout.addWidget(self.search_bar)

        # Title Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #ffffff;
            background: #2c3e50;
            padding: 20px;
            border-radius: 20px;
            font-family: 'Segoe UI', sans-serif;
            text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.5);
        """)
        self.label.setText("Riwayat Pemesanan Kamar")
        main_layout.addWidget(self.label)

        # Table Widget
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Tanggal Pemesanan", "Nama", "Jenis Kamar", "Total", "Status"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Styling Tabel
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #ecf0f1;
                border: 1px solid #34495e;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
                border-radius: 15px;
                padding: 15px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #ffffff;
                padding: 18px;
                font-size: 16px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

        # Data tabel
        self.data = [
            ["12/11/2024", "Sabrina", "Deluxe Room", "Rp 2.500.000", "Diproses"],
            ["14/11/2024", "Ella Gross", "Suite Room", "Rp 3.000.000", "Dikonfirmasi"],
            ["15/11/2024", "Mark Lee", "Standard Room", "Rp 500.000", "Dikonfirmasi"],
            ["16/11/2024", "Balmond", "Deluxe Room", "Rp 2.500.000", "Diproses"],
            ["17/11/2024", "Rose", "Executive Room", "Rp 1.500.000", "Dikonfirmasi"]
        ]
        self.load_table(self.data)

        main_layout.addWidget(self.tableWidget)

        # Tombol Layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(30)

        # Tombol Kembali dengan desain lebih elegan
        self.backButton = QtWidgets.QPushButton("Kembali", self.centralwidget)
        self.backButton.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;  /* Soft blue */
                color: white;
                border-radius: 20px;
                font-size: 18px;
                font-family: 'Segoe UI', sans-serif;
                box-shadow: 0px 4px 15px rgba(52, 152, 219, 0.4);
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #1f618d;  /* Darker blue on hover */
            }
        """)
        button_layout.addWidget(self.backButton)

        # Tombol Refresh dengan desain lebih elegan
        self.refreshButton = QtWidgets.QPushButton("Refresh", self.centralwidget)
        self.refreshButton.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;  /* Neon red */
                color: white;
                border-radius: 20px;
                font-size: 18px;
                font-family: 'Segoe UI', sans-serif;
                box-shadow: 0px 4px 15px rgba(231, 76, 60, 0.4);
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #c0392b;  /* Darker red on hover */
            }
        """)
        button_layout.addWidget(self.refreshButton)

        main_layout.addLayout(button_layout)
        MainWindow.setCentralWidget(self.centralwidget)

    def load_table(self, data):
        """Mengisi tabel dengan data."""
        self.tableWidget.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(value))

    def filter_table(self):
        """Logika untuk menyaring data di tabel berdasarkan Nama, Jenis Kamar, atau Status."""
        query = self.search_bar.text().lower()
        filtered_data = [
            row for row in self.data
            if query in row[1].lower()  # Mencari di Nama
            or query in row[2].lower()  # Mencari di Jenis Kamar
            or query in row[4].lower()  # Mencari di Status
        ]
        self.load_table(filtered_data)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Riwayat Pemesanan"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

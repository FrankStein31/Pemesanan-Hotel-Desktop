# -*- coding: utf-8 -*- 
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #f7f7f7;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #333;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 10px;
                font-size: 14px;
                padding: 8px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
            QPushButton:disabled {
                background-color: #A2A2A2;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 16px;
                color: #555;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }
            QHBoxLayout {
                margin-bottom: 20px;
            }
            QVBoxLayout {
                margin-left: 20px;
                margin-right: 20px;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Title Label
        self.titleLabel = QtWidgets.QLabel("Data Pelanggan Hotel Acumalaka", self.centralwidget)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.titleLabel)

        # Search Layout
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchInput = QtWidgets.QLineEdit(self.centralwidget)
        self.searchInput.setPlaceholderText("Cari pelanggan...")
        self.searchLayout.addWidget(self.searchInput)

        self.searchButton = QtWidgets.QPushButton("Cari", self.centralwidget)
        self.searchLayout.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.searchLayout)

        # Table
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(6)  # Mengubah jumlah kolom menjadi 6
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Nama", "Telepon", "No KTP", "Alamat", "Jenis Kelamin"])
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Disable editing
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # Set all columns to have the same width
        header = self.tableWidget.horizontalHeader()
        for i in range(self.tableWidget.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        self.verticalLayout.addWidget(self.tableWidget)

        # Button Layout
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.backButton = QtWidgets.QPushButton("Kembali", self.centralwidget)
        self.buttonLayout.addWidget(self.backButton)

        self.deleteButton = QtWidgets.QPushButton("Hapus", self.centralwidget)
        self.buttonLayout.addWidget(self.deleteButton)

        self.verticalLayout.addLayout(self.buttonLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setMenuBar(QtWidgets.QMenuBar(MainWindow))
        MainWindow.setStatusBar(QtWidgets.QStatusBar(MainWindow))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Signal Connections
        self.searchButton.clicked.connect(self.searchData)
        self.searchInput.returnPressed.connect(self.searchData)  # Trigger search on Enter key
        self.deleteButton.clicked.connect(self.deleteRow)
        self.backButton.clicked.connect(MainWindow.close)  # Menutup jendela utama

        # Load sample data
        self.loadSampleData()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Pelanggan"))

    def loadSampleData(self):
        """Load sample data into the table."""
        data = [
            ("001", "Lisa Blekpink", "081234567890", "1234567890123456", "Jl. Merdeka No. 10, Jakarta", "Perempuan"),
            ("002", "Hanni New Jeans", "082345678901", "1234567890123457", "Jl. Raya No. 15, Bandung", "Perempuan"),
            ("003", "Odette ML", "083456789012", "1234567890123458", "Jl. Sukses No. 20, Yogyakarta", "Perempuan"),
            ("004", "Jihyo Twice", "084567890123", "1234567890123459", "Jl. Sejahtera No. 25, Surabaya", "Perempuan"),
            ("005", "V BTS", "08376792123", "1234567890123460", "Jl. Pahlawan No. 30, Bali", "Laki-laki"),
        ]
        self.tableWidget.setRowCount(len(data))
        for row, (id_, name, phone, ktp, address, gender) in enumerate(data):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(id_))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(phone))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(ktp))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(address))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(gender))

    def searchData(self):
        """Search the table based on the input text."""
        query = self.searchInput.text().lower()
        for row in range(self.tableWidget.rowCount()):
            match = False
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            self.tableWidget.setRowHidden(row, not match)

    def deleteRow(self):
        """Delete the selected row from the table."""
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            self.tableWidget.removeRow(selected_row)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

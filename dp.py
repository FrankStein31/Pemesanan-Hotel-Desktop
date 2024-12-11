# -*- coding: utf-8 -*- 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from databasemanager import DatabaseManager

class Ui_MainWindow(object):
    def __init__(self):
        # Initialize database manager
        self.db_manager = DatabaseManager()

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
        self.tableWidget.setColumnCount(5)  # Changed to match database columns
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Nama", "Email", "Telepon", "Alamat"])
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
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

        self.addButton = QtWidgets.QPushButton("Tambah", self.centralwidget)
        self.buttonLayout.addWidget(self.addButton)

        self.deleteButton = QtWidgets.QPushButton("Hapus", self.centralwidget)
        self.buttonLayout.addWidget(self.deleteButton)

        self.editButton = QtWidgets.QPushButton("Edit", self.centralwidget)
        self.buttonLayout.addWidget(self.editButton)

        self.verticalLayout.addLayout(self.buttonLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setMenuBar(QtWidgets.QMenuBar(MainWindow))
        MainWindow.setStatusBar(QtWidgets.QStatusBar(MainWindow))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Signal Connections
        self.searchButton.clicked.connect(self.searchData)
        self.searchInput.returnPressed.connect(self.searchData)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.addButton.clicked.connect(self.addCustomer)
        self.editButton.clicked.connect(self.editCustomer)
        self.backButton.clicked.connect(MainWindow.close)

        # Load data from database
        self.loadCustomerData()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Pelanggan"))

    def loadCustomerData(self):
        """Load customer data from the database."""
        customers = self.db_manager.get_customers()
        self.tableWidget.setRowCount(len(customers))
        
        for row, customer in enumerate(customers):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(customer['id'])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(customer['name']))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(customer['email']))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(customer['phone']))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(customer['address']))

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
        """Delete the selected customer from the database."""
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            customer_id = self.tableWidget.item(selected_row, 0).text()
            
            # Konfirmasi penghapusan
            reply = QMessageBox.question(None, 'Konfirmasi Hapus', 
                                         f'Apakah Anda yakin ingin menghapus pelanggan dengan ID {customer_id}?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Hapus dari database
                if self.db_manager.delete_customer(int(customer_id)):
                    self.tableWidget.removeRow(selected_row)
                    QMessageBox.information(None, 'Berhasil', 'Pelanggan berhasil dihapus.')
                else:
                    QMessageBox.warning(None, 'Gagal', 'Gagal menghapus pelanggan.')

    def addCustomer(self):
        """Add a new customer to the database."""
        # Dialog untuk mengumpulkan informasi pelanggan
        name, ok1 = QInputDialog.getText(None, 'Tambah Pelanggan', 'Nama:')
        if not ok1 or not name:
            return
        
        email, ok2 = QInputDialog.getText(None, 'Tambah Pelanggan', 'Email:')
        if not ok2:
            return
        
        phone, ok3 = QInputDialog.getText(None, 'Tambah Pelanggan', 'Telepon:')
        if not ok3:
            return
        
        address, ok4 = QInputDialog.getText(None, 'Tambah Pelanggan', 'Alamat:')
        if not ok4:
            return

        # Tambah pelanggan ke database
        customer_id = self.db_manager.add_customer(name, email, phone, address)
        
        if customer_id:
            # Reload data setelah menambahkan pelanggan
            QMessageBox.information(None, 'Berhasil', 'Pelanggan berhasil ditambahkan.')
            self.loadCustomerData()
        else:
            QMessageBox.warning(None, 'Gagal', 'Gagal menambahkan pelanggan.')

    def editCustomer(self):
        """Edit an existing customer in the database."""
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(None, 'Peringatan', 'Pilih pelanggan yang ingin diedit.')
            return

        # Ambil informasi pelanggan yang dipilih
        customer_id = self.tableWidget.item(selected_row, 0).text()
        current_name = self.tableWidget.item(selected_row, 1).text()
        current_email = self.tableWidget.item(selected_row, 2).text()
        current_phone = self.tableWidget.item(selected_row, 3).text()
        current_address = self.tableWidget.item(selected_row, 4).text()

        # Dialog untuk edit informasi pelanggan
        name, ok1 = QInputDialog.getText(None, 'Edit Pelanggan', 'Nama:', text=current_name)
        if not ok1 or not name:
            return
        
        email, ok2 = QInputDialog.getText(None, 'Edit Pelanggan', 'Email:', text=current_email)
        if not ok2:
            return
        
        phone, ok3 = QInputDialog.getText(None, 'Edit Pelanggan', 'Telepon:', text=current_phone)
        if not ok3:
            return
        
        address, ok4 = QInputDialog.getText(None, 'Edit Pelanggan', 'Alamat:', text=current_address)
        if not ok4:
            return

        # Update pelanggan di database
        if self.db_manager.update_customer(int(customer_id), name, email, phone, address):
            QMessageBox.information(None, 'Berhasil', 'Pelanggan berhasil diperbarui.')
            self.loadCustomerData()
        else:
            QMessageBox.warning(None, 'Gagal', 'Gagal memperbarui pelanggan.')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
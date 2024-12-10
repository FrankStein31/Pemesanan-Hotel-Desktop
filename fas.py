# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        MainWindow.setStyleSheet("""
            background: linear-gradient(135deg, #00C9FF, #92FE9D);  /* New gradient background */
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)

        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setText("🌟 Fasilitas Hotel Acumalaka 🌟")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #006064;  /* Rich teal color */
            font-family: 'Roboto', sans-serif;
            margin-bottom: 20px;
        """)
        self.mainLayout.addWidget(self.titleLabel)

        # Search Bar
        self.searchLabel = QtWidgets.QLabel("Cari Fasilitas:", self.centralwidget)
        self.searchLabel.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #006064;
            padding: 10px;
        """)
        self.mainLayout.addWidget(self.searchLabel)

        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setPlaceholderText("Masukkan nama fasilitas untuk mencari")
        self.searchBar.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 2px solid #006064;  /* Strong border color */
            border-radius: 10px;
            background-color: #E0F7FA;  /* Soft background color */
        """)
        self.searchBar.textChanged.connect(self.filter_table)
        self.mainLayout.addWidget(self.searchBar)

        self.formLayout = QtWidgets.QGridLayout()
        self.formLayout.setSpacing(10)

        self.labelFasilitas = QtWidgets.QLabel("Nama Fasilitas:", self.centralwidget)
        self.labelFasilitas.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #006064;
            padding: 10px;
        """)
        self.formLayout.addWidget(self.labelFasilitas, 0, 0)

        self.inputFasilitas = QtWidgets.QLineEdit(self.centralwidget)
        self.inputFasilitas.setPlaceholderText("Masukkan nama fasilitas")
        self.inputFasilitas.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 2px solid #006064;
            border-radius: 10px;
            background-color: #E0F7FA;
        """)
        self.formLayout.addWidget(self.inputFasilitas, 0, 1)

        self.labelDeskripsi = QtWidgets.QLabel("Deskripsi Fasilitas:", self.centralwidget)
        self.labelDeskripsi.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #006064;
            padding: 10px;
        """)
        self.formLayout.addWidget(self.labelDeskripsi, 1, 0)

        self.inputDeskripsi = QtWidgets.QLineEdit(self.centralwidget)
        self.inputDeskripsi.setPlaceholderText("Masukkan deskripsi fasilitas")
        self.inputDeskripsi.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 2px solid #006064;
            border-radius: 10px;
            background-color: #E0F7FA;
        """)
        self.formLayout.addWidget(self.inputDeskripsi, 1, 1)

        # Input Harga
        self.labelHarga = QtWidgets.QLabel("Harga Fasilitas (IDR):", self.centralwidget)
        self.labelHarga.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #006064;
            padding: 10px;
        """)
        self.formLayout.addWidget(self.labelHarga, 2, 0)

        self.inputHarga = QtWidgets.QLineEdit(self.centralwidget)
        self.inputHarga.setPlaceholderText("Masukkan harga fasilitas")
        self.inputHarga.setStyleSheet("""
            font-size: 16px;
            padding: 12px;
            border: 2px solid #006064;
            border-radius: 10px;
            background-color: #E0F7FA;
        """)
        self.inputHarga.setValidator(QtGui.QIntValidator())
        self.formLayout.addWidget(self.inputHarga, 2, 1)

        self.mainLayout.addLayout(self.formLayout)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(15)

        self.addButton = QtWidgets.QPushButton("✨ Tambah Fasilitas ✨", self.centralwidget)
        self.addButton.setStyleSheet("""
            background-color: #00897B;  /* Deeper teal */
            color: white;
            font-size: 18px;
            border-radius: 12px;
            padding: 10px;
        """)
        self.addButton.clicked.connect(self.add_fasilitas)
        self.buttonLayout.addWidget(self.addButton)

        self.updateButton = QtWidgets.QPushButton("🔄 Update Fasilitas 🔄", self.centralwidget)
        self.updateButton.setStyleSheet("""
            background-color: #00796B;  /* Darker teal */
            color: white;
            font-size: 18px;
            border-radius: 12px;
            padding: 10px;
        """)
        self.updateButton.clicked.connect(self.update_fasilitas)
        self.buttonLayout.addWidget(self.updateButton)

        self.deleteButton = QtWidgets.QPushButton("❌ Hapus Fasilitas ❌", self.centralwidget)
        self.deleteButton.setStyleSheet("""
            background-color: #D32F2F;  /* Vibrant red */
            color: white;
            font-size: 18px;
            border-radius: 12px;
            padding: 10px;
        """)
        self.deleteButton.clicked.connect(self.delete_fasilitas)
        self.buttonLayout.addWidget(self.deleteButton)

        self.backButton = QtWidgets.QPushButton("🔙 Kembali", self.centralwidget)
        self.backButton.setStyleSheet("""
            background-color: #FF7043;  /* Warm orange */
            color: white;
            font-size: 18px;
            border-radius: 12px;
            padding: 10px;
        """)
        self.backButton.clicked.connect(self.go_back)
        self.buttonLayout.addWidget(self.backButton)

        self.mainLayout.addLayout(self.buttonLayout)

        self.facilityTable = QtWidgets.QTableWidget(self.centralwidget)
        self.facilityTable.setColumnCount(3)
        self.facilityTable.setHorizontalHeaderLabels(["Nama Fasilitas", "Deskripsi Fasilitas", "Harga (IDR)"])
        self.facilityTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.facilityTable.horizontalHeader().setStyleSheet("""
            font-size: 18px;
            color: #006064;
            background-color: #00796B;  /* Darker teal */
        """)
        self.facilityTable.setStyleSheet("""
            background-color: #ffffff;
            font-size: 16px;
            color: #006064;
            border: 1px solid #B2DFDB;  /* Light teal border */
        """)
        self.mainLayout.addWidget(self.facilityTable)

        self.facilities = []

        self.add_initial_data()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", "Fasilitas Hotel Acumalaka"))

    def add_fasilitas(self):
        name = self.inputFasilitas.text()
        description = self.inputDeskripsi.text()
        price = self.inputHarga.text()
        if name and description and price:
            self.facilities.append({"name": name, "description": description, "price": price})
            self.update_table()
            self.inputFasilitas.clear()
            self.inputDeskripsi.clear()
            self.inputHarga.clear()

    def update_fasilitas(self):
        selected_row = self.facilityTable.currentRow()
        if selected_row >= 0:
            name = self.inputFasilitas.text()
            description = self.inputDeskripsi.text()
            price = self.inputHarga.text()
            if name and description and price:
                self.facilities[selected_row] = {"name": name, "description": description, "price": price}
                self.update_table()
                self.inputFasilitas.clear()
                self.inputDeskripsi.clear()
                self.inputHarga.clear()

    def delete_fasilitas(self):
        selected_row = self.facilityTable.currentRow()
        if selected_row >= 0:
            self.facilities.pop(selected_row)
            self.update_table()

    def update_table(self):
        self.facilityTable.setRowCount(0)
        for facility in self.facilities:
            row_position = self.facilityTable.rowCount()
            self.facilityTable.insertRow(row_position)
            self.facilityTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(facility["name"]))
            self.facilityTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(facility["description"]))
            self.facilityTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(facility["price"]))

    def filter_table(self):
        search_term = self.searchBar.text().lower()
        filtered_facilities = [facility for facility in self.facilities if search_term in facility["name"].lower()]
        self.facilityTable.setRowCount(0)
        for facility in filtered_facilities:
            row_position = self.facilityTable.rowCount()
            self.facilityTable.insertRow(row_position)
            self.facilityTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(facility["name"]))
            self.facilityTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(facility["description"]))
            self.facilityTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(facility["price"]))

    def add_initial_data(self):
        initial_data = [
            {"name": "Spa", "description": "Relaksasi dengan layanan spa berkualitas tinggi", "price": "200.000"},
            {"name": "Game Center", "description": "Pusat hiburan dengan berbagai permainan seru", "price": "150.000"},
            {"name": "Bioskop", "description": "Nikmati film favorit dengan layar besar", "price": "200.000"},
            {"name": "Kolam Renang", "description": "Kolam renang outdoor dengan pemandangan indah", "price": "100.000"},
            {"name": "Gym", "description": "Fasilitas gym lengkap untuk menjaga kebugaran Anda", "price": "75.000"},
        ]
        self.facilities.extend(initial_data)
        self.update_table()

    def go_back(self):
        QtWidgets.QApplication.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

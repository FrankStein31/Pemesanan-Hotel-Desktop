# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from databasemanager import DatabaseManager

class Ui_MainWindow(object):
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.current_facility_id = None

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
        self.facilityTable.itemSelectionChanged.connect(self.on_table_item_selected)
        self.facilities = []

        # self.add_initial_data()
        self.load_facilities()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", "Fasilitas Hotel Acumalaka"))

    def load_facilities(self):
        # Clear existing facilities
        self.facilities = []
        
        # Fetch facilities from database
        db_facilities = self.db_manager.get_facilities()
        for facility in db_facilities:
            self.facilities.append({
                "id": facility['id'],
                "name": facility['facility_name'],
                "description": facility['description'],
                "price": facility['price']
            })
        
        self.update_table()

    def on_table_item_selected(self):
        # Method to populate input fields when a table row is selected
        selected_rows = self.facilityTable.selectedItems()
        if selected_rows:
            # Calculate the row index (first selected item's row)
            row = selected_rows[0].row()
            
            # Ensure row is within facilities list range
            if 0 <= row < len(self.facilities):
                facility = self.facilities[row]
                
                # Populate input fields
                self.inputFasilitas.setText(facility.get('name', ''))
                self.inputDeskripsi.setText(facility.get('description', ''))
                self.inputHarga.setText(facility.get('price', ''))

    def add_fasilitas(self):
        name = self.inputFasilitas.text()
        description = self.inputDeskripsi.text()
        price = self.inputHarga.text()
        
        if name and description and price:
            # Add to database
            facility_id = self.db_manager.add_facility(name, description, price)
            
            if facility_id:
                # Add to local list and update table
                self.facilities.append({
                    "id": facility_id,
                    "name": name,
                    "description": description,
                    "price": price
                })
                self.update_table()
                
                # Clear input fields
                self.inputFasilitas.clear()
                self.inputDeskripsi.clear()
                self.inputHarga.clear()
            else:
                QtWidgets.QMessageBox.warning(None, "Error", "Gagal menambahkan fasilitas")

    def update_fasilitas(self):
        # Get the currently selected row
        selected_rows = self.facilityTable.selectedIndexes()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(
                None, 
                "Peringatan", 
                "Pilih fasilitas yang ingin diupdate terlebih dahulu!"
            )
            return

        # Get the first selected row
        row = selected_rows[0].row()

        # Validate input fields
        name = self.inputFasilitas.text().strip()
        description = self.inputDeskripsi.text().strip()
        price = self.inputHarga.text().strip()

        # Check if all fields are filled
        if not (name and description and price):
            QtWidgets.QMessageBox.warning(
                None, 
                "Peringatan", 
                "Semua field harus diisi!"
            )
            return

        # Confirm update
        reply = QtWidgets.QMessageBox.question(
            None, 
            "Konfirmasi Update", 
            "Apakah Anda yakin ingin mengupdate fasilitas ini?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                # Get the facility ID from the current selection
                facility_id = self.facilities[row].get('id')

                # Update in database
                if self.db_manager.update_facility(facility_id, name, description, price):
                    # Update local list
                    self.facilities[row] = {
                        'id': facility_id,
                        'name': name, 
                        'description': description, 
                        'price': price
                    }

                    # Update table
                    self.update_table()

                    # Clear input fields
                    self.inputFasilitas.clear()
                    self.inputDeskripsi.clear()
                    self.inputHarga.clear()

                    # Show success message
                    QtWidgets.QMessageBox.information(
                        None, 
                        "Berhasil", 
                        "Fasilitas berhasil diupdate!"
                    )
                else:
                    QtWidgets.QMessageBox.warning(
                        None, 
                        "Gagal", 
                        "Gagal mengupdate fasilitas di database."
                    )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    None, 
                    "Error", 
                    f"Terjadi kesalahan: {str(e)}"
                )

    def delete_fasilitas(self):
        # Get the currently selected rows
        selected_rows = self.facilityTable.selectedIndexes()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(
                None, 
                "Peringatan", 
                "Pilih fasilitas yang ingin dihapus terlebih dahulu!"
            )
            return

        # Get the first selected row
        row = selected_rows[0].row()

        # Confirm deletion
        reply = QtWidgets.QMessageBox.question(
            None, 
            "Konfirmasi Hapus", 
            "Apakah Anda yakin ingin menghapus fasilitas ini?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                # Get the facility ID from the current selection
                facility_id = self.facilities[row].get('id')

                # Delete from database
                if self.db_manager.delete_facility(facility_id):
                    # Remove from local list
                    del self.facilities[row]

                    # Update table
                    self.update_table()

                    # Clear input fields
                    self.inputFasilitas.clear()
                    self.inputDeskripsi.clear()
                    self.inputHarga.clear()

                    # Show success message
                    QtWidgets.QMessageBox.information(
                        None, 
                        "Berhasil", 
                        "Fasilitas berhasil dihapus!"
                    )
                else:
                    QtWidgets.QMessageBox.warning(
                        None, 
                        "Gagal", 
                        "Gagal menghapus fasilitas dari database."
                    )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    None, 
                    "Error", 
                    f"Terjadi kesalahan: {str(e)}"
                )

    def update_table(self):
        # Disable sorting during update to prevent unexpected behavior
        self.facilityTable.setSortingEnabled(False)
        
        # Clear existing rows
        self.facilityTable.setRowCount(0)
        
        # Ensure facilities list is not None
        if not self.facilities:
            self.facilityTable.setSortingEnabled(True)
            return
        
        # Insert rows for each facility
        for facility in self.facilities:
            row_position = self.facilityTable.rowCount()
            self.facilityTable.insertRow(row_position)
            
            # Create table items with improved formatting and alignment
            name_item = QtWidgets.QTableWidgetItem(str(facility.get("name", "")))
            name_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            
            description_item = QtWidgets.QTableWidgetItem(str(facility.get("description", "")))
            description_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            
            price_item = QtWidgets.QTableWidgetItem(str(facility.get("price", "")))
            price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            
            # Set items in table
            self.facilityTable.setItem(row_position, 0, name_item)
            self.facilityTable.setItem(row_position, 1, description_item)
            self.facilityTable.setItem(row_position, 2, price_item)
        
        # Re-enable sorting
        self.facilityTable.setSortingEnabled(True)

    def filter_table(self):
        search_term = self.searchBar.text().lower()
        
        # If search term is empty, reload all facilities
        if not search_term:
            self.load_facilities()
            return
        
        # Perform database search
        db_facilities = self.db_manager.search_facilities(search_term)
        
        # Update local facilities list and table
        self.facilities = []
        for facility in db_facilities:
            self.facilities.append({
                "id": facility['id'],
                "name": facility['facility_name'],
                "description": facility['description'],
                "price": facility['price']
            })
        
        self.update_table()

    # def add_initial_data(self):
    #     initial_data = [
    #         {"name": "Spa", "description": "Relaksasi dengan layanan spa berkualitas tinggi", "price": "200.000"},
    #         {"name": "Game Center", "description": "Pusat hiburan dengan berbagai permainan seru", "price": "150.000"},
    #         {"name": "Bioskop", "description": "Nikmati film favorit dengan layar besar", "price": "200.000"},
    #         {"name": "Kolam Renang", "description": "Kolam renang outdoor dengan pemandangan indah", "price": "100.000"},
    #         {"name": "Gym", "description": "Fasilitas gym lengkap untuk menjaga kebugaran Anda", "price": "75.000"},
    #     ]
    #     self.facilities.extend(initial_data)
    #     self.update_table()

    def go_back(self):
        """
        Close current window and return to main dashboard
        """
        from inicr import Ui_MainWindow as menu
        
        # Import here to avoid circular import
        self.window = QtWidgets.QMainWindow()
        self.ui = menu()
        self.ui.setupUi(self.window)
        QtWidgets.QApplication.activeWindow().close()
        self.window.showMaximized()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

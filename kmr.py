from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)  # Ukuran jendela lebih besar
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout utama untuk widget pusat
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Menambahkan label di atas tabel dengan tulisan "Tipe Kamar di Hotel Acumalaka"
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setText("Tipe Kamar di Hotel Acumalaka")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)  # Agar tulisan berada di tengah
        self.title_label.setFont(QtGui.QFont("Comic Sans MS", 24, QtGui.QFont.Bold))
        self.title_label.setStyleSheet("""
            color: #3f6ad8;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        """)
        self.main_layout.addWidget(self.title_label)

        # Menambahkan search bar
        self.search_layout = QtWidgets.QHBoxLayout()

        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setPlaceholderText("Cari Tipe Kamar...")
        self.search_input.setFont(QtGui.QFont("Arial", 14))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 12px;
                border: 2px solid #3f6ad8;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #28a745;
                background-color: #f1f1f1;
            }
        """)
        self.search_input.textChanged.connect(self.search_rooms)
        self.search_layout.addWidget(self.search_input)

        self.main_layout.addLayout(self.search_layout)

        # Tabel untuk menampilkan data kamar tanpa kolom Aksi
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(3)  # Mengurangi kolom Aksi
        self.tableWidget.setHorizontalHeaderLabels(["Tipe Kamar", "Harga", "Deskripsi"])

        # Styling untuk header
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)  # Kolom Tipe Kamar
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)  # Kolom Harga
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)  # Kolom Deskripsi

        self.tableWidget.setMinimumHeight(400)  # Set ukuran minimal untuk tinggi tabel
        self.tableWidget.setMinimumWidth(900)  # Set ukuran minimal untuk lebar tabel

        # Menambahkan desain tabel
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # Mengizinkan edit saat klik ganda
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # Memilih seluruh baris
        self.tableWidget.setAlternatingRowColors(True)  # Baris bergantian warna untuk kenyamanan baca

        # Styling untuk tabel
        self.tableWidget.setStyleSheet(""" 
            QTableWidget {
                border: 2px solid #ddd;
                background-color: #f9f9f9;
                font-size: 16px;
                color: #333;
                font-family: "Arial";
            }
            QTableWidget::item {
                padding: 12px;
            }
            QHeaderView::section {
                background-color: #3f6ad8;
                color: white;
                font-weight: bold;
                font-size: 18px;
                padding: 10px;
                text-align: center;
            }
            QTableWidget::horizontalHeader {
                border: 2px solid #ddd;
            }
            QTableWidget::item:hover {
                background-color: #e9e9e9;
            }
        """)

        self.main_layout.addWidget(self.tableWidget)

        # Mengisi tabel dengan data awal
        self.populate_table()

        # Layout form untuk input data
        self.form_layout = QtWidgets.QFormLayout()
        self.room_name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.room_name_input.setPlaceholderText("Masukkan nama kamar")
        self.room_name_input.setFont(QtGui.QFont("Arial", 14))
        self.form_layout.addRow("Nama Kamar:", self.room_name_input)

        self.room_price_input = QtWidgets.QLineEdit(self.centralwidget)
        self.room_price_input.setPlaceholderText("Masukkan harga kamar")
        self.room_price_input.setFont(QtGui.QFont("Arial", 14))
        self.form_layout.addRow("Harga:", self.room_price_input)

        self.room_desc_input = QtWidgets.QLineEdit(self.centralwidget)
        self.room_desc_input.setPlaceholderText("Masukkan deskripsi kamar")
        self.room_desc_input.setFont(QtGui.QFont("Arial", 14))
        self.form_layout.addRow("Deskripsi:", self.room_desc_input)

        self.main_layout.addLayout(self.form_layout)

        # Layout untuk tombol
        self.button_layout = QtWidgets.QHBoxLayout()

        self.add_button = QtWidgets.QPushButton("Tambah Kamar", self.centralwidget)
        self.add_button.setStyleSheet(""" 
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.add_button.clicked.connect(self.add_room)
        self.button_layout.addWidget(self.add_button)

        self.update_button = QtWidgets.QPushButton("Perbarui Kamar", self.centralwidget)
        self.update_button.setStyleSheet(""" 
            QPushButton {
                background-color: #ffc107;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        self.update_button.clicked.connect(self.update_room)
        self.button_layout.addWidget(self.update_button)

        self.delete_button = QtWidgets.QPushButton("Hapus Kamar", self.centralwidget)
        self.delete_button.setStyleSheet(""" 
            QPushButton {
                background-color: #dc3545;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.delete_button.clicked.connect(self.delete_room)
        self.button_layout.addWidget(self.delete_button)

        self.clear_button = QtWidgets.QPushButton("Kosongkan Form", self.centralwidget)
        self.clear_button.setStyleSheet(""" 
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.clear_button.clicked.connect(self.clear_fields)
        self.button_layout.addWidget(self.clear_button)

        # Tombol Kembali
        self.back_button = QtWidgets.QPushButton("Kembali", self.centralwidget)
        self.back_button.setStyleSheet(""" 
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
        """)
        self.back_button.clicked.connect(self.back_action)
        self.button_layout.addWidget(self.back_button)

        self.main_layout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tipe Kamar Hotel"))

    def populate_table(self):
        # Menambahkan 5 data awal ke dalam tabel
        self.sample_data = [
            ("Standard Room", "Rp 500.000", "Kamar nyaman dengan fasilitas modern."),
            ("Executive Room", "Rp 1.500.000", "Kamar dasar untuk satu orang."),
            ("Deluxe Room", "Rp 2.500.000", "Suite mewah dengan kolam renang pribadi dan teras."),
            ("Suite Room", "Rp 3.000.000", "Kamar luas dengan tempat tidur king-size dan pemandangan laut."),
            ("Presidential Room", "Rp 5.000.000", "Kamar terjangkau dengan fasilitas dasar.")
        ]

        # Memasukkan data awal ke dalam tabel
        for data in self.sample_data:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(data[0]))
            self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(data[1]))
            self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(data[2]))

    def search_rooms(self):
        search_text = self.search_input.text().lower()
        self.tableWidget.setRowCount(0)  # Reset tabel
        for data in self.sample_data:
            if search_text in data[0].lower() or search_text in data[1].lower() or search_text in data[2].lower():
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(data[0]))
                self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(data[1]))
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(data[2]))

    def add_room(self):
        room_name = self.room_name_input.text()
        room_price = self.room_price_input.text()
        room_desc = self.room_desc_input.text()

        if room_name and room_price and room_desc:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(room_name))
            self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(room_price))
            self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(room_desc))

            self.clear_fields()
            self.sample_data.append((room_name, room_price, room_desc))
        else:
            self.show_error("Harap isi semua kolom.")

    def update_room(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            room_name = self.room_name_input.text()
            room_price = self.room_price_input.text()
            room_desc = self.room_desc_input.text()

            if room_name and room_price and room_desc:
                self.tableWidget.setItem(selected_row, 0, QtWidgets.QTableWidgetItem(room_name))
                self.tableWidget.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(room_price))
                self.tableWidget.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(room_desc))

                self.clear_fields()
                self.sample_data[selected_row] = (room_name, room_price, room_desc)
            else:
                self.show_error("Harap isi semua kolom.")
        else:
            self.show_error("Pilih kamar yang akan diperbarui.")

    def delete_room(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            self.tableWidget.removeRow(selected_row)
            del self.sample_data[selected_row]
        else:
            self.show_error("Pilih kamar yang akan dihapus.")

    def clear_fields(self):
        self.room_name_input.clear()
        self.room_price_input.clear()
        self.room_desc_input.clear()

    def show_error(self, message):
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage(message)
        error_dialog.exec_()

    def back_action(self):
        # Menutup aplikasi atau melakukan aksi lain
        QtWidgets.QApplication.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

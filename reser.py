from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import subprocess
import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Set theme
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #d4f1f4;
                font-family: 'Arial', sans-serif;
            }
            QLabel {
                font-size: 18px;
                color: #2a9df4;
                font-weight: bold;
                padding: 5px 0;
            }
            QLineEdit, QComboBox, QDateTimeEdit {
                background-color: #ffffff;
                border: 2px solid #2a9df4;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #ff007f;
                color: white;
                border-radius: 10px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout utama
        self.titleLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.titleLayout.setContentsMargins(20, 20, 20, 10)

        # Judul
        self.label = QtWidgets.QLabel("Form Reservasi Hotel Acumalaka", self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 32px; font-weight: bold; color: #ff007f;")
        self.titleLayout.addWidget(self.label)

        # Scroll Area
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_content_widget)

        # Layout di dalam scroll area
        self.scroll_layout = QtWidgets.QFormLayout(self.scroll_content_widget)
        self.scroll_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll_layout.setHorizontalSpacing(20)
        self.scroll_layout.setVerticalSpacing(15)

        # Tambahkan form
        self.add_form_field("Nama Lengkap:", QtWidgets.QLineEdit())
        self.add_form_field("No KTP:", QtWidgets.QLineEdit())
        self.add_form_field("Tanggal Check-in:", self.create_date_edit())
        self.add_form_field("Tanggal Check-out:", self.create_date_edit())

        # Fasilitas
        self.fasilitas_combo = self.create_combo(["Spa - Rp 200,000", "Game Center - Rp 150,000",
                                                  "Bioskop - Rp 200,000", "Kolam Renang - Rp 100,000",
                                                  "Gym - Rp 75,000"])
        self.add_form_field("Fasilitas:", self.fasilitas_combo)

        # Jenis Kelamin
        self.add_form_field("Jenis Kelamin:", self.create_combo(["Laki-Laki", "Perempuan"]))
        self.add_form_field("Jumlah Orang:", QtWidgets.QLineEdit())

        # Layout untuk jenis kamar
        self.room_layout = QtWidgets.QVBoxLayout()
        self.room_widgets = []  # Menyimpan referensi untuk jenis kamar dan jumlah kamar
        self.add_room_type_field()

        # Tambahkan tombol untuk hitung total harga
        self.calculate_price_button = QtWidgets.QPushButton("Hitung Total Harga")
        self.calculate_price_button.clicked.connect(self.calculate_total_price)
        self.room_layout.addWidget(self.calculate_price_button)

        # Label total harga
        self.total_price_label = QtWidgets.QLabel("Total Harga: Rp 0")
        self.room_layout.addWidget(self.total_price_label)

        self.scroll_layout.addRow(QtWidgets.QLabel("Jenis Kamar:"), self.room_layout)

        # Tambahkan scroll area ke layout utama
        self.titleLayout.addWidget(self.scroll_area)

        # Tombol navigasi
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.backButton = self.create_button("Kembali")
        self.backButton.clicked.connect(self.go_back_to_pet)
        self.reserveButton = self.create_button("Reservasi")
        self.reserveButton.clicked.connect(self.go_to_bayar)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.reserveButton)

        self.titleLayout.addLayout(self.buttonLayout)
        MainWindow.setCentralWidget(self.centralwidget)

    def add_form_field(self, label_text, widget):
        label = QtWidgets.QLabel(label_text)
        self.scroll_layout.addRow(label, widget)

    def create_combo(self, items):
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        return combo

    def create_date_edit(self):
        date_edit = QtWidgets.QDateTimeEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDisplayFormat("dd/MM/yyyy")
        date_edit.setDate(QtCore.QDate.currentDate())
        return date_edit

    def create_button(self, text):
        button = QtWidgets.QPushButton(text)
        button.setFixedHeight(40)
        return button

    def add_room_type_field(self):
        self.room_prices = {
            "Standard Room": 500000,
            "Executive Room": 1500000,
            "Deluxe Room": 2500000,
            "Suite Room": 3000000,
            "Presidential Room": 5000000
        }

        room_type_combobox = self.create_combo([f"{name} - Rp {price:,}" for name, price in self.room_prices.items()])
        room_quantity_input = QtWidgets.QLineEdit()
        room_quantity_input.setPlaceholderText("Jumlah Kamar")
        room_quantity_input.setValidator(QtGui.QIntValidator(0, 100))

        # Simpan referensi
        self.room_widgets.append((room_type_combobox, room_quantity_input))

        # Tambahkan ke layout
        room_layout_item = QtWidgets.QWidget()
        room_layout_item.setLayout(QtWidgets.QVBoxLayout())
        room_layout_item.layout().addWidget(QtWidgets.QLabel("Jenis Kamar:"))
        room_layout_item.layout().addWidget(room_type_combobox)
        room_layout_item.layout().addWidget(QtWidgets.QLabel("Jumlah Kamar:"))
        room_layout_item.layout().addWidget(room_quantity_input)

        self.room_layout.addWidget(room_layout_item)

    def calculate_total_price(self):
        total_price = 0

        # Mengambil jumlah orang
        try:
            num_people = int(self.scroll_layout.itemAt(5).widget().text())  # Mengambil input Jumlah Orang
        except ValueError:
            num_people = 1  # Default 1 orang jika input tidak valid

        # Mengambil harga fasilitas
        fasilitas_text = self.fasilitas_combo.currentText()
        fasilitas_price = int(fasilitas_text.split(" - Rp ")[1].replace(",", ""))
        total_price += fasilitas_price * num_people  # Fasilitas dihitung per orang

        # Mengambil harga kamar dan jumlah kamar
        for room_type_combobox, room_quantity_input in self.room_widgets:
            room_type_text = room_type_combobox.currentText()
            room_type = room_type_text.split(" - ")[0]
            try:
                room_quantity = int(room_quantity_input.text())
                total_price += self.room_prices[room_type] * room_quantity * num_people  # Harga kamar per orang
            except ValueError:
                pass

        # Menampilkan total harga
        self.total_price_label.setText(f"Total Harga: Rp {total_price:,}")

    def go_back_to_pet(self):
        subprocess.Popen(["python", "pet.py"])

    def go_to_bayar(self):
        order_number = random.randint(1000, 9999)
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.setText(f"Reservasi berhasil! Nomor Pesanan Anda: {order_number}")
        message.setWindowTitle("Reservasi Sukses")
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.exec_()
        subprocess.Popen(["python", "bayar.py"])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())

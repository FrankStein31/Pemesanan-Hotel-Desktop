import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from databasemanager import DatabaseManager

class Ui_MainWindow(object):
    def __init__(self):
        self.db_manager = DatabaseManager()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)  # Increased width for more columns
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout utama
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Search Bar
        self.search_bar = QtWidgets.QLineEdit(self.centralwidget)
        self.search_bar.setPlaceholderText("Cari berdasarkan Nama, Jenis Kamar, atau Metode Pembayaran")
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
        self.search_bar.textChanged.connect(self.filter_table)
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
        self.tableWidget.setRowCount(0)
        # self.tableWidget.setColumnCount(8)  # Increased column count
        # self.tableWidget.setHorizontalHeaderLabels([
        #     "Tanggal Pemesanan", 
        #     "Nama", 
        #     "Check-in", 
        #     "Check-out", 
        #     "Jenis Kamar", 
        #     "Nomor Kamar", 
        #     "Metode Pembayaran", 
        #     "Total"
        # ])
        self.tableWidget.setColumnCount(8)  
        self.tableWidget.setHorizontalHeaderLabels([
            "Tanggal Pemesanan", 
            "Nama", 
            "Check-in", 
            "Check-out", 
            "Jenis Kamar", 
            "Nomor Kamar", 
            "Status", 
            "Total"
        ])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Styling Tabel
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #ecf0f1;
                border: 1px solid #34495e;
                font-size: 14px;
                font-family: 'Segoe UI', sans-serif;
                border-radius: 15px;
                padding: 15px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: #ffffff;
                padding: 12px;
                font-size: 14px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

        main_layout.addWidget(self.tableWidget)

        # Tombol Layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(30)

        # Tombol Kembali 
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
        self.backButton.clicked.connect(self.go_back)

        # Tombol Refresh
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
        self.refreshButton.clicked.connect(self.load_reservation_history)
        button_layout.addWidget(self.refreshButton)

        main_layout.addLayout(button_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        # Load reservation history when the window is set up
        self.load_reservation_history()

    def go_back(self):
        """
        Close current window and return to main dashboard
        """
        from pet import Ui_MainWindow as DashboardWindowpet
        
        # Import here to avoid circular import
        self.window = QtWidgets.QMainWindow()
        self.ui = DashboardWindowpet()
        self.ui.setupUi(self.window)
        QtWidgets.QApplication.activeWindow().close()
        self.window.showMaximized()

    def load_reservation_history(self):
        """Mengambil data riwayat reservasi dari database dengan detail lengkap."""
        try:
            query = """
            SELECT 
                reservations.created_at AS tanggal_pemesanan, 
                customers.name AS nama, 
                reservations.check_in_date AS check_in,
                reservations.check_out_date AS check_out,
                room_types.type_name AS jenis_kamar, 
                rooms.room_number AS nomor_kamar,
                reservations.status AS status_reservasi,
                reservations.total_price AS total
            FROM 
                reservations
            JOIN customers ON reservations.customer_id = customers.id
            JOIN reservation_rooms ON reservations.id = reservation_rooms.reservation_id
            JOIN rooms ON reservation_rooms.room_id = rooms.id
            JOIN room_types ON rooms.room_type_id = room_types.id
            ORDER BY 
                reservations.created_at DESC
            """
            
            self.db_manager.cursor.execute(query)
            results = self.db_manager.cursor.fetchall()
            
            # Clear existing rows
            self.tableWidget.setRowCount(0)

            # Populate table
            for row_data in results:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                
                # Format dates
                booking_date = row_data['tanggal_pemesanan'].strftime("%d/%m/%Y")
                check_in = row_data['check_in'].strftime("%d/%m/%Y")
                check_out = row_data['check_out'].strftime("%d/%m/%Y")
                
                # Format total price
                total = f"Rp {row_data['total']:,.0f}".replace(',', '.')

                # Set table items
                self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(booking_date)))
                self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(row_data['nama'])))
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(check_in)))
                self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(check_out)))
                self.tableWidget.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(row_data['jenis_kamar'])))
                self.tableWidget.setItem(row_position, 5, QtWidgets.QTableWidgetItem(str(row_data['nomor_kamar'])))
                self.tableWidget.setItem(row_position, 6, QtWidgets.QTableWidgetItem(str(row_data['status_reservasi'])))
                self.tableWidget.setItem(row_position, 7, QtWidgets.QTableWidgetItem(total))

        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Error loading reservation history: {str(e)}")
            print(f"Detailed error: {e}")
            import traceback
            traceback.print_exc()

    def filter_table(self):
        """Filter tabel berdasarkan input pencarian."""
        query = self.search_bar.text().lower()
        
        for row in range(self.tableWidget.rowCount()):
            show_row = query == "" or any(
                query in str(self.tableWidget.item(row, col).text()).lower() 
                for col in range(self.tableWidget.columnCount())
            )
            
            self.tableWidget.setRowHidden(row, not show_row)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Riwayat Pemesanan"))

class MainWindowWithHistory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindowWithHistory()
    MainWindow.showMaximized()
    sys.exit(app.exec_())
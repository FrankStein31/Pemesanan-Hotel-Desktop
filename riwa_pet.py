import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from databasemanager import DatabaseManager

class Ui_MainWindow(object):
    def __init__(self):
        self.db_manager = DatabaseManager()

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
        self.search_bar.setPlaceholderText("Cari berdasarkan Nama atau Jenis Kamar")
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
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Tanggal Pemesanan", "Nama", "Jenis Kamar", "Total"])
        # self.tableWidget.setHorizontalHeaderLabels(["Tanggal Pemesanan", "Nama", "Jenis Kamar", "Total", "Status"])
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
        """Mengambil data riwayat reservasi dari database."""
        try:
            # Sederhanakan query
            query = """
            SELECT 
                created_at AS tanggal_pemesanan, 
                (SELECT name FROM customers WHERE id = customer_id) AS nama, 
                (SELECT type_name FROM room_types 
                JOIN rooms ON rooms.room_type_id = room_types.id 
                JOIN reservation_rooms ON reservation_rooms.room_id = rooms.id 
                WHERE reservation_rooms.reservation_id = reservations.id 
                LIMIT 1) AS jenis_kamar, 
                total_price AS total
            FROM 
                reservations
            ORDER BY 
                created_at DESC
            """
            
            # Execute query
            self.db_manager.cursor.execute(query)
            results = self.db_manager.cursor.fetchall()
            
            # Print results for debugging
            print("Number of reservations:", len(results))
            for result in results:
                print(result)

            # Clear existing rows
            self.tableWidget.setRowCount(0)

            # Populate table
            for row_data in results:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                
                # Format date
                date = row_data['tanggal_pemesanan'].strftime("%d/%m/%Y")
                
                # Format total price
                total = f"Rp {row_data['total']:,.0f}".replace(',', '.')

                # Set table items
                self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(date)))
                self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(row_data['nama'])))
                self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(row_data['jenis_kamar'])))
                self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(total))
                # self.tableWidget.setItem(row_position, 4, QtWidgets.QTableWidgetItem(row_data['status']))

        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Error loading reservation history: {str(e)}")
            print(f"Detailed error: {e}")
            import traceback
            traceback.print_exc()

    def filter_table(self):
        """Filter tabel berdasarkan input pencarian."""
        query = self.search_bar.text().lower()
        
        for row in range(self.tableWidget.rowCount()):
            # Tentukan apakah baris harus ditampilkan
            show_row = query == "" or any(
                query in str(self.tableWidget.item(row, col).text()).lower() 
                for col in range(self.tableWidget.columnCount())
            )
            
            self.tableWidget.setRowHidden(row, QtCore.QModelIndex(), not show_row)

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
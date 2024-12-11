from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Scroll area setup
        scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("border: none;")

        scrollContent = QtWidgets.QWidget()
        scrollArea.setWidget(scrollContent)

        mainLayout = QtWidgets.QVBoxLayout(scrollContent)
        mainLayout.setContentsMargins(40, 40, 40, 40)
        mainLayout.setSpacing(20)

        # Background gradient (dark, elegant tones)
        scrollContent.setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                        stop:0 #3a4e77, stop:1 #62799a);
        """)

        # Title label with elegant style
        self.label = QtWidgets.QLabel(scrollContent)
        self.label.setText("Hotel Acumalaka Gallery")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-size: 48px;
            font-weight: 800;
            color: #f4d03f;
            font-family: 'Georgia', serif;
            text-transform: uppercase;
            text-shadow: 3px 3px 15px rgba(0, 0, 0, 0.5);
        """)
        mainLayout.addWidget(self.label)

        # Detailed information for rooms and facilities
        self.room_details = {
            "ys.jpg": {
                "name": "Standard Room",
                "description": "Kamar nyaman dengan fasilitas dasar yang lengkap.",
                "price": "Rp 500.000/malam",
                "features": [
                    "Tempat tidur queen size",
                    "AC",
                    "TV LCD",
                    "Wi-Fi gratis",
                    "Kamar mandi dalam"
                ]
            },
            "suite.jpg": {
                "name": "Executive Room",
                "description": "Kamar eksklusif dengan pemandangan indah dan fasilitas premium.",
                "price": "Rp 1.500.000/malam",
                "features": [
                    "Tempat tidur king size",
                    "Area kerja pribadi",
                    "Balkon pribadi",
                    "TV layar besar",
                    "Minibar",
                    "Akses kolam renang eksklusif"
                ]
            },
            "sui.jpg": {
                "name": "Deluxe Room",
                "description": "Kamar mewah dengan desain modern dan fasilitas lengkap.",
                "price": "Rp 2.500.000/malam",
                "features": [
                    "Tempat tidur king size spesial",
                    "Ruang duduk pribadi",
                    "Pemandangan kota",
                    "Fasilitas coffee maker",
                    "Layanan kamar 24 jam",
                    "Akses gym gratis"
                ]
            },
            "spa.jpg": {
                "name": "Spa Facility",
                "description": "Fasilitas spa berkelas dengan berbagai treatment menenangkan.",
                "price": "Mulai dari Rp 200.000/sesi",
                "features": [
                    "Massage tradisional",
                    "Treatment wajah",
                    "Aromaterapi",
                    "Sauna",
                    "Terapis berpengalaman"
                ]
            },
            "gc.jpg": {
                "name": "Game Center",
                "description": "Pusat hiburan modern dengan berbagai permainan seru.",
                "price": "Rp 150.000/jam",
                "features": [
                    "Playstation 5",
                    "Meja billiard",
                    "Meja ping pong",
                    "Konsol game terbaru",
                    "Ruangan ber-AC"
                ]
            },
            "bio.jpg": {
                "name": "Bioskop Hotel",
                "description": "Bioskop privat dengan layar lebar dan sistem suara canggih.",
                "price": "Rp 200.000/sesi",
                "features": [
                    "Layar 4K",
                    "Sistem suara Dolby Atmos",
                    "Kursi empuk",
                    "Pilihan film terbaru",
                    "Layanan cemilan"
                ]
            }
        }

        # Image categories
        image_categories = [
            ("Rooms", ["ys.jpg", "suite.jpg", "sui.jpg"]),
            ("Facilities", ["spa.jpg", "gc.jpg", "bio.jpg"])
        ]

        # Create expandable image gallery
        for category_name, images in image_categories:
            # Category Label
            categoryLabel = QtWidgets.QLabel(scrollContent)
            categoryLabel.setText(category_name)
            categoryLabel.setStyleSheet("""
                font-size: 24px;
                color: #f4d03f;
                font-weight: 700;
                font-family: 'Georgia', serif;
                text-transform: uppercase;
            """)
            mainLayout.addWidget(categoryLabel)

            # Image Grid for this category
            categoryGrid = QtWidgets.QGridLayout()
            categoryGrid.setSpacing(15)

            for row in range(0, len(images), 3):
                for col in range(min(3, len(images) - row)):
                    image_path = images[row + col]
                    
                    # Image Widget
                    imageLabel = QtWidgets.QLabel(scrollContent)
                    
                    # Closure to capture the current image path
                    def create_image_handler(path):
                        return lambda event: self.show_image_details(path)
                    
                    pixmap = QtGui.QPixmap(image_path).scaled(
                        250, 250, 
                        QtCore.Qt.KeepAspectRatio, 
                        QtCore.Qt.SmoothTransformation
                    )
                    imageLabel.setPixmap(pixmap)
                    imageLabel.setStyleSheet("""
                        border: 3px solid #f4d03f;
                        border-radius: 15px;
                        padding: 5px;
                        cursor: pointer;
                    """)
                    
                    # Use closure to handle image click
                    imageLabel.mousePressEvent = create_image_handler(image_path)
                    
                    categoryGrid.addWidget(imageLabel, row // 3, col)

            mainLayout.addLayout(categoryGrid)

        # Back button with elegant hover effect
        self.backButton = QtWidgets.QPushButton(scrollContent)
        self.backButton.setText("Kembali")
        self.backButton.setStyleSheet("""
            background-color: #f4d03f;
            color: #2d4059;
            font-size: 20px;
            font-weight: bold;
            padding: 15px;
            border-radius: 30px;
            font-family: 'Georgia', serif;
        """)
        self.backButton.clicked.connect(self.goBack)
        mainLayout.addWidget(self.backButton)

        # Add scroll area to the main window
        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.addWidget(scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle("Hotel Acumalaka - Image Gallery")

    def show_image_details(self, image_path):
        """
        Show detailed information about the selected image
        """
        if image_path not in self.room_details:
            QtWidgets.QMessageBox.information(None, "Informasi", "Detail tidak tersedia.")
            return

        details = self.room_details[image_path]
        
        # Create dialog
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(details['name'])
        dialog.setStyleSheet("background-color: #f0f0f0;")
        
        # Main layout
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Image
        imageLabel = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(image_path).scaled(
            400, 400, 
            QtCore.Qt.KeepAspectRatio, 
            QtCore.Qt.SmoothTransformation
        )
        imageLabel.setPixmap(pixmap)
        imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(imageLabel)
        
        # Title
        titleLabel = QtWidgets.QLabel(details['name'])
        titleLabel.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2d4059;
            margin-bottom: 10px;
        """)
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(titleLabel)
        
        # Description
        descLabel = QtWidgets.QLabel(details['description'])
        descLabel.setStyleSheet("""
            font-size: 16px;
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        """)
        descLabel.setWordWrap(True)
        layout.addWidget(descLabel)
        
        # Price
        priceLabel = QtWidgets.QLabel(f"Harga: {details['price']}")
        priceLabel.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 10px;
        """)
        priceLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(priceLabel)
        
        # Features
        featuresLabel = QtWidgets.QLabel("Fasilitas:")
        featuresLabel.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2d4059;
            margin-bottom: 5px;
        """)
        layout.addWidget(featuresLabel)
        
        # Features List
        featuresList = QtWidgets.QListWidget()
        featuresList.addItems(details['features'])
        featuresList.setStyleSheet("""
            font-size: 14px;
            color: #333;
        """)
        layout.addWidget(featuresList)
        
        # Close Button
        closeButton = QtWidgets.QPushButton("Tutup")
        closeButton.setStyleSheet("""
            background-color: #2d4059;
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)
        closeButton.clicked.connect(dialog.close)
        layout.addWidget(closeButton)
        
        # Show dialog
        dialog.exec_()

    def goBack(self):
        """
        Close current window and return to main dashboard
        """
        from dash import Ui_MainWindow as DashboardWindow
        
        # Import here to avoid circular import
        self.window = QtWidgets.QMainWindow()
        self.ui = DashboardWindow()
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
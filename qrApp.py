from pathlib import Path 
import qrcode
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QDialog, QMainWindow, QLabel, QWidget,
                                QVBoxLayout, QHBoxLayout, QGridLayout, 
                                QPushButton, QLineEdit, QSlider, QComboBox, 
                                QProgressBar, QListWidget, QFileDialog)
from PySide6.QtGui import QIcon, QFont, QImage, QImage, QPixmap

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

class QrApp(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
         
        self.setFixedSize(400, 400)
        self.setFont(QFont("Segoe UI", 10))
        self.setWindowTitle("QR Code")

        layout = QVBoxLayout(self)

        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pixmap = pixmap
        qr_label.setPixmap(self.pixmap)

        layout.addWidget(qr_label)
        

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selected_folder = ""

        self.setFont(QFont("Segoe UI", 10))
        self.setFixedSize(500, 350)
        self.setWindowIcon(QIcon(str(resource_path("icon1.ico"))))
        #self.setStyleSheet("background-color: #f0f0f0;")
        self.setWindowTitle("QR Code Generator")
        self.setAcceptDrops(True)


        container = QWidget()

        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()

        self.setLayout(layout)

        self.label = QLabel("Enter URL: ")
        self.url = QLineEdit()

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.browse_btn = QPushButton("Save QRCode")
        self.generate_btn = QPushButton("Generate QRCode")

        self.browse_btn.clicked.connect(self.select_folder)
        self.generate_btn.clicked.connect(self.generate)

        layout1.addWidget(self.label)
        layout1.addWidget(self.url)

        self.layout2.addWidget(self.generate_btn)

        layout.addLayout(layout1)
        layout.addLayout(self.layout2)
        
    def dragEnterEvent(self, event):
        return super().dragEnterEvent(event)
    
    def generate(self):
        url = self.url.text().strip()
        self.qr = qrcode.make(url)
        self.qr = self.qr.convert("RGB")

        data = self.qr.tobytes("raw", "RGB")
        image = QImage(
        data,
        self.qr.width,
        self.qr.height,
        self.qr.width * 3,
        QImage.Format_RGB888
    ).copy()

        pixmap = QPixmap.fromImage(image)

        self.qrWindow = QrApp(pixmap, self)
        self.qrWindow.show()

            
        self.layout2.addWidget(self.browse_btn)

    def select_folder(self):
        
        file, _ = QFileDialog.getSaveFileName(
                        self,
                        "Save QR Code",
                        "",
                        "JPG Files (*.jpg *.jpeg);;PNG Files (*.png)",
                    )
        if file:
            path = Path(file)
            self.qr.save(path)


app = QApplication()
window = Main()
print(window.url.text())
window.show()
app.exec()
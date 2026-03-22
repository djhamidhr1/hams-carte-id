from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(52)
        self.setStyleSheet("background-color: #13131f; border-right: 1px solid #2e2e4e;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 12, 6, 12)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignTop)

        tools = [
            ("↖", "Sélection"),
            ("T", "Texte"),
            ("🖼", "Image"),
            ("▬", "Code-barres"),
            ("⬛", "QR Code"),
            ("╱", "Ligne"),
            ("□", "Rectangle"),
            ("○", "Ellipse"),
        ]
        for icon, tooltip in tools:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 40)
            btn.setToolTip(tooltip)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a3e;
                    color: white;
                    border-radius: 8px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #7c9ef8;
                    color: #0d0d1a;
                }
            """)
            layout.addWidget(btn)
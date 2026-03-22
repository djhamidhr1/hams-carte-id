from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class Toolbar(QWidget):
    def __init__(self, canvas=None, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.setFixedWidth(52)
        self.setStyleSheet("background-color: #13131f; border-right: 1px solid #2e2e4e;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 12, 6, 12)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignTop)

        tools = [
            ("↖", "select", "Sélection"),
            ("T", "text", "Texte"),
            ("🖼", "image", "Image"),
            ("▬", "barcode", "Code-barres"),
            ("⬛", "qr", "QR Code"),
            ("╱", "line", "Ligne"),
            ("□", "rect", "Rectangle"),
            ("○", "ellipse", "Ellipse"),
        ]
        for icon, tool_id, tooltip in tools:
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
            btn.clicked.connect(lambda checked, t=tool_id: self._set_tool(t))
            layout.addWidget(btn)

    def _set_tool(self, tool):
        if self.canvas:
            self.canvas.set_tool(tool)
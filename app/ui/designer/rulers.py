from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont

RULER_SIZE = 25

class Ruler(QWidget):
    def __init__(self, orientation, parent=None):
        super().__init__(parent)
        self.orientation = orientation
        self.px_per_mm = 3.78
        self.offset = 40
        if orientation == Qt.Horizontal:
            self.setFixedHeight(RULER_SIZE)
        else:
            self.setFixedWidth(RULER_SIZE)
        self.setStyleSheet("background-color: #1a1a2e;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#1a1a2e"))

        if self.orientation == Qt.Horizontal:
            max_px = self.width()
        else:
            max_px = self.height()

        max_mm = int((max_px - self.offset) / self.px_per_mm) + 5

        for mm in range(0, max_mm + 1):
            pos = int(self.offset + mm * self.px_per_mm)

            if self.orientation == Qt.Horizontal:
                if pos > self.width():
                    break
                if mm % 10 == 0:
                    # Graduation cm — label chiffre seulement
                    painter.setPen(QColor("#bbbbbb"))
                    painter.drawLine(pos, 0, pos, RULER_SIZE)
                    painter.setFont(QFont("Arial", 7, QFont.Bold))
                    cm_val = mm // 10
                    if cm_val == 0:
                        painter.drawText(pos + 2, 11, "cm")
                    else:
                        painter.drawText(pos + 2, 11, str(cm_val))
                elif mm % 5 == 0:
                    painter.setPen(QColor("#666666"))
                    painter.drawLine(pos, RULER_SIZE - 12, pos, RULER_SIZE)
                else:
                    painter.setPen(QColor("#3a3a5a"))
                    painter.drawLine(pos, RULER_SIZE - 5, pos, RULER_SIZE)

            else:
                if pos > self.height():
                    break
                if mm % 10 == 0:
                    painter.setPen(QColor("#bbbbbb"))
                    painter.drawLine(0, pos, RULER_SIZE, pos)
                    painter.setFont(QFont("Arial", 7, QFont.Bold))
                    cm_val = mm // 10
                    painter.save()
                    painter.translate(11, pos - 2)
                    painter.rotate(-90)
                    if cm_val == 0:
                        painter.drawText(0, 0, "cm")
                    else:
                        painter.drawText(0, 0, str(cm_val))
                    painter.restore()
                elif mm % 5 == 0:
                    painter.setPen(QColor("#666666"))
                    painter.drawLine(RULER_SIZE - 12, pos, RULER_SIZE, pos)
                else:
                    painter.setPen(QColor("#3a3a5a"))
                    painter.drawLine(RULER_SIZE - 5, pos, RULER_SIZE, pos)

        painter.end()
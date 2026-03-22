from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QFont
from ui.designer.rulers import Ruler, RULER_SIZE
from PyQt5.QtWidgets import QSizePolicy

CARD_W = 323
CARD_H = 204

class DraggableText(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.setFlags(
            QGraphicsTextItem.ItemIsMovable |
            QGraphicsTextItem.ItemIsSelectable |
            QGraphicsTextItem.ItemSendsGeometryChanges
        )
        self.setDefaultTextColor(QColor("#000000"))
        self.setFont(QFont("Arial", 12))

class CardView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setStyleSheet("background-color: #2a2a3e; border: none;")
        self.setAlignment(Qt.AlignCenter)
        self.current_tool = "select"
        self._draw_card()

    def set_tool(self, tool):
        self.current_tool = tool

    def _draw_card(self):
        self.scene.clear()
        shadow = QGraphicsRectItem(4, 4, CARD_W, CARD_H)
        shadow.setBrush(QBrush(QColor("#111")))
        shadow.setPen(QPen(Qt.NoPen))
        self.scene.addItem(shadow)
        self.card = QGraphicsRectItem(0, 0, CARD_W, CARD_H)
        self.card.setBrush(QBrush(QColor("white")))
        self.card.setPen(QPen(QColor("#cccccc"), 1))
        self.scene.addItem(self.card)
        self.setSceneRect(-40, -40, CARD_W+80, CARD_H+80)

    def mousePressEvent(self, event):
        if self.current_tool == "text":
            pos = self.mapToScene(event.pos())
            if 0 <= pos.x() <= CARD_W and 0 <= pos.y() <= CARD_H:
                txt = DraggableText("Votre texte ici")
                txt.setPos(pos.x(), pos.y())
                self.scene.addItem(txt)
                self.current_tool = "select"
        else:
            super().mousePressEvent(event)

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #2a2a3e;")
        self.setSizePolicy(
            self.sizePolicy().Expanding,
            self.sizePolicy().Expanding
        )

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_row = QHBoxLayout()
        top_row.setSpacing(0)
        top_row.setContentsMargins(0, 0, 0, 0)

        corner = QWidget()
        corner.setFixedSize(RULER_SIZE, RULER_SIZE)
        corner.setStyleSheet("background-color: #1a1a2e;")
        top_row.addWidget(corner)

        self.ruler_h = Ruler(Qt.Horizontal)
        top_row.addWidget(self.ruler_h, 1)
        main_layout.addLayout(top_row)

        center_row = QHBoxLayout()
        center_row.setSpacing(0)
        center_row.setContentsMargins(0, 0, 0, 0)

        self.ruler_v = Ruler(Qt.Vertical)
        center_row.addWidget(self.ruler_v)

        self.card_view = CardView()
        center_row.addWidget(self.card_view, 1)
        main_layout.addLayout(center_row, 1)

    def set_tool(self, tool):
        self.card_view.set_tool(tool)
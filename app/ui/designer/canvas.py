from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter

CARD_W = 323
CARD_H = 204

class Canvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setStyleSheet("background-color: #2a2a3e; border: none;")
        self.setAlignment(Qt.AlignCenter)
        self._draw_card()

    def _draw_card(self):
        self.scene.clear()
        shadow = QGraphicsRectItem(4, 4, CARD_W, CARD_H)
        shadow.setBrush(QBrush(QColor("#111")))
        shadow.setPen(QPen(Qt.NoPen))
        self.scene.addItem(shadow)
        card = QGraphicsRectItem(0, 0, CARD_W, CARD_H)
        card.setBrush(QBrush(QColor("white")))
        card.setPen(QPen(QColor("#cccccc"), 1))
        self.scene.addItem(card)
        txt = QGraphicsTextItem("Carte CR80 — 85.6 × 54 mm")
        txt.setDefaultTextColor(QColor("#aaaaaa"))
        txt.setPos(60, 90)
        self.scene.addItem(txt)
        self.setSceneRect(-40, -40, CARD_W+80, CARD_H+80)
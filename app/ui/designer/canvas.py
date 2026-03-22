from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsTextItem, QGraphicsPixmapItem, QFileDialog,
    QTabWidget, QLabel, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QFont, QPixmap
from ui.designer.rulers import Ruler, RULER_SIZE

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

class DraggableImage(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlags(
            QGraphicsPixmapItem.ItemIsMovable |
            QGraphicsPixmapItem.ItemIsSelectable |
            QGraphicsPixmapItem.ItemSendsGeometryChanges
        )

class CardView(QGraphicsView):
    def __init__(self, face="Recto", parent=None):
        super().__init__(parent)
        self.face = face
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setStyleSheet("background-color: #2a2a3e; border: none;")
        self.setAlignment(Qt.AlignCenter)
        self.current_tool = "select"
        self.on_item_selected = None
        self._draw_card()
        self.scene.selectionChanged.connect(self._on_selection)

    def _on_selection(self):
        items = self.scene.selectedItems()
        if items and self.on_item_selected:
            self.on_item_selected(items[0])

    def set_tool(self, tool):
        self.current_tool = tool
        if tool == "image":
            self._import_image()
        elif tool == "qr":
            self._add_qr()
        elif tool == "barcode":
            self._add_barcode()

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
        label = QGraphicsTextItem(f"── {self.face} ── 85.6 × 54 mm")
        label.setDefaultTextColor(QColor("#cccccc"))
        label.setFont(QFont("Arial", 9))
        label.setPos(80, 90)
        self.scene.addItem(label)
        self.setSceneRect(-40, -40, CARD_W+80, CARD_H+80)

    def _import_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Importer une image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if path:
            pixmap = QPixmap(path)
            if pixmap.width() > CARD_W or pixmap.height() > CARD_H:
                pixmap = pixmap.scaled(
                    CARD_W // 2, CARD_H // 2,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            img = DraggableImage(pixmap)
            img.setPos(10, 10)
            self.scene.addItem(img)
        self.current_tool = "select"

    def _add_qr(self):
        text, ok = QInputDialog.getText(
            self, "QR Code", "Contenu du QR Code :",
            text="https://hams-carte-id.com"
        )
        if ok and text:
            try:
                from modules.qr import generate_qr
                pixmap = generate_qr(text, size=80)
                img = DraggableImage(pixmap)
                img.setPos(CARD_W - 90, CARD_H - 90)
                self.scene.addItem(img)
            except Exception as e:
                print(f"Erreur QR: {e}")
        self.current_tool = "select"

    def _add_barcode(self):
        text, ok = QInputDialog.getText(
            self, "Code-barres", "Numéro du code-barres :",
            text="123456789012"
        )
        if ok and text:
            try:
                from modules.barcode import generate_barcode
                pixmap = generate_barcode(text)
                if pixmap:
                    img = DraggableImage(pixmap)
                    img.setPos(10, CARD_H - 60)
                    self.scene.addItem(img)
            except Exception as e:
                print(f"Erreur barcode: {e}")
        self.current_tool = "select"

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

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Règle horizontale
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

        # Zone centrale
        center_row = QHBoxLayout()
        center_row.setSpacing(0)
        center_row.setContentsMargins(0, 0, 0, 0)
        self.ruler_v = Ruler(Qt.Vertical)
        center_row.addWidget(self.ruler_v)

        # Onglets
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background: #2a2a3e; }
            QTabBar::tab {
                background: #13131f; color: #888;
                padding: 6px 18px;
                border: 1px solid #2e2e4e;
                border-bottom: none;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background: #2a2a3e; color: white;
                border-top: 2px solid #7c9ef8;
            }
            QTabBar::tab:hover { color: white; }
        """)

        # Onglet Recto
        self.recto_view = CardView("Recto")
        self.tabs.addTab(self.recto_view, "◻  Face Avant (Recto)")

        # Onglet Verso
        self.verso_view = CardView("Verso")
        self.tabs.addTab(self.verso_view, "◻  Face Arrière (Verso)")

        # Onglet Recto + Verso vertical
        both_widget = QWidget()
        both_widget.setStyleSheet("background:#2a2a3e;")
        both_layout = QVBoxLayout(both_widget)
        both_layout.setContentsMargins(20, 16, 20, 16)
        both_layout.setSpacing(16)
        both_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        lbl_r = QLabel("RECTO")
        lbl_r.setStyleSheet("color:#7c9ef8; font-size:11px; font-weight:bold;")
        lbl_r.setAlignment(Qt.AlignHCenter)
        both_layout.addWidget(lbl_r)
        self.recto_preview = CardView("Recto")
        self.recto_preview.setFixedHeight(int(CARD_H * 1.4))
        both_layout.addWidget(self.recto_preview)

        lbl_v = QLabel("VERSO")
        lbl_v.setStyleSheet("color:#7c9ef8; font-size:11px; font-weight:bold;")
        lbl_v.setAlignment(Qt.AlignHCenter)
        both_layout.addWidget(lbl_v)
        self.verso_preview = CardView("Verso")
        self.verso_preview.setFixedHeight(int(CARD_H * 1.4))
        both_layout.addWidget(self.verso_preview)
        both_layout.addStretch()
        self.tabs.addTab(both_widget, "⬜⬜  Recto + Verso")

        # Onglet Côte à Côte
        side_widget = QWidget()
        side_widget.setStyleSheet("background:#2a2a3e;")
        side_layout = QHBoxLayout(side_widget)
        side_layout.setContentsMargins(20, 20, 20, 20)
        side_layout.setSpacing(40)
        side_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        left_side = QVBoxLayout()
        lbl_rs = QLabel("RECTO")
        lbl_rs.setStyleSheet("color:#7c9ef8; font-size:11px; font-weight:bold;")
        lbl_rs.setAlignment(Qt.AlignHCenter)
        self.recto_side = CardView("Recto")
        left_side.addWidget(lbl_rs)
        left_side.addWidget(self.recto_side)

        right_side = QVBoxLayout()
        lbl_vs = QLabel("VERSO")
        lbl_vs.setStyleSheet("color:#7c9ef8; font-size:11px; font-weight:bold;")
        lbl_vs.setAlignment(Qt.AlignHCenter)
        self.verso_side = CardView("Verso")
        right_side.addWidget(lbl_vs)
        right_side.addWidget(self.verso_side)

        side_layout.addLayout(left_side)
        side_layout.addLayout(right_side)
        self.tabs.addTab(side_widget, "◫  Côte à Côte")

        center_row.addWidget(self.tabs, 1)
        main_layout.addLayout(center_row, 1)

        # Vue active par défaut
        self.card_view = self.recto_view
        self.tabs.currentChanged.connect(self._on_tab_change)

    def _on_tab_change(self, idx):
        views = [
            self.recto_view,
            self.verso_view,
            self.recto_preview,
            self.recto_side,
        ]
        self.card_view = views[idx] if idx < len(views) else self.recto_view

    def set_tool(self, tool):
        self.card_view.set_tool(tool)
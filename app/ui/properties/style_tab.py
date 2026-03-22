from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QPushButton, QColorDialog, QFontComboBox,
    QSlider, QFrame, QGraphicsTextItem, QComboBox, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

class StyleTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_item = None
        self.text_color = QColor("#000000")
        self.highlight_color = QColor("#ffff00")
        self.bg_color = QColor("#ffffff")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        self._build_ui(layout)
        scroll.setWidget(container)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def _build_ui(self, L):

        # === POLICE ===
        self._section(L, "POLICE")
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont("Arial"))
        self.font_combo.setStyleSheet(self._inp())
        self.font_combo.currentFontChanged.connect(self._apply)
        L.addWidget(self.font_combo)

        row = QHBoxLayout()
        row.addWidget(self._lbl("Taille :"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(4, 144)
        self.size_spin.setValue(12)
        self.size_spin.setStyleSheet(self._inp())
        self.size_spin.valueChanged.connect(self._apply)
        row.addWidget(self.size_spin)

        self.btn_grow = QPushButton("A↑")
        self.btn_grow.setFixedSize(32, 28)
        self.btn_grow.setStyleSheet(self._tool())
        self.btn_grow.setToolTip("Augmenter la taille")
        self.btn_grow.clicked.connect(lambda: self.size_spin.setValue(self.size_spin.value() + 1))
        row.addWidget(self.btn_grow)

        self.btn_shrink = QPushButton("A↓")
        self.btn_shrink.setFixedSize(32, 28)
        self.btn_shrink.setStyleSheet(self._tool())
        self.btn_shrink.setToolTip("Réduire la taille")
        self.btn_shrink.clicked.connect(lambda: self.size_spin.setValue(self.size_spin.value() - 1))
        row.addWidget(self.btn_shrink)
        L.addLayout(row)

        # === FORMATAGE ===
        self._section(L, "FORMATAGE")

        row1 = QHBoxLayout()
        self.btn_bold      = self._fbtn("B",  bold=True,      tip="Gras (Ctrl+G)")
        self.btn_italic    = self._fbtn("I",  italic=True,    tip="Italique (Ctrl+I)")
        self.btn_underline = self._fbtn("U",  underline=True, tip="Souligné (Ctrl+U)")
        self.btn_strikeout = self._fbtn("S̶",                  tip="Barré")
        self.btn_clear     = QPushButton("✕")
        self.btn_clear.setFixedSize(36, 32)
        self.btn_clear.setToolTip("Effacer la mise en forme")
        self.btn_clear.setStyleSheet(self._tool())
        self.btn_clear.clicked.connect(self._clear_format)
        for b in [self.btn_bold, self.btn_italic, self.btn_underline, self.btn_strikeout]:
            b.clicked.connect(self._apply)
            row1.addWidget(b)
        row1.addWidget(self.btn_clear)
        row1.addStretch()
        L.addLayout(row1)

        row2 = QHBoxLayout()
        self.btn_sub = self._fbtn("X₂", tip="Indice")
        self.btn_sup = self._fbtn("X²", tip="Exposant")
        self.btn_upper = QPushButton("AA")
        self.btn_upper.setFixedSize(36, 32)
        self.btn_upper.setToolTip("Majuscules")
        self.btn_upper.setStyleSheet(self._tool())
        self.btn_upper.clicked.connect(self._toggle_upper)
        row2.addWidget(self._lbl("x₂ x² Aa :"))
        row2.addWidget(self.btn_sub)
        row2.addWidget(self.btn_sup)
        row2.addWidget(self.btn_upper)
        row2.addStretch()
        L.addLayout(row2)

        # === COULEURS ===
        self._section(L, "COULEURS")

        self.btn_text_color = QPushButton("A  Couleur texte")
        self.btn_text_color.setFixedHeight(32)
        self.btn_text_color.setStyleSheet("QPushButton { background:#000; color:white; border-radius:6px; font-weight:bold; font-size:12px; }")
        self.btn_text_color.clicked.connect(self._pick_text)
        L.addWidget(self.btn_text_color)

        row3 = QHBoxLayout()
        self.btn_highlight = QPushButton("🖍 Surlignage")
        self.btn_highlight.setFixedHeight(30)
        self.btn_highlight.setStyleSheet("QPushButton { background:#ffff00; color:#000; border-radius:6px; font-size:11px; }")
        self.btn_highlight.clicked.connect(self._pick_highlight)

        self.btn_bg = QPushButton("▣ Fond boîte")
        self.btn_bg.setFixedHeight(30)
        self.btn_bg.setStyleSheet("QPushButton { background:#fff; color:#333; border:1px solid #444; border-radius:6px; font-size:11px; }")
        self.btn_bg.clicked.connect(self._pick_bg)
        row3.addWidget(self.btn_highlight)
        row3.addWidget(self.btn_bg)
        L.addLayout(row3)

        # === ALIGNEMENT ===
        self._section(L, "ALIGNEMENT")

        align_row = QHBoxLayout()
        for icon, align, tip in [
            ("⬅", Qt.AlignLeft,    "Aligner à gauche"),
            ("↔", Qt.AlignHCenter, "Centrer"),
            ("➡", Qt.AlignRight,   "Aligner à droite"),
            ("☰", Qt.AlignJustify, "Justifier"),
        ]:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 32)
            btn.setToolTip(tip)
            btn.setStyleSheet(self._tool())
            btn.clicked.connect(lambda checked, a=align: self._apply_align(a))
            align_row.addWidget(btn)
        align_row.addStretch()
        L.addLayout(align_row)

        # === RETRAIT ===
        self._section(L, "RETRAIT")
        indent_row = QHBoxLayout()
        btn_indent_less = QPushButton("⇤ Diminuer")
        btn_indent_less.setFixedHeight(30)
        btn_indent_less.setToolTip("Diminuer le retrait")
        btn_indent_less.setStyleSheet(self._tool())
        btn_indent_less.clicked.connect(lambda: self._apply_indent(-20))

        btn_indent_more = QPushButton("Augmenter ⇥")
        btn_indent_more.setFixedHeight(30)
        btn_indent_more.setToolTip("Augmenter le retrait")
        btn_indent_more.setStyleSheet(self._tool())
        btn_indent_more.clicked.connect(lambda: self._apply_indent(20))
        indent_row.addWidget(btn_indent_less)
        indent_row.addWidget(btn_indent_more)
        L.addLayout(indent_row)

        # === INTERLIGNE ===
        self._section(L, "INTERLIGNE")
        self.line_spacing = QComboBox()
        self.line_spacing.addItems(["1.0", "1.15", "1.5", "2.0", "2.5", "3.0"])
        self.line_spacing.setCurrentIndex(1)
        self.line_spacing.setStyleSheet(self._inp())
        L.addWidget(self.line_spacing)

        # === LISTES ===
        self._section(L, "LISTES")
        list_row = QHBoxLayout()
        for icon, tip in [("• Liste puces", "Liste à puces"), ("1. Liste numéros", "Liste numérotée")]:
            btn = QPushButton(icon)
            btn.setFixedHeight(30)
            btn.setToolTip(tip)
            btn.setStyleSheet(self._tool())
            list_row.addWidget(btn)
        L.addLayout(list_row)

        # === EFFETS ===
        self._section(L, "EFFETS DE TEXTE")
        effects_row = QHBoxLayout()
        for icon, tip in [("💡 Éclat", "Éclat"), ("💧 Ombre", "Ombre"), ("🔲 Contour", "Contour")]:
            btn = QPushButton(icon)
            btn.setFixedHeight(30)
            btn.setToolTip(tip)
            btn.setStyleSheet(self._tool())
            effects_row.addWidget(btn)
        L.addLayout(effects_row)

        # === OPACITÉ ===
        self._section(L, "OPACITÉ")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.setStyleSheet("""
            QSlider::groove:horizontal { background:#2a2a3e; height:6px; border-radius:3px; }
            QSlider::handle:horizontal { background:#7c9ef8; width:14px; height:14px;
                border-radius:7px; margin:-4px 0; }
            QSlider::sub-page:horizontal { background:#7c9ef8; border-radius:3px; }
        """)
        self.opacity_slider.valueChanged.connect(self._apply_opacity)
        L.addWidget(self.opacity_slider)
        self.opacity_label = QLabel("100%")
        self.opacity_label.setStyleSheet("color:#888; font-size:11px;")
        self.opacity_label.setAlignment(Qt.AlignCenter)
        L.addWidget(self.opacity_label)
        L.addStretch()

    # ── Helpers ──────────────────────────────────────────
    def _section(self, L, title):
        lbl = QLabel(title)
        lbl.setStyleSheet("color:#7c9ef8; font-size:10px; font-weight:bold; margin-top:4px;")
        L.addWidget(lbl)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color:#2e2e4e;")
        L.addWidget(line)

    def _lbl(self, t):
        l = QLabel(t)
        l.setStyleSheet("color:#888; font-size:10px;")
        return l

    def _inp(self):
        return "background:#2a2a3e; color:white; border:1px solid #3e3e5e; border-radius:6px; padding:4px; font-size:12px;"

    def _tool(self):
        return """QPushButton { background:#2a2a3e; color:white; border-radius:6px; font-size:12px; }
                  QPushButton:checked { background:#7c9ef8; color:#0d0d1a; }
                  QPushButton:hover { background:#3e3e6e; }"""

    def _fbtn(self, text, bold=False, italic=False, underline=False, tip=""):
        btn = QPushButton(text)
        btn.setFixedSize(36, 32)
        btn.setCheckable(True)
        btn.setToolTip(tip)
        f = QFont()
        f.setBold(bold); f.setItalic(italic); f.setUnderline(underline)
        btn.setFont(f)
        btn.setStyleSheet(self._tool())
        return btn

    # ── Appliquer ─────────────────────────────────────────
    def set_item(self, item):
        self.current_item = item
        if isinstance(item, QGraphicsTextItem):
            font = item.font()
            self.font_combo.setCurrentFont(font)
            self.size_spin.setValue(font.pointSize() if font.pointSize() > 0 else 12)
            self.btn_bold.setChecked(font.bold())
            self.btn_italic.setChecked(font.italic())
            self.btn_underline.setChecked(font.underline())
            self.btn_strikeout.setChecked(font.strikeOut())
            opacity = int(item.opacity() * 100)
            self.opacity_slider.setValue(opacity)
            self.opacity_label.setText(f"{opacity}%")

    def _apply(self):
        if not self.current_item or not isinstance(self.current_item, QGraphicsTextItem):
            return
        font = self.font_combo.currentFont()
        font.setPointSize(self.size_spin.value())
        font.setBold(self.btn_bold.isChecked())
        font.setItalic(self.btn_italic.isChecked())
        font.setUnderline(self.btn_underline.isChecked())
        font.setStrikeOut(self.btn_strikeout.isChecked())
        self.current_item.setFont(font)

    def _apply_align(self, align):
        if not self.current_item or not isinstance(self.current_item, QGraphicsTextItem):
            return
        self.current_item.setTextWidth(self.current_item.boundingRect().width())

    def _apply_indent(self, delta):
        if not self.current_item or not isinstance(self.current_item, QGraphicsTextItem):
            return
        pos = self.current_item.pos()
        self.current_item.setPos(max(0, pos.x() + delta), pos.y())

    def _clear_format(self):
        if not self.current_item or not isinstance(self.current_item, QGraphicsTextItem):
            return
        font = QFont("Arial", 12)
        self.current_item.setFont(font)
        self.current_item.setDefaultTextColor(QColor("#000000"))
        self.font_combo.setCurrentFont(font)
        self.size_spin.setValue(12)
        self.btn_bold.setChecked(False)
        self.btn_italic.setChecked(False)
        self.btn_underline.setChecked(False)
        self.btn_strikeout.setChecked(False)

    def _toggle_upper(self):
        if not self.current_item or not isinstance(self.current_item, QGraphicsTextItem):
            return
        txt = self.current_item.toPlainText()
        self.current_item.setPlainText(txt.upper() if txt != txt.upper() else txt.lower())

    def _pick_text(self):
        color = QColorDialog.getColor(self.text_color, self, "Couleur du texte")
        if color.isValid():
            self.text_color = color
            self.btn_text_color.setStyleSheet(f"""
                QPushButton {{ background:{color.name()};
                color:{'white' if color.lightness()<128 else 'black'};
                border-radius:6px; font-weight:bold; font-size:12px; }}""")
            if self.current_item and isinstance(self.current_item, QGraphicsTextItem):
                self.current_item.setDefaultTextColor(color)

    def _pick_highlight(self):
        color = QColorDialog.getColor(self.highlight_color, self, "Couleur de surlignage")
        if color.isValid():
            self.highlight_color = color
            self.btn_highlight.setStyleSheet(f"""
                QPushButton {{ background:{color.name()};
                color:{'white' if color.lightness()<128 else 'black'};
                border-radius:6px; font-size:11px; }}""")

    def _pick_bg(self):
        color = QColorDialog.getColor(self.bg_color, self, "Couleur de fond")
        if color.isValid():
            self.bg_color = color
            self.btn_bg.setStyleSheet(f"""
                QPushButton {{ background:{color.name()};
                color:{'white' if color.lightness()<128 else 'black'};
                border:1px solid #444; border-radius:6px; font-size:11px; }}""")

    def _apply_opacity(self, value):
        self.opacity_label.setText(f"{value}%")
        if self.current_item:
            self.current_item.setOpacity(value / 100)
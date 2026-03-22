from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget,
    QFontComboBox, QSpinBox, QColorDialog, QComboBox, QToolBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from ui.designer.canvas import Canvas
from ui.designer.toolbar import Toolbar

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hams Carte ID")
        self.setMinimumSize(1200, 750)
        self.setStyleSheet("background-color: #1e1e2e; color: white;")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.stack.addWidget(self._build_dashboard())
        self.stack.addWidget(self._build_editor())
        self.stack.setCurrentIndex(0)

    def _build_dashboard(self):
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        left = QFrame()
        left.setFixedWidth(260)
        left.setStyleSheet("background-color: #13131f; border-right: 1px solid #2e2e4e;")
        ll = QVBoxLayout(left)
        ll.setContentsMargins(20, 30, 20, 20)
        ll.setSpacing(12)
        title = QLabel("HAMS CARTE ID")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #7c9ef8;")
        ll.addWidget(title)
        ll.addWidget(self._lbl("ID-PRO Designer v1.0", "#888", 9))
        ll.addSpacing(30)
        btn_new = self._btn("＋  Nouvelle Carte Vierge", "#7c9ef8", "#0d0d1a", h=44)
        btn_new.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        ll.addWidget(btn_new)
        ll.addWidget(self._btn("📂  Utiliser un Modèle", "#2e2e4e", "white", h=44))
        ll.addStretch()
        ll.addWidget(self._btn("⚙️  Paramètres", "transparent", "#888", h=38))
        layout.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(40, 30, 40, 30)
        rl.addWidget(self._lbl("Bienvenue dans Hams Carte ID 👋", "white", 22, bold=True))
        rl.addWidget(self._lbl("Créez, gérez et imprimez vos cartes.", "#888", 13))
        rl.addSpacing(30)
        rl.addWidget(self._lbl("Projets Récents", "#7c9ef8", 13, bold=True))
        rl.addSpacing(10)
        cards_row = QHBoxLayout()
        for nom in ["Badges Staff 2026", "Cartes Membres PSF", "Badges Visiteurs"]:
            card = QFrame()
            card.setFixedSize(220, 140)
            card.setStyleSheet("QFrame{background:#2a2a3e;border-radius:12px;border:1px solid #3e3e5e;}QFrame:hover{border-color:#7c9ef8;}")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 16, 16, 16)
            cl.addWidget(self._lbl(nom, "white", 11, bold=True))
            cl.addStretch()
            be = self._btn("✏️ Éditer", "#7c9ef8", "#0d0d1a", h=30)
            be.clicked.connect(lambda: self.stack.setCurrentIndex(1))
            cl.addWidget(be)
            cards_row.addWidget(card)
        cards_row.addStretch()
        rl.addLayout(cards_row)
        rl.addStretch()
        layout.addWidget(right)
        return page

    def _build_editor(self):
        page = QWidget()
        page.setStyleSheet("background-color: #1e1e2e;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Barre navigation ──
        nav = QFrame()
        nav.setFixedHeight(40)
        nav.setStyleSheet("background:#13131f; border-bottom:1px solid #2e2e4e;")
        nav_l = QHBoxLayout(nav)
        nav_l.setContentsMargins(10, 0, 10, 0)
        nav_l.setSpacing(8)
        btn_home = self._btn("🏠 Accueil", "#2e2e4e", "white", h=28, pad=10)
        btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        nav_l.addWidget(btn_home)
        nav_l.addWidget(self._lbl("  Éditeur — Nouvelle Carte CR80", "#7c9ef8", 12, bold=True))
        nav_l.addStretch()
        nav_l.addWidget(self._btn("💾 Enregistrer", "#2e2e4e", "white", h=28, pad=10))
        nav_l.addWidget(self._btn("🖨️ Imprimer", "#7c9ef8", "#0d0d1a", h=28, pad=10))
        layout.addWidget(nav)

        # ── Barre style Word ──
        ribbon = QFrame()
        ribbon.setFixedHeight(72)
        ribbon.setStyleSheet("background:#1a1a2e; border-bottom:2px solid #3e3e6e;")
        rb = QHBoxLayout(ribbon)
        rb.setContentsMargins(6, 4, 6, 4)
        rb.setSpacing(2)

        # BLOC POLICE
        bloc_police = self._bloc("Police")
        bp = QVBoxLayout(bloc_police)
        bp.setContentsMargins(4, 2, 4, 0)
        bp.setSpacing(2)

        # Rangée 1 : Police + Taille + A↑ A↓
        r1 = QHBoxLayout()
        r1.setSpacing(2)
        self.font_combo = QFontComboBox()
        self.font_combo.setFixedSize(140, 22)
        self.font_combo.setCurrentFont(QFont("Arial"))
        self.font_combo.setStyleSheet(self._inp())
        self.font_combo.currentFontChanged.connect(self._apply_font)
        r1.addWidget(self.font_combo)

        self.size_combo = QComboBox()
        self.size_combo.setFixedSize(44, 22)
        self.size_combo.addItems(["6","8","9","10","11","12","14","16","18","20","24","28","36","48","72"])
        self.size_combo.setCurrentText("12")
        self.size_combo.setStyleSheet(self._inp())
        self.size_combo.currentTextChanged.connect(self._apply_font)
        r1.addWidget(self.size_combo)

        for icon, tip, delta in [("A↑","Agrandir",1),("A↓","Réduire",-1)]:
            b = QPushButton(icon)
            b.setFixedSize(22, 22)
            b.setToolTip(tip)
            b.setStyleSheet(self._ts())
            b.clicked.connect(lambda c, d=delta: self._change_size(d))
            r1.addWidget(b)
        r1.addStretch()
        bp.addLayout(r1)

        # Rangée 2 : G I S ab x₂ x² ✕ | A🖍
        r2 = QHBoxLayout()
        r2.setSpacing(2)

        self.btn_bold      = self._tb("G",  22, bold=True,      tip="Gras")
        self.btn_italic    = self._tb("I",  22, italic=True,    tip="Italique")
        self.btn_underline = self._tb("S",  22, underline=True, tip="Souligné")
        self.btn_strike    = self._tb("ab̶", 26,                 tip="Barré")
        self.btn_sub       = self._tb("x₂", 26,                tip="Indice")
        self.btn_sup       = self._tb("x²", 26,                tip="Exposant")

        for b in [self.btn_bold, self.btn_italic, self.btn_underline,
                  self.btn_strike, self.btn_sub, self.btn_sup]:
            b.clicked.connect(self._apply_font)
            r2.addWidget(b)

        btn_clear = QPushButton("✕")
        btn_clear.setFixedSize(22, 22)
        btn_clear.setToolTip("Effacer mise en forme")
        btn_clear.setStyleSheet(self._ts())
        btn_clear.clicked.connect(self._clear_fmt)
        r2.addWidget(btn_clear)

        r2.addWidget(self._vsep())

        # Couleur texte A avec barre couleur
        self.text_color = QColor("#000000")
        self.btn_tc = QPushButton("A")
        self.btn_tc.setFixedSize(26, 22)
        self.btn_tc.setToolTip("Couleur du texte")
        self.btn_tc.setStyleSheet("QPushButton{background:#2a2a3e;color:white;border-radius:3px;font-weight:bold;border-bottom:3px solid #ff0000;font-size:13px;}")
        self.btn_tc.clicked.connect(self._pick_tc)
        r2.addWidget(self.btn_tc)

        # Surlignage
        self.highlight_color = QColor("#ffff00")
        self.btn_hl = QPushButton("🖍")
        self.btn_hl.setFixedSize(26, 22)
        self.btn_hl.setToolTip("Surlignage")
        self.btn_hl.setStyleSheet("QPushButton{background:#2a2a3e;color:white;border-radius:3px;border-bottom:3px solid #ffff00;font-size:12px;}")
        self.btn_hl.clicked.connect(self._pick_hl)
        r2.addWidget(self.btn_hl)

        r2.addStretch()
        bp.addLayout(r2)
        rb.addWidget(bloc_police)
        rb.addWidget(self._vsep())

        # BLOC PARAGRAPHE
        bloc_para = self._bloc("Paragraphe")
        pp = QVBoxLayout(bloc_para)
        pp.setContentsMargins(4, 2, 4, 0)
        pp.setSpacing(2)

        # Rangée 1 : Listes + Retrait + Bordure
        rp1 = QHBoxLayout()
        rp1.setSpacing(2)
        for icon, tip in [("≡•","Liste puces"),("≡1","Liste numéros"),("≡↕","Liste multi-niveaux"),
                          ("⇤","Diminuer retrait"),("⇥","Augmenter retrait"),
                          ("▦","Trame de fond"),("⬚","Bordures")]:
            b = QPushButton(icon)
            b.setFixedSize(26, 22)
            b.setToolTip(tip)
            b.setStyleSheet(self._ts())
            rp1.addWidget(b)
        rp1.addStretch()
        pp.addLayout(rp1)

        # Rangée 2 : Alignement + Interligne + Tri
        rp2 = QHBoxLayout()
        rp2.setSpacing(2)
        self.align_btns = []
        for icon, tip in [("⬅","Aligner à gauche"),("↔","Centrer"),
                          ("➡","Aligner à droite"),("☰","Justifier")]:
            b = QPushButton(icon)
            b.setFixedSize(26, 22)
            b.setCheckable(True)
            b.setToolTip(tip)
            b.setStyleSheet(self._ts())
            self.align_btns.append(b)
            rp2.addWidget(b)

        rp2.addWidget(self._vsep())

        self.spacing_combo = QComboBox()
        self.spacing_combo.addItems(["1.0","1.15","1.5","2.0","3.0"])
        self.spacing_combo.setCurrentText("1.15")
        self.spacing_combo.setFixedSize(48, 22)
        self.spacing_combo.setToolTip("Interligne")
        self.spacing_combo.setStyleSheet(self._inp())
        rp2.addWidget(self.spacing_combo)

        for icon, tip in [("A↕","Trier"),("¶","Afficher marques")]:
            b = QPushButton(icon)
            b.setFixedSize(26, 22)
            b.setToolTip(tip)
            b.setStyleSheet(self._ts())
            rp2.addWidget(b)

        rp2.addStretch()
        pp.addLayout(rp2)
        rb.addWidget(bloc_para)
        rb.addStretch()
        layout.addWidget(ribbon)

        # ── Zone principale ──
        main_area = QHBoxLayout()
        main_area.setSpacing(0)
        main_area.setContentsMargins(0, 0, 0, 0)

        self.canvas = Canvas()
        toolbar = Toolbar(canvas=self.canvas)
        main_area.addWidget(toolbar)
        main_area.addWidget(self.canvas)

        # Panneau couches
        layers = QFrame()
        layers.setFixedWidth(180)
        layers.setStyleSheet("background:#13131f; border-left:1px solid #2e2e4e;")
        ll2 = QVBoxLayout(layers)
        ll2.setContentsMargins(10, 10, 10, 10)
        ll2.addWidget(self._lbl("Couches", "#7c9ef8", 11, bold=True))
        line = QFrame(); line.setFrameShape(QFrame.HLine); line.setStyleSheet("color:#2e2e4e;")
        ll2.addWidget(line)
        for nom in ["🎨 Couleur (YMC)", "⬛ Noir (K)", "🔲 Overlay (O)"]:
            l = QLabel(nom)
            l.setStyleSheet("color:#888; font-size:11px; padding:3px 0;")
            ll2.addWidget(l)
        ll2.addStretch()
        main_area.addWidget(layers)
        layout.addLayout(main_area)

        self.canvas.card_view.on_item_selected = self._on_select
        return page

    def _on_select(self, item):
        from PyQt5.QtWidgets import QGraphicsTextItem
        if isinstance(item, QGraphicsTextItem):
            f = item.font()
            self.font_combo.setCurrentFont(f)
            self.size_combo.setCurrentText(str(f.pointSize() if f.pointSize() > 0 else 12))
            self.btn_bold.setChecked(f.bold())
            self.btn_italic.setChecked(f.italic())
            self.btn_underline.setChecked(f.underline())
            self.btn_strike.setChecked(f.strikeOut())

    def _apply_font(self):
        from PyQt5.QtWidgets import QGraphicsTextItem
        for item in self.canvas.card_view.scene.selectedItems():
            if isinstance(item, QGraphicsTextItem):
                f = self.font_combo.currentFont()
                try: f.setPointSize(int(self.size_combo.currentText()))
                except: pass
                f.setBold(self.btn_bold.isChecked())
                f.setItalic(self.btn_italic.isChecked())
                f.setUnderline(self.btn_underline.isChecked())
                f.setStrikeOut(self.btn_strike.isChecked())
                item.setFont(f)

    def _change_size(self, d):
        try:
            self.size_combo.setCurrentText(str(max(4, int(self.size_combo.currentText()) + d)))
        except: pass

    def _clear_fmt(self):
        from PyQt5.QtWidgets import QGraphicsTextItem
        for item in self.canvas.card_view.scene.selectedItems():
            if isinstance(item, QGraphicsTextItem):
                item.setFont(QFont("Arial", 12))
                item.setDefaultTextColor(QColor("#000000"))
        self.font_combo.setCurrentFont(QFont("Arial"))
        self.size_combo.setCurrentText("12")
        for b in [self.btn_bold, self.btn_italic, self.btn_underline, self.btn_strike]:
            b.setChecked(False)

    def _pick_tc(self):
        c = QColorDialog.getColor(self.text_color, self, "Couleur texte")
        if c.isValid():
            self.text_color = c
            self.btn_tc.setStyleSheet(f"QPushButton{{background:#2a2a3e;color:white;border-radius:3px;font-weight:bold;border-bottom:3px solid {c.name()};font-size:13px;}}")
            from PyQt5.QtWidgets import QGraphicsTextItem
            for item in self.canvas.card_view.scene.selectedItems():
                if isinstance(item, QGraphicsTextItem):
                    item.setDefaultTextColor(c)

    def _pick_hl(self):
        c = QColorDialog.getColor(self.highlight_color, self, "Surlignage")
        if c.isValid():
            self.highlight_color = c
            self.btn_hl.setStyleSheet(f"QPushButton{{background:#2a2a3e;color:white;border-radius:3px;border-bottom:3px solid {c.name()};font-size:12px;}}")

    # ── Helpers ──
    def _bloc(self, title):
        f = QFrame()
        f.setStyleSheet("QFrame{border:none;}")
        f.setFixedHeight(62)
        return f

    def _vsep(self):
        s = QFrame()
        s.setFrameShape(QFrame.VLine)
        s.setFixedWidth(1)
        s.setFixedHeight(50)
        s.setStyleSheet("color:#3e3e5e;")
        return s

    def _tb(self, text, w=22, bold=False, italic=False, underline=False, tip=""):
        btn = QPushButton(text)
        btn.setFixedSize(w, 22)
        btn.setCheckable(True)
        btn.setToolTip(tip)
        f = QFont(); f.setBold(bold); f.setItalic(italic); f.setUnderline(underline)
        btn.setFont(f)
        btn.setStyleSheet(self._ts())
        return btn

    def _lbl(self, t, color="white", size=12, bold=False):
        l = QLabel(t)
        l.setStyleSheet(f"color:{color};font-size:{size}px;font-weight:{'bold' if bold else 'normal'};")
        return l

    def _btn(self, text, bg, fg, h=32, pad=12):
        btn = QPushButton(text)
        btn.setFixedHeight(h)
        btn.setStyleSheet(f"QPushButton{{background:{bg};color:{fg};border-radius:6px;padding:0 {pad}px;font-size:12px;}}QPushButton:hover{{background:#3e3e6e;}}")
        return btn

    def _inp(self):
        return "background:#2a2a3e;color:white;border:1px solid #3e3e5e;border-radius:3px;font-size:12px;"

    def _ts(self):
        return "QPushButton{background:#2a2a3e;color:white;border-radius:3px;font-size:11px;}QPushButton:checked{background:#7c9ef8;color:#0d0d1a;}QPushButton:hover{background:#3e3e6e;}"
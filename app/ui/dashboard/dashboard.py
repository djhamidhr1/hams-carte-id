from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.designer.canvas import Canvas
from ui.designer.toolbar import Toolbar

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hams Carte ID — Dashboard")
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
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(20, 30, 20, 20)
        left_layout.setSpacing(12)

        title = QLabel("HAMS CARTE ID")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #7c9ef8;")
        left_layout.addWidget(title)

        subtitle = QLabel("ID-PRO Designer v1.0")
        subtitle.setFont(QFont("Arial", 9))
        subtitle.setStyleSheet("color: #888;")
        left_layout.addWidget(subtitle)
        left_layout.addSpacing(30)

        btn_new = QPushButton("＋  Nouvelle Carte Vierge")
        btn_new.setFixedHeight(44)
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #7c9ef8;
                color: #0d0d1a;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #a0b8ff; }
        """)
        btn_new.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        left_layout.addWidget(btn_new)

        btn_template = QPushButton("📂  Utiliser un Modèle")
        btn_template.setFixedHeight(44)
        btn_template.setStyleSheet("""
            QPushButton {
                background-color: #2e2e4e;
                color: white;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #3e3e6e; }
        """)
        left_layout.addWidget(btn_template)
        left_layout.addStretch()

        btn_settings = QPushButton("⚙️  Paramètres")
        btn_settings.setFixedHeight(38)
        btn_settings.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888;
                border: 1px solid #2e2e4e;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover { color: white; border-color: #7c9ef8; }
        """)
        left_layout.addWidget(btn_settings)
        layout.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(40, 30, 40, 30)

        header = QLabel("Bienvenue dans Hams Carte ID 👋")
        header.setFont(QFont("Arial", 22, QFont.Bold))
        right_layout.addWidget(header)

        desc = QLabel("Créez, gérez et imprimez vos cartes d'identification professionnelles.")
        desc.setStyleSheet("color: #888; font-size: 13px;")
        right_layout.addWidget(desc)
        right_layout.addSpacing(30)

        recent_label = QLabel("Projets Récents")
        recent_label.setFont(QFont("Arial", 13, QFont.Bold))
        recent_label.setStyleSheet("color: #7c9ef8;")
        right_layout.addWidget(recent_label)
        right_layout.addSpacing(10)

        cards_layout = QHBoxLayout()
        for nom in ["Badges Staff 2026", "Cartes Membres PSF", "Badges Visiteurs"]:
            card = QFrame()
            card.setFixedSize(220, 140)
            card.setStyleSheet("""
                QFrame {
                    background-color: #2a2a3e;
                    border-radius: 12px;
                    border: 1px solid #3e3e5e;
                }
                QFrame:hover { border-color: #7c9ef8; }
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 16, 16, 16)
            card_title = QLabel(nom)
            card_title.setFont(QFont("Arial", 11, QFont.Bold))
            card_layout.addWidget(card_title)
            card_layout.addStretch()
            btn_edit = QPushButton("✏️ Éditer")
            btn_edit.setFixedHeight(30)
            btn_edit.setStyleSheet("""
                QPushButton {
                    background-color: #7c9ef8;
                    color: #0d0d1a;
                    border-radius: 6px;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #a0b8ff; }
            """)
            btn_edit.clicked.connect(lambda: self.stack.setCurrentIndex(1))
            card_layout.addWidget(btn_edit)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        right_layout.addLayout(cards_layout)
        right_layout.addStretch()
        layout.addWidget(right)
        return page

    def _build_editor(self):
        page = QWidget()
        page.setStyleSheet("background-color: #1e1e2e;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        topbar = QFrame()
        topbar.setFixedHeight(48)
        topbar.setStyleSheet("background-color: #13131f; border-bottom: 1px solid #2e2e4e;")
        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(16, 0, 16, 0)

        btn_home = QPushButton("🏠 Accueil")
        btn_home.setFixedHeight(32)
        btn_home.setStyleSheet("""
            QPushButton {
                background-color: #2e2e4e;
                color: white;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #7c9ef8; color: #0d0d1a; }
        """)
        btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        top_layout.addWidget(btn_home)
        top_layout.addSpacing(16)

        title = QLabel("Éditeur — Nouvelle Carte CR80")
        title.setStyleSheet("color: #7c9ef8; font-weight: bold; font-size: 13px;")
        top_layout.addWidget(title)
        top_layout.addStretch()

        btn_save = QPushButton("💾 Enregistrer")
        btn_save.setFixedHeight(32)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #2e2e4e;
                color: white;
                border-radius: 6px;
                padding: 0 12px;
            }
            QPushButton:hover { background-color: #3e3e6e; }
        """)
        top_layout.addWidget(btn_save)

        btn_print = QPushButton("🖨️ Imprimer")
        btn_print.setFixedHeight(32)
        btn_print.setStyleSheet("""
            QPushButton {
                background-color: #7c9ef8;
                color: #0d0d1a;
                border-radius: 6px;
                padding: 0 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #a0b8ff; }
        """)
        top_layout.addWidget(btn_print)
        layout.addWidget(topbar)

        main_area = QHBoxLayout()
        main_area.setSpacing(0)
        main_area.setContentsMargins(0, 0, 0, 0)

        toolbar = Toolbar()
        main_area.addWidget(toolbar)

        self.canvas = Canvas()
        main_area.addWidget(self.canvas)

        props = QFrame()
        props.setFixedWidth(240)
        props.setStyleSheet("background-color: #13131f; border-left: 1px solid #2e2e4e;")
        props_layout = QVBoxLayout(props)
        props_layout.setContentsMargins(16, 16, 16, 16)

        props_title = QLabel("Propriétés")
        props_title.setFont(QFont("Arial", 12, QFont.Bold))
        props_title.setStyleSheet("color: #7c9ef8;")
        props_layout.addWidget(props_title)
        props_layout.addSpacing(10)

        hint = QLabel("Sélectionnez un élément\nsur la carte pour voir\nses propriétés.")
        hint.setStyleSheet("color: #555; font-size: 12px;")
        props_layout.addWidget(hint)
        props_layout.addStretch()
        main_area.addWidget(props)

        layout.addLayout(main_area)
        return page
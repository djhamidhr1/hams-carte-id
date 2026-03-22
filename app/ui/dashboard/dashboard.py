from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hams Carte ID — Dashboard")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet("background-color: #1e1e2e; color: white;")
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Panneau gauche
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

        # Zone centrale
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(40, 30, 40, 30)

        header = QLabel("Bienvenue dans Hams Carte ID 👋")
        header.setFont(QFont("Arial", 22, QFont.Bold))
        header.setStyleSheet("color: white;")
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

        # Cartes projets exemple
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
            card_title.setStyleSheet("color: white;")
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
            card_layout.addWidget(btn_edit)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        right_layout.addLayout(cards_layout)
        right_layout.addStretch()
        layout.addWidget(right)
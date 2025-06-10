from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QSizePolicy, QFrame

class TabSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet('''
            QWidget { background: #23272e; color: #e0e0e0; }
            QGroupBox { border: 1.2px solid #888; border-radius: 5px; margin-top: 12px; background: #23272e; }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                top: -10px;
                padding: 0 12px 0 12px;
                font-weight: bold;
                font-size: 15px;
                color: #fff;
                background: #23272e;
            }
            QLabel { font-size: 13px; color: #e0e0e0; }
            QPushButton { background: #2d313a; border: 1px solid #888; border-radius: 3px; font-size: 13px; font-weight: bold; padding: 6px 20px; color: #e0e0e0; margin: 0 6px; }
            QPushButton:pressed { background: #22242a; }
        ''')
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(16, 16, 16, 12)
        main_layout.setSpacing(12)
        group = QGroupBox("Configuración de la Aplicación")
        group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        vbox = QVBoxLayout(group)
        vbox.setSpacing(10)
        self.theme_btn = QPushButton("Alternar Tema Oscuro")
        self.theme_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        vbox.addWidget(self.theme_btn)
        main_layout.addWidget(group)
        about = QGroupBox("Acerca de")
        about.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        about_vbox = QVBoxLayout(about)
        about_vbox.setSpacing(10)
        about_vbox.addWidget(QLabel("GestorIP Pro v2.0\n\nDesarrollado para la gestión avanzada de configuraciones de red."))
        main_layout.addWidget(about)
        self.setLayout(main_layout)
        self.setMinimumWidth(520)
        self.setMinimumHeight(480)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

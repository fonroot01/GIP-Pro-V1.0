from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QHBoxLayout, QSizePolicy, QFrame

class TabTools(QWidget):
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
            QLineEdit { border: 1px solid #888; border-radius: 3px; padding: 4px 10px; font-size: 13px; background: #181a1b; color: #e0e0e0; }
            QPushButton { background: #2d313a; border: 1px solid #888; border-radius: 3px; font-size: 13px; font-weight: bold; padding: 6px 20px; color: #e0e0e0; margin: 0 6px; }
            QPushButton:pressed { background: #22242a; }
        ''')
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(16, 16, 16, 12)
        main_layout.setSpacing(12)
        group = QGroupBox("Herramientas de Diagnóstico")
        group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        hbox = QHBoxLayout()
        hbox.setSpacing(16)
        self.ping_input = QLineEdit()
        self.ping_btn = QPushButton("Ping")
        hbox.addWidget(QLabel("Ping a:"))
        hbox.addWidget(self.ping_input)
        hbox.addWidget(self.ping_btn)
        group.setLayout(hbox)
        main_layout.addWidget(group)
        self.setLayout(main_layout)
        self.setMinimumWidth(520)
        self.setMinimumHeight(480)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

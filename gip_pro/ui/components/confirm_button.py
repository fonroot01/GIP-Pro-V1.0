from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QGroupBox, QSizePolicy, QFrame
from PyQt6.QtGui import QFont

# Botón de confirmación personalizado
# Aquí se define un botón con animaciones o estilos propios

class ConfirmButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: #0078d4; color: white; border-radius: 4px; font-weight: bold;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(32)
        self.setMinimumWidth(120)
        self.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.clicked.connect(self.animate_click)

    def animate_click(self):
        # Aquí puedes agregar animación visual si lo deseas
        pass

class ProxyConfigWidget(QWidget):
    """Widget para configurar proxy en la UI"""
    def __init__(self, network_tools, parent=None):
        super().__init__(parent)
        self.network_tools = network_tools
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet('''
            QWidget { background: #23272e; color: #e0e0e0; }
            QGroupBox { border: 1.2px solid #888; border-radius: 5px; margin-top: 2px; background: #23272e; }
            QGroupBox::title { left: 4px; top: 1px; padding: 0 1px 0 1px; font-weight: bold; color: #e0e0e0; background: transparent; }
            QLabel { font-size: 12px; color: #e0e0e0; }
            QLineEdit, QComboBox { border: 1px solid #888; border-radius: 3px; padding: 1px 3px; font-size: 12px; background: #181a1b; color: #e0e0e0; min-width: 90px; max-width: 180px; }
            QPushButton { background: #2d313a; border: 1px solid #888; border-radius: 3px; font-size: 12px; font-weight: bold; padding: 2px 6px; min-width: 80px; max-width: 120px; color: #e0e0e0; margin: 0 1px; }
            QPushButton:pressed { background: #22242a; }
            QCheckBox { font-size: 12px; color: #e0e0e0; }
        ''')
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        frame = QFrame()
        frame.setStyleSheet("QFrame { background: #23272e; border: none; }")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        group = QGroupBox("Configuración de Proxy")
        group.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        form = QFormLayout(group)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        form.setHorizontalSpacing(3)
        form.setVerticalSpacing(1)
        self.interface_input = QLineEdit()
        self.proxy_address_input = QLineEdit()
        self.proxy_port_input = QLineEdit()
        self.proxy_type_combo = QComboBox()
        self.proxy_type_combo.addItems(['http', 'socks'])
        self.apply_btn = QPushButton('Aplicar Proxy')
        self.apply_btn.clicked.connect(self.apply_proxy)
        for widget in [self.interface_input, self.proxy_address_input, self.proxy_port_input, self.proxy_type_combo]:
            widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        form.addRow('Interfaz:', self.interface_input)
        form.addRow('Dirección Proxy:', self.proxy_address_input)
        form.addRow('Puerto:', self.proxy_port_input)
        form.addRow('Tipo:', self.proxy_type_combo)
        form.addRow(self.apply_btn)
        frame_layout.addWidget(group, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)
        self.setMinimumWidth(520)
        self.setMinimumHeight(320)
        self.setMaximumWidth(700)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def apply_proxy(self):
        interface = self.interface_input.text()
        address = self.proxy_address_input.text()
        port = self.proxy_port_input.text()
        proxy_type = self.proxy_type_combo.currentText()
        if interface and address and port:
            self.network_tools.set_proxy(interface, address, port, proxy_type)

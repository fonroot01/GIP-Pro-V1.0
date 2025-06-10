# Widget de entrada de IP personalizado
# Aquí se define un widget para ingresar IPs

from PyQt6.QtWidgets import QLineEdit

class IPInput(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("192.168.1.100")
        self.setMaxLength(15)
        self.setInputMask("000.000.000.000;_")
        self.setStyleSheet("border: 2px solid #0078d4; border-radius: 4px; padding: 6px;")

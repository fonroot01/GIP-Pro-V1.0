from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal

class NetworkConfigGroup(QGroupBox):
    """Grupo de configuración de red con campos IP, máscara, gateway"""
    
    config_changed = pyqtSignal(dict)  # Señal emitida cuando cambia la configuración
    
    def __init__(self, parent=None):
        super().__init__("Configuración de Red", parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(10)
        
        # Interfaz de red
        layout.addWidget(QLabel("Interfaz de red:"), 0, 0)
        self.interface_combo = QComboBox()
        layout.addWidget(self.interface_combo, 0, 1)
        
        # Dirección IP
        layout.addWidget(QLabel("Dirección IP:"), 1, 0)
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.100")
        layout.addWidget(self.ip_input, 1, 1)
        
        # Máscara de subred
        layout.addWidget(QLabel("Máscara de subred:"), 2, 0)
        self.mask_input = QLineEdit()
        self.mask_input.setPlaceholderText("255.255.255.0")
        layout.addWidget(self.mask_input, 2, 1)
        
        # Gateway
        layout.addWidget(QLabel("Gateway:"), 3, 0)
        self.gateway_input = QLineEdit()
        self.gateway_input.setPlaceholderText("192.168.1.1")
        layout.addWidget(self.gateway_input, 3, 1)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Aplicar IP")
        self.dhcp_btn = QPushButton("Auto")
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.dhcp_btn)
        layout.addLayout(button_layout, 4, 0, 1, 2)
        
        # Conectar señales
        self.ip_input.textChanged.connect(self._emit_config)
        self.mask_input.textChanged.connect(self._emit_config)
        self.gateway_input.textChanged.connect(self._emit_config)
        
    def set_interfaces(self, interfaces):
        """Actualiza la lista de interfaces disponibles"""
        current = self.interface_combo.currentText()
        self.interface_combo.clear()
        self.interface_combo.addItems(interfaces)
        if current in interfaces:
            self.interface_combo.setCurrentText(current)
            
    def get_config(self):
        """Obtiene la configuración actual"""
        return {
            'interface': self.interface_combo.currentText(),
            'ip': self.ip_input.text(),
            'mask': self.mask_input.text(),
            'gateway': self.gateway_input.text()
        }
        
    def set_config(self, config):
        """Establece la configuración"""
        if 'interface' in config:
            index = self.interface_combo.findText(config['interface'])
            if index >= 0:
                self.interface_combo.setCurrentIndex(index)
        if 'ip' in config:
            self.ip_input.setText(config['ip'])
        if 'mask' in config:
            self.mask_input.setText(config['mask'])
        if 'gateway' in config:
            self.gateway_input.setText(config['gateway'])
            
    def _emit_config(self):
        """Emite la señal de cambio de configuración"""
        self.config_changed.emit(self.get_config())

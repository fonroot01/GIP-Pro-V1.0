from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QCheckBox, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal

class ProxyConfigGroup(QGroupBox):
    """Grupo de configuración de proxy"""
    
    config_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__("Configuración de Proxy", parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Checkbox para habilitar/deshabilitar
        self.enable_proxy = QCheckBox("Habilitar Proxy")
        layout.addWidget(self.enable_proxy)
        
        # Grid para servidor y puerto
        grid = QGridLayout()
        
        # Servidor
        grid.addWidget(QLabel("Servidor:"), 0, 0)
        self.server_input = QLineEdit()
        self.server_input.setEnabled(False)
        grid.addWidget(self.server_input, 0, 1)
        
        # Puerto
        grid.addWidget(QLabel("Puerto:"), 1, 0)
        self.port_input = QLineEdit()
        self.port_input.setEnabled(False)
        grid.addWidget(self.port_input, 1, 1)
        
        layout.addLayout(grid)
        
        # Botón probar
        self.test_btn = QPushButton("Probar Proxy")
        self.test_btn.setObjectName("secondary")
        self.test_btn.setEnabled(False)
        layout.addWidget(self.test_btn)
        
        # Conectar señales
        self.enable_proxy.toggled.connect(self._handle_proxy_toggle)
        self.server_input.textChanged.connect(self._emit_config)
        self.port_input.textChanged.connect(self._emit_config)
        
    def _handle_proxy_toggle(self, enabled):
        self.server_input.setEnabled(enabled)
        self.port_input.setEnabled(enabled)
        self.test_btn.setEnabled(enabled)
        self._emit_config()
        
    def get_config(self):
        return {
            'enabled': self.enable_proxy.isChecked(),
            'server': self.server_input.text(),
            'port': self.port_input.text()
        }
        
    def set_config(self, config):
        if 'enabled' in config:
            self.enable_proxy.setChecked(config['enabled'])
        if 'server' in config:
            self.server_input.setText(config['server'])
        if 'port' in config:
            self.port_input.setText(config['port'])
            
    def _emit_config(self):
        self.config_changed.emit(self.get_config())

from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal

class DNSConfigGroup(QGroupBox):
    """Grupo de configuración DNS con campos para DNS primario y secundario"""
    
    config_changed = pyqtSignal(dict)  # Señal emitida cuando cambia la configuración
    
    def __init__(self, parent=None):
        super().__init__("Configuración DNS", parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(10)
        
        # DNS Primario
        layout.addWidget(QLabel("DNS Primario:"), 0, 0)
        self.primary_dns = QLineEdit()
        self.primary_dns.setPlaceholderText("8.8.8.8")
        layout.addWidget(self.primary_dns, 0, 1)
        
        # DNS Secundario
        layout.addWidget(QLabel("DNS Secundario:"), 1, 0)
        self.secondary_dns = QLineEdit()
        self.secondary_dns.setPlaceholderText("8.8.4.4")
        layout.addWidget(self.secondary_dns, 1, 1)
        
        # Presets de DNS
        preset_layout = QHBoxLayout()
        self.google_dns = QPushButton("Google DNS")
        self.cloudflare_dns = QPushButton("Cloudflare DNS")
        self.opendns = QPushButton("OpenDNS")
        preset_layout.addWidget(self.google_dns)
        preset_layout.addWidget(self.cloudflare_dns)
        preset_layout.addWidget(self.opendns)
        layout.addLayout(preset_layout, 2, 0, 1, 2)
        
        # Botón aplicar
        self.apply_btn = QPushButton("Aplicar DNS")
        layout.addWidget(self.apply_btn, 3, 0, 1, 2)
        
        # Conectar señales
        self.google_dns.clicked.connect(lambda: self.set_preset("google"))
        self.cloudflare_dns.clicked.connect(lambda: self.set_preset("cloudflare"))
        self.opendns.clicked.connect(lambda: self.set_preset("opendns"))
        self.primary_dns.textChanged.connect(self._emit_config)
        self.secondary_dns.textChanged.connect(self._emit_config)
        
    def set_preset(self, preset):
        """Establece un preset de DNS"""
        presets = {
            "google": ("8.8.8.8", "8.8.4.4"),
            "cloudflare": ("1.1.1.1", "1.0.0.1"),
            "opendns": ("208.67.222.222", "208.67.220.220")
        }
        if preset in presets:
            primary, secondary = presets[preset]
            self.primary_dns.setText(primary)
            self.secondary_dns.setText(secondary)
            
    def get_config(self):
        """Obtiene la configuración actual"""
        return {
            'primary_dns': self.primary_dns.text(),
            'secondary_dns': self.secondary_dns.text()
        }
        
    def set_config(self, config):
        """Establece la configuración"""
        if 'primary_dns' in config:
            self.primary_dns.setText(config['primary_dns'])
        if 'secondary_dns' in config:
            self.secondary_dns.setText(config['secondary_dns'])
            
    def _emit_config(self):
        """Emite la señal de cambio de configuración"""
        self.config_changed.emit(self.get_config())

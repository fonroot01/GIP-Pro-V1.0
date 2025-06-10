from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QLabel
)
from PyQt6.QtCore import Qt, QTimer

class StatusBar(QFrame):
    """Barra de estado con información del sistema y mensajes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("status_bar")
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Mensaje de estado
        self.status_msg = QLabel()
        self.status_msg.setObjectName("status_message")
        layout.addWidget(self.status_msg)
        
        layout.addStretch()
        
        # IP Pública
        self.public_ip = QLabel()
        self.public_ip.setObjectName("public_ip")
        layout.addWidget(self.public_ip)
        
        layout.addSpacing(20)
        
        # Sistema Operativo
        self.os_info = QLabel()
        self.os_info.setObjectName("os_info")
        layout.addWidget(self.os_info)
        
        # Timer para limpiar mensajes
        self.msg_timer = QTimer(self)
        self.msg_timer.timeout.connect(self.clear_status)
        self.msg_timer.setSingleShot(True)
        
    def show_success(self, message, duration=3000):
        """Muestra un mensaje de éxito"""
        self.status_msg.setText(f"✅ {message}")
        self.status_msg.setProperty("type", "success")
        self.msg_timer.start(duration)
        
    def show_error(self, message, duration=3000):
        """Muestra un mensaje de error"""
        self.status_msg.setText(f"❌ {message}")
        self.status_msg.setProperty("type", "error")
        self.msg_timer.start(duration)
        
    def show_warning(self, message, duration=3000):
        """Muestra un mensaje de advertencia"""
        self.status_msg.setText(f"⚠️ {message}")
        self.status_msg.setProperty("type", "warning")
        self.msg_timer.start(duration)
        
    def clear_status(self):
        """Limpia el mensaje de estado"""
        self.status_msg.clear()
        self.status_msg.setProperty("type", "")
        
    def update_public_ip(self, ip):
        """Actualiza la IP pública mostrada"""
        self.public_ip.setText(f"IP Pública: {ip}")
        
    def update_os_info(self, os_name):
        """Actualiza la información del sistema operativo"""
        self.os_info.setText(f"SO: {os_name}")

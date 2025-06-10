from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QTimer

class StatusLabel(QLabel):
    """Label para mostrar mensajes de estado con auto-desaparición"""
    
    def __init__(self, parent=None, duration=3000):
        super().__init__(parent)
        self.duration = duration
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clear)
        self.timer.setSingleShot(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hide()
        
    def show_message(self, message, status_type='info'):
        """Muestra un mensaje con el tipo de estado especificado"""
        self.setText(message)
        self.setProperty('class', status_type)
        self.style().polish(self)  # Forzar actualización de estilo
        self.show()
        self.timer.start(self.duration)
        
    def show_success(self, message):
        """Muestra un mensaje de éxito"""
        self.show_message(message, 'success')
        
    def show_error(self, message):
        """Muestra un mensaje de error"""
        self.show_message(message, 'error')
        
    def show_warning(self, message):
        """Muestra un mensaje de advertencia"""
        self.show_message(message, 'warning')

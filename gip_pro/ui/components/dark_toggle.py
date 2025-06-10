# Toggle para modo oscuro/claro
# Aquí se define el widget para cambiar el tema

from PyQt6.QtWidgets import QCheckBox, QApplication  # type: ignore
from PyQt6.QtGui import QGuiApplication  # type: ignore
from ..compact_mode import apply_compact_style

class DarkToggle(QCheckBox):  # type: ignore[misc]
    def __init__(self, parent=None):
        super().__init__("🌙 Modo Oscuro", parent)
        self.setChecked(True)
        
        # Estilo consistente para ambos temas, ocultando el indicador
        self.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 4px;
                min-height: 24px;
                background-color: rgba(0, 0, 0, 0.1);
            }
            QCheckBox::indicator {
                width: 0px;
                height: 0px;
            }
            QCheckBox:checked {
                color: #ffffff;
                background-color: rgba(0, 0, 0, 0.2);
            }
            QCheckBox:!checked {
                color: #000000;
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        
        self.stateChanged.connect(self.toggle_theme)

    def toggle_theme(self, state):
        app = QApplication.instance()
        if isinstance(app, QApplication):
            apply_compact_style(app, dark=bool(state))
            # Actualizar el texto según el tema
            self.setText("🌙 Modo Oscuro" if state else "☀️ Modo Claro")

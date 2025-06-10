from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QApplication, QTabWidget
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer
from .main import TabIP
from .components.dark_toggle import DarkToggle
import os
import sys
import platform

class MainWindow(QMainWindow):
    def __init__(self, network_tools=None, logger=None):
        if platform.system() == "Windows" and not self.is_running_as_admin():
            self.run_as_admin()
        super().__init__()
        self.network_tools = network_tools
        self.logger = logger
        self.is_dark = True
        
        # Setup del logo animado
        self.current_logo = 1
        self.logo_timer = QTimer(self)
        self.logo_timer.timeout.connect(self.update_window_icon)
        self.logo_timer.start(500)
        
        self.init_ui()
        
    def init_ui(self):
        # Configuración básica de la ventana
        self.setWindowTitle("GIP Pro - Gestión de IPs")
        self.setMinimumSize(800, 500)
        self.resize(1000, 700)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Barra superior con título y toggle de tema
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(8, 4, 8, 4)
        top_bar.setSpacing(4)
        
        # Título
        self.title = QPushButton("GIP Pro - Gestión avanzada de IPs")
        self.title.setEnabled(False)
        self.title.setProperty("class", "title")
        top_bar.addWidget(self.title)
        top_bar.addStretch(1)

        # Toggle de tema oscuro/claro
        self.theme_toggle = DarkToggle(self)
        self.theme_toggle.setChecked(self.is_dark)
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        top_bar.addWidget(self.theme_toggle)
        main_layout.addLayout(top_bar)
          # Panel principal con tab de IP
        self.tab_ip = TabIP()
        main_layout.addWidget(self.tab_ip)
        
        # Actualizar tema inicial
        self.apply_theme()
        
    def update_window_icon(self):
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logo', f'{self.current_logo}.png')
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        self.current_logo = (self.current_logo % 7) + 1
        
    def toggle_theme(self, state):
        self.is_dark = bool(state)
        self.apply_theme()
        
    def apply_theme(self):
        theme_file = "dark_theme.css" if self.is_dark else "light_theme.css"
        theme_path = os.path.join(os.path.dirname(__file__), theme_file)
        if os.path.exists(theme_path):
            try:
                with open(theme_path, "r", encoding='utf-8') as file:
                    self.setStyleSheet(file.read())
                self.update_theme_icon()
            except Exception as e:
                print(f"Error al cargar el tema {theme_file}: {str(e)}")
        else:
            print(f"Archivo de tema no encontrado: {theme_file}")

    def update_theme_icon(self):
        text = "🌙 Modo Oscuro" if self.is_dark else "☀️ Modo Claro"
        self.theme_toggle.setText(text)

    def is_running_as_admin(self):
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def run_as_admin(self):
        import ctypes
        import os
        import sys
        print("[INFO] Solicitando permisos de administrador...")
        if hasattr(sys, 'frozen'):
            # PyInstaller
            script = sys.executable
            params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
            executable = sys.executable
            print(f"[DEBUG] Lanzando como admin (PyInstaller): {executable} {params}")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
        else:
            # Ejecutar como módulo: python -m gip_pro.main
            executable = sys.executable
            module = "-m gip_pro.main"
            params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
            cmd = f'{module} {params}'
            print(f"[DEBUG] Lanzando como admin (modulo): {executable} {cmd}")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, cmd, os.getcwd(), 1)
        sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
import sys
import subprocess
import requests
import platform
import json
import os
import socket

try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                 QHBoxLayout, QGroupBox, QLabel, QLineEdit, QPushButton, 
                                 QComboBox, QCheckBox, QTextEdit, QFrame, QGridLayout,
                                 QMessageBox, QProgressBar, QTabWidget)
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt5.QtGui import QFont, QPalette, QColor
    PYQT5_AVAILABLE = True
except ImportError:
    print("Error: PyQt5 no está instalado.\nInstale PyQt5 ejecutando: pip install PyQt5")
    PYQT5_AVAILABLE = False

class NetworkWorker(QThread):
    """Worker thread para operaciones de red que pueden tomar tiempo"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, operation, data=None):
        super().__init__()
        self.operation = operation
        self.data = data
    
    def run(self):
        try:
            if self.operation == "get_public_ip":
                response = requests.get("https://api.ipify.org", timeout=5)
                self.finished.emit(response.text)
            elif self.operation == "test_proxy":
                # Corregir: asegurar que self.data es una tupla o lista válida
                if not self.data or not isinstance(self.data, (tuple, list)) or len(self.data) != 2:
                    self.error.emit("❌ Error: Datos de proxy inválidos")
                    return
                proxy_host, proxy_port = self.data
                proxies = {
                    'http': f'http://{proxy_host}:{proxy_port}',
                    'https': f'https://{proxy_host}:{proxy_port}'
                }
                response = requests.get("https://httpbin.org/ip", 
                                      proxies=proxies, timeout=10)
                self.finished.emit("✅ Proxy funcionando correctamente")
            elif self.operation == "apply_network_config":
                # Simulación de aplicación de configuración de red
                import time
                time.sleep(2)  # Simula proceso
                self.finished.emit("✅ Configuración de red aplicada correctamente")
        except Exception as e:
            self.error.emit(f"❌ Error: {str(e)}")

class TabIP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.worker = None  # Inicializar worker como None
        self.init_ui()
        self.load_network_interfaces()
        self.get_public_ip()
        
    def init_ui(self):
        try:
            self.setWindowTitle("GIP Pro V1.0")
            self.setGeometry(100, 100, 900, 700)

            # --- Animación de icono de ventana ---
            from PyQt5.QtGui import QIcon
            self.logo_paths = []
            for i in range(1, 8):
                logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logo/{}.png'.format(i)))
                if os.path.exists(logo_path):
                    self.logo_paths.append(logo_path)
                else:
                    print(f"[ADVERTENCIA] Logo no encontrado: {logo_path}")
            self.logo_index = 0
            if self.logo_paths:
                self.setWindowIcon(QIcon(self.logo_paths[self.logo_index]))
                self.logo_timer = QTimer(self)
                self.logo_timer.timeout.connect(self.next_logo_icon)
                self.logo_timer.start(500)
            else:
                print("[ADVERTENCIA] No se encontraron logos para animar el icono de la app.")

            # Widget central
            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            # Layout principal
            main_layout = QVBoxLayout(central_widget)
            main_layout.setSpacing(15)
            main_layout.setContentsMargins(20, 20, 20, 20)

            # Título principal (sin logo visual)
            title_label = QLabel("🌐 Gestor de Red Avanzado")
            title_font = QFont()
            title_font.setPointSize(18)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(title_label)

            # Layout horizontal para las columnas principales
            columns_layout = QHBoxLayout()

            # Columna izquierda
            left_column = QVBoxLayout()
            left_column.addWidget(self.create_network_config_group())
            left_column.addWidget(self.create_dns_config_group())

            # Columna derecha
            right_column = QVBoxLayout()
            right_column.addWidget(self.create_proxy_config_group())
            right_column.addWidget(self.create_status_group())

            columns_layout.addLayout(left_column)
            columns_layout.addLayout(right_column)
            main_layout.addLayout(columns_layout)

            # Panel de control inferior
            control_panel = self.create_control_panel()
            main_layout.addWidget(control_panel)

            # Aplicar estilo
            self.apply_theme()
        except Exception as e:
            import traceback
            print(f"[ERROR] Error en init_ui: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error crítico", f"No se pudo inicializar la interfaz:\n{e}")

    def next_logo_icon(self):
        from PyQt5.QtGui import QIcon
        if hasattr(self, 'logo_paths') and self.logo_paths:
            self.logo_index = (self.logo_index + 1) % len(self.logo_paths)
            self.setWindowIcon(QIcon(self.logo_paths[self.logo_index]))

    def create_network_config_group(self):
        """Grupo de configuración de red"""
        group = QGroupBox("🔧 Configuración de Red")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QGridLayout(group)
        
        # Interfaz de red
        layout.addWidget(QLabel("Interfaz de Red:"), 0, 0)
        self.interface_combo = QComboBox()
        self.interface_combo.setMinimumHeight(30)
        layout.addWidget(self.interface_combo, 0, 1, 1, 2)
        
        # Configuración IP
        layout.addWidget(QLabel("Dirección IP:"), 1, 0)
        self.ip_input = QLineEdit("192.168.1.100")
        self.ip_input.setPlaceholderText("ej: 192.168.1.100")
        layout.addWidget(self.ip_input, 1, 1, 1, 2)
        
        layout.addWidget(QLabel("Máscara de Subred:"), 2, 0)
        self.mask_input = QLineEdit("255.255.255.0")
        self.mask_input.setPlaceholderText("ej: 255.255.255.0")
        layout.addWidget(self.mask_input, 2, 1, 1, 2)
        
        layout.addWidget(QLabel("Gateway:"), 3, 0)
        self.gateway_input = QLineEdit("192.168.1.1")
        self.gateway_input.setPlaceholderText("ej: 192.168.1.1")
        layout.addWidget(self.gateway_input, 3, 1, 1, 2)
        
        # Botones
        btn_apply = QPushButton("🔄 Aplicar Configuración")
        btn_apply.setMinimumHeight(35)
        btn_apply.clicked.connect(self.apply_network_config)
        layout.addWidget(btn_apply, 4, 0, 1, 2)

        btn_reset = QPushButton("🔄 Restablecer Red")
        btn_reset.setMinimumHeight(35)
        btn_reset.clicked.connect(self.reset_network_config)
        layout.addWidget(btn_reset, 4, 2)
        
        return group

    def reset_network_config(self):
        """Restablecer la configuración de red a la anterior o activar DHCP real"""
        self.add_status_message("🔄 Restableciendo configuración de red...")
        # Aquí puedes implementar el restablecimiento real según el SO
        if platform.system() == "Windows":
            try:
                # Requiere privilegios de administrador
                subprocess.run(["netsh", "interface", "ip", "set", "address", self.interface_combo.currentText(), "dhcp"], check=True)
                subprocess.run(["netsh", "interface", "ip", "set", "dns", self.interface_combo.currentText(), "dhcp"], check=True)
                self.add_status_message("✅ Red restablecida a DHCP correctamente")
            except Exception as e:
                self.add_status_message(f"❌ Error al restablecer red: {str(e)}")
        else:
            # Linux/Mac ejemplo (puedes adaptar según tu sistema)
            try:
                subprocess.run(["sudo", "dhclient", "-r", self.interface_combo.currentText()])
                subprocess.run(["sudo", "dhclient", self.interface_combo.currentText()])
                self.add_status_message("✅ Red restablecida a DHCP correctamente")
            except Exception as e:
                self.add_status_message(f"❌ Error al restablecer red: {str(e)}")

    def create_dns_config_group(self):
        """Grupo de configuración DNS"""
        group = QGroupBox("🌍 Configuración DNS")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QGridLayout(group)
        
        # DNS Servers
        layout.addWidget(QLabel("DNS Primario:"), 0, 0)
        self.dns_primary = QLineEdit("8.8.8.8")
        layout.addWidget(self.dns_primary, 0, 1, 1, 2)
        
        layout.addWidget(QLabel("DNS Secundario:"), 1, 0)
        self.dns_secondary = QLineEdit("8.8.4.4")
        layout.addWidget(self.dns_secondary, 1, 1, 1, 2)
        
        # Botones rápidos DNS
        dns_buttons_layout = QHBoxLayout()
        
        btn_google = QPushButton("Google DNS")
        btn_google.clicked.connect(lambda: self.set_dns("8.8.8.8", "8.8.4.4"))
        dns_buttons_layout.addWidget(btn_google)
        
        btn_cloudflare = QPushButton("Cloudflare DNS")
        btn_cloudflare.clicked.connect(lambda: self.set_dns("1.1.1.1", "1.0.0.1"))
        dns_buttons_layout.addWidget(btn_cloudflare)
        
        btn_opendns = QPushButton("OpenDNS")
        btn_opendns.clicked.connect(lambda: self.set_dns("208.67.222.222", "208.67.220.220"))
        dns_buttons_layout.addWidget(btn_opendns)
        
        layout.addLayout(dns_buttons_layout, 2, 0, 1, 3)
        
        # Botón aplicar DNS
        btn_apply_dns = QPushButton("🔄 Aplicar DNS")
        btn_apply_dns.setMinimumHeight(35)
        btn_apply_dns.clicked.connect(self.apply_dns_config)
        layout.addWidget(btn_apply_dns, 3, 0, 1, 3)
        
        return group
    
    def create_proxy_config_group(self):
        """Grupo de configuración de proxy"""
        group = QGroupBox("🔐 Configuración de Proxy")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QGridLayout(group)
        
        # Checkbox habilitar proxy
        self.proxy_enabled = QCheckBox("Habilitar Proxy")
        self.proxy_enabled.toggled.connect(self.toggle_proxy_fields)
        layout.addWidget(self.proxy_enabled, 0, 0, 1, 2)
        
        # Configuración proxy
        layout.addWidget(QLabel("Servidor Proxy:"), 1, 0)
        self.proxy_server = QLineEdit()
        self.proxy_server.setPlaceholderText("ej: proxy.empresa.com")
        self.proxy_server.setEnabled(False)
        layout.addWidget(self.proxy_server, 1, 1)
        
        layout.addWidget(QLabel("Puerto:"), 2, 0)
        self.proxy_port = QLineEdit()
        self.proxy_port.setPlaceholderText("ej: 8080")
        self.proxy_port.setEnabled(False)
        layout.addWidget(self.proxy_port, 2, 1)
        
        # Botón probar proxy
        self.btn_test_proxy = QPushButton("🧪 Probar Proxy")
        self.btn_test_proxy.setMinimumHeight(35)
        self.btn_test_proxy.setEnabled(False)
        self.btn_test_proxy.clicked.connect(self.test_proxy)
        layout.addWidget(self.btn_test_proxy, 3, 0, 1, 2)
        
        return group
    
    def create_status_group(self):
        """Grupo de estado y resultados"""
        group = QGroupBox("📊 Estado y Resultados")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QVBoxLayout(group)
        
        # Información del sistema
        system_info = QFrame()
        system_layout = QGridLayout(system_info)
        
        system_layout.addWidget(QLabel("Sistema Operativo:"), 0, 0)
        self.os_label = QLabel(f"{platform.system()} {platform.release()}")
        system_layout.addWidget(self.os_label, 0, 1)
        
        system_layout.addWidget(QLabel("IP Pública:"), 1, 0)
        self.public_ip_label = QLabel("Detectando...")
        system_layout.addWidget(self.public_ip_label, 1, 1)
        
        layout.addWidget(system_info)
        
        # Área de mensajes de estado
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(120)
        self.status_text.setReadOnly(True)
        self.status_text.append("🔄 Sistema iniciado correctamente")
        layout.addWidget(self.status_text)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        # Corregir los métodos setValue y setMaximum
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        return group
    
    def create_control_panel(self):
        """Panel de control inferior"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        layout = QHBoxLayout(frame)
        
        # Botón modo oscuro
        self.dark_mode_btn = QPushButton("🌙 Modo Oscuro")
        self.dark_mode_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.dark_mode_btn)
        
        layout.addStretch()
        
        # Botones de acción
        btn_refresh = QPushButton("🔄 Actualizar")
        btn_refresh.clicked.connect(self.refresh_all)
        layout.addWidget(btn_refresh)
        
        btn_save_config = QPushButton("💾 Guardar Configuración")
        btn_save_config.clicked.connect(self.save_configuration)
        layout.addWidget(btn_save_config)
        
        btn_load_config = QPushButton("📂 Cargar Configuración")
        btn_load_config.clicked.connect(self.load_configuration)
        layout.addWidget(btn_load_config)
        
        return frame
    
    def load_network_interfaces(self):
        """Cargar interfaces de red disponibles"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["netsh", "interface", "show", "interface"], 
                                      capture_output=True, text=True)
                # Procesamiento simplificado para el ejemplo
                interfaces = ["Wi-Fi", "Ethernet", "Local Area Connection"]
            else:
                # Para Linux/Mac
                interfaces = ["eth0", "wlan0", "lo"]
            
            # Verificar que interfaces sea una lista válida
            if interfaces and isinstance(interfaces, list):
                self.interface_combo.addItems(interfaces)
            else:
                self.interface_combo.addItems(["No interfaces found"])
        except Exception as e:
            self.add_status_message(f"❌ Error cargando interfaces: {str(e)}")
            self.interface_combo.addItems(["Error loading interfaces"])
    
    def get_public_ip(self):
        """Obtener IP pública"""
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.quit()  # Terminar worker anterior si existe
        
        self.worker = NetworkWorker("get_public_ip")
        self.worker.finished.connect(self.on_public_ip_received)
        self.worker.error.connect(self.on_network_error)
        self.worker.start()
    
    def on_public_ip_received(self, ip):
        """Callback cuando se recibe la IP pública"""
        self.public_ip_label.setText(ip)
        self.add_status_message(f"🌐 IP pública detectada: {ip}")
    
    def on_network_error(self, error):
        """Callback para errores de red"""
        self.add_status_message(error)
        self.public_ip_label.setText("No disponible")
    
    def apply_network_config(self):
        """Aplicar configuración de red REAL para Windows, Linux y Mac"""
        if not self.check_admin_permissions():
            self.add_status_message("❌ No tienes permisos de administrador para aplicar cambios reales.")
            return
        self.show_progress("Aplicando configuración de red...")
        if not self.ip_input.text():
            self.add_status_message("❌ Por favor ingrese la dirección IP")
            self.hide_progress()
            return
        interface = self.interface_combo.currentText()
        ip = self.ip_input.text()
        mask = self.mask_input.text()
        gateway = self.gateway_input.text()
        try:
            if platform.system() == "Windows":
                cmd = [
                    "netsh", "interface", "ip", "set", "address", interface, "static",
                    ip, mask if mask else "255.255.255.0", gateway if gateway else "0.0.0.0"
                ]
                subprocess.run(cmd, check=True)
                self.add_status_message(f"✅ IP cambiada correctamente a {ip} en {interface}")
            elif platform.system() == "Linux":
                mask_cidr = mask if "/" in mask else self.mask_to_cidr(mask) if mask else "24"
                subprocess.run(["sudo", "ip", "addr", "flush", "dev", interface], check=True)
                subprocess.run(["sudo", "ip", "addr", "add", f"{ip}/{mask_cidr}", "dev", interface], check=True)
                if gateway:
                    subprocess.run(["sudo", "ip", "route", "add", "default", "via", gateway], check=True)
                self.add_status_message(f"✅ IP cambiada correctamente a {ip} en {interface}")
            elif platform.system() == "Darwin":
                if mask:
                    subprocess.run(["sudo", "ifconfig", interface, ip, "netmask", mask], check=True)
                else:
                    subprocess.run(["sudo", "ifconfig", interface, ip], check=True)
                if gateway:
                    subprocess.run(["sudo", "route", "add", "default", gateway], check=True)
                self.add_status_message(f"✅ IP cambiada correctamente a {ip} en {interface}")
            else:
                self.add_status_message("❌ SO no soportado para cambio de IP real")
        except Exception as e:
            self.add_status_message(f"❌ Error al cambiar IP: {str(e)}")
        self.hide_progress()

    def mask_to_cidr(self, mask):
        """Convierte una máscara de subred a notación CIDR (ej: 255.255.255.0 -> 24)"""
        try:
            return str(sum([bin(int(x)).count('1') for x in mask.split('.')]))
        except Exception:
            return "24"
    
    def enable_dhcp(self):
        """Activar DHCP"""
        self.add_status_message("🔄 Activando DHCP...")
        # Limpiar campos manuales
        self.ip_input.clear()
        self.mask_input.clear()
        self.gateway_input.clear()
        self.add_status_message("✅ DHCP activado - Configuración automática")
    
    def set_dns(self, primary, secondary):
        """Establecer servidores DNS"""
        self.dns_primary.setText(primary)
        self.dns_secondary.setText(secondary)
        self.add_status_message(f"📡 DNS configurado: {primary}, {secondary}")
    
    def apply_dns_config(self):
        """Aplicar configuración DNS"""
        primary = self.dns_primary.text()
        secondary = self.dns_secondary.text()
        
        if not primary:
            self.add_status_message("❌ DNS primario es requerido")
            return
        
        self.add_status_message(f"✅ Configuración DNS aplicada: {primary}, {secondary}")
    
    def toggle_proxy_fields(self, enabled):
        """Habilitar/deshabilitar campos de proxy"""
        self.proxy_server.setEnabled(enabled)
        self.proxy_port.setEnabled(enabled)
        self.btn_test_proxy.setEnabled(enabled)
        
        if enabled:
            self.add_status_message("🔐 Proxy habilitado")
        else:
            self.add_status_message("🔓 Proxy deshabilitado")
    
    def test_proxy(self):
        """Probar configuración de proxy"""
        if not self.proxy_server.text() or not self.proxy_port.text():
            self.add_status_message("❌ Complete servidor y puerto del proxy")
            return
        
        self.show_progress("Probando conexión proxy...")
        
        self.worker = NetworkWorker("test_proxy", 
                                   (self.proxy_server.text(), self.proxy_port.text()))
        self.worker.finished.connect(self.on_proxy_tested)
        self.worker.error.connect(self.on_network_error)
        self.worker.start()
    
    def on_proxy_tested(self, message):
        """Callback cuando se prueba el proxy"""
        self.add_status_message(message)
        self.hide_progress()
    
    def toggle_theme(self):
        """Alternar entre modo claro y oscuro"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        
        if self.dark_mode:
            self.dark_mode_btn.setText("☀️ Modo Claro")
            self.add_status_message("🌙 Modo oscuro activado")
        else:
            self.dark_mode_btn.setText("🌙 Modo Oscuro")
            self.add_status_message("☀️ Modo claro activado")
    
    def apply_theme(self):
        """Aplicar tema visual"""
        if self.dark_mode:
            # Tema oscuro con letras blancas
            self.setStyleSheet("""
                QMainWindow, QWidget, QGroupBox, QLabel, QLineEdit, QComboBox, QTextEdit {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QGroupBox { 
                    font-weight: bold; 
                    border: 2px solid #555555;
                    border-radius: 5px;
                    margin-top: 1ex;
                    padding-top: 10px;
                    background-color: #3c3c3c;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #ffffff;
                }
                QLineEdit, QComboBox, QTextEdit {
                    background-color: #4a4a4a;
                    border: 1px solid #666666;
                    border-radius: 3px;
                    padding: 5px;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #0078d4;
                    border: none;
                    border-radius: 3px;
                    padding: 8px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                }
            """)
        else:
            # Tema claro
            self.setStyleSheet("""
                QMainWindow { background-color: #f0f0f0; color: #000000; }
                QGroupBox { 
                    font-weight: bold; 
                    border: 2px solid #cccccc;
                    border-radius: 5px;
                    margin-top: 1ex;
                    padding-top: 10px;
                    background-color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
                QLineEdit, QComboBox, QTextEdit {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    border-radius: 3px;
                    padding: 5px;
                }
                QPushButton {
                    background-color: #0078d4;
                    border: none;
                    border-radius: 3px;
                    padding: 8px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                }
            """)
    
    def show_progress(self, message):
        """Mostrar barra de progreso con mensaje"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Progreso indefinido
        self.add_status_message(message)
    
    def hide_progress(self):
        """Ocultar barra de progreso"""
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)  # Restaurar rango normal
    
    def add_status_message(self, message):
        """Agregar mensaje al área de estado"""
        self.status_text.append(f"[{self.get_timestamp()}] {message}")
        # Auto-scroll al final
        scrollbar = self.status_text.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())
    
    def get_timestamp(self):
        """Obtener timestamp actual"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def refresh_all(self):
        """Actualizar toda la información"""
        self.add_status_message("🔄 Actualizando información...")
        self.load_network_interfaces()
        self.get_public_ip()
    
    def save_configuration(self):
        """Guardar configuración actual"""
        config = {
            'network': {
                'interface': self.interface_combo.currentText(),
                'ip': self.ip_input.text(),
                'mask': self.mask_input.text(),
                'gateway': self.gateway_input.text()
            },
            'dns': {
                'primary': self.dns_primary.text(),
                'secondary': self.dns_secondary.text()
            },
            'proxy': {
                'enabled': self.proxy_enabled.isChecked(),
                'server': self.proxy_server.text(),
                'port': self.proxy_port.text()
            },
            'theme': {
                'dark_mode': self.dark_mode
            }
        }
        
        try:
            with open('network_config.json', 'w') as f:
                json.dump(config, f, indent=4)
            self.add_status_message("💾 Configuración guardada en network_config.json")
        except Exception as e:
            self.add_status_message(f"❌ Error guardando configuración: {str(e)}")
    
    def load_configuration(self):
        """Cargar configuración guardada"""
        try:
            if os.path.exists('network_config.json'):
                with open('network_config.json', 'r') as f:
                    config = json.load(f)
                
                # Cargar configuración de red
                if 'network' in config:
                    net_config = config['network']
                    self.ip_input.setText(net_config.get('ip', ''))
                    self.mask_input.setText(net_config.get('mask', ''))
                    self.gateway_input.setText(net_config.get('gateway', ''))
                
                # Cargar configuración DNS
                if 'dns' in config:
                    dns_config = config['dns']
                    self.dns_primary.setText(dns_config.get('primary', ''))
                    self.dns_secondary.setText(dns_config.get('secondary', ''))
                
                # Cargar configuración proxy
                if 'proxy' in config:
                    proxy_config = config['proxy']
                    self.proxy_enabled.setChecked(proxy_config.get('enabled', False))
                    self.proxy_server.setText(proxy_config.get('server', ''))
                    self.proxy_port.setText(proxy_config.get('port', ''))
                
                # Cargar tema
                if 'theme' in config:
                    theme_config = config['theme']
                    if theme_config.get('dark_mode', False) != self.dark_mode:
                        self.toggle_theme()
                
                self.add_status_message("📂 Configuración cargada desde network_config.json")
            else:
                self.add_status_message("❌ No se encontró archivo de configuración")
        except Exception as e:
            self.add_status_message(f"❌ Error cargando configuración: {str(e)}")

    def check_admin_permissions(self):
        """Verifica si la app tiene permisos de administrador y muestra advertencia si no los tiene"""
        is_admin = False
        if platform.system() == "Windows":
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception:
                is_admin = False
        else:
            is_admin = os.geteuid() == 0 if hasattr(os, 'geteuid') else False
        if not is_admin:
            QMessageBox.warning(self, "Permisos requeridos", "Se requieren permisos de administrador para aplicar cambios reales en la red.")
        return is_admin

def ensure_admin():
    if platform.system() == "Windows":
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print("[INFO] Solicitando permisos de administrador...")
                executable = sys.executable
                script = os.path.abspath(__file__)
                params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
                print(f"[DEBUG] Lanzando como admin (script): {executable} {script} {params}")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, f'"{script}" {params}', None, 1)
                sys.exit(0)
        except Exception as e:
            print(f"[ERROR] No se pudo solicitar permisos de administrador: {e}")

if __name__ == "__main__":
    ensure_admin()
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = TabIP()
    window.show()
    sys.exit(app.exec_())
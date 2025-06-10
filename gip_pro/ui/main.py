## Desarrolado por Alfonso Mosquera, Informático y Desarrollador de Software

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

            # Pie de página con copyright
            copyright_label = QLabel("© 2025 Alfonso Mosquera")
            copyright_font = QFont()
            copyright_font.setPointSize(8)
            copyright_label.setFont(copyright_font)
            copyright_label.setAlignment(Qt.AlignCenter)
            copyright_label.setStyleSheet("color: gray;")
            main_layout.addWidget(copyright_label)

            # Aplicar estilo
            self.apply_theme()
        except Exception as e:
            import traceback
            print(f"[ERROR] Error en init_ui: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error crítico", f"No se pudo inicializar la interfaz:\n{e}")

        # Asignar atributos para títulos y subtítulos
        # Título principal
        # Refuerzo: solo el título principal en negrita
        if hasattr(self, 'centralWidget'):
            for widget in self.findChildren(QLabel):
                # Si es el título principal (centrado y grande)
                if widget.text().startswith("🌐 Gestor de Red Avanzado"):
                    font = QFont()
                    font.setPointSize(18)
                    font.setBold(True)
                    widget.setFont(font)
                else:
                    # Todos los QLabel de datos/descripciones en fuente normal
                    font = QFont()
                    font.setPointSize(10)
                    font.setBold(False)
                    widget.setFont(font)
        # Subtítulos de grupos (QGroupBox)
        for group in self.findChildren(QGroupBox):
            font = QFont()
            font.setPointSize(10)
            font.setBold(True)
            group.setFont(font)
        # QLineEdit, QComboBox, QTextEdit, QCheckBox, QPushButton en fuente normal
        for widget in self.findChildren((QLineEdit, QComboBox, QTextEdit, QCheckBox, QPushButton)):
            font = QFont()
            font.setPointSize(10)
            font.setBold(False)
            widget.setFont(font)

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
        # Separación extra del título
        layout.setContentsMargins(10, 25, 10, 10)  # margen superior aumentado
        layout.setVerticalSpacing(12)

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
        if platform.system() == "Windows":
            try:
                subprocess.run(["netsh", "interface", "ip", "set", "address", self.interface_combo.currentText(), "dhcp"], check=True)
                subprocess.run(["netsh", "interface", "ip", "set", "dns", self.interface_combo.currentText(), "dhcp"], check=True)
                self.add_status_message("✅ Red restablecida a DHCP correctamente")
            except Exception as e:
                self.add_status_message(f"❌ Error al restablecer red: {str(e)}")
        else:
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
        # Separación extra del título
        layout.setContentsMargins(10, 30, 10, 10)  # margen superior aumentado
        layout.setVerticalSpacing(12)
        
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
        # Separación extra del título
        layout.setContentsMargins(10, 30, 10, 10)  # margen superior aumentado
        layout.setVerticalSpacing(10)
        
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
    
    def toggle_proxy_fields(self):
        """Habilita o deshabilita los campos de proxy según el checkbox"""
        enabled = self.proxy_enabled.isChecked()
        self.proxy_server.setEnabled(enabled)
        self.proxy_port.setEnabled(enabled)
        self.btn_test_proxy.setEnabled(enabled)

    def on_public_ip_received(self, ip):
        """Callback cuando se recibe la IP pública"""
        if hasattr(self, 'public_ip_label') and self.public_ip_label:
            self.public_ip_label.setText(ip)
        self.add_status_message(f"🌐 IP pública detectada: {ip}")

    def on_network_error(self, error):
        """Callback para errores de red"""
        self.add_status_message(error)
        if hasattr(self, 'public_ip_label') and self.public_ip_label:
            self.public_ip_label.setText("No disponible")
    
    def apply_network_config(self):
        """Aplicar configuración de red REAL para Windows, Linux y Mac, robusto ante errores"""
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
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    self.add_status_message(f"❌ Error al cambiar IP: {result.stderr.strip() or result.stdout.strip()}")
                else:
                    self.add_status_message(f"✅ IP cambiada correctamente a {ip} en {interface}")
            elif platform.system() == "Linux":
                mask_cidr = mask if "/" in mask else self.mask_to_cidr(mask) if mask else "24"
                cmds = [
                    ["sudo", "ip", "addr", "flush", "dev", interface],
                    ["sudo", "ip", "addr", "add", f"{ip}/{mask_cidr}", "dev", interface]
                ]
                if gateway:
                    cmds.append(["sudo", "ip", "route", "add", "default", "via", gateway])
                for c in cmds:
                    result = subprocess.run(c, capture_output=True, text=True)
                    if result.returncode != 0:
                        self.add_status_message(f"❌ Error: {result.stderr.strip() or result.stdout.strip()}")
                        self.hide_progress()
                        return
                self.add_status_message(f"✅ IP cambiada correctamente a {ip} en {interface}")
            elif platform.system() == "Darwin":
                cmds = []
                if mask:
                    cmds.append(["sudo", "ifconfig", interface, ip, "netmask", mask])
                else:
                    cmds.append(["sudo", "ifconfig", interface, ip])
                if gateway:
                    cmds.append(["sudo", "route", "add", "default", gateway])
                for c in cmds:
                    result = subprocess.run(c, capture_output=True, text=True)
                    if result.returncode != 0:
                        self.add_status_message(f"❌ Error: {result.stderr.strip() or result.stdout.strip()}")
                        self.hide_progress()
                        return
                self.add_status_message(f"✅ IP cambiada correctamente a {ip} en {interface}")
            else:
                self.add_status_message("❌ SO no soportado para cambio de IP real")
        except subprocess.CalledProcessError as e:
            self.add_status_message(f"❌ Error al cambiar IP: {e.stderr.strip() if hasattr(e, 'stderr') and e.stderr else str(e)}")
        except Exception as e:
            self.add_status_message(f"❌ Error inesperado al cambiar IP: {str(e)}")
        finally:
            self.hide_progress()

    def mask_to_cidr(self, mask):
        """Convierte una máscara de subred a notación CIDR (ej: 255.255.255.0 -> 24)"""
        try:
            return str(sum([bin(int(x)).count('1') for x in mask.split('.')]))
        except Exception:
            return "24"

    def apply_dns_config(self):
        """Aplica la configuración DNS seleccionada en la interfaz elegida"""
        interface = self.interface_combo.currentText()
        dns1 = self.dns_primary.text().strip()
        dns2 = self.dns_secondary.text().strip()
        if not dns1:
            self.add_status_message("❌ Debes ingresar al menos un DNS primario.")
            return
        self.show_progress("Aplicando configuración DNS...")
        try:
            if platform.system() == "Windows":
                cmds = [["netsh", "interface", "ip", "set", "dns", interface, "static", dns1, "primary"]]
                if dns2:
                    cmds.append(["netsh", "interface", "ip", "add", "dns", interface, dns2, "index=2"])
                for cmd in cmds:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode != 0:
                        self.add_status_message(f"❌ Error al aplicar DNS: {result.stderr.strip() or result.stdout.strip()}")
                        self.hide_progress()
                        return
                self.add_status_message(f"✅ DNS aplicado correctamente: {dns1}{', ' + dns2 if dns2 else ''}")
            elif platform.system() in ("Linux", "Darwin"):
                # Usar resolv.conf (requiere sudo) o nmcli si está disponible
                try:
                    # Intentar con nmcli si existe
                    result = subprocess.run(["which", "nmcli"], capture_output=True, text=True)
                    if result.returncode == 0:
                        cmds = [["sudo", "nmcli", "con", "mod", interface, "ipv4.dns", f"{dns1} {dns2}" if dns2 else dns1],
                                ["sudo", "nmcli", "con", "up", interface]]
                        for cmd in cmds:
                            result = subprocess.run(cmd, capture_output=True, text=True)
                            if result.returncode != 0:
                                self.add_status_message(f"❌ Error al aplicar DNS: {result.stderr.strip() or result.stdout.strip()}")
                                self.hide_progress()
                                return
                        self.add_status_message(f"✅ DNS aplicado correctamente: {dns1}{', ' + dns2 if dns2 else ''}")
                    else:
                        # Fallback: editar /etc/resolv.conf (requiere sudo)
                        resolv_lines = [f"nameserver {dns1}\n"]
                        if dns2:
                            resolv_lines.append(f"nameserver {dns2}\n")
                        with open("/etc/resolv.conf", "w") as f:
                            f.writelines(resolv_lines)
                        self.add_status_message(f"✅ DNS aplicado en /etc/resolv.conf: {dns1}{', ' + dns2 if dns2 else ''}")
                except Exception as e:
                    self.add_status_message(f"❌ Error al aplicar DNS: {str(e)}")
            else:
                self.add_status_message("❌ SO no soportado para cambio de DNS real")
        except Exception as e:
            self.add_status_message(f"❌ Error inesperado al aplicar DNS: {str(e)}")
        finally:
            self.hide_progress()
    
    def test_proxy(self):
        """Prueba la configuración de proxy actual"""
        if not self.proxy_enabled.isChecked():
            self.add_status_message("⚠️ El proxy no está habilitado.")
            return
        proxy_host = self.proxy_server.text().strip()
        proxy_port = self.proxy_port.text().strip()
        if not proxy_host or not proxy_port:
            self.add_status_message("❌ Debes ingresar el servidor y puerto del proxy.")
            return
        self.add_status_message("🧪 Probando proxy...")
        # Usar un worker thread para no bloquear la UI
        if hasattr(self, 'worker') and self.worker is not None:
            self.worker.quit()
        self.worker = NetworkWorker("test_proxy", (proxy_host, proxy_port))
        self.worker.finished.connect(lambda msg: self.add_status_message(msg))
        self.worker.error.connect(lambda err: self.add_status_message(err))
        self.worker.start()

    def add_status_message(self, message):
        """Agrega un mensaje al área de estado"""
        if hasattr(self, 'status_text') and self.status_text:
            self.status_text.append(message)
        else:
            print(message)

    def toggle_theme(self):
        """Alterna entre modo oscuro y claro"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def refresh_all(self):
        """Actualiza las interfaces de red y la IP pública"""
        self.add_status_message("🔄 Actualizando información de red...")
        self.load_network_interfaces()
        self.get_public_ip()

    def save_configuration(self):
        """Guarda la configuración actual en un archivo JSON"""
        from PyQt5.QtWidgets import QFileDialog
        config = {
            'interface': self.interface_combo.currentText(),
            'ip': self.ip_input.text(),
            'mask': self.mask_input.text(),
            'gateway': self.gateway_input.text(),
            'dns_primary': self.dns_primary.text(),
            'dns_secondary': self.dns_secondary.text(),
            'proxy_enabled': self.proxy_enabled.isChecked(),
            'proxy_server': self.proxy_server.text(),
            'proxy_port': self.proxy_port.text()
        }
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar configuración", "configuracion_gip.json", "Archivos JSON (*.json)", options=options)
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
                self.add_status_message(f"💾 Configuración guardada en: {file_path}")
            except Exception as e:
                self.add_status_message(f"❌ Error al guardar configuración: {e}")

    def load_configuration(self):
        """Carga una configuración desde un archivo JSON"""
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Cargar configuración", "", "Archivos JSON (*.json)", options=options)
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.interface_combo.setCurrentText(config.get('interface', ''))
                self.ip_input.setText(config.get('ip', ''))
                self.mask_input.setText(config.get('mask', ''))
                self.gateway_input.setText(config.get('gateway', ''))
                self.dns_primary.setText(config.get('dns_primary', ''))
                self.dns_secondary.setText(config.get('dns_secondary', ''))
                self.proxy_enabled.setChecked(config.get('proxy_enabled', False))
                self.proxy_server.setText(config.get('proxy_server', ''))
                self.proxy_port.setText(config.get('proxy_port', ''))
                self.add_status_message(f"📂 Configuración cargada desde: {file_path}")
            except Exception as e:
                self.add_status_message(f"❌ Error al cargar configuración: {e}")

    def set_dns(self, primary, secondary):
        """Establece los valores de los campos DNS primario y secundario en la UI"""
        if hasattr(self, 'dns_primary') and hasattr(self, 'dns_secondary'):
            self.dns_primary.setText(primary)
            self.dns_secondary.setText(secondary)
        self.add_status_message(f"🌍 DNS configurado: {primary}, {secondary}")

    def apply_theme(self):
        """Aplica el tema oscuro o claro a la interfaz, con fuentes y colores adecuados"""
        palette = QPalette()
        if self.dark_mode:
            # Colores base del tema oscuro
            palette.setColor(QPalette.Window, QColor(30, 30, 30))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(45, 45, 45))  # Más claro para mejor contraste
            palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, QColor(255, 255, 255))  # Texto blanco puro
            palette.setColor(QPalette.Button, QColor(45, 45, 45))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(38, 79, 120))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            palette.setColor(QPalette.PlaceholderText, QColor(180, 180, 180))  # Gris claro para placeholders
            # Color para widgets deshabilitados
            palette.setColor(QPalette.Disabled, QPalette.Text, QColor(140, 140, 140))
            palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(140, 140, 140))
            QApplication.setPalette(palette)
            
            # Ajustar colores de placeholder para cada campo de entrada
            for widget in self.findChildren(QLineEdit):
                widget.setStyleSheet("""
                    QLineEdit {
                        color: white;
                        background-color: rgb(45, 45, 45);
                    }
                    QLineEdit:disabled {
                        color: rgb(140, 140, 140);
                        background-color: rgb(35, 35, 35);
                    }
                """)
            # Mejorar contraste de títulos de grupos y etiquetas
            for group in self.findChildren(QGroupBox):
                group.setStyleSheet("QGroupBox { color: #FFF; border: none; margin-top: 15px; }")
                layout = group.layout()
                if layout is not None:
                    layout.setContentsMargins(10, 25, 10, 10)  # margen superior igual en todos los modos
            # Etiquetas en blanco
            for label in self.findChildren(QLabel):
                label.setStyleSheet("color: #FFF;")
            # Texto de botones en negro fuerte y normal, sin negrita extra
            for btn in self.findChildren(QPushButton):
                btn.setStyleSheet("QPushButton { color: #000; background-color: #FFF; font-weight: normal; } QPushButton:disabled { color: #888; background-color: #EEE; }")
            # Texto de campos de entrada en blanco
            for widget in self.findChildren(QLineEdit):
                widget.setStyleSheet("QLineEdit { color: #FFF; background-color: rgb(45,45,45); border: 1px solid #AAA; } QLineEdit:disabled { color: #888; background-color: #333; }")
            # ComboBox (interfaz de red) texto negro sobre fondo blanco
            for combo in self.findChildren(QComboBox):
                combo.setStyleSheet("QComboBox { color: #000; background-color: #FFF; border: 1px solid #AAA; } QComboBox QAbstractItemView { color: #000; background: #FFF; }")
            # Área de estado en blanco
            if hasattr(self, 'status_text'):
                self.status_text.setStyleSheet("QTextEdit { color: #FFF; background-color: #181818; border: 1px solid #AAA; }")
            # Separar más el título de grupo de proxy de la opción Habilitar Proxy
            for group in self.findChildren(QGroupBox):
                if 'Proxy' in group.title():
                    layout = group.layout()
                    if layout is not None:
                        layout.setContentsMargins(10, 20, 10, 10)
        else:
            # Modo claro - colores por defecto
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(38, 79, 120))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            palette.setColor(QPalette.PlaceholderText, QColor(128, 128, 128))
            QApplication.setPalette(palette)
            
            # Restaurar estilos personalizados en modo claro
            for group in self.findChildren(QGroupBox):
                group.setStyleSheet("")
                layout = group.layout()
                if layout is not None:
                    layout.setContentsMargins(10, 30, 10, 10)  # margen superior igual en todos los modos
            for label in self.findChildren(QLabel):
                label.setStyleSheet("")
            for btn in self.findChildren(QPushButton):
                btn.setStyleSheet("")
            for widget in self.findChildren(QLineEdit):
                widget.setStyleSheet("")
            for combo in self.findChildren(QComboBox):
                combo.setStyleSheet("")
            if hasattr(self, 'status_text'):
                self.status_text.setStyleSheet("")

    def check_admin_permissions(self):
        """Verifica si la app tiene permisos de administrador/root"""
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except Exception:
            return False

    def show_progress(self, mensaje="Procesando..."):
        """Muestra la barra de progreso y un mensaje opcional"""
        if hasattr(self, 'progress_bar') and self.progress_bar:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(30)
        self.add_status_message(mensaje)

    def hide_progress(self):
        """Oculta la barra de progreso"""
        if hasattr(self, 'progress_bar') and self.progress_bar:
            self.progress_bar.setVisible(False)
            self.progress_bar.setValue(0)

if __name__ == "__main__":
    if not PYQT5_AVAILABLE:
        print("PyQt5 no está instalado. No se puede iniciar la aplicación.")
        sys.exit(1)

    # --- Solicitar permisos de administrador al inicio ---
    def is_admin():
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except Exception:
            return False

    if not is_admin():
        if platform.system() == "Windows":
            import ctypes
            # Relanzar el script con privilegios de administrador
            params = ' '.join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0)
        else:
            print("[ADVERTENCIA] Ejecuta la app como root/sudo para todas las funciones.")
            import time
            time.sleep(2)

    app = QApplication(sys.argv)
    window = TabIP()
    window.show()
    sys.exit(app.exec_())
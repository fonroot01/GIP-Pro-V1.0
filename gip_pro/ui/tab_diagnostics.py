from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QGroupBox, QFormLayout, QLineEdit
from PyQt6.QtCore import Qt

# Pestaña de herramientas de diagnóstico
# Aquí se define la UI de diagnóstico
class DiagnosticsTab(QWidget):
    def __init__(self, network_tools, logger):
        super().__init__()
        self.network_tools = network_tools
        self.logger = logger
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Grupo de pruebas de conectividad
        connectivity_group = QGroupBox("🌐 Pruebas de Conectividad")
        connectivity_layout = QFormLayout(connectivity_group)
        self.ping_input = QLineEdit()
        self.ping_input.setPlaceholderText("8.8.8.8 o dominio...")
        self.ping_btn = QPushButton("Ping")
        self.ping_btn.clicked.connect(self.run_ping)
        self.ping_result = QTextEdit()
        self.ping_result.setReadOnly(True)
        connectivity_layout.addRow("Destino:", self.ping_input)
        connectivity_layout.addRow(self.ping_btn)
        connectivity_layout.addRow("Resultado:", self.ping_result)
        layout.addWidget(connectivity_group)

        # Grupo de traceroute
        traceroute_group = QGroupBox("🛣️ Traceroute")
        traceroute_layout = QFormLayout(traceroute_group)
        self.traceroute_input = QLineEdit()
        self.traceroute_input.setPlaceholderText("8.8.8.8 o dominio...")
        self.traceroute_btn = QPushButton("Traceroute")
        self.traceroute_btn.clicked.connect(self.run_traceroute)
        self.traceroute_result = QTextEdit()
        self.traceroute_result.setReadOnly(True)
        traceroute_layout.addRow("Destino:", self.traceroute_input)
        traceroute_layout.addRow(self.traceroute_btn)
        traceroute_layout.addRow("Resultado:", self.traceroute_result)
        layout.addWidget(traceroute_group)

        # Grupo de consulta DNS
        dns_group = QGroupBox("🔎 Consulta DNS")
        dns_layout = QFormLayout(dns_group)
        self.dns_input = QLineEdit()
        self.dns_input.setPlaceholderText("Dominio...")
        self.dns_btn = QPushButton("Consultar DNS")
        self.dns_btn.clicked.connect(self.run_dns_lookup)
        self.dns_result = QTextEdit()
        self.dns_result.setReadOnly(True)
        dns_layout.addRow("Dominio:", self.dns_input)
        dns_layout.addRow(self.dns_btn)
        dns_layout.addRow("Resultado:", self.dns_result)
        layout.addWidget(dns_group)

        self.setLayout(layout)

    def run_ping(self):
        target = self.ping_input.text()
        if not target:
            self.ping_result.setText("Ingrese un destino válido.")
            return
        success, output = self.network_tools.ping_test(target)
        self.ping_result.setText(output)
        self.logger.log_info(f"Ping a {target}: {'éxito' if success else 'fallo'}")

    def run_traceroute(self):
        target = self.traceroute_input.text()
        if not target:
            self.traceroute_result.setText("Ingrese un destino válido.")
            return
        success, output = self.network_tools.traceroute_test(target)
        self.traceroute_result.setText(output)
        self.logger.log_info(f"Traceroute a {target}: {'éxito' if success else 'fallo'}")

    def run_dns_lookup(self):
        domain = self.dns_input.text()
        if not domain:
            self.dns_result.setText("Ingrese un dominio válido.")
            return
        success, output = self.network_tools.dns_lookup(domain)
        self.dns_result.setText(str(output))
        self.logger.log_info(f"Consulta DNS a {domain}: {'éxito' if success else 'fallo'}")

# Pestaña para manejar perfiles
# Aquí se define la UI de gestión de perfiles

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, 
    QGroupBox, QAbstractItemView, QListWidgetItem, QMessageBox, QFormLayout, 
    QSizePolicy, QFrame, QTextEdit
)
from ..profile_manager import ProfileManager
import json
from datetime import datetime

class TabProfiles(QWidget):
    def __init__(self, network_tools=None, logger=None, parent=None):
        super().__init__(parent)
        self.network_tools = network_tools
        self.logger = logger
        self.profile_manager = ProfileManager()
        self.selected_profile = None
        self.init_ui()
        self.refresh_profiles()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Grupo de perfiles
        group = QGroupBox("📋 Perfiles de Red")
        group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QHBoxLayout(group)
        layout.setSpacing(16)

        # Panel izquierdo: Lista de perfiles
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(8)
        
        # Lista de perfiles
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.list.itemClicked.connect(self.on_profile_selected)
        self.list.setMinimumWidth(250)
        left_layout.addWidget(self.list)

        # Panel derecho: Detalles del perfil
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(12)

        # Detalles del perfil
        details_group = QGroupBox("Detalles del Perfil")
        details_layout = QFormLayout(details_group)
        details_layout.setSpacing(8)

        self.name_label = QLabel("--")
        self.interface_label = QLabel("--")
        self.created_label = QLabel("--")
        self.ip_label = QLabel("--")
        self.mask_label = QLabel("--")
        self.gateway_label = QLabel("--")
        self.dns_label = QLabel("--")

        details_layout.addRow("Nombre:", self.name_label)
        details_layout.addRow("Interfaz:", self.interface_label)
        details_layout.addRow("Creado:", self.created_label)
        details_layout.addRow("IP:", self.ip_label)
        details_layout.addRow("Máscara:", self.mask_label)
        details_layout.addRow("Gateway:", self.gateway_label)
        details_layout.addRow("DNS:", self.dns_label)

        right_layout.addWidget(details_group)

        # Botones de acción
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.apply_btn = QPushButton("✔️ Aplicar")
        self.delete_btn = QPushButton("❌ Eliminar")
        
        for btn in [self.apply_btn, self.delete_btn]:
            btn.setMinimumWidth(120)
            btn.setEnabled(False)
            btn_layout.addWidget(btn)

        right_layout.addLayout(btn_layout)
        right_layout.addStretch()

        # Agregar paneles al layout principal
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        main_layout.addWidget(group)

        # Conectar señales
        self.apply_btn.clicked.connect(self.apply_selected_profile)
        self.delete_btn.clicked.connect(self.delete_selected_profile)

    def refresh_profiles(self):
        """Actualiza la lista de perfiles"""
        self.list.clear()
        profiles = self.profile_manager.get_all_profiles()
        for profile in profiles:
            item = QListWidgetItem(profile.get('name', 'Sin nombre'))
            item.setData(Qt.ItemDataRole.UserRole, profile.get('id'))
            self.list.addItem(item)

    def on_profile_selected(self, item):
        """Maneja la selección de un perfil"""
        profile_id = item.data(Qt.ItemDataRole.UserRole)
        profile = self.profile_manager.get_profile(profile_id)
        
        if profile:
            self.selected_profile = profile
            self.name_label.setText(profile.get('name', '--'))
            self.interface_label.setText(profile.get('interface', '--'))
            
            # Formatear fecha de creación
            created_at = profile.get('created_at', '')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at)
                    created_at = dt.strftime("%d/%m/%Y %H:%M")
                except:
                    pass
            self.created_label.setText(created_at or '--')
            
            self.ip_label.setText(profile.get('ip', '--'))
            self.mask_label.setText(profile.get('mask', '--'))
            self.gateway_label.setText(profile.get('gateway', '--'))
            
            # Formatear DNS
            dns1 = profile.get('dns1', '')
            dns2 = profile.get('dns2', '')
            dns_text = dns1
            if dns2:
                dns_text += f", {dns2}"
            self.dns_label.setText(dns_text or '--')
            
            self.apply_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            self.clear_details()

    def clear_details(self):
        """Limpia los detalles del perfil"""
        self.selected_profile = None
        self.name_label.setText('--')
        self.interface_label.setText('--')
        self.created_label.setText('--')
        self.ip_label.setText('--')
        self.mask_label.setText('--')
        self.gateway_label.setText('--')
        self.dns_label.setText('--')
        self.apply_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

    def apply_selected_profile(self):
        """Aplica el perfil seleccionado"""
        if not self.selected_profile:
            return
            
        if not self.network_tools:
            QMessageBox.warning(
                self,
                "Error",
                "No hay herramientas de red disponibles"
            )
            return
            
        try:
            # Verificar que el método existe antes de usarlo
            if hasattr(self.network_tools, 'set_static_ip'):
                # Aplicar configuración IP usando el método correcto
                success = self.network_tools.set_static_ip(
                    self.selected_profile['interface'],
                    self.selected_profile['ip'],
                    self.selected_profile['mask'],
                    self.selected_profile.get('gateway', '')
                )
                
                if not success:
                    raise Exception("No se pudo configurar la IP estática")
                    
            elif hasattr(self.network_tools, 'configure_static_ip'):
                # Método alternativo si existe
                success = self.network_tools.configure_static_ip(
                    interface=self.selected_profile['interface'],
                    ip_address=self.selected_profile['ip'],
                    subnet_mask=self.selected_profile['mask'],
                    gateway=self.selected_profile.get('gateway', '')
                )
                
                if not success:
                    raise Exception("No se pudo configurar la IP estática")
            else:
                raise Exception("Método de configuración de IP no disponible")
            
            # Aplicar DNS si están configurados y el método existe
            dns1 = self.selected_profile.get('dns1')
            dns2 = self.selected_profile.get('dns2')
            
            if dns1 and hasattr(self.network_tools, 'configure_dns'):
                dns_servers = [dns1]
                if dns2:
                    dns_servers.append(dns2)
                    
                dns_success = self.network_tools.configure_dns(
                    self.selected_profile['interface'],
                    dns_servers
                )
                
                if not dns_success:
                    print(f"Advertencia: No se pudieron configurar los DNS")
                    
            QMessageBox.information(
                self,
                "Perfil aplicado",
                f"Perfil '{self.selected_profile['name']}' aplicado correctamente"
            )
            
            if self.logger:
                self.logger.log_connection_event(
                    'profile_applied',
                    f"Perfil '{self.selected_profile['name']}' aplicado",
                    True
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al aplicar el perfil: {str(e)}"
            )
            
            if self.logger:
                self.logger.log_connection_event(
                    'profile_applied',
                    f"Error al aplicar perfil: {str(e)}",
                    False
                )

    def delete_selected_profile(self):
        """Elimina el perfil seleccionado"""
        if not self.selected_profile:
            return
            
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el perfil '{self.selected_profile['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.profile_manager.delete_profile(self.selected_profile['id']):
                self.refresh_profiles()
                self.clear_details()
                
                if self.logger:
                    self.logger.log_connection_event(
                        'profile_deleted',
                        f"Perfil '{self.selected_profile['name']}' eliminado",
                        True
                    )
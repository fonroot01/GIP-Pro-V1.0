# Gestión de perfiles de red (guardar/cargar)

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

PROFILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'profiles.json')

class ProfileManager:
    def __init__(self):
        self.profiles: List[Dict] = []
        self.load_profiles()

    def load_profiles(self) -> None:
        """Carga los perfiles desde el archivo"""
        try:
            if os.path.exists(PROFILE_PATH):
                with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.profiles = data.get('profiles', [])
        except Exception as e:
            print(f"Error al cargar perfiles: {str(e)}")
            self.profiles = []

    def save_profiles(self) -> None:
        """Guarda los perfiles en el archivo"""
        try:
            os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
            with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
                json.dump({'profiles': self.profiles}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar perfiles: {str(e)}")

    def add_profile(self, profile: Dict) -> bool:
        """
        Agrega un nuevo perfil
        
        Args:
            profile: Diccionario con los datos del perfil
            
        Returns:
            bool: True si se agregó correctamente
        """
        try:
            # Agregar campos adicionales
            profile['created_at'] = datetime.now().isoformat()
            profile['id'] = len(self.profiles)
            profile['name'] = self.generate_profile_name(profile)
            
            self.profiles.append(profile)
            self.save_profiles()
            return True
        except Exception:
            return False

    def delete_profile(self, profile_id: int) -> bool:
        """
        Elimina un perfil por su ID
        
        Args:
            profile_id: ID del perfil a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            self.profiles = [p for p in self.profiles if p.get('id') != profile_id]
            self.save_profiles()
            return True
        except Exception:
            return False

    def get_profile(self, profile_id: int) -> Optional[Dict]:
        """
        Obtiene un perfil por su ID
        
        Args:
            profile_id: ID del perfil
            
        Returns:
            Dict o None: Datos del perfil o None si no existe
        """
        try:
            return next((p for p in self.profiles if p.get('id') == profile_id), None)
        except Exception:
            return None

    def get_all_profiles(self) -> List[Dict]:
        """
        Obtiene todos los perfiles
        
        Returns:
            List[Dict]: Lista de perfiles
        """
        return self.profiles

    def generate_profile_name(self, profile: Dict) -> str:
        """
        Genera un nombre descriptivo para el perfil
        
        Args:
            profile: Datos del perfil
            
        Returns:
            str: Nombre generado
        """
        interface = profile.get('interface', '')
        ip = profile.get('ip', '')
        if not ip:
            return f"{interface} - DHCP"
        return f"{interface} - {ip}"

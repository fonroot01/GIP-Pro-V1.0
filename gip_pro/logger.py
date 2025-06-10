# Registro de eventos, historial o errores
import os
from datetime import datetime
from typing import List, Optional
import json

LOG_PATH = os.path.join(os.path.dirname(__file__), 'data', 'logs.txt')
LOG_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'data', 'log_config.json')

class NetworkLogger:
    def __init__(self):
        self.log_entries: List[dict] = []
        self.max_entries = 100  # Máximo número de entradas en memoria
        self.load_config()
        self.load_logs()
    
    def load_config(self):
        """Carga la configuración del logger"""
        try:
            if os.path.exists(LOG_CONFIG_PATH):
                with open(LOG_CONFIG_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.max_entries = config.get('max_entries', 100)
        except Exception:
            pass

    def save_config(self):
        """Guarda la configuración del logger"""
        try:
            os.makedirs(os.path.dirname(LOG_CONFIG_PATH), exist_ok=True)
            with open(LOG_CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump({'max_entries': self.max_entries}, f)
        except Exception:
            pass

    def load_logs(self):
        """Carga los logs existentes"""
        try:
            if os.path.exists(LOG_PATH):
                with open(LOG_PATH, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            self.log_entries.append(entry)
                        except:
                            continue
                # Mantener solo las últimas max_entries
                self.log_entries = self.log_entries[-self.max_entries:]
        except Exception:
            pass

    def save_logs(self):
        """Guarda los logs en disco"""
        try:
            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
            with open(LOG_PATH, 'w', encoding='utf-8') as f:
                for entry in self.log_entries:
                    f.write(json.dumps(entry) + '\n')
        except Exception:
            pass

    def log_connection_event(self, event_type: str, details: str, success: bool = True):
        """
        Registra un evento de conexión
        
        Args:
            event_type: Tipo de evento (ip_change, dns_change, dhcp, test, etc)
            details: Detalles del evento
            success: Si el evento fue exitoso
        """
        timestamp = datetime.now().isoformat()
        entry = {
            'timestamp': timestamp,
            'type': event_type,
            'details': details,
            'success': success
        }
        
        self.log_entries.append(entry)
        if len(self.log_entries) > self.max_entries:
            self.log_entries.pop(0)
        
        self.save_logs()

    def get_recent_logs(self, limit: Optional[int] = None) -> List[dict]:
        """
        Obtiene los logs más recientes
        
        Args:
            limit: Número máximo de logs a retornar
            
        Returns:
            Lista de los últimos eventos registrados
        """
        if limit is None or limit > len(self.log_entries):
            return self.log_entries
        return self.log_entries[-limit:]

    def clear_logs(self):
        """Limpia todos los logs"""
        self.log_entries.clear()
        self.save_logs()

# Alias para mantener compatibilidad
Logger = NetworkLogger

# Lógica de cambio IP, DNS, diagnóstico, etc.
import platform
import subprocess
import os

class NetworkTools:
    def __init__(self, logger=None):
        self.logger = logger
        self.system = platform.system()
    
    def is_admin(self):
        if self.system == 'Windows':
            import ctypes
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception:
                return False
        else:
            try:
                import os
                geteuid = getattr(os, 'geteuid', None)
                if callable(geteuid):
                    return geteuid() == 0
                return False
            except Exception:
                return False

    def change_ip(self, interface, ip, mask, gateway):
        if not self.is_admin():
            raise PermissionError('Se requieren privilegios de administrador para cambiar la IP.')
            
        if self.system == 'Windows':
            cmd = f'netsh interface ip set address name="{interface}" static {ip} {mask if mask else "255.255.255.0"} {gateway if gateway else ""}'
            subprocess.run(cmd, shell=True, check=True)
        elif self.system == 'Linux':
            cmd = f'nmcli con mod "{interface}" ipv4.addresses {ip}/{mask if mask else "24"}'
            subprocess.run(cmd, shell=True, check=True)
            if gateway:
                subprocess.run(f'nmcli con mod "{interface}" ipv4.gateway {gateway}', shell=True, check=True)
            subprocess.run(f'nmcli con mod "{interface}" ipv4.method manual', shell=True, check=True)
            subprocess.run(f'nmcli con up "{interface}"', shell=True, check=True)
        else:
            raise NotImplementedError('Solo implementado para Windows y Linux')
        
        if self.logger:
            self.logger.log_event('change_ip', {'interface': interface, 'ip': ip, 'mask': mask, 'gateway': gateway})

    def set_dns(self, interface, dns1, dns2=None):
        if not self.is_admin():
            raise PermissionError('Se requieren privilegios de administrador para cambiar DNS.')
            
        if self.system == 'Windows':
            subprocess.run(f'netsh interface ip set dns name="{interface}" static {dns1}', shell=True, check=True)
            if dns2:
                subprocess.run(f'netsh interface ip add dns name="{interface}" {dns2} index=2', shell=True, check=True)
        elif self.system == 'Linux':
            dns = dns1
            if dns2:
                dns += f',{dns2}'
            subprocess.run(f'nmcli con mod "{interface}" ipv4.dns "{dns}"', shell=True, check=True)
            subprocess.run(f'nmcli con up "{interface}"', shell=True, check=True)
        else:
            raise NotImplementedError('Solo implementado para Windows y Linux')
            
        if self.logger:
            self.logger.log_event('set_dns', {'interface': interface, 'dns1': dns1, 'dns2': dns2})

    def restore_dhcp(self, interface):
        if not self.is_admin():
            raise PermissionError('Se requieren privilegios de administrador para restaurar DHCP.')
            
        if self.system == 'Windows':
            subprocess.run(f'netsh interface ip set address name="{interface}" source=dhcp', shell=True, check=True)
            subprocess.run(f'netsh interface ip set dns name="{interface}" source=dhcp', shell=True, check=True)
        elif self.system == 'Linux':
            subprocess.run(f'nmcli con mod "{interface}" ipv4.method auto', shell=True, check=True)
            subprocess.run(f'nmcli con up "{interface}"', shell=True, check=True)
        else:
            raise NotImplementedError('Solo implementado para Windows y Linux')
            
        if self.logger:
            self.logger.log_event('restore_dhcp', {'interface': interface})

    def set_proxy(self, interface, proxy_address, proxy_port, proxy_type='http', username=None, password=None):
        if not self.is_admin():
            raise PermissionError('Se requieren privilegios de administrador para configurar el proxy.')
            
        if self.system == 'Windows':
            cmd = f'netsh winhttp set proxy {proxy_address}:{proxy_port}'
            subprocess.run(cmd, shell=True)
        elif self.system == 'Linux':
            os.environ['http_proxy'] = f'http://{proxy_address}:{proxy_port}'
            os.environ['https_proxy'] = f'https://{proxy_address}:{proxy_port}'
        else:
            raise NotImplementedError('Sistema operativo no soportado para proxy')
            
        if self.logger:
            self.logger.log_event('set_proxy', {
                'interface': interface,
                'proxy_address': proxy_address,
                'proxy_port': proxy_port,
                'proxy_type': proxy_type
            })
        return True

    def get_os(self):
        """Obtiene el nombre del sistema operativo."""
        if self.system == 'Windows':
            try:
                release = platform.win32_ver()[0]
                return f"Windows {release}"
            except:
                return "Windows"
        elif self.system == 'Linux':
            try:
                return f"Linux {platform.linux_distribution()[0]}"
            except:
                return "Linux"
        else:
            return self.system

    def ping_test(self, target, count=4):
        """Realiza una prueba de ping al destino especificado."""
        try:
            if self.system == 'Windows':
                command = f'ping -n {count} {target}'
            else:
                command = f'ping -c {count} {target}'
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            success = result.returncode == 0
            
            if self.logger:
                self.logger.log_event('ping_test', {'target': target, 'success': success})
            
            return success, result.stdout
        except Exception as e:
            if self.logger:
                self.logger.log_error('ping_test', str(e))
            return False, str(e)

    def get_active_interfaces(self):
        """Obtiene la lista de interfaces de red activas."""
        try:
            import netifaces
            interfaces = []
            for iface in netifaces.interfaces():
                try:
                    if netifaces.ifaddresses(iface).get(netifaces.AF_INET):
                        interfaces.append(iface)
                except:
                    continue
            return interfaces if interfaces else ["Ethernet", "Wi-Fi"]
        except ImportError:
            if self.system == 'Windows':
                try:
                    output = subprocess.check_output('netsh interface show interface', shell=True, text=True)
                    interfaces = []
                    for line in output.split('\n'):
                        if 'Enabled' in line:
                            iface = line.split()[-1]
                            interfaces.append(iface)
                    return interfaces if interfaces else ["Ethernet", "Wi-Fi"]
                except:
                    return ["Ethernet", "Wi-Fi"]
            else:
                try:
                    output = subprocess.check_output('ip link show', shell=True, text=True)
                    interfaces = []
                    for line in output.split('\n'):
                        if ':' in line and 'lo:' not in line:
                            iface = line.split(':')[1].strip()
                            interfaces.append(iface)
                    return interfaces if interfaces else ["eth0", "wlan0"]
                except:
                    return ["eth0", "wlan0"]

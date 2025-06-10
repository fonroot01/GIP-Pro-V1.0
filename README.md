# GIP Pro v1.0

![GIP Pro](https://img.shields.io/badge/version-1.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)

**GIP Pro** es una aplicación de escritorio multiplataforma para la configuración avanzada de redes en sistemas Windows, Linux y macOS. Permite gestionar de manera gráfica y sencilla la configuración de interfaces de red, servidores DNS y configuraciones de proxy.

## 🚀 Características

### Configuración de Red
- **Gestión de Interfaces**: Soporte para Wi-Fi, Ethernet y otras interfaces de red
- **Configuración IP**: Asignación automática (DHCP) o manual de direcciones IP
- **Máscara de Subred**: Configuración personalizada de máscaras de red
- **Gateway**: Configuración de puerta de enlace predeterminada
- **DNS Personalizado**: Configuración de servidores DNS primario y secundario

### Proveedores DNS Preconfigurados
- **Google DNS** (8.8.8.8 / 8.8.4.4)
- **Cloudflare DNS** (1.1.1.1 / 1.0.0.1)
- **OpenDNS** (208.67.222.222 / 208.67.220.220)

### Configuración de Proxy
- **Habilitar/Deshabilitar Proxy**: Control completo del proxy del sistema
- **Servidor Proxy**: Configuración de servidor personalizado
- **Puerto**: Especificación de puerto personalizado
- **Probar Proxy**: Validación de configuración de proxy

### Herramientas de Red
- **Aplicar Configuración**: Aplicación inmediata de cambios
- **DHCP**: Obtención automática de configuración de red
- **Guardar Perfil**: Persistencia de configuraciones
- **Diagnósticos**: Herramientas para probar conectividad

## 📋 Requisitos del Sistema

- **Windows**: Windows 10/11 o superior
- **Linux**: Ubuntu 18.04+, Debian 10+, CentOS 7+, Arch Linux
- **macOS**: macOS 10.14 (Mojave) o superior
- **Permisos**: Administrador/Root/Sudo (requerido para cambios de red)
- **Memoria RAM**: Mínimo 2GB
- **Espacio en Disco**: 50MB libres

## 🛠️ Instalación

### Windows
1. Descarga el archivo `.exe` desde [Releases](https://github.com/fonroot01/GIP-Pro-V1.0/releases)
2. Ejecuta el instalador (se ejecutará automáticamente como administrador)
3. Sigue las instrucciones del asistente de instalación
4. Inicia la aplicación desde el menú de inicio

### Linux

#### Ubuntu/Debian
```bash
# Descarga el paquete .deb
wget https://github.com/fonroot01/GIP-Pro-V1.0/releases/latest/download/gip-pro.deb

# Instala el paquete
sudo dpkg -i gip-pro.deb

# Instala dependencias si es necesario
sudo apt-get install -f
```

#### Instalación desde Cualquier distribución
```bash
git clone https://github.com/fonroot01/GIP-Pro-V1.0.git
cd GIP-Pro-V1.0
chmod +x install.sh
sudo ./install.sh
```

### macOS

#### Usando Homebrew (Recomendado)
```bash
# Añade el tap personalizado
brew tap fonroot01/gip-pro

# Instala GIP Pro
brew install gip-pro
```

#### Instalación Manual
1. Descarga el archivo `.dmg` desde [Releases](https://github.com/fonroot01/GIP-Pro-V1.0/releases)
2. Abre el archivo `.dmg`
3. Arrastra GIP Pro a la carpeta Aplicaciones
4. Ejecuta desde Launchpad o Finder

#### Instalación desde código fuente
```bash
git clone https://github.com/fonroot01/GIP-Pro-V1.0.git
cd GIP-Pro-V1.0
chmod +x install-macos.sh
sudo ./install-macos.sh
```
### Interfaz Gráfica 
![Interfaz de GIP Pro](https://github.com/user-attachments/assets/788f39b0-348a-499e-b656-b7a434fde962)




## 💻 Uso

### Configuración Básica de Red

1. **Seleccionar Interfaz**: Elige la interfaz de red (Wi-Fi, Ethernet, etc.)
2. **Configurar IP**: 
   - Automático: Marca "Auto" para DHCP
   - Manual: Ingresa la dirección IP deseada
3. **Establecer Máscara**: Define la máscara de subred (ej: 255.255.255.0)
4. **Configurar Gateway**: Especifica la puerta de enlace
5. **Aplicar Cambios**: Haz clic en "Aplicar IP"

> **Nota**: En Linux y macOS es necesario ejecutar la aplicación con permisos de administrador (`sudo`) para realizar cambios en la configuración de red.

### Configuración de DNS

1. Selecciona un proveedor preconfigurado (Google, Cloudflare, OpenDNS)
2. O configura servidores DNS personalizados:
   - **DNS Primario**: Servidor DNS principal
   - **DNS Secundario**: Servidor DNS de respaldo

### Configuración de Proxy

1. Marca "Habilitar Proxy"
2. Ingresa la dirección del **Servidor**
3. Especifica el **Puerto**
4. Haz clic en "Probar Proxy" para verificar la conexión

## 🔧 Funcionalidades Avanzadas

### Perfiles de Red
- Guarda múltiples configuraciones de red
- Cambio rápido entre perfiles
- Exportación e importación de configuraciones

### Diagnósticos
- **Probar Conexión**: Verifica la conectividad a Internet
- **Información de Red**: Muestra detalles de la configuración actual
- **Estado del Proxy**: Monitorea el estado de la conexión proxy

## 🐛 Solución de Problemas

### Problemas Comunes

**La aplicación no inicia**
- **Windows**: Ejecutar como administrador
- **Linux/macOS**: Ejecutar con `sudo` o verificar permisos
- Verificar compatibilidad del sistema

**No se pueden aplicar cambios de red**
- Confirmar permisos de administrador/sudo
- **Windows**: Verificar configuración de firewall
- **Linux**: Verificar que NetworkManager esté activo
- **macOS**: Verificar permisos de red en Preferencias del Sistema

**Dependencias faltantes (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install network-manager python3-gi gir1.2-gtk-3.0

# CentOS/RHEL/Fedora
sudo dnf install NetworkManager python3-gobject gtk3-devel

# Arch Linux
sudo pacman -S networkmanager python-gobject gtk3
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Alfonso Mosquera**
- GitHub: [@fonroot01](https://github.com/fonroot01)
- LinkedIn: [Alfonso Ángel Mosquera A.](https://www.linkedin.com/in/alfonso-%C3%A1ngel-mosquera-a-4a919b341/)
- Email: alfomosque22@gmail.com
- Donaciones: [PayPal](https://www.paypal.com/paypalme/alfomosque22)

## 🔗 Enlaces del Repositorio

```bash
# HTTPS
git clone https://github.com/fonroot01/GIP-Pro-V1.0.git

# SSH
git clone git@github.com:fonroot01/GIP-Pro-V1.0.git

# GitHub CLI
gh repo clone fonroot01/GIP-Pro-V1.0
```

---
<div align="center">
  <p>⭐ Si este proyecto te fue útil, no olvides darle una estrella. ¡Saludos desde Colombia! 🇨🇴</p>
</div>

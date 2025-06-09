# GIP Pro v1.0

![GIP Pro](https://img.shields.io/badge/version-1.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)

**GIP Pro** es una aplicación de escritorio multiplataforma para la configuración avanzada de redes en sistemas Windows y Linux. Permite gestionar de manera grafica y sencilla la configuración de interfaces de red, servidores DNS y configuraciones de proxy.

## 🚀 Características

### Configuración de Red
- **Gestión de Interfaces**: Soporte para Wi-Fi y otras interfaces de red
- **Configuración IP**: Asignación automática o manual de direcciones IP
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

### Herramientas de Red
- **Aplicar Configuración**: Aplicación inmediata de cambios
- **DHCP**: Obtención automática de configuración de red
- **Guardar Perfil**: Persistencia de configuraciones
- **Probar Proxy**: Validación de configuración de proxy

## 📋 Requisitos del Sistema

- **Sistema Operativo**: Windows 10/11 o Linux (Ubuntu 18.04+, Debian 10+, CentOS 7+, Arch Linux)
- **Permisos**: Administrador/Root (requerido para cambios de red)
- **Memoria RAM**: Mínimo 2GB
- **Espacio en Disco**: 50MB libres

## 🛠️ Instalación

### Windows
1. Ejecuta el .exe de GIP Pro que te pedira ejecutarse automáticamente como administrador
2. Sigue las instrucciones del asistente de instalación
3. Inicia la aplicación desde el menú de inicio

### Linux

#### Ubuntu/Debian
```bash
# Descarga el paquete .deb
wget https://github.com/fonroot/gip-pro/releases/latest/download/gip-pro.deb

# Instala el paquete
sudo dpkg -i gip-pro.deb

# Instala dependencias si es necesario
sudo apt-get install -f
```

#### Arch Linux
```bash
# Descarga e instala desde AUR
yay -S gip-pro

# O manualmente
git clone https://aur.archlinux.org/gip-pro.git
cd gip-pro
makepkg -si
```

#### CentOS/RHEL/Fedora
```bash
# Descarga el paquete .rpm
wget https://github.com/fonroot01/gip-pro/releases/latest/download/gip-pro.rpm

# Instala el paquete
sudo rpm -i gip-pro.rpm

# O usando dnf/yum
sudo dnf install gip-pro.rpm
```

#### Instalación desde código fuente
```bash
git clone [https://github.com/fonroot01/GIP-Pro-V1.0.git]
cd gip-pro
chmod +x install.sh
sudo ./install.sh
```

## 💻 Uso

### Configuración Básica de Red

1. **Seleccionar Interfaz**: Elige la interfaz de red (Wi-Fi, Ethernet, etc.)
2. **Configurar IP**: 
   - Automático: Marca "Auto" para DHCP
   - Manual: Ingresa la dirección IP deseada
3. **Establecer Máscara**: Define la máscara de subred (ej: 255.255.255.0)
4. **Configurar Gateway**: Especifica la puerta de enlace
5. **Aplicar Cambios**: Haz clic en "Aplicar IP"

> **Nota para Linux**: Es posible que necesites ejecutar la aplicación con `sudo` para realizar cambios en la configuración de red.

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
- **Linux**: Ejecutar con `sudo` o verificar permisos
- Verificar compatibilidad del sistema

**No se pueden aplicar cambios de red**
- **Windows**: Confirmar permisos de administrador
- **Linux**: Usar `sudo gip-pro` o verificar permisos de NetworkManager
- Verificar que la interfaz de red esté activa

**Problemas de conectividad**
- Usar "Probar Conexión" para diagnosticar
- **Windows**: Verificar configuración de firewall
- **Linux**: Revisar configuración de iptables/ufw

**Dependencias faltantes (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install network-manager python3-gi gir1.2-gtk-3.0

# CentOS/RHEL
sudo yum install NetworkManager python3-gobject gtk3-devel

# Arch Linux
sudo pacman -S networkmanager python-gobject gtk3
```

## 📝 Registro de Cambios

### v1.0.0
- Lanzamiento inicial
- Configuración básica de red
- Soporte para DNS personalizado
- Gestión de proxy
- Interfaz de usuario moderna

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia Apache 2.0. Ver el archivo [LICENSE](LICENSE) para más detalles.

### Términos principales de la Licencia Apache 2.0:
- ✅ **Uso comercial** permitido
- ✅ **Modificación** permitida
- ✅ **Distribución** permitida
- ✅ **Uso privado** permitido
- ✅ **Uso de patentes** garantizado
- ❗ **Incluir licencia y copyright** en distribuciones
- ❗ **Incluir notificación de cambios** si se modifica

## 👨‍💻 Autor

**Alfonso Mosquera**
- Si esta herramienta te ha sido útil y quieres apoyar su desarrollo, puedes hacer una donación vía PayPal: [Donar con PayPal](https://www.paypal.com/paypalme/alfomosque22/5)
- Linkedin: https://www.linkedin.com/in/alfonso-%C3%A1ngel-mosquera-a-4a919b341/
- Email: alfomosque22@gmail.com

Tu apoyo me motiva a seguir desarrollando herramientas útiles y gratuitas. ¡Gracias! 🙌

## 🙏 Agradecimientos

- Inspirado en herramientas de administración de red
- Gracias a la comunidad de desarrolladores por el feedback
- Iconos por [Lucide Icons](https://lucide.dev/)
---
<div align="center">
  <p>⭐ Si este proyecto te fue útil, no olvides regalarme un estrella, saludos desde Colombia panita. 🇨🇴 </p>
</div>

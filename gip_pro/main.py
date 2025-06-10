# filepath: c:\PROYECTOS_Python\GIP Pro\gip_pro\main.py
import sys
import platform
from PyQt6.QtWidgets import QApplication
from gip_pro.ui.main_window import MainWindow

def ensure_admin():
    if platform.system() == "Windows":
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print("[INFO] Solicitando permisos de administrador...")
                executable = sys.executable
                module = "-m gip_pro.main"
                params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
                cmd = f'{module} {params}'
                print(f"[DEBUG] Lanzando como admin (modulo): {executable} {cmd}")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, cmd, None, 1)
                sys.exit(0)
        except Exception as e:
            print(f"[ERROR] No se pudo solicitar permisos de administrador: {e}")

def main():
    ensure_admin()
    app = QApplication(sys.argv)
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        import traceback
        print(f"[ERROR] Error al iniciar la aplicación: {e}")
        traceback.print_exc()
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Error crítico", f"No se pudo iniciar la aplicación:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

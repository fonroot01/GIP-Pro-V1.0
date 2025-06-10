# Vista modo compacto
# Aquí se define la UI para el modo compacto

from PyQt6.QtWidgets import QApplication

def get_dark_style():
    """Retorna el estilo oscuro completo"""
    return '''
    QMainWindow {
        background: #1a1a1a;
    }

    #centralWidget {
        background: #1a1a1a;
    }

    QLabel, QPushButton {
        color: #ffffff;
    }

    QPushButton[class="title"] {
        font-family: "Segoe UI", sans-serif;
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        border: none;
        background: transparent;
        text-align: left;
        padding: 0;
        margin: 0;
    }

    QGroupBox {
        border: 1px solid #333333;
        border-radius: 6px;
        background: #242424;
        margin-top: 8px;
        font-weight: bold;
        padding: 10px;
    }

    QGroupBox::title {
        color: #ffffff;
        padding: 0 8px;
        subcontrol-origin: margin;
        subcontrol-position: top left;
    }

    QLineEdit, QComboBox {
        color: #ffffff;
        background: #2a2a2a;
        border: 1px solid #333333;
        border-radius: 4px;
        padding: 8px 12px;
        min-height: 20px;
    }

    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #007acc;
    }

    QComboBox::drop-down {
        border: none;
        background: #2a2a2a;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #ffffff;
        margin-right: 10px;
    }

    QPushButton {
        background: #007acc;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 12px;
        min-height: 20px;
        font-weight: bold;
    }

    QPushButton:hover {
        background: #0098ff;
    }

    QPushButton:pressed {
        background: #005a9e;
    }

    QPushButton[flat="true"] {
        background: transparent;
        color: #ffffff;
        border: 1px solid #333333;
    }

    QPushButton[flat="true"]:hover {
        background: rgba(255, 255, 255, 30);
    }

    QTextEdit {
        color: #ffffff;
        background: #2a2a2a;
        border: 1px solid #333333;
        border-radius: 4px;
        padding: 8px;
    }

    QTabWidget::pane {
        border: 1px solid #333333;
        background: #242424;
    }

    QTabBar::tab {
        background: #2a2a2a;
        color: #ffffff;
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }

    QTabBar::tab:selected {
        background: #007acc;
    }

    QTabBar::tab:hover:!selected {
        background: #333333;
    }
    '''

def get_light_style():
    """Retorna el estilo claro completo"""
    return '''
    QMainWindow {
        background: #f5f5f5;
    }

    #centralWidget {
        background: #f5f5f5;
    }

    QLabel, QPushButton {
        color: #000000;
    }

    QPushButton[class="title"] {
        font-family: "Segoe UI", sans-serif;
        font-size: 18px;
        font-weight: bold;
        color: #000000;
        border: none;
        background: transparent;
        text-align: left;
        padding: 0;
        margin: 0;
    }

    QGroupBox {
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        background: #ffffff;
        margin-top: 8px;
        font-weight: bold;
        padding: 10px;
    }

    QGroupBox::title {
        color: #000000;
        padding: 0 8px;
        subcontrol-origin: margin;
        subcontrol-position: top left;
    }

    QLineEdit, QComboBox {
        color: #000000;
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 8px 12px;
        min-height: 20px;
    }

    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #007acc;
    }

    QComboBox::drop-down {
        border: none;
        background: #ffffff;
    }

    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #000000;
        margin-right: 10px;
    }

    QPushButton {
        background: #007acc;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 12px;
        min-height: 20px;
        font-weight: bold;
    }

    QPushButton:hover {
        background: #0098ff;
    }

    QPushButton:pressed {
        background: #005a9e;
    }

    QPushButton[flat="true"] {
        background: transparent;
        color: #000000;
        border: 1px solid #e0e0e0;
    }

    QPushButton[flat="true"]:hover {
        background: rgba(0, 0, 0, 13);
    }

    QTextEdit {
        color: #000000;
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        padding: 8px;
    }

    QTabWidget::pane {
        border: 1px solid #e0e0e0;
        background: #ffffff;
    }

    QTabBar::tab {
        background: #f0f0f0;
        color: #000000;
        padding: 8px 16px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }

    QTabBar::tab:selected {
        background: #007acc;
        color: white;
    }

    QTabBar::tab:hover:!selected {
        background: #e0e0e0;
    }
    '''

def apply_compact_style(app: QApplication, dark: bool = True):
    """Aplica el estilo compacto a la aplicación"""
    if not isinstance(app, QApplication):
        return
        
    # Aplicar el estilo correspondiente
    if dark:
        app.setStyleSheet(get_dark_style())
    else:
        app.setStyleSheet(get_light_style())
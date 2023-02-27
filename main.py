# =============================================================================
# Freezer 1.0.0
# Created by Dmitry Obydennov
# Date: 27/02/2023
# =============================================================================

import os
import sys
import psutil
import keyboard
import qdarktheme

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QColor
from configparser import ConfigParser

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем конфигурационный файл, если его нет
        if not os.path.exists('config.ini'):
            with open('config.ini', 'w') as f:
                f.write('[Settings]\nHotkey = Ctrl+Alt+F')

        # Считываем конфигурационный файл
        self.config = ConfigParser()
        self.config.read('config.ini')

        # Находим процесс explorer.exe
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'explorer.exe':
                self.explorer_pid = proc.info['pid']
                break

        # Изначально заморозка отключена
        self.frozen = False

        # Создаем виджеты
        self.info_label = QLabel('Проводник разморожен!')
        self.info_label.setStyleSheet('color: #4caf50')
        #self.hotkey_label = QLabel('Комбинация клавиш: ' + self.config.get('Settings', 'Hotkey'))
        self.hotkey_label = QLabel('Комбинация клавиш: <font color="#f4c65f">' + self.config.get('Settings', 'Hotkey') + '</font>')
        self.toggle_button = QPushButton('Заморозить')

        # Добавляем обработчик нажатия на кнопку
        self.toggle_button.clicked.connect(self.toggle_freeze)

        # Создаем макет и добавляем виджеты
        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addWidget(self.hotkey_label)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)

        # Регистрируем обработчик нажатия клавиш
        keyboard.add_hotkey(self.config.get('Settings', 'Hotkey'), self.toggle_freeze, suppress=True)

    # Функция для замораживания и размораживания процесса
    def toggle_freeze(self):
        if self.frozen:
            psutil.Process(self.explorer_pid).resume()
            self.frozen = False
            self.info_label.setText('Проводник разморожен!')
            self.info_label.setStyleSheet('color: #4caf50')
            self.toggle_button.setText('Заморозить')
        else:
            psutil.Process(self.explorer_pid).suspend()
            self.frozen = True
            self.info_label.setText('Проводник заморожен!')
            self.info_label.setStyleSheet('color: #1a73e8')
            self.toggle_button.setText('Разморозить')

    # При закрытии окна отключаем горячие клавиши
    def closeEvent(self, event):
        keyboard.clear_all_hotkeys()


if __name__ == '__main__':
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    app.setApplicationName("Freezer")
    qdarktheme.setup_theme("auto")
    window = Window()
    window.show()
    sys.exit(app.exec_())
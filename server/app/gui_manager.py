# app/gui_manager.py
import webview
import threading
from .config import HTML_CONTENT
from .tray import run_tray

class GUIManager:
    def __init__(self, server_stopper):
        self.window = None
        self.server_stopper = server_stopper
        self.tray_active = False

    def create_window(self):
        self.window = webview.create_window(
            title="Сервер",
            html=HTML_CONTENT,
            width=420,
            height=320,
            resizable=False,
            confirm_close=False
        )
        
        self.window.events.minimized += self.on_minimized
        self.window.events.restored += self.on_restored
        return self.window

    def update_status(self, status):
        # Эта функция вызывается из потока сервера, pywebview thread-safe для evaluate_js
        if self.window:
            # Экранируем статус на всякий случай
            safe_status = status.replace("'", "\\'")
            self.window.evaluate_js(f"document.getElementById('status').innerText = 'Статус: {safe_status}'")

    def on_minimized(self):
        if not self.tray_active:
            self.window.hide()
            self.tray_active = True
            # Запускаем трей в отдельном потоке, так как он блокирующий
            threading.Thread(
                target=run_tray, 
                args=(self.window, self.server_stopper), 
                daemon=True
            ).start()

    def on_restored(self):
        # Когда окно восстанавливается (через логику трея window.show()), 
        # трей сам останавливается внутри своей функции show_window
        self.tray_active = False

    def start(self):
        webview.start(debug=False)
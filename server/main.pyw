# main.py
import threading
import sys
import tkinter as tk
from tkinter import messagebox

from app.utils import check_internet, is_port_free
from app.server import WebSocketServer
from app.gui_manager import GUIManager
from app.config import PORT

def main():
    # 1. Предварительные проверки
    if not check_internet():
        show_error("Нет интернета. Программа не может быть запущена.")
        sys.exit(1)

    if not is_port_free(PORT):
        show_error(f"Порт {PORT} занят.")
        sys.exit(1)

    # 2. Инициализация компонентов
    # Нам нужно создать GUI менеджер заранее, чтобы передать callback обновления статуса серверу
    # Но окно создадим чуть позже
    
    server = None
    
    def stop_server_wrapper():
        if server:
            server.stop()

    gui = GUIManager(server_stopper=stop_server_wrapper)
    
    # Callback для сервера, чтобы обновлять UI
    def update_ui_status(text):
        gui.update_status(text)

    server = WebSocketServer(status_callback=update_ui_status)

    # 3. Запуск сервера в отдельном потоке
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    # 4. Создание и запуск окна (блокирует основной поток)
    gui.create_window()
    gui.start()

def show_error(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка", message)
    root.destroy()

if __name__ == "__main__":
    main()
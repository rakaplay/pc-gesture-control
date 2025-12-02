# app/tray.py
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item
import sys

def create_tray_icon_image():
    image = Image.new('RGB', (32, 32), color='black')
    draw = ImageDraw.Draw(image)
    # Используем встроенный шрифт или загружаем
    try:
        font = ImageFont.load_default()
    except:
        font = None
    draw.text((10, 8), "S", font=font, fill='white')
    return image

def run_tray(window, server_stopper_func):
    """
    Запускает трей. Блокирующая функция (запускать в потоке).
    """
    def show_window(icon):
        icon.stop()
        window.show()

    def quit_app(icon):
        icon.stop()
        if server_stopper_func:
            server_stopper_func()
        window.destroy()
        sys.exit(0)

    icon = pystray.Icon(
        "LocalServer",
        create_tray_icon_image(),
        "Локальный сервер",
        menu=pystray.Menu(
            item('Показать', show_window),
            item('Выход', quit_app)
        )
    )
    icon.run()
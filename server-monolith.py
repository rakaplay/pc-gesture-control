import asyncio
import websockets
import pyautogui
import json
import time
import threading
import webview
import tkinter as tk
from tkinter import messagebox
import requests
import socket
import werkzeug
from websockets import *
import sys
import pystray
from pystray import MenuItem as item
from PIL import Image
import io

# Отключаем fail-safe для pyautogui
pyautogui.FAILSAFE = False

# размер экрана
screenWidth, screenHeight = pyautogui.size()

# параметры для курсора
prev_x = None
prev_y = None
sm_factor = 0.9
k_factor = 0.2

def safe_zone(x, k):
    return x * 2 - 0.5

def smooth_coordinates(x, y):
    global prev_x, prev_y
    if prev_x is None or prev_y is None:
        prev_x = x
        prev_y = y
        return x, y
    sm_x = prev_x * sm_factor + x * (1 - sm_factor)
    sm_y = prev_y * sm_factor + y * (1 - sm_factor)
    prev_x = sm_x
    prev_y = sm_y
    return sm_x, sm_y

# Проверка интернета
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=1)
        return True
    except requests.ConnectionError:
        return False

# Проверка, свободен ли порт
def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return True
        except OSError:
            return False

# HTML-код встроен в Python
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Локальный сервер</title>
    <link href="styles.css" rel="stylesheet">
    <link rel="stylesheet" href="../static/css/styles.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&family=Noto+Emoji:wght@300..700&family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&family=Onest:wght@100..900&family=Oswald:wght@200..700&display=swap" rel="stylesheet">
</head>
<style>

html {
  scroll-behavior: smooth;
}

* {
  -webkit-tap-highlight-color: transparent;
  transition: all 0.3s ease;
}

body {
  margin: 0;
  font-family: var(--md-ref-typeface-plain);
  background: #1c1c1c;
  color: #fff;
}

md-top-app-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  backdrop-filter: blur(10px);
  padding: 20px;
}

main {
  padding: 120px 20px 40px;
  max-width: 900px;
  margin: 0 auto;
}

.menu {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.menu a {
  font-size: 1.2em;
  color: var(--md-sys-color-primary);
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 10px;
}

.menu a:hover {
  background-color: var(--md-sys-color-primary);
  color: #fff;
}

.card {
  width: 80%;
  padding: 10px;
  margin: 10px auto;
  border-radius: 15px;
  text-align: left;

  background-color: #121212;
}

.filled_card {
  background-color: #282828;
  margin: 10px 0;
  border-radius: 12px;
  padding: 15px;
}

.elevated_card {
  background-color: #121212;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  border-radius: 12px;
}

.outlined_card {
  background-color: #121212;
  border: 1px solid #666;
  border-radius: 12px;
}

h1, h2, h3 {
  margin-top: 0;
  font-family: var(--md-ref-typeface-brand);
  position: relative;
  scroll-margin-top: 120px;
}

h1 {
  font-weight: 600;
  font-size: 2.2em;
  margin-bottom: 10px;
  color: #fff;
}

h2 {
  font-weight: 300;
  font-size: 1.6em;
  margin-bottom: 8px;
}

p, li {
  font-size: 1em;
  line-height: 1.6em;
}

ul {
  padding-left: 25px;
}

a {
  color: var(--md-sys-color-secondary);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

pre {
  background: #222;
  border-radius: 8px;
  color: #eee;
  padding: 12px;
  overflow-x: auto;
  font-family: monospace;
}

footer {
  text-align: center;
  padding: 25px;
  font-size: 0.9em;
  color: #aaa;
  border-top: 1px solid #444;
  margin-top: 40px;
  background-color: inherit;
}

:root {
  --md-sys-color-primary:  #7bafd4;
  --md-sys-color-tertiary: #928e93;
  --md-sys-color-secondary: #7395AE;
  --md-ref-typeface-brand: 'Manrope', sans-serif;
  --md-ref-typeface-plain: 'Manrope', sans-serif;
  --background-gradient: #1c1c1c;
  --text-color: #fff;
  --card-bg: #121212;
  --filled-card-bg: #282828;
  --outlined-card-bg: #121212;
  --outlined-card-border: 1px solid #666;
  --link-color: var(--md-sys-color-secondary);
  --pre-bg: #222;
  --pre-color: #eee;
  --footer-color: #aaa;
  --footer-border: 1px solid #444;
}

.anch {
  opacity: 0;
  font-size: 0.8em;
  margin-left: 8px;
  color: var(--md-sys-color-secondary);
  text-decoration: none;
  transition: opacity 0.3s ease;
}



.video-container {
  max-width: 80vw;
  margin: 0 auto;
  display: flex;
  justify-content: center; 
  align-items: center;  
}

.video-container canvas {
  width: 50%;
  height: auto;
  margin: auto;
  border-radius: 10px;
}

video {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

#pointer, #scroll_point {
  position: fixed;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  pointer-events: none;
  display: none;
  background-color: rgba(255, 170, 170, 0.8);
  z-index: 100;
  transition: transform 0.1s linear;
  animation: pulse 1s infinite;
  box-shadow: 0 0 10px rgba(255, 170, 170, 0.8);
}

#scroll_point {
  background-color: rgba(252, 213, 130, 0.8);
  box-shadow: 0 0 10px rgba(252, 213, 130, 0.8);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

h1 {
  font-size: 500%;
  text-align: center;
  padding: 20px 0px;
}

@media (max-width: 600px) {
  .video-container canvas {
    width: 100%;
  }
}

md-switch {
  --md-switch-track-color: #ccc;
  --md-switch-handle-color: #fff;
  --md-switch-icon-color: #333;
  --md-switch-selected-track-color: var(--md-sys-color-primary);
  --md-switch-selected-handle-color: #fff;
  --md-switch-selected-icon-color: #fff;
  --md-switch-hover-track-color: #b3b3b3;
  --md-switch-hover-handle-color: #f0f0f0;
  --md-switch-selected-hover-track-color: color-mix(in srgb, var(--md-sys-color-primary) 90%, white 10%);
  --md-switch-selected-hover-handle-color: #f0f0f0;
  --md-switch-focus-track-color: #999;
  --md-switch-focus-handle-color: #e0e0e0;
  --md-switch-selected-focus-track-color: color-mix(in srgb, var(--md-sys-color-primary) 80%, black 20%);
  --md-switch-selected-focus-handle-color: #e0e0e0;
  --md-switch-pressed-track-color: #808080;
  --md-switch-pressed-handle-color: #d0d0d0;
  --md-switch-selected-pressed-track-color: color-mix(in srgb, var(--md-sys-color-primary) 70%, black 30%);
  --md-switch-selected-pressed-handle-color: #d0d0d0;
  --md-switch-hover-state-layer-color: transparent;
  --md-switch-selected-hover-state-layer-color: transparent;
}

md-switch:hover {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.beautify-content {
  display: flex;
  gap: 16px;
  justify-content: center;
  text-align: center;
  vertical-align: middle;
}

.settings-container {
  flex-wrap: wrap;
  max-width: 800px;
  margin: 0 auto;
}

.setting-item {
  flex: 1 1 calc(40% - 0px);
  box-sizing: border-box;
  text-align: center;
  vertical-align: middle;
  margin: 0px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.animated-gradient-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  overflow: hidden;
  opacity: 1;
  background: none;
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animated-gradient-bg::before {
  content: "";
  position: absolute;
  width: 500%;
  height: 500%;
  top: -200%;
  left: -200%;
  opacity: 1;
  background-blend-mode: lighten;
  background: radial-gradient(circle at 0% 100%, #fff 0%, var(--md-sys-color-tertiary) 20%, rgb(0, 0, 0) 99%),
              radial-gradient(circle at 100% 0%, #fff 0%, var(--md-sys-color-secondary) 20%, rgb(0, 0, 0) 99%);
  animation: rotate 10s infinite linear;
}

.btn-style {
  user-select: none;
  flex-shrink: 0;
  box-sizing: border-box;
  font-family: var(--md-ref-typeface-plain);
  border: 1px solid var(--md-sys-color-secondary);
  font-size: 14px;
  padding: 10px 20px;
  border-radius: 20px;
  background-color: var(--md-sys-color-secondary);
  color: #fff;
  position: relative;
  overflow: hidden;
}

.btn-style[disabled] {
  background-color: #111;
  color: #333;
  border-color: #111;
}

.btn-style:hover {
  cursor: pointer;
}

.btn-style::after {
  content: '';
  position: absolute;
  width: 10px;
  height: 10px;
  background-color: #ffffff10;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(1);
  opacity: 0;
  transition: none;
}

.btn-style[disabled]::after {
  display: none;
}

.btn-style[disabled]:hover {
  cursor: default;
}

.btn-style:active::after {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
  animation: ripple 0.6s ease-out forwards;
}

@keyframes ripple {
  0% { transform: translate(-50%, -50%) scale(1); }
  80% { background-color: #ffffff20; transform: translate(-50%, -50%) scale(45); }
  100% { transform: translate(-50%, -50%) scale(30); opacity: 0; }
}

.switch {
  flex-shrink: 0;
  font-size: 17px;
  position: relative;
  display: inline-block;
  width: 3.2em;
  height: 2em;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  background-color: #242424;
  position: absolute;
  cursor: pointer;
  inset: 0;
  border: 2px solid #555;
  border-radius: 50px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.slider:before {
  position: absolute;
  content: "";
  height: 1.5em;
  width: 1.5em;
  left: 0.1em;
  bottom: 0.15em;
  background-color: white;
  border-radius: inherit;
  transform: scale(0.8);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
}

.switch input + .slider:active::before {
  transform: scale(1.05);
}

.switch input:checked + .slider {
  border: 1px solid var(--md-sys-color-primary);
  background-color: var(--md-sys-color-primary);
}

.switch input:checked + .slider:before {
  transform: translateX(1.3em);
}

.slide {
  -webkit-appearance: none;
  width: 150px;
  height: 5px;
  border-radius: 20px;
  background: linear-gradient(to right, var(--md-sys-color-secondary) var(--value, 50%), lightgray var(--value, 50%));
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slide::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: var(--md-sys-color-primary);
  cursor: pointer;
}

.centerer {
  width: 50%;
  padding: 0px;
  margin: 25px auto;
}
.there-will-be-video{
  display: flex;
  text-align: center;
  display: none;
}

.status-style{
  text-align: center; 
  margin-bottom: 10px; 
  font-size: 1.2em; 
}
#status{
  margin: 0 auto;
  background-color: rgba(255, 0, 0, 0.2);
  width: fit-content;
  height: fit-content;
  padding: 10px 10px;
  border-radius: 20px;
  transition: all 0.5s ease-in-out;
}
</style>
<body class="dark-theme">
    <div class="animated-gradient-bg"></div>
    
    <div class="card outlined-card">
        <table>
            <tr>
                <div style="text-align:center"><h2>Локальный сервер</h2></div>
            </tr>
            <tr>
                <div id="status" style="text-align:center">Статус: Ожидание</div>
            </tr>
        </table>
    </div>
</body>
</html>
"""

# Функция для обновления статуса через pywebview
def update_status(status):
    if window:
        window.evaluate_js(f"document.getElementById('status').innerText = 'Статус: {status}'")

async def echo(websocket):
    """Обработчик сообщений WebSocket."""
    global window
    hold_min_time = 0.175
    press_start_time = None
    is_mouse_down = False
    right_press_start_time = None
    is_right_mouse_down = False

    scroll_baseline = None
    inertia_velocity = 0
    last_scroll_event_time = time.time()
    deceleration = 200
    scroll_update_interval = 0.2

    min_x = screenWidth * (-0.5)
    max_x = screenWidth * 1.5
    min_y = screenHeight * (-0.5)
    max_y = screenHeight * 1.5

    altTab_active = False
    stamp = time.time()
    cntr = 0

    update_status("Подключение есть")

    try:
        while True:
            try:
                if time.time() - stamp < 1:
                    cntr += 1
                else:
                    print(cntr)
                    cntr = 0
                    stamp = time.time()

                message = await asyncio.wait_for(websocket.recv(), timeout=scroll_update_interval)
                spec = json.loads(message)

                if spec.get("ping", False):
                    await websocket.send(json.dumps({"pong": True}))
                    continue

                if spec.get('allowedDistance', False):
                    continue

                if "altTab" in spec:
                    cmd = spec["altTab"]
                    if cmd == "start":
                        if not altTab_active:
                            pyautogui.keyDown('alt')
                            pyautogui.press('tab')
                            altTab_active = True
                    elif cmd == "next":
                        if altTab_active:
                            pyautogui.press('tab')
                    elif cmd == "release":
                        if altTab_active:
                            pyautogui.keyUp('alt')
                            altTab_active = False
                    continue

                if spec.get('scroll', False):
                    current_scrollY = spec.get('scrollY', 0)
                    if scroll_baseline is None:
                        scroll_baseline = current_scrollY
                    offset = (scroll_baseline - current_scrollY)
                    factor = 200
                    scroll_delta = offset * factor
                    inertia_velocity = scroll_delta
                    last_scroll_event_time = time.time()
                    pyautogui.scroll(int(scroll_delta), _pause=False)
                    update_status("Подключение есть, замечен скролл")
                    continue
                else:
                    scroll_baseline = None

                spec1 = safe_zone(spec['x'], k_factor)
                spec2 = safe_zone(spec['y'], k_factor)
                abs_x = min(spec1 * screenWidth, screenWidth)
                abs_y = min(spec2 * screenHeight, screenHeight)
                sm_x, sm_y = smooth_coordinates(abs_x, abs_y)
                sm_x = max(min(sm_x, max_x), min_x)
                sm_y = max(min(sm_y, max_y), min_y)
                if abs(sm_x - abs_x) > 1 and abs(sm_y - abs_y) > 1:
                    pyautogui.moveTo(sm_x, sm_y, 0, pyautogui.easeInQuad, _pause=False)
                    update_status("Подключение есть, замечена рука")

                new_click = spec.get('click', False)
                current_time = time.time()
                if new_click:
                    if press_start_time is None:
                        press_start_time = current_time
                    if not is_mouse_down and (current_time - press_start_time) >= hold_min_time:
                        pyautogui.mouseDown(_pause=False)
                        is_mouse_down = True
                else:
                    if press_start_time is not None:
                        if is_mouse_down:
                            pyautogui.mouseUp(_pause=False)
                        else:
                            pyautogui.click(_pause=False)
                    press_start_time = None
                    is_mouse_down = False

                new_right_click = spec.get('right_click', False)
                if new_right_click:
                    if right_press_start_time is None:
                        right_press_start_time = current_time
                    if not is_right_mouse_down and (current_time - right_press_start_time) >= hold_min_time:
                        pyautogui.mouseDown(button='right', _pause=False)
                        is_right_mouse_down = True
                else:
                    if right_press_start_time is not None:
                        if is_right_mouse_down:
                            pyautogui.mouseUp(button='right', _pause=False)
                        else:
                            pyautogui.rightClick(_pause=False)
                        right_press_start_time = None
                        is_right_mouse_down = False

            except asyncio.TimeoutError:
                time_since_last_scroll = time.time() - last_scroll_event_time
                if time_since_last_scroll > scroll_update_interval and abs(inertia_velocity) > 0:
                    scroll_amount = inertia_velocity * scroll_update_interval
                    pyautogui.scroll(int(scroll_amount))
                    if inertia_velocity > 0:
                        inertia_velocity -= deceleration * scroll_update_interval
                        if inertia_velocity < 0:
                            inertia_velocity = 0
                    elif inertia_velocity < 0:
                        inertia_velocity += deceleration * scroll_update_interval
                        if inertia_velocity > 0:
                            inertia_velocity = 0

            except websockets.ConnectionClosed:
                update_status("Ожидание")
                break

            except Exception as e:
                print(f"Ошибка: {e}")

    finally:
        if is_mouse_down:
            pyautogui.mouseUp(_pause=False)
        if is_right_mouse_down:
            pyautogui.mouseUp(button='right', _pause=False)
        if altTab_active:
            pyautogui.keyUp('alt')

# Глобальные переменные
server_thread = None
server_loop = None
server_stop_event = None
window = None
tray_icon = None

# Проверка порта перед запуском
if not is_port_free(8082):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка", "Порт 8082 занят. Пожалуйста, проверьте, что другие программы не используют его.")
    root.destroy()
    sys.exit(1)

def run_server():
    """Запуск сервера в отдельном потоке."""
    global server_loop, server_stop_event
    server_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(server_loop)
    server_stop_event = asyncio.Event()

    async def server_main():
        update_status("Ожидание")
        async with websockets.serve(echo, "localhost", 8082):
            await asyncio.Future()

    try:
        server_loop.run_until_complete(server_main())
    except Exception as e:
        print("Сервер завершился с ошибкой:", e)
    finally:
        server_loop.close()

def start_server_automatically():
    """Автоматический запуск сервера."""
    global server_thread
    update_status("Устанавливаем подключение")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

# Создание иконки для трея
def create_tray_icon():
    # Создаём простую иконку (16x16 пикселей, чёрный квадрат с белой буквой "S")
    image = Image.new('RGB', (32, 32), color='black')
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((16, 16), "S", font=font, fill='white')
    return image

# Управление треем
def setup_tray():
    global tray_icon, window
    def show_window(icon):
        icon.stop()
        window.show()
        tray_icon = None

    def quit_app(icon):
        icon.stop()
        if server_loop:
            server_loop.call_soon_threadsafe(server_stop_event.set)
        window.destroy()
        sys.exit(0)

    tray_icon = pystray.Icon(
        "LocalServer",
        create_tray_icon(),
        "Локальный сервер",
        menu=pystray.Menu(
            item('Показать', show_window),
            item('Выход', quit_app)
        )
    )
    tray_icon.run()

# Обработчик сворачивания окна
def on_minimized():
    global tray_icon
    if not tray_icon:
        window.hide()
        threading.Thread(target=setup_tray, daemon=True).start()

# Обработчик восстановления окна
def on_restored():
    global tray_icon
    if tray_icon:
        tray_icon.stop()
        tray_icon = None

if __name__ == "__main__":
    # Проверка интернета
    if not check_internet():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Нет интернета. Программа не может быть запущена.")
        root.destroy()
        sys.exit(1)

    # Создание окна pywebview с встроенным HTML
    window = webview.create_window(
        title="Сервер",
        html=HTML_CONTENT,  # Встроенный HTML вместо внешнего файла
        width=400,
        height=170,
        x=None,
        y=None,
        resizable=False,
        fullscreen=False,
        min_size=(200, 120),
        hidden=False,  # Окно видно при запуске
        frameless=False,
        easy_drag=True,
        minimized=False,
        maximized=False,
        on_top=False,
        confirm_close=False,
        background_color="#FFFFFF",
        transparent=False,
        text_select=False
    )

    # Привязка обработчиков сворачивания и восстановления
    window.events.minimized += on_minimized
    window.events.restored += on_restored

    # Автоматический запуск сервера
    threading.Thread(target=start_server_automatically, daemon=True).start()

    # Запуск приложения
    webview.start(debug=False)  # Отключаем режим отладки
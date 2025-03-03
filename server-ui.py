import asyncio
import json
import time
import threading

import pyautogui
from websockets.server import serve

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivymd.app import MDApp

pyautogui.FAILSAFE = False

# Размер экрана
screenWidth, screenHeight = pyautogui.size()

# Параметры сглаживания для курсора
prev_x = None
prev_y = None
sm_factor = 0.85
k_factor = 0.2

def safe_zone(x, k):
    return x * 2 - (2/4)


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

async def echo(websocket, path):
    hold_min_time = 0.175
    press_start_time = None
    is_mouse_down = False
    right_press_start_time = None  # Для правого клика
    is_right_mouse_down = False   # Для правого клика

    scroll_baseline = None
    inertia_velocity = 200
    last_scroll_event_time = time.time()
    deceleration = 200
    scroll_update_interval = 0.2

    # Зоны для ограничения движения курсора
    min_x =  screenHeight * (-0.5)
    max_x = screenWidth * 1.5
    min_y =  screenWidth * (-0.5)
    max_y = screenHeight * 1.5

    # Переменная для alt+tab режима
    altTab_active = False

    while True:
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=scroll_update_interval)
            spec = json.loads(message)
            
            # Обработка сообщений для alt+tab
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
                pyautogui.moveTo(sm_x, sm_y, 0.01, pyautogui.easeInQuad, _pause=False)
            
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

            # Обработка правого клика
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

        except Exception as e:
            if '1001' not in str(e):
                print(f"Ошибка: {e}")

# --- МЕХАНИЗМ ЗАПУСКА СЕРВЕРА В ОТДЕЛЬНОМ ПОТОКЕ ---

# Глобальные переменные для управления сервером
server_thread = None
server_loop = None
server_stop_event = None

def run_server():
    """Запускает сервер в отдельном потоке."""
    global server_loop, server_stop_event
    server_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(server_loop)
    server_stop_event = asyncio.Event()

    async def server_main():
        async with serve(echo, "localhost", 8082):
            await server_stop_event.wait()  # Ожидаем команды остановки

    try:
        server_loop.run_until_complete(server_main())
    except Exception as e:
        print("Сервер завершился с ошибкой:", e)
    finally:
        server_loop.close()



class MainApp(MDApp):
    status_text = StringProperty("Не подключено")

    def build(self):
        # Ограничиваем размер окна
        Window.size = (250, 180)
        kv = '''
MDBoxLayout:
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(10)
    md_bg_color: (17/255, 17/255, 17/255)

    MDLabel:
        text: "Статус: " + app.status_text
        halign: "center"
        color: (240/255, 240/255, 240/255)
        font_style: "H6"
        size_hint_y: None
        height: self.texture_size[1]

    MDFillRoundFlatButton:
        md_bg_color: (128/255, 128/255, 0)
        text: "Подключиться"
        pos_hint: {"center_x": 0.5}
        on_release: app.connect_server()

    MDFillRoundFlatButton:
        md_bg_color: (128/255, 128/255, 0)
        text: "Отключиться"
        pos_hint: {"center_x": 0.5}
        on_release: app.disconnect_server()
'''
        return Builder.load_string(kv)

    def connect_server(self):
        """Запускает сервер, если он не запущен."""
        global server_thread
        if server_thread is None or not server_thread.is_alive():
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            self.status_text = "Подключено"
        else:
            self.status_text = "Уже подключено"

    def disconnect_server(self):
        """Останавливает сервер, если он запущен."""
        global server_thread, server_loop, server_stop_event
        if server_loop and server_stop_event:
            server_loop.call_soon_threadsafe(server_stop_event.set)
            self.status_text = "Отключено"
            if server_thread:
                server_thread.join(timeout=2)
        else:
            self.status_text = "Не подключено"

if __name__ == "__main__":
    MainApp().run()

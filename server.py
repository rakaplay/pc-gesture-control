import asyncio
import json
import time
from websockets.server import serve
import pyautogui

pyautogui.FAILSAFE = False


# Размер экрана
screenWidth, screenHeight = pyautogui.size()

# Переменные для сглаживания
prev_x = None
prev_y = None
sm_factor = 0.75
k_factor = 0.5

def safe_zone(x, k):
    return ((x - k) * 2) + k

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
    deceleration = 500
    scroll_update_interval = 0.2

    min_x =  screenHeight * (-0.3)
    max_x = screenWidth * 1.3
    min_y =  screenWidth * (-0.3)
    max_y = screenHeight * 1.3

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
                        pyautogui.press('tab')  # Открываем меню alt+tab
                        altTab_active = True
                elif cmd == "next":
                    if altTab_active:
                        pyautogui.press('tab')  # Циклично переключаем окно
                elif cmd == "release":
                    if altTab_active:
                        pyautogui.keyUp('alt')
                        altTab_active = False
                continue  # Пропускаем остальную обработку для alt+tab

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

            # Правый клик
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

async def main():
    async with serve(echo, "localhost", 8082):
        await asyncio.Future()

asyncio.run(main())

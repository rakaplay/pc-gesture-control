# app/input_handler.py
import pyautogui
import time

# Отключаем fail-safe
pyautogui.FAILSAFE = False

class InputHandler:
    def __init__(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.prev_x = None
        self.prev_y = None
        self.sm_factor = 0.9
        self.k_factor = 0.2
        
        # Параметры кликов
        self.press_start_time = None
        self.is_mouse_down = False
        self.right_press_start_time = None
        self.is_right_mouse_down = False
        self.hold_min_time = 0.175
        
        # Параметры скролла
        self.scroll_baseline = None
        self.altTab_active = False

    def _safe_zone(self, x):
        return x * 2 - 0.5

    def _smooth_coordinates(self, x, y):
        if self.prev_x is None or self.prev_y is None:
            self.prev_x = x
            self.prev_y = y
            return x, y
        sm_x = self.prev_x * self.sm_factor + x * (1 - self.sm_factor)
        sm_y = self.prev_y * self.sm_factor + y * (1 - self.sm_factor)
        self.prev_x = sm_x
        self.prev_y = sm_y
        return sm_x, sm_y

    def handle_alt_tab(self, cmd):
        if cmd == "start":
            if not self.altTab_active:
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                self.altTab_active = True
        elif cmd == "next":
            if self.altTab_active:
                pyautogui.press('tab')
        elif cmd == "release":
            if self.altTab_active:
                pyautogui.keyUp('alt')
                self.altTab_active = False

    def handle_scroll(self, current_scrollY):
        if self.scroll_baseline is None:
            self.scroll_baseline = current_scrollY
        
        offset = (self.scroll_baseline - current_scrollY)
        scroll_delta = offset * 200
        pyautogui.scroll(int(scroll_delta), _pause=False)
        return scroll_delta # Возвращаем для инерции, если нужно

    def reset_scroll(self):
        self.scroll_baseline = None

    def process_movement(self, raw_x, raw_y):
        spec1 = self._safe_zone(raw_x)
        spec2 = self._safe_zone(raw_y)
        
        abs_x = min(spec1 * self.screenWidth, self.screenWidth)
        abs_y = min(spec2 * self.screenHeight, self.screenHeight)
        
        min_x, max_x = self.screenWidth * -0.5, self.screenWidth * 1.5
        min_y, max_y = self.screenHeight * -0.5, self.screenHeight * 1.5
        
        sm_x, sm_y = self._smooth_coordinates(abs_x, abs_y)
        sm_x = max(min(sm_x, max_x), min_x)
        sm_y = max(min(sm_y, max_y), min_y)
        
        if abs(sm_x - abs_x) > 1 and abs(sm_y - abs_y) > 1:
            pyautogui.moveTo(sm_x, sm_y, 0, pyautogui.easeInQuad, _pause=False)

    def process_clicks(self, is_click, is_right_click):
        current_time = time.time()
        
        # Левый клик
        if is_click:
            if self.press_start_time is None:
                self.press_start_time = current_time
            if not self.is_mouse_down and (current_time - self.press_start_time) >= self.hold_min_time:
                pyautogui.mouseDown(_pause=False)
                self.is_mouse_down = True
        else:
            if self.press_start_time is not None:
                if self.is_mouse_down:
                    pyautogui.mouseUp(_pause=False)
                else:
                    pyautogui.click(_pause=False)
            self.press_start_time = None
            self.is_mouse_down = False

        # Правый клик (аналогично можно вынести в отдельный метод для DRY)
        if is_right_click:
            if self.right_press_start_time is None:
                self.right_press_start_time = current_time
            if not self.is_right_mouse_down and (current_time - self.right_press_start_time) >= self.hold_min_time:
                pyautogui.mouseDown(button='right', _pause=False)
                self.is_right_mouse_down = True
        else:
            if self.right_press_start_time is not None:
                if self.is_right_mouse_down:
                    pyautogui.mouseUp(button='right', _pause=False)
                else:
                    pyautogui.rightClick(_pause=False)
            self.right_press_start_time = None
            self.is_right_mouse_down = False

    def cleanup(self):
        if self.is_mouse_down: pyautogui.mouseUp(_pause=False)
        if self.is_right_mouse_down: pyautogui.mouseUp(button='right', _pause=False)
        if self.altTab_active: pyautogui.keyUp('alt')
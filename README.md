# pc-gesture-control (Releases)
Touchless gesture control for your computer. Uses Mediapipe and Python for hand detection and input emulation. Supports Windows and Chrome. This is a compiled version.

## How do I use it?
1. **Download the "dist-onefile" folder**  
   You can find it in the `releases` branch.
2. **Run the `.EXE` file inside**  
   This is the server that receives gesture data from the site.
3. **Press "Connect" ("Подключиться")**  
   This starts the WebSocket connection.
4. **Open https://rakaplay.github.io**  
   This is the web client that runs locally but is hosted on GitHub Pages.
5. **Allow camera access**  
   This enables Google Mediapipe to detect your hand and send data to the server.
6. **(Optional) Enable "PiP mode" ("Включить PiP режим")**  
   This makes it run in the background.

## Supported gestures
1. **Click** — Bring your index finger and thumb together (like Apple Vision Pro users do).  
2. **Pointer movement** — Keep your index finger and thumb together.  
3. **Scroll** — Cross your fingers.  
4. **Right-click** — Touch your ring finger to your thumb.  
5. **Alt+Tab** — Touch your little finger to your thumb for 0.5s to open the Alt+Tab menu. Repeating the gesture switches windows.

## System requirements
### Minimum:
- CPU **(>2 GHz)**
- **2 GB RAM**

### Recommended:
#### If you have a GPU:
- **GTX 7xx or newer**

#### If you don’t have a GPU but have a good CPU:
- CPU **(>2 GHz)**
- **4 GB RAM**

---

## Описание на русском

# pc-gesture-control (Релизы)
Бесконтактное управление компьютером с помощью жестов. Использует Mediapipe и Python для распознавания рук и эмуляции ввода. Поддерживает Windows и Chrome. Это скомпилированная версия.

## Как пользоваться?
1. **Скачайте папку "dist-onefile"**  
   Она находится в ветке `releases`.
2. **Запустите `.EXE` файл внутри**  
   Это сервер, который получает данные о жестах с сайта.
3. **Нажмите "Подключиться"**  
   Это запускает WebSocket-соединение.
4. **Откройте https://rakaplay.github.io**  
   Это веб-клиент, работающий локально, но размещённый на GitHub Pages.
5. **Разрешите доступ к камере**  
   Это активирует Google Mediapipe для распознавания руки и отправки данных на сервер.
6. **(Опционально) Включите "PiP режим"**  
   Это позволит работать в фоне.

## Поддерживаемые жесты
1. **Клик** — Сомкните указательный палец и большой (как в Apple Vision Pro).  
2. **Управление курсором** — Держите указательный и большой палец вместе.  
3. **Скроллинг** — Скрестите пальцы.  
4. **ПКМ (Правая кнопка мыши)** — Коснитесь безымянным пальцем большого.  
5. **Alt+Tab** — Коснитесь мизинцем большого пальца на 0,5 секунды, чтобы открыть меню Alt+Tab. Повтор жеста переключает окна.

## Системные требования
### Минимальные:
- **Процессор (>2 ГГц)**
- **2 ГБ ОЗУ**

### Рекомендуемые:
#### Если есть видеокарта:
- **GTX 7xx и новее**

#### Если видеокарты нет, но процессор мощный:
- **Процессор (>2 ГГц)**
- **4 ГБ ОЗУ**

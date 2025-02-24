
# ENGLISH
# pc-gesture-control
 Touchless gesture control of your computer. Uses Mediapipe and Python for hand detection and input emulation. Supports Windows and Chrome. In beta right now.
## How do I run it? 
#### 1. Download "dist" folder. 
Download it from `releases`["https://github.com/rakaplay/pc-gesture-control/tree/releases"] branch and run. This is server build that was made with `pyinstaller`. In the future, it is planned to make compiled `.EXE` using `Nuitka`, to make file lighter. 
#### 2. Open `.EXE` file in it. 
This is a server that gets movement and gesture info from site. 
#### Press "Connect" ("Подключиться").
This button runs websocket. 
#### 3. Open https://rakaplay.github.io 
This is a project page, hosted on GitHub Pages. It runs locally, so there are requirements below. 
#### 4. Allow camera for site.
When you allow access to the camera, the Google MediaPipe model will start and start sending data to the server to control the PC. 
#### (Optionally) 5. Turn on "PiP mode" (Включить PiP режим)
Enable this mode if you want everything to work well in the background. 
## Which input events are supported?
1. Click. Just bring your index finger and thumb together like guys with Apple Vision Pro do.
2. Pointer-controlling. Just keep your index finger and thumb together.
3. Scroll. You need to keep your fingers crossed.
4. Right mouse click. You need to make ring finger touch your thumb.
5. Alt+Tab. You need to make little finger touch your thumb for 0.5s to open the Alt+Tab menu. The same gesture chooses next window and when there isn't any Alt+Tab gestures, the last choosed window opens.
## Any requirements?
Yes!
### Minimal requirements:
-  CPU (>2 Ghz)
-  2 GB of RAM
### Recommemned requirements:
#### If you have a videocard:
-  GTX 7xx and below
#### If you don't have videocard, but you have good CPU:
-  CPU with >2 Ghz
-  4 GB of RAM




# RU
# Управление ПК жестами
Бесконтактное управление компьютером с помощью жестов. Использует Mediapipe и Python для обнаружения рук и эмуляции ввода. Поддерживает Windows и Chrome. На данный момент в бета-версии.

## Какие события ввода поддерживаются?
1. Клик. Просто соедините указательный палец и большой палец, как это делают владельцы Apple Vision Pro.
2. Управление указателем. Просто держите указательный палец и большой палец вместе.
3. Прокрутка. Нужно сложить пальцы крест-накрест.
4. Правая кнопка мыши. Необходимо прикоснуться кольцевым пальцем к большому пальцу.
5. Alt+Tab. Нужно, чтобы мизинец коснулся большого пальца на 0,5 секунды, чтобы открыть меню Alt+Tab. Этот же жест выбирает следующее окно, а когда жестов Alt+Tab нет, открывается последнее выбранное окно.

## Есть ли требования?
Да!

### Минимальные требования:
-  Процессор (>2 ГГц)
-  2 ГБ оперативной памяти

### Рекомендуемые требования:
#### Если у вас есть видеокарта:
-  GTX 7xx и ниже

#### Если у вас нет видеокарты, но есть хороший процессор:
-  Процессор с >2 ГГц
-  4 ГБ оперативной памяти
#### Евгения Сергеевна, надо сначала сервак запустить и нажать "Подключиться", а потом уже сайт rakaplay.github.io запускать. Теперь сайт хостится на GitHub! 

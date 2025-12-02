# app/config.py

PORT = 8082
HOST = "localhost"

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gest.ai Server</title>
    
    <!-- Шрифты и иконки -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Manrope:wght@200..800&family=Martian+Mono&family=Old+Standard+TT&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined" rel="stylesheet">

    <style>
        /* --- main.css variables --- */
        :root {
            --bg-color: #000000;
            --bar-color: #131313;
            --text-color: #ffffff;
            --font-main: 'Inter', sans-serif;
            --font-title: 'Inter', sans-serif;
            --button-border: #3f3f3f;
            --button-color: #3a3a3a;
            --body-color: #222222;
            --accent: #83ceeb;
        }

        /* --- Global Reset & Body --- */
        * {
            box-sizing: border-box;
            user-select: none; /* Чтобы не выделять текст в приложении */
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--body-color);
            font-family: var(--font-main);
            color: var(--text-color);
            overflow: hidden; /* Убираем скроллбары окна */
            height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* --- Top Bar --- */
        .top-app-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 50px;
            background-color: var(--bar-color);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            border-bottom: 1px solid #333;
        }

        .top-app-bar__title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-color);
            letter-spacing: 0.5px;
        }

        /* --- Layout & Blocks (inference.css adapted) --- */
        .main {
            margin-top: 50px; /* Отступ под хедером */
            padding: 20px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: calc(100% - 50px);
        }

        .block {
            background-color: #141414;
            width: 90%;
            max-width: 400px;
            padding: 20px;
            border-radius: 30px; /* Чуть меньше 48pt для компактности сервера */
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }

        .block--title {
            font-size: 24px;
            font-weight: 700;
            padding: 10px 0;
        }

        /* --- Status Indicator --- */
        #status-container {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: #2a2a2a;
            padding: 8px 20px;
            border-radius: 50px;
            margin-top: 10px;
            border: 1px solid var(--button-border);
        }

        #status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: #ff4444; /* Красный по умолчанию */
            box-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
            transition: all 0.3s ease;
        }

        #status-text {
            font-size: 14px;
            font-weight: 500;
        }

        /* --- Buttons (button.css) --- */
        .button {
            padding: 8px 16px;
            background: var(--button-color);
            border: none;
            border-radius: 50px;
            color: #ffffff;
            cursor: pointer;
            font-size: 13px;
            font-family: var(--font-main);
            transition: 0.2s ease;
            outline: none;
            text-decoration: none;
            display: inline-block;
        }

        .button:hover {
            background-color: #4a4a4a;
            filter: brightness(110%);
        }

        .button:active {
            transform: scale(0.95);
        }

        .button--accent {
            background: var(--accent);
            color: black;
            font-weight: 600;
        }
        
        .button--accent:hover {
            background: #68b8d8;
        }

        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 5px;
        }

        /* Анимация градиента на фоне (опционально, как в оригинале) */
        .inference-bg {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: -1;
            background: radial-gradient(circle at 50% -20%, #222 0%, #000 70%);
        }

    </style>
</head>
<body>
    <div class="inference-bg"></div>
    
    <header class="top-app-bar">
        <h1 class="top-app-bar__title">Локальный сервер Gest.ai</h1>
    </header>

    <div class="main">
        <!-- Блок статуса -->
        <div class="block">
            <div style="margin-bottom: 10px; color: #aaa; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Состояние</div>
            <div id="status-container">
                <div id="status-dot"></div>
                <div id="status-text">Ожидание подключения...</div>
            </div>
            <div style="margin-top: 15px; font-size: 12px; color: #666;">
                Порт: <span style="color: #fff;">8082</span> &bull; Хост: <span style="color: #fff;">localhost</span>
            </div>
        </div>

        <!-- Блок управления (для примера) -->
        <div class="block" style="padding: 15px; background-color: transparent; box-shadow: none;">
             <div class="controls">
                <!-- Кнопки вызывают функции Python через pywebview API, если настроено, или просто ссылки -->
                <!-- В данном скрипте логика кнопок была в трее, но можно добавить сюда 'Свернуть' -->
                <button class="button" onclick="window.pywebview.api.minimize()">Свернуть</button>
                <button class="button button--accent" onclick="window.pywebview.api.quit()">Выход</button>
            </div>
        </div>
    </div>

    <script>
        // Функция обновления статуса, которую вызывает Python
        function updateStatus(text) {
            const dot = document.getElementById('status-dot');
            const label = document.getElementById('status-text');
            
            label.innerText = text;

            if (text.toLowerCase().includes("подключение есть") || text.toLowerCase().includes("активно")) {
                dot.style.backgroundColor = "#00ff88";
                dot.style.boxShadow = "0 0 10px rgba(0, 255, 136, 0.5)";
            } else if (text.toLowerCase().includes("ожидание")) {
                dot.style.backgroundColor = "#ffaa00";
                dot.style.boxShadow = "0 0 10px rgba(255, 170, 0, 0.5)";
            } else {
                dot.style.backgroundColor = "#ff4444";
                dot.style.boxShadow = "0 0 10px rgba(255, 68, 68, 0.5)";
            }
        }
        
        // Перенаправляем стандартную функцию Python на новую логику
        window.document.getElementById = (function(orig) {
            return function(id) {
                if (id === 'status') {
                    // Создаем фиктивный объект, чтобы старый код Python:
                    // document.getElementById('status').innerText = '...'
                    // работал с новым updateStatus
                    return {
                        set innerText(val) {
                            updateStatus(val);
                        }
                    };
                }
                return orig.call(document, id);
            };
        })(window.document.getElementById);

    </script>
</body>
</html>
"""

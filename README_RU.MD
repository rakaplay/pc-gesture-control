---

## Описание на русском

# pc-gesture-control
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
 
---

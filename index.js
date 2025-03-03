let flipX = true;
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('h1[id], h2[id], h3[id]').forEach(heading => {
    if (!heading.querySelector('.anch')) {
      const anchor = document.createElement('a');
      anchor.href = `#${heading.id}`;
      anchor.className = 'anch';
      anchor.textContent = '#';
      heading.appendChild(anchor);
    }
  });
});

// Глобальные переменные для alt+tab
let altTabGestureActive = false;
let altTabGestureStartTime = null;
let altTabLastDetectedTime = null;
let altTabWasDetected = false;
const ALT_TAB_HOLD_TIME = 500; 
const ALT_TAB_IDLE_TIME = 2000; 

const video_element = document.getElementById("video");
const canvas_element = document.getElementById("canvas");
const canvas_risovka = canvas_element.getContext("2d");
const pointer = document.getElementById("pointer");
const scrollPointer = document.getElementById("scroll_point");
const turn_on_camera = document.getElementById("turn_on_camera");
const turn_off_camera = document.getElementById("turn_off_camera");
const pipButton = document.getElementById("pipButton");
const status = document.getElementById("status");

const socket = new WebSocket("ws://localhost:8082");
socket.addEventListener("open", () => console.log("Вебсокет подключён"));
socket.addEventListener("error", (error) => console.error("Вебсокет, ошибка:", error));

let pipVideo;
let camera = null;
let cameraActive = false;

let prev_abs_x = null;
let prev_abs_y = null;
const threshold = 0;

turn_on_camera.addEventListener("click", () => {
  navigator.mediaDevices.getUserMedia({ video: { frameRate: { ideal: 30, max: 60 } } })
    .then((stream) => {
      video_element.srcObject = stream;
      cameraActive = true;
      status.innerText = "Ожидание руки";
      status.style.color = "orange";
      
      turn_on_camera.disabled = true;
      turn_off_camera.disabled = false;

      camera = new Camera(video_element, {
        onFrame: async () => await hands.send({ image: video_element }),
        width: 640,
        height: 360,
      });
      camera.start();

      pipVideo = document.createElement("video");
      pipVideo.style.display = "none";
      pipVideo.srcObject = canvas_element.captureStream(60);
      document.body.appendChild(pipVideo);

      pipVideo.addEventListener("loadedmetadata", () => {
        pipButton.disabled = false;
        console.log("Metadata загружены, кнопка PiP активна");
      });

      pipVideo.play().then(() => console.log("pipVideo запущен"))
        .catch(err => console.error("Ошибка воспроизведения pipVideo:", err));
    })
    .catch((err) => console.error("Ошибка доступа к камере:", err));
});

turn_off_camera.addEventListener("click", () => {
  if (camera) {
    camera.stop();
    camera = null;
    cameraActive = false;
    status.innerText = "Камера остановлена";
    status.style.color = "red";
    turn_on_camera.disabled = false;
    turn_off_camera.disabled = true;
    const stream = video_element.srcObject;
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      video_element.srcObject = null;
    }
    if (pipVideo) {
      document.body.removeChild(pipVideo);
      pipVideo = null;
      pipButton.disabled = true;
    }
  }
});

pipButton.addEventListener("click", async () => {
  try {
    if (document.pictureInPictureElement) {
      await document.exitPictureInPicture();
      pipButton.innerText = "Включить PiP";
    } else {
      await pipVideo.requestPictureInPicture();
      pipButton.innerText = "Выключить PiP";
    }
  } catch (error) {
    console.error("Ошибка переключения PiP:", error);
  }
});

const hands = new Hands({
  locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
});
hands.setOptions({
  maxNumHands: 1,
  modelComplexity: 0,
  minDetectionConfidence: 0.8,
  minTrackingConfidence: 0.8,
});

hands.onResults((results) => {
  canvas_risovka.clearRect(0, 0, canvas_element.width, canvas_element.height);
  canvas_risovka.drawImage(video_element, 0, 0, canvas_element.width, canvas_element.height);

  if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
    if (cameraActive) {
      status.innerText = "Рука распознана";
      status.style.color = "green";
    }
    const landmarks = results.multiHandLandmarks[0];
    drawConnectors(canvas_risovka, landmarks, HAND_CONNECTIONS, { color: "#44EE22", lineWidth: 4 });
    drawLandmarks(canvas_risovka, landmarks, { color: "#EE7722", radius: 3 });

    let indexFinger = landmarks[8];
    let scrollIndexFinger = landmarks[7];
    let scrollMiddleFinger = landmarks[12];
    let thumb = landmarks[4];
    let bezymFinger = landmarks[16];
    let mainPoint = landmarks[1];
    let mizinFinger = landmarks[20];
    let relativeXClick = mainPoint.x;
    let relativeYClick = mainPoint.y;
    if (document.getElementById("flipX").selected){
     relativeXClick = 1 - mainPoint.x;
    } else {
     relativeXClick = mainPoint.x;
    }
    if (document.getElementById("flipY").selected){
      relativeYClick = 1 - mainPoint.y;
     } else {
      relativeYClick = mainPoint.y;
    }
    
    const absoluteXClick = relativeXClick * window.innerWidth;
    const absoluteYClick = relativeYClick * window.innerHeight;


    
    const relativeXScroll = 1 - indexFinger.x;
    const relativeYScroll = indexFinger.y;
    const absoluteXScroll = relativeXScroll * window.innerWidth;
    const absoluteYScroll = relativeYScroll * window.innerHeight;

    let scrollFlag = false;
    let right_click_flag = false; 
    if (scrollMiddleFinger && indexFinger) {
      const scrollDistance = Math.hypot(
        (scrollMiddleFinger.x - scrollIndexFinger.x) * canvas_element.width,
        (scrollMiddleFinger.y - scrollIndexFinger.y) * canvas_element.height
      );
      if (scrollDistance < 18) {
        scrollFlag = true;
        scrollPointer.style.transform = `translate(${absoluteXClick - scrollPointer.offsetWidth / 2}px, ${absoluteYClick - scrollPointer.offsetHeight / 2}px)`;
        scrollPointer.style.display = "block";
        status.innerText = 'Рука распознана; распознан скролл';
      } else {
        scrollFlag = false;
        status.innerText = 'Рука распознана; жестов не обнаружено';
        scrollPointer.style.display = "none";
      }
    } else {
      pointer.style.display = "none";
    }

    let click_flag = false;
    let move_flag = false;
    if (indexFinger && thumb) {
      const distance = Math.hypot(
        (indexFinger.x - thumb.x) * canvas_element.width,
        (indexFinger.y - thumb.y) * canvas_element.height
      );
      if (distance < 20) {
        click_flag = true;
        pointer.style.transform = `translate(${absoluteXClick - pointer.offsetWidth / 2}px, ${absoluteYClick - pointer.offsetHeight / 2}px)`;
        pointer.style.display = "block";
        if (!scrollFlag) status.innerText = 'Рука распознана; распознан клик';

      } else if (distance < 40) {
        move_flag = true;
        pointer.style.transform = `translate(${absoluteXClick - pointer.offsetWidth / 2}px, ${absoluteYClick - pointer.offsetHeight / 2}px)`;
        pointer.style.display = "block";
        if (!scrollFlag) status.innerText = 'Рука распознана; обнаружены близкие друг к другу указательный и большой пальцы';
      } else {
        move_flag = false;
        pointer.style.display = "none";
      }
    } else {
      status.innerText = "Рука распознана; жестов не обнаружено";
      pointer.style.display = "none";
    }
    // Проверка для правого клика (большой и безымянный пальцы)
    if (thumb && bezymFinger) {
      const rightClickDistance = Math.hypot(
        (thumb.x - bezymFinger.x) * canvas_element.width,
        (thumb.y - bezymFinger.y) * canvas_element.height
      );
      if (rightClickDistance < 20) {
        right_click_flag = true;
        pointer.style.transform = `translate(${absoluteXClick - pointer.offsetWidth / 2}px, ${absoluteYClick - pointer.offsetHeight / 2}px)`;
        pointer.style.display = "block";
      }
    }
    
    if (socket.readyState === WebSocket.OPEN) {
      if (!prev_abs_x || Math.abs(absoluteXClick - prev_abs_x) > threshold || Math.abs(absoluteYClick - prev_abs_y) > threshold) {
        if (scrollFlag) {
          socket.send(JSON.stringify({ scroll: true, scrollY: relativeYScroll, moveFlag: false }));
        } else {
          socket.send(JSON.stringify({ x: relativeXClick, y: relativeYClick, click: click_flag, right_click: right_click_flag, scroll: false, moveFlag: move_flag }));
        }
        prev_abs_x = absoluteXClick;
        prev_abs_y = absoluteYClick;
      }
    }

    // --- Обработка жеста alt+tab ---
    let now = Date.now();
    let altTabCurrentlyDetected = false;
    if (mizinFinger && thumb) {
      const altTabDistance = Math.hypot(
        (mizinFinger.x - thumb.x) * canvas_element.width,
        (mizinFinger.y - thumb.y) * canvas_element.height
      );
      altTabCurrentlyDetected = (altTabDistance < 18);
    }
    if (altTabCurrentlyDetected) {
      if (!altTabGestureActive) {
        if (altTabGestureStartTime === null) {
          altTabGestureStartTime = now;
        }
        if (now - altTabGestureStartTime >= ALT_TAB_HOLD_TIME) {
          socket.send(JSON.stringify({ altTab: "start" }));
          altTabGestureActive = true;
        }
      } else {
        // Если жест возобновлён после кратковременного отсутствия – выбираем следующее окно
        if (!altTabWasDetected) {
          socket.send(JSON.stringify({ altTab: "next" }));
        }
      }
      altTabLastDetectedTime = now;
    } else {
      if (altTabGestureActive && altTabLastDetectedTime && (now - altTabLastDetectedTime >= ALT_TAB_IDLE_TIME)) {
        socket.send(JSON.stringify({ altTab: "release" }));
        altTabGestureActive = false;
        altTabGestureStartTime = null;
        altTabLastDetectedTime = null;
      } else if (!altTabGestureActive) {
        altTabGestureStartTime = null;
        altTabLastDetectedTime = null;
      }
    }
    altTabWasDetected = altTabCurrentlyDetected;
    // --- Конец обработки alt+tab ---
    
  } else {
    if (cameraActive) {
      status.innerText = "Ожидание руки";
      status.style.color = "orange";
    }
    pointer.style.display = "none";
    scrollPointer.style.display = "none";
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const themeToggler = document.getElementById('theme-toggler');

  // Загружаем сохраненную тему из localStorage
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-theme');
    themeToggler.selected = true;
  }

  // Переключаем тему при изменении состояния переключателя
  themeToggler.addEventListener('change', () => {
    if (themeToggler.selected) {
      document.body.classList.add('dark-theme');
      localStorage.setItem('theme', 'dark');
    } else {
      document.body.classList.remove('dark-theme');
      localStorage.setItem('theme', 'light');
    }
  });
});

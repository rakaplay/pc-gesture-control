// Чтобы код был чище, я воспользовался нейросетями.

document.addEventListener('DOMContentLoaded', () => {
    const checkboxButtons = document.querySelectorAll('.checkboxbutton');
  
    checkboxButtons.forEach(button => {
      button.addEventListener('click', () => {
        const targetCheckboxId = button.dataset.target;
        const checkbox = document.getElementById(targetCheckboxId);
        
        if (checkbox) {

          checkbox.checked = !checkbox.checked;
          if (checkbox.checked) {
            button.classList.add('button--pressed'); 
          } else {
            button.classList.remove('button--pressed');
          }
        } else {
          console.error(`Чекбокс с ID "${targetCheckboxId}" не найден для кнопки:`, button);
        }
      });
    });
  });
  document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('input', function() {
      const percent = (this.value - this.min) / (this.max - this.min) * 100;
      this.style.background = `linear-gradient(to right, #525252 ${percent}%, #111111 ${percent}%)`;
    });
  
    // Триггерим обновление стиля при загрузке
    slider.dispatchEvent(new Event('input'));
  });


        // Этот скрипт должен идти после загрузки DOM или быть в defer/DOMContentLoaded
        document.addEventListener('DOMContentLoaded', () => {

          // --- Элементы управления сворачиванием/разворачиванием ---
          const minimizeButton = document.querySelector('.minim');
          const maximizeButton = document.querySelector('.maximize');
          const set1 = document.querySelector('.block--set1');
          const set2 = document.querySelector('.block--set2');
          const set2Title = document.querySelector('.set2-title'); // Заголовок Настроек
          const set3 = document.querySelector('.block--set3');

          // --- Элементы из Set 1 ---
          const turnOnCameraButton1 = document.getElementById('turn_on_camera');
          const turnOffCameraButton1 = document.getElementById('turn_off_camera');
          const pipButton1 = document.getElementById('pipButton');
          const faqButton1 = document.getElementById('faqButton');

          // --- Элементы из Set 2 ---
          const flipXCheckbox = document.getElementById('flipX');
          const flipYCheckbox = document.getElementById('flipY');
          const workDistanceSlider2 = document.getElementById('work-distance');
          const toggleFlipXButton2 = document.getElementById('toggleFlipXButton'); // Кнопка для X в set 2
          const toggleFlipYButton2 = document.getElementById('toggleFlipYButton'); // Кнопка для Y в set 2


          // --- Элементы из Set 3 ---
          const flipXButton3 = document.getElementById('set3-flipX');
          const flipYButton3 = document.getElementById('set3-flipY');
          const workDistanceSlider3 = document.getElementById('set3-work-distance');
          const turnOnCameraButton3 = document.getElementById('set3-turn_on_camera');
          const turnOffCameraButton3 = document.getElementById('set3-turn_off_camera');
          const pipButton3 = document.getElementById('set3-pipButton');
          const faqButton3 = document.getElementById('set3-faq');

          // --- Проверка наличия элементов (хорошая практика) ---
          if (!minimizeButton || !maximizeButton || !set1 || !set2 || !set2Title || !set3 ||
              !turnOnCameraButton1 || !turnOffCameraButton1 || !pipButton1 || !faqButton1 ||
              !flipXCheckbox || !flipYCheckbox || !workDistanceSlider2 || !toggleFlipXButton2 || !toggleFlipYButton2 ||
              !flipXButton3 || !flipYButton3 || !workDistanceSlider3 || !turnOnCameraButton3 ||
              !turnOffCameraButton3 || !pipButton3 || !faqButton3) {
              console.error('Один или несколько необходимых элементов не найдены на странице!');
              return; // Прекратить выполнение, если что-то отсутствует
          }

          // --- Функции для анимации скрытия/показа ---
          function hideElements(elements, associatedButton = null) {
              elements.forEach(el => {
                  if (el) el.classList.add('fading-out');
              });
              if (associatedButton) associatedButton.classList.add('fading-out');

              setTimeout(() => {
                  elements.forEach(el => {
                      if (el) el.classList.add('hidden');
                      if (el) el.classList.remove('fading-out');
                  });
                  if (associatedButton) {
                      associatedButton.classList.add('hidden');
                      associatedButton.classList.remove('fading-out');
                  }
              }, 300); // Должно совпадать с transition duration в CSS
          }

          function showElements(elements, associatedButton = null) {
               elements.forEach(el => {
                  if (el) {
                      el.classList.remove('hidden');
                      el.classList.add('start-fade-in'); // Начальное состояние перед анимацией
                  }
               });
               if (associatedButton) {
                   associatedButton.classList.remove('hidden');
                   associatedButton.classList.add('start-fade-in');
               }

               // requestAnimationFrame гарантирует, что стили 'start-fade-in' применятся перед удалением
               requestAnimationFrame(() => {
                  elements.forEach(el => {
                     if (el) el.classList.remove('start-fade-in');
                  });
                  if (associatedButton) associatedButton.classList.remove('start-fade-in');
               });
          }

          // --- Логика сворачивания/разворачивания ---
          minimizeButton.addEventListener('click', () => {
              hideElements([set1, set2, set2Title], minimizeButton); // Скрываем Set1, Set2, заголовок Настроек и кнопку Свернуть
              showElements([set3]);                             // Показываем Set3 (кнопка Развернуть внутри него)
          });

          maximizeButton.addEventListener('click', () => {
              hideElements([set3]);                               // Скрываем Set3
              showElements([set1, set2, set2Title], minimizeButton); // Показываем Set1, Set2, заголовок и кнопку Свернуть
          });

          // --- Привязка функциональности кнопок Set 3 к Set 1 и Set 2 ---

          // Камера Вкл (Set 3 -> Set 1)
          turnOnCameraButton3.addEventListener('click', () => {
              if (turnOnCameraButton1 && !turnOnCameraButton1.disabled) {
                  turnOnCameraButton1.click(); // Вызываем клик на оригинальной кнопке
              }
          });

          // Камера Выкл (Set 3 -> Set 1)
          turnOffCameraButton3.addEventListener('click', () => {
              if (turnOffCameraButton1 && !turnOffCameraButton1.disabled) {
                  turnOffCameraButton1.click();
              }
          });

          // PiP (Фоновый режим) (Set 3 -> Set 1)
          pipButton3.addEventListener('click', () => {
              if (pipButton1 && !pipButton1.disabled) {
                  pipButton1.click();
              }
          });

          // FAQ (Set 3 -> Set 1)
          faqButton3.addEventListener('click', () => {
              if (faqButton1 && !faqButton1.disabled) {
                  faqButton1.click(); // Это вызовет `onClick="top.location.href='faq'"`
              }
          });

          // Инверсия X (Set 3 -> Set 2 Checkbox)
          flipXButton3.addEventListener('click', () => {
              if (flipXCheckbox) {
                  flipXCheckbox.checked = !flipXCheckbox.checked;
                  // Инициируем событие change, если на него есть другие обработчики
                  flipXCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
                   // Можно также визуально синхронизировать кнопку в set2, если нужно
                   if (toggleFlipXButton2) {
                       toggleFlipXButton2.classList.toggle('active', flipXCheckbox.checked);
                   }
              }
          });

           // Инверсия Y (Set 3 -> Set 2 Checkbox)
           flipYButton3.addEventListener('click', () => {
              if (flipYCheckbox) {
                  flipYCheckbox.checked = !flipYCheckbox.checked;
                  flipYCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
                   // Синхронизация кнопки в set2
                   if (toggleFlipYButton2) {
                       toggleFlipYButton2.classList.toggle('active', flipYCheckbox.checked);
                   }
              }
          });

           // Синхронизация состояния checkbox -> кнопок в set 2 и set 3 при загрузке или изменении
           const syncFlipButtons = () => {
               if (toggleFlipXButton2) toggleFlipXButton2.classList.toggle('active', flipXCheckbox.checked);
               if (flipXButton3) flipXButton3.classList.toggle('active', flipXCheckbox.checked); // Добавим класс active и для set3
               if (toggleFlipYButton2) toggleFlipYButton2.classList.toggle('active', flipYCheckbox.checked);
               if (flipYButton3) flipYButton3.classList.toggle('active', flipYCheckbox.checked); // Добавим класс active и для set3
           };

           if (flipXCheckbox) flipXCheckbox.addEventListener('change', syncFlipButtons);
           if (flipYCheckbox) flipYCheckbox.addEventListener('change', syncFlipButtons);
           syncFlipButtons(); // Первичная синхронизация при загрузке


           // Максимальное расстояние (Синхронизация слайдеров Set 3 <-> Set 2)
           workDistanceSlider3.addEventListener('input', (e) => {
              if (workDistanceSlider2) {
                  workDistanceSlider2.value = e.target.value;
                  // Инициируем событие input для slider2, если на него есть обработчики
                  workDistanceSlider2.dispatchEvent(new Event('input', { bubbles: true }));
              }
          });

          workDistanceSlider2.addEventListener('input', (e) => {
              if (workDistanceSlider3) {
                  workDistanceSlider3.value = e.target.value;
                   // Инициируем событие input для slider3, если нужно (маловероятно)
                  // workDistanceSlider3.dispatchEvent(new Event('input', { bubbles: true }));
              }
          });
           // Установка начального значения для set3 слайдера из set2
           if (workDistanceSlider2 && workDistanceSlider3) {
               workDistanceSlider3.value = workDistanceSlider2.value;
           }


           // --- Дополнительно: Синхронизация состояния disabled/active кнопок из Set 1 в Set 3 ---
           // Используем MutationObserver для отслеживания изменений атрибутов в Set 1
           const observeButtonState = (sourceButton, targetButton) => {
              if (!sourceButton || !targetButton) return;

              const observer = new MutationObserver(mutations => {
                  mutations.forEach(mutation => {
                      if (mutation.type === 'attributes' && (mutation.attributeName === 'disabled' || mutation.attributeName === 'class')) {
                          // Синхронизация disabled
                          targetButton.disabled = sourceButton.disabled;
                          // Синхронизация класса active (если используется для визуального состояния)
                          if (sourceButton.classList.contains('active')) {
                              targetButton.classList.add('active');
                          } else {
                              targetButton.classList.remove('active');
                          }
                          // Можно добавить специфичные классы для disabled вида в set3, если нужно
                           targetButton.classList.toggle('disabled-look', sourceButton.disabled);
                      }
                  });
              });

              observer.observe(sourceButton, { attributes: true });
               // Первичная синхронизация
               targetButton.disabled = sourceButton.disabled;
               if (sourceButton.classList.contains('active')) targetButton.classList.add('active'); else targetButton.classList.remove('active');
               targetButton.classList.toggle('disabled-look', sourceButton.disabled);
           };

           observeButtonState(turnOnCameraButton1, turnOnCameraButton3);
           observeButtonState(turnOffCameraButton1, turnOffCameraButton3);
           observeButtonState(pipButton1, pipButton3);
           observeButtonState(faqButton1, faqButton3);

           // Наблюдение за checkbox для обновления кнопок в Set 3 (добавлено выше в syncFlipButtons)

      });
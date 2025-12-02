
function redirect(url) {
    const content = document.querySelector('#content');
    let isAnimating = false;
  
    if (!content || isAnimating) return;
    isAnimating = true;
  
    localStorage.setItem('pageTransition', 'blurred');
  
    content.style.transition = 'filter 0.2s ease';
    content.style.filter = 'blur(4px)';
  
    setTimeout(() => {
      window.location.href = url;
    }, 300);
  }
  

  document.addEventListener('DOMContentLoaded', () => {
    const content = document.querySelector('#content');
    const transitionState = localStorage.getItem('pageTransition');
  
    if (content && transitionState === 'blurred') {
      content.style.filter = 'blur(4px)';
      
      setTimeout(() => {
        content.style.transition = 'filter 0.2s ease';
        content.style.filter = 'blur(0)';
        
        setTimeout(() => {
          localStorage.removeItem('pageTransition');
        }, 300);
      }, 50);
    }
  });
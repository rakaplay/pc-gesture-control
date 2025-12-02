document.addEventListener("DOMContentLoaded", () => {
    const playButton = document.getElementById("playButton");
    const videos = [
        document.getElementById("vid"),
        document.getElementById("vid2")
    ];
    
    const playIcon = playButton.querySelector('.play-icon');
    const pauseIcon = playButton.querySelector('.pause-icon');

    playButton.addEventListener("click", () => {
        const isPaused = videos[0].paused; 
        if (isPaused) {
            const playPromises = videos.map(video => video.play());
            
            Promise.all(playPromises)
                .then(() => {
                    playIcon.style.display = 'none';
                    pauseIcon.style.display = 'inline';
                })
                .catch((error) => {
                    console.error("Ошибка при воспроизведении видео:", error);
                });
        } else {
            videos.forEach(video => video.pause());
            playIcon.style.display = 'inline';
            pauseIcon.style.display = 'none';
        }
    });
});


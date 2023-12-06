function updateTime() {
    var dateTimeElement = document.getElementById("date-time");
    var now = new Date();

    var options = {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'
    };
    var formattedDateTime = " " + "Today is " + now.toLocaleDateString('en-EN', options);

    dateTimeElement.textContent = formattedDateTime;
}

setInterval(updateTime, 1000);
updateTime();


var currentMovie = 0;
var movieImages = [
    "/viewer/static/viewer/movies/DieHard.webp",
    "/static/viewer/movies/Superstore.jpg",
    "/static/viewer/movies/SurvivingChristmas.jpg",
    "/static/viewer/movies/PulpFiction.jpg",
    "/static/viewer/movies/JustGoWithIt.jpg",
    "/static/viewer/movies/DieGoldfische.jpg",
];

const links = [
    'https://video.pmgstatic.com/files/videos/157/748/157748427/163165341_9ec7c5.mp4',
    'https://video.pmgstatic.com/files/videos/157/821/157821775/167614153_g86l31.mp4',
    'https://video.pmgstatic.com/files/videos/000/305/305390/157701061_73a03b.mp4',
    'https://video.pmgstatic.com/files/videos/157/692/157692434/158469266_d071fa.mp4',
    'https://video.pmgstatic.com/files/videos/000/311/311941/157713187_3fbede.mp4',
    'https://video.pmgstatic.com/files/videos/157/749/157749188/163225997_967cd3.mp4',
];

function showNextMovie() {
    currentMovie++;
    if (currentMovie >= movieImages.length) {
        currentMovie = 0;
    }
    updateMovie();
}

function showPreviousMovie() {
    currentMovie--;
    if (currentMovie < 0) {
        currentMovie = movieImages.length - 1;
    }
    updateMovie();
}

function updateMovie() {
    var movieBox = document.getElementById('movieBox');
    var videoContainer = document.querySelector('.video-container');
    var video = document.getElementById('movieVideo');
    var imageContainer = document.querySelector('.image-container');

    video.pause();
    videoContainer.style.display = 'none';
    imageContainer.style.display = 'block';

    var newImage = document.createElement('img');
    newImage.src = movieImages[currentMovie];
    newImage.classList.add('movie-image');

    // Získáme rozměry .movie-box z CSS
    var movieBoxStyles = window.getComputedStyle(movieBox);
    var movieBoxWidth = parseInt(movieBoxStyles.width);
    var movieBoxHeight = parseInt(movieBoxStyles.height);

    // Nastavíme rozměry obrázku podle rozměrů .movie-box
    newImage.style.width = movieBoxWidth + 'px';
    newImage.style.height = movieBoxHeight + 'px';

    var oldImage = movieBox.querySelector('.image-container img');
    if (oldImage) {
        movieBox.querySelector('.image-container').replaceChild(newImage, oldImage);
    } else {
        movieBox.querySelector('.image-container').appendChild(newImage);
    }
}

function toggleVideo() {
    var movieBox = document.getElementById('movieBox');
    var videoContainer = document.querySelector('.video-container');
    var video = document.getElementById('movieVideo');
    var imageContainer = document.querySelector('.image-container');

    if (videoContainer.style.display === 'none') {
        // Video není viditelné, tak ho přehrajeme
        video.src = links[currentMovie];
        video.play();
        videoContainer.style.display = 'flex';
        imageContainer.style.display = 'none';
    } else {
        // Video je viditelné, tak ho zastavíme
        video.pause();
        videoContainer.style.display = 'none';
        imageContainer.style.display = 'block';
    }
}

updateMovie(); // Zobrazí první film při načtení stránky

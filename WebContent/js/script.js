function toggleMenu() {
    const menu = document.querySelector(".menu-links");
    const icon = document.querySelector(".hamburger-icon");
    menu.classList.toggle("open")
    icon.classList.toggle("open")
}

function desktopToggleMenu() {
    const menu = document.querySelector(".desktop-menu-links");
    const icon = document.querySelector(".desktop-icon");
    menu.classList.toggle("open")
    icon.classList.toggle("open")
}

let currentIndex = 0;

function moveSlide(step) {
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    
    currentIndex = (currentIndex + step + totalSlides) % totalSlides;
    const offset = -currentIndex * 100;
    
    document.querySelector('.slider').style.transform = `translateX(${offset}%)`;
}
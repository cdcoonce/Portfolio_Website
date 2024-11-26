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

function shinyToggleMenu() {
    const menu = document.querySelector(".shiny-menu-links");
    const icon = document.querySelector(".shiny-icon");
    menu.classList.toggle("open")
    icon.classList.toggle("open")
}

function shinyHamtoggleMenu() {
    const menu = document.querySelector(".shiny-hamburger-menu-links");
    const icon = document.querySelector(".shiny-hamburger-icon");
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

document.addEventListener("DOMContentLoaded", () => {
    const testimonials = document.querySelectorAll(".testimonial");
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    let currentIndex = 0;
  
    function showTestimonial(index) {
      testimonials.forEach((testimonial, i) => {
        testimonial.classList.remove("active");
        testimonial.style.opacity = 0;
        if (i === index) {
          testimonial.classList.add("active");
          testimonial.style.opacity = 1;
        }
      });
    }
  
    function nextTestimonial() {
      currentIndex = (currentIndex + 1) % testimonials.length;
      showTestimonial(currentIndex);
    }
  
    function prevTestimonial() {
      currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
      showTestimonial(currentIndex);
    }
  
    nextButton.addEventListener("click", nextTestimonial);
    prevButton.addEventListener("click", prevTestimonial);
  
    // Automatically scroll every 10 seconds
    setInterval(nextTestimonial, 10000);
  
    // Initialize the first testimonial
    showTestimonial(currentIndex);
  });
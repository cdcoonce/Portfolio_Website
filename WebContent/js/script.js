
let currentIndex = 0;

function moveSlide(step) {
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    
    currentIndex = (currentIndex + step + totalSlides) % totalSlides;
    const offset = -currentIndex * 100;
    
    document.querySelector('.slider').style.transform = `translateX(${offset}%)`;
}

/* === Testimonials Slider === */

    document.addEventListener("DOMContentLoaded", () => {
        const testimonials = document.querySelectorAll(".testimonial");
        const prevButton = document.getElementById("prev");
        const nextButton = document.getElementById("next");
        const dotsContainer = document.querySelector(".dots-container");
        let currentIndex = 0;
        let testimonialsToShow = getTestimonialsToShow();

        function getTestimonialsToShow() {
            return window.innerWidth >= 1200 ? 2 : 1; // Show 2 on large screens, 1 on small screens
        }
        
        window.addEventListener("resize", () => {
            testimonialsToShow = getTestimonialsToShow();
            showTestimonial(currentIndex); // Re-render testimonials
            createDots();
        });

        function createDots() {
        dotsContainer.innerHTML = "";

        testimonials.forEach((_, index) => {
            const dot = document.createElement("div");
            if (window.innerWidth > 1200) {
                if (index % 2 == 0)
                dot.classList.add("dot");
                if (index == 0) 
                    dot.classList.add("active"); // Make the first dot active initially
                    dotsContainer.appendChild(dot);
            } else {
                    dot.classList.add("dot");
                if (index == 0) 
                    dot.classList.add("active"); // Make the first dot active initially
                    dotsContainer.appendChild(dot);
            }
        });
        }

        function updateDots() {
        const dots = document.querySelectorAll(".dot");
        dots.forEach((dot, index) => {
            if (window.innerWidth > 1200) {
                if (index == currentIndex / 2) {
                    dot.classList.add("active");
                } else {
                    dot.classList.remove("active");
                }
            } else {
                if (index == currentIndex) {
                    dot.classList.add("active");
                } else {
                    dot.classList.remove("active");
                }
            }
        });
        }

        function showTestimonial(index) {
            testimonials.forEach((testimonial, i) => {
                testimonial.classList.remove("active");
                testimonial.style.opacity = 0;
            
                // Activate the current testimonial
                if (window.innerWidth > 1200) {
                if (i == testimonials.length - 1) {
                    testimonial.classList.add("active");
                    testimonial.style.opacity = 1;
                    }
                } else {
                    if (i == currentIndex) {
                        testimonial.classList.add("active");
                        testimonial.style.opacity = 1;
                    }
                }
            });
            updateDots();
        }

        function showTestimonials(index) {
        testimonials.forEach((testimonial, i) => {
            testimonial.classList.remove("active");
            testimonial.style.opacity = 0;

            // Activate the current and the next testimonial
            if (i >= index && i < index + testimonialsToShow) {
                testimonial.classList.add("active");
                testimonial.style.opacity = 1;
            }
        });
        updateDots();
    }

        function nextTestimonial() {
            // Ensure the next index is within bounds
            if (window.innerWidth > 1200) {
                if (currentIndex + testimonialsToShow < testimonials.length) {
                currentIndex++;
                currentIndex++;
                } else {
                currentIndex = 0; // Reset to the start if at the end
                }
                showTestimonials(currentIndex);
            } else {
                if (currentIndex + testimonialsToShow < testimonials.length) {
                    currentIndex++;
                } else {
                currentIndex = 0; // Reset to the start if at the end
                }
                showTestimonial(currentIndex);
            }
        }

        function prevTestimonial() {
            // Ensure the previous index is within bounds
            if (window.innerWidth > 1200) {
                if (currentIndex > 0) {
                    currentIndex--;
                    currentIndex--;
                } else {
                    currentIndex = Math.max(0, testimonials.length - testimonialsToShow); // Move to the last visible pair
                }
                showTestimonials(currentIndex);
            } else {
                if (currentIndex > 0) {
                    currentIndex--;
                } else {
                    currentIndex = Math.max(0, testimonials.length - testimonialsToShow); // Move to the last visible pair
                }
                showTestimonial(currentIndex);
            }
        }

        nextButton.addEventListener("click", nextTestimonial);
        prevButton.addEventListener("click", prevTestimonial);

        // Automatically scroll every 10 seconds
        setInterval(() => {
            if (currentIndex + testimonialsToShow < testimonials.length) {
                nextTestimonial();
            } else {
                currentIndex = 0; // Reset to the first set
                showTestimonials(currentIndex);
            }
        }, 20000);

        // Initialize the first testimonial
        showTestimonials(currentIndex);
        createDots();
    });


/* === Projects Carousel === */

    document.addEventListener("DOMContentLoaded", () => {
        const carousel = document.querySelector(".carousel");
        const items = document.querySelectorAll(".carousel-item");
        const prevButton = document.getElementById("prev");
        const nextButton = document.getElementById("next");
    
        // Start with the second item as the active item
        let currentIndex = 1;
    
        function updateCarousel() {
        items.forEach((item, index) => {
            // Reset all items
            item.classList.remove("active");
            item.style.transform = "scale(0.8)";
            item.style.opacity = "0.5"; // Default dimmed
    
            if (index === currentIndex) {
            item.classList.add("active");
            item.style.transform = "scale(1.2)";
            item.style.opacity = "1";
            }
            else if (index === currentIndex - 1 || index === currentIndex + 1) {
            item.style.transform = "scale(0.9)";
            item.style.opacity = "0.8";
            }
        });
    
        // Adjust the transform of the carousel to center the active item
        const offset = -(currentIndex - 1) * (items[0].offsetWidth + 16); // Adjust for gap
        carousel.style.transform = `translateX(${offset}px)`;
        }
    
        function nextTestimonial() {
        // Loop back to the first item if at the end
        currentIndex = (currentIndex + 1) % items.length;
        updateCarousel();
        }
    
        function prevTestimonial() {
        // Loop back to the last item if at the beginning
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        updateCarousel();
        }
    
        prevButton.addEventListener("click", prevTestimonial);
        nextButton.addEventListener("click", nextTestimonial);
    
        // Initialize the carousel
        updateCarousel();
    });

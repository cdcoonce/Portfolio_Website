
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
        const prevButtonTestimonial = document.getElementById("prevRec");
        const nextButtonTestimonial = document.getElementById("nextRec");
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

        nextButtonTestimonial.addEventListener("click", nextTestimonial);
        prevButtonTestimonial.addEventListener("click", prevTestimonial);

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
        const maxDistance = Math.floor(items.length);
        const indicatorsContainer = document.querySelector(".project-indicators");
    
        // Start with the second item as the active item
        let currentIndex = 2;

        function createProjectIndicators() {
            indicatorsContainer.innerHTML = ""; // Clear existing indicators
    
            items.forEach((_, index) => {
                const indicator = document.createElement("div");
                indicator.classList.add("project-indicator");
                if (index === currentIndex) indicator.classList.add("active"); // Highlight the active indicator
                indicator.addEventListener("click", () => goToProject(index)); // Navigate to the corresponding project
                indicatorsContainer.appendChild(indicator);
            });
        }
    
        function updateProjectIndicators() {
            const indicators = document.querySelectorAll(".project-indicator");
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle("active", index === currentIndex);
            });
        }
    

        function updateCarousel() {
            items.forEach((item, index) => {
            const distance = Math.abs(index - currentIndex);



            if (window.innerWidth < 900) {
                item.classList.remove("active");
                item.style.transform = "scale(0.8)";
                item.style.opacity = "0.5";
                item.style.maxWidth = "500px";

                if (index === currentIndex) {
                    item.classList.add("active");
                    item.style.display = "block"; // Show the active item
                    item.style.opacity = "1"; // Fully visible
                    item.style.transform = "scale(1)";
                    item.style.width = "375px";
                } else {
                    item.style.display = "none"; // Hide non-active items
                }
            } else {
                item.classList.remove("active");
                item.style.transform = "scale(0.2)";
                item.style.opacity = "0.2";
                item.style.marginLeft = "8px";
                item.style.marginRight = "8px";
                item.style.maxWidth = "100px";

                if (distance === 0) {
                    item.classList.add("active");
                    item.style.transform = "scale(1.20)";
                    item.style.opacity = "1";
                    item.style.marginLeft = "40px";
                    item.style.marginRight = "40px";
                    item.style.maxWidth = "500px";
                } else if (distance <= maxDistance) {
                    const scaleFactor = 1.20 - (distance * 0.4);
                    const opacityFactor = 1 - (distance * 0.3);
                    const gapFactor = 20 - (distance * 4);
                    const maxWidthFactor = 500 - (distance * 50);

                    item.style.transform = `scale(${Math.min(1, scaleFactor)})`;
                    item.style.opacity = Math.max(0.5, opacityFactor).toString();
                    item.style.marginLeft = `${Math.min(0, -gapFactor)}px`;
                    item.style.marginRight = `${Math.min(0, -gapFactor)}px`;
                    item.style.maxWidth = `${Math.max(100, maxWidthFactor)}px`;
                }
            }
        });
    
        // Adjust the transform of the carousel to center the active item
        if (window.innerWidth >= 900) {
            const offset = -(currentIndex - 1) * (items[0].offsetWidth + 15);
            carousel.style.transform = `translateX(${offset}px)`;
        }

        updateProjectIndicators();
        
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

        function goToProject(index) {
            currentIndex = index; // Update the current index
            updateCarousel();
        }
    
        prevButton.addEventListener("click", prevTestimonial);
        nextButton.addEventListener("click", nextTestimonial);
        window.addEventListener("resize", () => {
            updateCarousel();
        });
    
        // Initialize the carousel
        updateCarousel();
        createProjectIndicators();
    });

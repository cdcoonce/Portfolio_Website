
/* === Projects Keyword Filter === */

    document.addEventListener("DOMContentLoaded", () => {
        const filters = document.querySelectorAll(".projects-filter .filter");
        const cards = document.querySelectorAll(".project-card");
    
        filters.forEach(filter => {
        filter.addEventListener("click", () => {
            // Update active filter style
            filters.forEach(f => f.classList.remove("active"));
            filter.classList.add("active");
    
            const filterValue = filter.getAttribute("data-filter");
    
            cards.forEach(card => {
            const tags = card.getAttribute("data-tags");
            // Show all cards if filter is 'all', else check if tag is included
            if (filterValue === "all" || tags.includes(filterValue)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
            });
        });
        });
    });

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


    let currentIndex = 0;

    function moveSlide(step) {
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        
        currentIndex = (currentIndex + step + totalSlides) % totalSlides;
        const offset = -currentIndex * 100;
        
        document.querySelector('.slider').style.transform = `translateX(${offset}%)`;
    }

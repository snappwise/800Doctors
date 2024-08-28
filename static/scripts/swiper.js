var swiper = new Swiper(".testimonial-swiper", {
    slidesPerView: 4,
    loop: true,
    // mousewheel: true,
    keyboard: {
        enabled: true,
    },
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    breakpoints: {
        991: {
            slidesPerView: 4
        },
        767: {
            slidesPerView: 3
        },
        567: {
            slidesPerView: 2
        },
        0: {
            slidesPerView: 1
        }
    },
    mouseGrab: true,
    spaceBetween: 20,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
});
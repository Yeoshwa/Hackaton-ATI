// Animation d'apparition des bento-box au scroll

document.addEventListener('DOMContentLoaded', function() {
    // Animation bento-box (fade/slide)
    const boxes = document.querySelectorAll('.bento-box');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('bento-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });
    boxes.forEach(box => {
        observer.observe(box);
    });

    // Animation hero section (fade-in + slide-up)
    const hero = document.querySelector('.hero-section');
    if (hero) {
        hero.style.opacity = 0;
        hero.style.transform = 'translateY(40px)';
        setTimeout(() => {
            hero.style.transition = 'opacity 0.8s cubic-bezier(.4,0,.2,1), transform 0.8s cubic-bezier(.4,0,.2,1)';
            hero.style.opacity = 1;
            hero.style.transform = 'translateY(0)';
        }, 200);
    }

    // Animation section titles (fade-in)
    document.querySelectorAll('.section-title').forEach((el, i) => {
        el.style.opacity = 0;
        el.style.transform = 'translateY(30px)';
        setTimeout(() => {
            el.style.transition = 'opacity 0.7s '+(0.2+i*0.1)+'s cubic-bezier(.4,0,.2,1), transform 0.7s '+(0.2+i*0.1)+'s cubic-bezier(.4,0,.2,1)';
            el.style.opacity = 1;
            el.style.transform = 'translateY(0)';
        }, 300);
    });

    // Animation stat-box (zoom-in)
    document.querySelectorAll('.stat-box').forEach((el, i) => {
        el.style.opacity = 0;
        el.style.transform = 'scale(0.85)';
        setTimeout(() => {
            el.style.transition = 'opacity 0.7s '+(0.3+i*0.1)+'s cubic-bezier(.4,0,.2,1), transform 0.7s '+(0.3+i*0.1)+'s cubic-bezier(.4,0,.2,1)';
            el.style.opacity = 1;
            el.style.transform = 'scale(1)';
        }, 400);
    });

    // Animation testimonials (fade-in left/right)
    document.querySelectorAll('.testimonial').forEach((el, i) => {
        el.style.opacity = 0;
        el.style.transform = i%2===0 ? 'translateX(-40px)' : 'translateX(40px)';
        setTimeout(() => {
            el.style.transition = 'opacity 0.7s '+(0.4+i*0.1)+'s cubic-bezier(.4,0,.2,1), transform 0.7s '+(0.4+i*0.1)+'s cubic-bezier(.4,0,.2,1)';
            el.style.opacity = 1;
            el.style.transform = 'translateX(0)';
        }, 500);
    });

    // Animation contact form (fade-in)
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.style.opacity = 0;
        setTimeout(() => {
            contactForm.style.transition = 'opacity 0.8s 0.7s cubic-bezier(.4,0,.2,1)';
            contactForm.style.opacity = 1;
        }, 700);
    }
});
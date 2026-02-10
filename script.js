document.addEventListener('DOMContentLoaded', () => {
    // Mobile Navigation Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.nav');

    if (navToggle && nav) {
        navToggle.addEventListener('click', () => {
            const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', !isExpanded);
            nav.classList.toggle('nav--open');
        });
    }

    // Close mobile menu when a link is clicked
    const navLinks = document.querySelectorAll('.nav__link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (nav.classList.contains('nav--open')) {
                nav.classList.remove('nav--open');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    });

    // Smooth scrolling for anchor links (safeguard for older browsers, though CSS does most of it)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Account for fixed header height
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.scrollY - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Header opacity control on homepage only
    const isHomepage = window.location.pathname.endsWith('index.html') ||
        window.location.pathname.endsWith('/') ||
        window.location.pathname === '';

    if (isHomepage) {
        const header = document.querySelector('.header');

        function updateHeaderBackground() {
            const scrollPosition = window.scrollY;

            if (scrollPosition === 0) {
                // At the top - transparent background
                header.style.backgroundColor = 'transparent';
                header.style.boxShadow = 'none';
                header.style.transition = 'background-color 0.3s ease, box-shadow 0.3s ease';
            } else {
                // Scrolled down - solid background
                header.style.backgroundColor = 'var(--color-primary)';
                header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
                header.style.transition = 'background-color 0.3s ease, box-shadow 0.3s ease';
            }
        }

        // Initial check
        updateHeaderBackground();

        // Update on scroll
        window.addEventListener('scroll', updateHeaderBackground);
    }

    // --- Animation Initialization ---
    // 1. Landing Page Animations
    const heroContent = document.querySelector('.hero__content');
    if (heroContent) {
        const subtitle = heroContent.querySelector('.hero__subtitle');
        const actions = heroContent.querySelector('.hero__actions');

        if (subtitle) {
            subtitle.classList.add('hero-animate');
            subtitle.classList.add('delay-100');
        }

        if (actions) {
            const buttons = actions.querySelectorAll('.btn');
            buttons.forEach((btn, index) => {
                btn.classList.add('hero-animate');
                // Stagger button animations: 200ms, 300ms, etc.
                if (index === 0) btn.classList.add('delay-200');
                if (index === 1) btn.classList.add('delay-300');
            });
        }
    }

    // 2. Scroll Animations (Intersection Observer)
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% of element is visible
    };

    const scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Animate only once
            }
        });
    }, observerOptions);

    const scrollElements = document.querySelectorAll('.animate-on-scroll');
    scrollElements.forEach(el => scrollObserver.observe(el));
});

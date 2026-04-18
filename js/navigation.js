/* ============================================
   Direct Research Korea — Navigation
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
  // --- Navbar scroll effect ---
  const nav = document.querySelector('.nav');
  if (nav) {
    let lastScrollY = 0;
    const handleScroll = () => {
      const scrollY = window.scrollY;
      if (scrollY > 50) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
      lastScrollY = scrollY;
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // --- Mobile menu toggle ---
  const toggle = document.querySelector('.nav__toggle');
  const mobileMenu = document.querySelector('.nav__mobile');
  
  if (toggle && mobileMenu) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('open');
      mobileMenu.classList.toggle('open');
      document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
    });

    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        toggle.classList.remove('open');
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  // --- Active link highlighting ---
  const currentPath = window.location.pathname.replace(/\/+$/, '') || '/';
  document.querySelectorAll('.nav__link, .nav__dropdown-item').forEach(link => {
    const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/+$/, '') || '/';
    if (linkPath === currentPath) {
      link.classList.add('active');
    }
  });

  // --- Scroll reveal animation ---
  const revealElements = document.querySelectorAll('.reveal');
  if (revealElements.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
  }

  // --- Back to top button ---
  const backToTop = document.querySelector('.back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 500) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    }, { passive: true });

    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Smooth anchor scroll ---
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // --- Hero particles ---
  const particleContainer = document.querySelector('.hero__particles');
  if (particleContainer) {
    for (let i = 0; i < 30; i++) {
      const particle = document.createElement('div');
      particle.classList.add('hero__particle');
      particle.style.left = Math.random() * 100 + '%';
      particle.style.animationDelay = Math.random() * 15 + 's';
      particle.style.animationDuration = (10 + Math.random() * 20) + 's';
      particle.style.width = (1 + Math.random() * 2) + 'px';
      particle.style.height = particle.style.width;
      particleContainer.appendChild(particle);
    }
  }
});

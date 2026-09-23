(function () {
  "use strict";

  // ---------------------------------------------------------------
  // Mobile menu
  // ---------------------------------------------------------------
  const menuToggle = document.querySelector("[data-mobile-menu-toggle]");
  const menuClose = document.querySelector("[data-mobile-menu-close]");
  const menuBackdrop = document.querySelector("[data-mobile-menu-backdrop]");

  function openMenu() {
    if (!menuBackdrop) return;
    menuBackdrop.classList.remove("hidden");
    document.body.classList.add("overflow-hidden");
    menuToggle && menuToggle.setAttribute("aria-expanded", "true");
  }
  function closeMenu() {
    if (!menuBackdrop) return;
    menuBackdrop.classList.add("hidden");
    document.body.classList.remove("overflow-hidden");
    menuToggle && menuToggle.setAttribute("aria-expanded", "false");
  }
  menuToggle && menuToggle.addEventListener("click", openMenu);
  menuClose && menuClose.addEventListener("click", closeMenu);
  menuBackdrop &&
    menuBackdrop.addEventListener("click", function (e) {
      if (e.target === menuBackdrop) closeMenu();
    });

  // ---------------------------------------------------------------
  // Desktop dropdowns (Gallery / More)
  // ---------------------------------------------------------------
  document.querySelectorAll("[data-dropdown]").forEach(function (dropdown) {
    const toggle = dropdown.querySelector("[data-dropdown-toggle]");
    const menu = dropdown.querySelector("[data-dropdown-menu]");
    if (!toggle || !menu) return;

    function show() {
      menu.classList.remove("opacity-0", "invisible", "translate-y-1");
    }
    function hide() {
      menu.classList.add("opacity-0", "invisible", "translate-y-1");
    }
    dropdown.addEventListener("mouseenter", show);
    dropdown.addEventListener("mouseleave", hide);
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      menu.classList.contains("invisible") ? show() : hide();
    });
    document.addEventListener("click", function (e) {
      if (!dropdown.contains(e.target)) hide();
    });
  });

  // ---------------------------------------------------------------
  // Hero slider (auto-rotating fade slides)
  // ---------------------------------------------------------------
  const slider = document.querySelector("[data-hero-slider]");
  if (slider) {
    const slides = Array.from(slider.querySelectorAll("[data-hero-slide]"));
    const dots = Array.from(slider.querySelectorAll("[data-hero-dot]"));
    let current = 0;
    let timer = null;

    function goTo(index) {
      slides.forEach(function (slide, i) {
        slide.classList.toggle("opacity-100", i === index);
        slide.classList.toggle("opacity-0", i !== index);
        slide.classList.toggle("pointer-events-none", i !== index);
      });
      dots.forEach(function (dot, i) {
        dot.classList.toggle("bg-brand-gold", i === index);
        dot.classList.toggle("w-8", i === index);
        dot.classList.toggle("bg-white/50", i !== index);
        dot.classList.toggle("w-2.5", i !== index);
      });
      current = index;
    }
    function next() {
      goTo((current + 1) % slides.length);
    }
    function restart() {
      clearInterval(timer);
      timer = setInterval(next, 6000);
    }
    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () {
        goTo(i);
        restart();
      });
    });
    if (slides.length > 1) {
      goTo(0);
      restart();
    }
  }

  // ---------------------------------------------------------------
  // Animated stat counters (triggered on scroll into view)
  // ---------------------------------------------------------------
  const counters = document.querySelectorAll("[data-counter]");
  if (counters.length && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const target = parseInt(el.getAttribute("data-counter"), 10) || 0;
          const duration = 1400;
          const start = performance.now();
          function tick(now) {
            const progress = Math.min((now - start) / duration, 1);
            el.textContent = Math.floor(progress * target).toLocaleString();
            if (progress < 1) requestAnimationFrame(tick);
            else el.textContent = target.toLocaleString();
          }
          requestAnimationFrame(tick);
          observer.unobserve(el);
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach(function (el) {
      observer.observe(el);
    });
  }

  // ---------------------------------------------------------------
  // FAQ accordion
  // ---------------------------------------------------------------
  document.querySelectorAll("[data-faq-item]").forEach(function (item) {
    const btn = item.querySelector("[data-faq-question]");
    const panel = item.querySelector("[data-faq-answer]");
    if (!btn || !panel) return;
    btn.addEventListener("click", function () {
      const isOpen = item.getAttribute("data-open") === "true";
      document.querySelectorAll("[data-faq-item]").forEach(function (other) {
        other.setAttribute("data-open", "false");
        other.querySelector("[data-faq-answer]").style.maxHeight = null;
        const icon = other.querySelector("[data-faq-icon]");
        if (icon) icon.style.transform = "rotate(0deg)";
      });
      if (!isOpen) {
        item.setAttribute("data-open", "true");
        panel.style.maxHeight = panel.scrollHeight + "px";
        const icon = item.querySelector("[data-faq-icon]");
        if (icon) icon.style.transform = "rotate(180deg)";
      }
    });
  });

  // ---------------------------------------------------------------
  // Destinations search/filter (client-side quick filter, form still
  // submits server-side for full results / pagination)
  // ---------------------------------------------------------------
  const filterInput = document.querySelector("[data-live-filter]");
  if (filterInput) {
    filterInput.addEventListener("input", function () {
      const term = filterInput.value.trim().toLowerCase();
      document.querySelectorAll("[data-filter-item]").forEach(function (item) {
        const label = (item.getAttribute("data-filter-label") || "").toLowerCase();
        item.classList.toggle("hidden", term.length > 0 && !label.includes(term));
      });
    });
  }

  // ---------------------------------------------------------------
  // Simple photo lightbox
  // ---------------------------------------------------------------
  const lightbox = document.querySelector("[data-lightbox]");
  if (lightbox) {
    const lightboxImg = lightbox.querySelector("[data-lightbox-img]");
    const lightboxCaption = lightbox.querySelector("[data-lightbox-caption]");
    document.querySelectorAll("[data-lightbox-trigger]").forEach(function (trigger) {
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        lightboxImg.setAttribute("src", trigger.getAttribute("href"));
        lightboxCaption.textContent = trigger.getAttribute("data-caption") || "";
        lightbox.classList.remove("hidden");
        document.body.classList.add("overflow-hidden");
      });
    });
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox || e.target.closest("[data-lightbox-close]")) {
        lightbox.classList.add("hidden");
        lightboxImg.setAttribute("src", "");
        document.body.classList.remove("overflow-hidden");
      }
    });
  }
})();

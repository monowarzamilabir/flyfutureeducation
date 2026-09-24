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

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // ---------------------------------------------------------------
  // Hero carousel: photo wipes in per slide, headline rises word by word
  // ---------------------------------------------------------------
  const hero = document.querySelector("[data-hero]");
  if (hero) {
    const photos = Array.from(hero.querySelectorAll("[data-hero-photo]"));
    const copies = Array.from(hero.querySelectorAll("[data-hero-copy]"));
    const progress = hero.querySelector("[data-hero-progress]");
    const counter = hero.querySelector("[data-hero-current]");
    const toggle = hero.querySelector("[data-hero-toggle]");
    const live = hero.querySelector("[data-hero-live]");
    let current = -1;
    let userPaused = reduceMotion;
    let focusHold = false;

    hero.querySelectorAll("[data-split]").forEach(function (el) {
      const text = el.textContent.trim();
      el.setAttribute("aria-label", text);
      el.innerHTML = text
        .split(/\s+/)
        .map(function (word, i) {
          return '<span class="split-word" aria-hidden="true"><span style="--i:' + i + '">' + escapeHtml(word) + "</span></span>";
        })
        .join(" ");
    });

    function syncPaused() {
      hero.classList.toggle("is-paused", userPaused || focusHold || document.hidden);
      hero.classList.toggle("is-stopped", userPaused);
      if (toggle) {
        toggle.setAttribute("aria-label", userPaused ? "Play slideshow" : "Pause slideshow");
        toggle.setAttribute("aria-pressed", String(userPaused));
      }
      if (live) live.setAttribute("aria-live", userPaused ? "polite" : "off");
    }

    function restartProgress() {
      if (!progress) return;
      progress.classList.remove("is-running");
      void progress.offsetWidth;
      progress.classList.add("is-running");
    }

    function goTo(index, dir) {
      const next = (index + photos.length) % photos.length;
      if (next === current) return;
      const prev = current;
      current = next;

      if (prev >= 0) {
        const oldPhoto = photos[prev];
        const oldCopy = copies[prev];
        oldPhoto.classList.remove("is-active");
        oldPhoto.classList.add("is-leaving");
        oldCopy.classList.remove("is-active");
        oldCopy.classList.add("is-leaving");
        setTimeout(function () {
          oldPhoto.classList.remove("is-leaving");
        }, reduceMotion ? 0 : 1300);
        setTimeout(function () {
          oldCopy.classList.remove("is-leaving");
        }, reduceMotion ? 0 : 600);
      }

      const photo = photos[current];
      photo.classList.remove("is-leaving");
      photo.style.transition = "none";
      photo.style.clipPath = dir < 0 ? "inset(0 100% 0 0)" : "inset(0 0 0 100%)";
      void photo.offsetWidth;
      photo.style.transition = "";
      photo.style.clipPath = "";
      photo.classList.add("is-active");

      copies[current].classList.remove("is-leaving");
      copies[current].classList.add("is-active");
      if (counter) counter.textContent = String(current + 1).padStart(2, "0");
      restartProgress();
    }

    progress &&
      progress.addEventListener("animationend", function () {
        goTo(current + 1, 1);
      });
    hero.querySelector("[data-hero-next]").addEventListener("click", function () {
      goTo(current + 1, 1);
    });
    hero.querySelector("[data-hero-prev]").addEventListener("click", function () {
      goTo(current - 1, -1);
    });
    toggle &&
      toggle.addEventListener("click", function () {
        userPaused = !userPaused;
        syncPaused();
      });
    hero.addEventListener("focusin", function () {
      focusHold = true;
      syncPaused();
    });
    hero.addEventListener("focusout", function (e) {
      if (hero.contains(e.relatedTarget)) return;
      focusHold = false;
      syncPaused();
    });
    document.addEventListener("visibilitychange", syncPaused);

    let touchX = null;
    hero.addEventListener("touchstart", function (e) {
      touchX = e.touches[0].clientX;
    }, { passive: true });
    hero.addEventListener("touchend", function (e) {
      if (touchX === null) return;
      const dx = e.changedTouches[0].clientX - touchX;
      touchX = null;
      if (Math.abs(dx) > 50) dx < 0 ? goTo(current + 1, 1) : goTo(current - 1, -1);
    }, { passive: true });

    if (finePointer && !reduceMotion) {
      let tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
      function drift() {
        cx += (tx - cx) * 0.06;
        cy += (ty - cy) * 0.06;
        hero.style.setProperty("--mx", cx.toFixed(4));
        hero.style.setProperty("--my", cy.toFixed(4));
        raf = Math.abs(tx - cx) + Math.abs(ty - cy) > 0.001 ? requestAnimationFrame(drift) : null;
      }
      hero.addEventListener("pointermove", function (e) {
        const r = hero.getBoundingClientRect();
        tx = ((e.clientX - r.left) / r.width - 0.5) * 2;
        ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
        if (!raf) raf = requestAnimationFrame(drift);
      });
      hero.addEventListener("pointerleave", function () {
        tx = ty = 0;
        if (!raf) raf = requestAnimationFrame(drift);
      });
    }

    syncPaused();
    goTo(0, 1);
  }

  // ---------------------------------------------------------------
  // Trailing cursor + card photos that drift with the pointer
  // ---------------------------------------------------------------
  if (finePointer && !reduceMotion) {
    const ring = document.createElement("div");
    const dot = document.createElement("div");
    const label = document.createElement("span");
    ring.className = "cursor-ring";
    dot.className = "cursor-dot";
    label.className = "cursor-label";
    ring.setAttribute("aria-hidden", "true");
    dot.setAttribute("aria-hidden", "true");
    ring.appendChild(label);
    document.body.append(ring, dot);

    let x = -100, y = -100, rx = -100, ry = -100, raf = null;
    function follow() {
      rx += (x - rx) * 0.18;
      ry += (y - ry) * 0.18;
      ring.style.transform = "translate3d(" + rx + "px," + ry + "px,0)";
      raf = Math.abs(x - rx) + Math.abs(y - ry) > 0.2 ? requestAnimationFrame(follow) : null;
    }
    document.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      x = e.clientX;
      y = e.clientY;
      dot.style.transform = "translate3d(" + x + "px," + y + "px,0)";
      document.documentElement.classList.add("has-cursor");
      if (!raf) raf = requestAnimationFrame(follow);
    }, { passive: true });
    document.documentElement.addEventListener("mouseleave", function () {
      document.documentElement.classList.remove("has-cursor");
    });
    document.addEventListener("pointerover", function (e) {
      const labelled = e.target.closest("[data-cursor]");
      const interactive = e.target.closest("a, button, select, label[for], [role='button']");
      ring.classList.toggle("is-label", !!labelled);
      ring.classList.toggle("is-hover", !labelled && !!interactive);
      label.textContent = labelled ? labelled.getAttribute("data-cursor") : "";
    });

    document.addEventListener("pointermove", function (e) {
      const card = e.target.closest && e.target.closest("[data-drift]");
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty("--px", (((e.clientX - r.left) / r.width - 0.5) * 2).toFixed(3));
      card.style.setProperty("--py", (((e.clientY - r.top) / r.height - 0.5) * 2).toFixed(3));
    }, { passive: true });
    document.addEventListener("pointerout", function (e) {
      const card = e.target.closest && e.target.closest("[data-drift]");
      if (card && !card.contains(e.relatedTarget)) {
        card.style.setProperty("--px", "0");
        card.style.setProperty("--py", "0");
      }
    });
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

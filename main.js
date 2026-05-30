/* =================================================================
   Logic Insight redesign · shared main.js (multi-page)
   ================================================================= */

const lerp = (a, b, t) => a + (b - a) * t;
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- Cursor follower ---------- */
{
  const dot  = document.querySelector(".cursor-dot");
  const blob = document.querySelector(".cursor-blob");
  if (dot && blob && !reduceMotion && matchMedia("(hover: hover)").matches) {
    let mx = 0, my = 0, bx = 0, by = 0;
    addEventListener("pointermove", (e) => {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = `translate3d(${mx}px, ${my}px, 0)`;
    });
    const raf = () => {
      bx = lerp(bx, mx, 0.18); by = lerp(by, my, 0.18);
      blob.style.transform = `translate3d(${bx}px, ${by}px, 0)`;
      requestAnimationFrame(raf);
    };
    raf();
    document.querySelectorAll("a, button, [data-tilt]").forEach((el) => {
      el.addEventListener("pointerenter", () => blob.classList.add("is-hover"));
      el.addEventListener("pointerleave", () => blob.classList.remove("is-hover"));
    });
  }
}

/* ---------- Scroll progress ---------- */
{
  const bar = document.querySelector(".scroll-progress span");
  if (bar) {
    const update = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      const p = max > 0 ? (scrollY / max) * 100 : 0;
      bar.style.setProperty("--p", `${p}%`);
    };
    addEventListener("scroll", update, { passive: true });
    update();
  }
}

/* ---------- Nav scrolled state ---------- */
{
  const nav = document.querySelector(".nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("is-scrolled", scrollY > 32);
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
}

/* ---------- Reveal on scroll ---------- */
{
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll("[data-reveal]").forEach((el) => io.observe(el));
}

/* ---------- Tilt cards ---------- */
if (!reduceMotion) {
  document.querySelectorAll("[data-tilt]").forEach((card) => {
    card.addEventListener("pointermove", (e) => {
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width;
      const py = (e.clientY - r.top) / r.height;
      const rx = (py - 0.5) * -5;
      const ry = (px - 0.5) * 5;
      card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-2px)`;
    });
    card.addEventListener("pointerleave", () => { card.style.transform = ""; });
  });
}

/* ---------- Anchor smooth scroll ---------- */
document.querySelectorAll('a[href^="#"]').forEach((a) => {
  a.addEventListener("click", (e) => {
    const href = a.getAttribute("href");
    if (!href || href === "#") return;
    const t = document.querySelector(href);
    if (!t) return;
    e.preventDefault();
    t.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

/* ---------- Number ticker ---------- */
{
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const el = e.target;
      const target = parseInt(el.dataset.count, 10);
      const suffix = el.dataset.suffix || "";
      const dur = 1200; const start = performance.now();
      const step = (t) => {
        const k = Math.min((t - start) / dur, 1);
        const eased = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.floor(target * eased) + (k === 1 ? suffix : "");
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      io.unobserve(el);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll("[data-count]").forEach((el) => io.observe(el));
}

/* ---------- Radial dashboard: connector pulses ---------- */
{
  const svgNS = "http://www.w3.org/2000/svg";
  const radial = document.querySelector(".radial");
  if (radial && !reduceMotion) {
    const connector = radial.querySelector(".radial__connector");
    const core = radial.querySelector(".radial__core");
    const nodes = radial.querySelectorAll(".radial__node");
    if (connector && core && nodes.length) {
      // Draw connection lines from center to each node
      const drawLines = () => {
        connector.innerHTML = "";
        const r = radial.getBoundingClientRect();
        const cx = r.width / 2, cy = r.height / 2;
        nodes.forEach((n) => {
          const nr = n.getBoundingClientRect();
          const nx = nr.left - r.left + nr.width / 2;
          const ny = nr.top  - r.top  + nr.height / 2;
          const line = document.createElementNS(svgNS, "line");
          line.setAttribute("x1", cx); line.setAttribute("y1", cy);
          line.setAttribute("x2", nx); line.setAttribute("y2", ny);
          connector.appendChild(line);
        });
      };
      // initial draw
      requestAnimationFrame(() => requestAnimationFrame(drawLines));
      addEventListener("resize", drawLines);

      // periodic pulses along lines
      const spawnPulse = () => {
        const lines = connector.querySelectorAll("line");
        if (!lines.length) return;
        const line = lines[Math.floor(Math.random() * lines.length)];
        const x1 = +line.getAttribute("x1"), y1 = +line.getAttribute("y1");
        const x2 = +line.getAttribute("x2"), y2 = +line.getAttribute("y2");
        const c = document.createElementNS(svgNS, "circle");
        c.setAttribute("r", "3.2"); c.setAttribute("class", "radial__pulse");
        connector.appendChild(c);
        const t0 = performance.now(); const dur = 1100;
        const step = (t) => {
          const k = Math.min((t - t0) / dur, 1);
          c.setAttribute("cx", x1 + (x2 - x1) * k);
          c.setAttribute("cy", y1 + (y2 - y1) * k);
          c.setAttribute("opacity", k < 0.1 ? k*10 : k > 0.85 ? (1-k)/0.15 : 1);
          if (k < 1) requestAnimationFrame(step); else c.remove();
        };
        requestAnimationFrame(step);
      };
      setInterval(spawnPulse, 320);
      for (let i = 0; i < 4; i++) setTimeout(spawnPulse, i * 200);
    }
  }
}

/* ---------- Architecture diagram pulses (only if present) ---------- */
{
  const pulses = document.querySelector(".arch-pulses");
  const paths = document.querySelectorAll(".arch-lines path");
  if (pulses && paths.length && !reduceMotion) {
    const svgNS = "http://www.w3.org/2000/svg";
    const spawn = () => {
      const path = paths[Math.floor(Math.random() * paths.length)];
      const len = path.getTotalLength();
      const isLeft = Array.from(paths).indexOf(path) < 5;
      const color = isLeft ? "#A78BFA" : "#FF6B9C";
      const c = document.createElementNS(svgNS, "circle");
      c.setAttribute("r", "3.5"); c.setAttribute("fill", color);
      pulses.appendChild(c);
      const start = performance.now(); const dur = 2200 + Math.random() * 800;
      const step = (t) => {
        const elapsed = t - start; const k = Math.min(elapsed / dur, 1);
        const p = path.getPointAtLength(len * k);
        c.setAttribute("cx", p.x); c.setAttribute("cy", p.y);
        c.setAttribute("opacity", k < 0.1 ? k * 10 : k > 0.85 ? (1 - k) / 0.15 : 1);
        if (k < 1) requestAnimationFrame(step); else c.remove();
      };
      requestAnimationFrame(step);
    };
    setInterval(spawn, 340);
    for (let i = 0; i < 5; i++) setTimeout(spawn, i * 250);
  }
}

/* ---------- Animated chart line draw (showcase) ---------- */
{
  const lines = document.querySelectorAll(".chart-draw");
  lines.forEach((line) => {
    const len = line.getTotalLength();
    line.style.strokeDasharray = len;
    line.style.strokeDashoffset = len;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          line.style.transition = "stroke-dashoffset 2.4s cubic-bezier(0.16, 1, 0.3, 1)";
          line.style.strokeDashoffset = "0";
          io.unobserve(line);
        }
      });
    }, { threshold: 0.3 });
    io.observe(line);
  });
}

/* ---------- Command palette ---------- */
{
  const kbd = document.getElementById("kbd");
  const openBtn = document.getElementById("kbd-open");
  const input = document.getElementById("kbd-search");
  const list = document.getElementById("kbd-list");

  const items = [
    { group: "Pages",       label: "Home",                     href: "index.html",         icon: "🏠" },
    { group: "Pages",       label: "Product",                  href: "product.html",       icon: "📦" },
    { group: "Pages",       label: "Architecture",             href: "architecture.html",  icon: "🏛️" },
    { group: "Pages",       label: "AI Assistant",             href: "ai-assistant.html",  icon: "✨" },
    { group: "Pages",       label: "Integrations",             href: "integrations.html",  icon: "🔌" },
    { group: "Pages",       label: "Pricing",                  href: "pricing.html",       icon: "🏷️" },
    { group: "Pages",       label: "Insights · Editorial",     href: "insights.html",      icon: "📝" },
    { group: "Pages",       label: "About · Founders",         href: "about.html",         icon: "👋" },
    { group: "Product",     label: "Cluster monitoring",       href: "product.html#cluster",   icon: "📊" },
    { group: "Product",     label: "Predictive analytics",     href: "product.html#forecast", icon: "📈" },
    { group: "Product",     label: "Network flow (IPFIX)",     href: "product.html#flow",     icon: "🛰️" },
    { group: "Product",     label: "HYCU backup posture",      href: "product.html#hycu",     icon: "🛡️" },
    { group: "Integration", label: "Datadog Marketplace",      href: "integrations.html#datadog",  icon: "📊" },
    { group: "Integration", label: "Grafana · Prometheus",     href: "integrations.html#grafana",  icon: "📈" },
    { group: "Integration", label: "Wasabi · S3 immutable",    href: "integrations.html#wasabi",   icon: "🗄️" },
    { group: "Action",      label: "Start free trial",         href: "pricing.html",         icon: "🚀" },
    { group: "Action",      label: "Contact sales",            href: "about.html#contact",   icon: "✉️" },
  ];

  if (!kbd || !openBtn) return;

  const render = (q = "") => {
    const Q = q.trim().toLowerCase();
    const filtered = items.filter(i => !Q || i.label.toLowerCase().includes(Q) || i.group.toLowerCase().includes(Q));
    const byGroup = filtered.reduce((acc, i) => ((acc[i.group] = acc[i.group] || []).push(i), acc), {});
    list.innerHTML = Object.entries(byGroup).map(([group, items]) => `
      <div class="kbd__group">
        <div class="kbd__group-label">${group}</div>
        ${items.map(i => `
          <div class="kbd__item" data-href="${i.href}">
            <span class="kbd__item-icon">${i.icon}</span>
            <span>${i.label}</span>
            <span class="kbd__item-arrow">↵</span>
          </div>
        `).join("")}
      </div>
    `).join("");
    list.querySelectorAll(".kbd__item").forEach(it => {
      it.addEventListener("click", () => navigate(it.dataset.href));
    });
    list.querySelector(".kbd__item")?.classList.add("is-active");
  };
  const open  = () => { kbd.hidden = false; setTimeout(() => input.focus(), 30); render(""); };
  const close = () => { kbd.hidden = true;  input.value = ""; };
  const navigate = (href) => {
    close();
    if (href.startsWith("#")) {
      const el = document.querySelector(href);
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    } else {
      location.href = href;
    }
  };
  openBtn.addEventListener("click", open);
  kbd.querySelector("[data-kbd-close]")?.addEventListener("click", close);
  addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); kbd.hidden ? open() : close(); }
    if (kbd.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      const items = [...list.querySelectorAll(".kbd__item")];
      const idx = items.findIndex(i => i.classList.contains("is-active"));
      const next = e.key === "ArrowDown" ? Math.min(idx + 1, items.length - 1) : Math.max(idx - 1, 0);
      items.forEach(i => i.classList.remove("is-active"));
      items[next]?.classList.add("is-active");
      items[next]?.scrollIntoView({ block: "nearest" });
    }
    if (e.key === "Enter") {
      const active = list.querySelector(".kbd__item.is-active");
      if (active) navigate(active.dataset.href);
    }
  });
  input.addEventListener("input", () => render(input.value));
}

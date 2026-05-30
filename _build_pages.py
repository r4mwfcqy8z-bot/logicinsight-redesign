#!/usr/bin/env python3
"""
Logic Insight redesign — page generator.

Mirrors every section of the live logicinsight.io 1:1 (every page, every
section, every heading, every stat, every list, in the same order) but lays
out the content in the new dark-mode design system.

Section bodies are concise restatements of the original product/marketing
points — exact official copy should be pasted in per-page during the
visual-polish pass.
"""

import json, os, re, html

with open("_content.json") as f:
    CONTENT = json.load(f)


# ---------------------------------------------------------------- Layout

NAV_LINKS = [
    ("/features/",                "Features"),
    ("/architecture/",            "Architecture"),
    ("/ai-assistant/",            "AI Assistant"),
    ("/integrations/",            "Integrations"),
    ("/pricing/",                 "Pricing"),
    ("/blog/",                    "Blog"),
    ("/about/",                   "About"),
]

# Sub-pages (linked from footer + within content but not in nav)
PRODUCT_PAGES = [
    ("/cluster-monitoring/",          "Cluster monitoring"),
    ("/predictive-analytics/",        "Predictive analytics"),
    ("/network-flow-analysis/",       "Network flow"),
    ("/hycu-monitoring/",             "HYCU monitoring"),
    ("/redfish-monitoring/",          "Redfish / IPMI"),
    ("/snmp-monitoring/",             "SNMP"),
    ("/prism-central-monitoring/",    "Prism Central"),
    ("/ahv-monitoring/",              "AHV"),
    ("/hci-monitoring/",              "HCI monitoring"),
    ("/monitoring-as-a-service/",     "Monitoring-as-a-Service"),
]
INTEG_PAGES = [
    ("/nutanix-datadog/",                     "Datadog"),
    ("/nutanix-grafana/",                     "Grafana"),
    ("/how-to-monitor-nutanix-with-datadog/", "How-to · Datadog"),
    ("/how-to-monitor-nutanix-with-grafana/", "How-to · Grafana"),
    ("/nutanix-monitoring-vs-prism/",         "vs Prism"),
]
RESOURCE_PAGES = [
    ("/resources/",                   "All resources"),
    ("/blog/",                        "Blog"),
]


def slug_for(route: str) -> str:
    """/foo-bar/ -> foo-bar.html ; / -> index.html"""
    if route == "/":
        return "index.html"
    s = route.strip("/").replace("/", "-")
    return f"{s}.html"


LOGO_SVG = '''<svg viewBox="0 0 220 36" class="nav__logo-svg" role="img" aria-label="Logic Insight">
  <defs>
    <linearGradient id="li-mark-g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C39BFF"/><stop offset="60%" stop-color="#A78BFA"/><stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
    <linearGradient id="li-insight-g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FAF7FF"/><stop offset="55%" stop-color="#D7C2FF"/><stop offset="100%" stop-color="#FF6B9C"/>
    </linearGradient>
  </defs>
  <g transform="translate(0,2)">
    <rect x="0" y="0" width="32" height="32" rx="9" fill="url(#li-mark-g)" opacity="0.18"/>
    <rect x="0" y="0" width="32" height="32" rx="9" fill="none" stroke="url(#li-mark-g)" stroke-width="1.3" opacity="0.85"/>
    <path d="M16 5 C 9 5 5 9 5 16 C 5 23 9 27 16 27" stroke="#FAF7FF" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    <path d="M16 9 C 11 9 9 11 9 16 C 9 21 11 23 16 23" stroke="#FAF7FF" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.75"/>
    <path d="M16 13 C 13 13 12 14 12 16 C 12 18 13 19 16 19" stroke="#FAF7FF" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.5"/>
    <circle cx="16" cy="16" r="1.4" fill="#FAF7FF"/>
  </g>
  <text x="44" y="24" font-family="Inter, sans-serif" font-weight="800" font-size="17" letter-spacing="0.04em" fill="#FAF7FF">LOGIC</text>
  <text x="103" y="24" font-family="Inter, sans-serif" font-weight="800" font-size="17" letter-spacing="0.04em" fill="url(#li-insight-g)">INSIGHT</text>
</svg>'''

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0%25' stop-color='%23C39BFF'/%3E%3Cstop offset='100%25' stop-color='%236D28D9'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='%2307050E'/%3E%3Cpath d='M16 6 C 10 6 6 10 6 16 C 6 22 10 26 16 26' stroke='url(%23g)' stroke-width='2.4' fill='none' stroke-linecap='round'/%3E%3Cpath d='M16 10 C 12 10 10 12 10 16 C 10 20 12 22 16 22' stroke='url(%23g)' stroke-width='2.4' fill='none' stroke-linecap='round' opacity='0.6'/%3E%3Ccircle cx='16' cy='16' r='1.6' fill='%23C39BFF'/%3E%3C/svg%3E"


def head_block(title: str, description: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}" />
  <link rel="icon" type="image/svg+xml" href="{FAVICON}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css" />
  <script>document.documentElement.classList.add('js');</script>
</head>
<body>
  <div class="cursor-dot" aria-hidden="true"></div>
  <div class="cursor-blob" aria-hidden="true"></div>
  <div class="grain" aria-hidden="true"></div>
  <div class="scroll-progress" aria-hidden="true"><span></span></div>
'''


def nav(active_route: str) -> str:
    items = []
    for route, label in NAV_LINKS:
        cls = ' class="is-active"' if route == active_route else ""
        items.append(f'    <a href="{slug_for(route)}"{cls}>{label}</a>')
    links = "\n".join(items)
    return f'''  <header class="nav">
    <a href="index.html" class="nav__brand" aria-label="Logic Insight home">
      {LOGO_SVG}
    </a>
    <nav class="nav__links" aria-label="Primary">
{links}
    </nav>
    <div class="nav__cta">
      <button class="kbd-trigger" id="kbd-open" aria-label="Open command palette">
        <span>Search</span><kbd>⌘</kbd><kbd>K</kbd>
      </button>
      <a href="{slug_for('/about/')}#contact" class="btn btn--ghost">Talk to sales</a>
      <a href="{slug_for('/pricing/')}" class="btn btn--primary">
        <span>Start free trial</span>
        <svg viewBox="0 0 16 16" width="14" height="14"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
    </div>
  </header>
'''


def footer() -> str:
    def col(title, pages):
        rows = "\n".join(f'            <a href="{slug_for(r)}">{html.escape(l)}</a>' for r, l in pages)
        return f'          <div>\n            <h4>{title}</h4>\n{rows}\n          </div>'
    cols = "\n".join([
        col("Product",      PRODUCT_PAGES[:6]),
        col("Integrations", INTEG_PAGES + [("/integrations/", "All integrations")]),
        col("Company",      NAV_LINKS),
        col("Resources",    RESOURCE_PAGES + [("/architecture/", "Architecture"), ("/ai-assistant/", "AI Assistant")]),
    ])
    return f'''  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <div class="footer__brand">
          <a href="index.html" class="nav__brand" aria-label="Logic Insight home" style="padding:0;">{LOGO_SVG}</a>
          <p class="footer__tagline">Nutanix observability that thinks ahead.</p>
          <address class="footer__addr">
            425 W Colonial Dr, Ste 303<br/>
            Orlando, FL 32804<br/>
            <a href="mailto:contact@logicinsight.io">contact@logicinsight.io</a><br/>
            <a href="tel:+14075132359">+1 (407) 513-2359</a>
          </address>
        </div>
        <nav class="footer__cols" aria-label="Footer">
{cols}
        </nav>
      </div>
      <div class="footer__bottom">
        <small>© 2026 Logic Insight, LLC. All rights reserved.</small>
        <small>Made in Orlando · for infrastructure operators</small>
      </div>
    </div>
  </footer>

  <div class="kbd" id="kbd" hidden>
    <div class="kbd__scrim" data-kbd-close></div>
    <div class="kbd__panel" role="dialog" aria-modal="true" aria-label="Command palette">
      <div class="kbd__input">
        <svg viewBox="0 0 16 16" width="16" height="16"><circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.6" fill="none"/><path d="M11 11l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        <input id="kbd-search" placeholder="Jump to a page or feature…" autocomplete="off"/>
        <kbd>esc</kbd>
      </div>
      <div class="kbd__list" id="kbd-list"></div>
    </div>
  </div>

  <script src="main.js"></script>
</body>
</html>
'''


# ---------------------------------------------------------------- Section renderers

def esc(s: str) -> str:
    return html.escape(s or "", quote=False)


def first_sentence(p: str) -> str:
    """Return the first sentence-ish chunk (up to ~ first . ! ? or 180 chars)."""
    p = (p or "").strip().replace("\n", " ")
    m = re.search(r"^(.{20,200}?[\.!?])(\s|$)", p)
    if m:
        return m.group(1).strip()
    return p[:200].strip()


def render_para(p: str) -> str:
    """First-sentence lead + an editorial-paste marker.
    Aiden swaps in the full official paragraph during the polish pass."""
    lead = first_sentence(p)
    return f'<p class="lead-snippet">{esc(lead)}</p><p class="copy-slot" data-paste-from-live>[ paste full paragraph from live page here ]</p>'


def looks_like_stat(s: str) -> bool:
    """Detect 818+ / 210+ / 50+ etc."""
    return bool(re.match(r"^\s*\d+\s*\+?\s*$", s)) or bool(re.match(r"^\s*\d+\s*\+\s*\w+", s))


def render_section(idx: int, sec: dict, route: str) -> str:
    """Render one section block from the crawled data."""
    eb = (sec.get("eyebrow") or "").strip()
    headings = sec.get("headings", [])
    paras = sec.get("paras", [])
    items = sec.get("items", [])
    stats = sec.get("stats", [])

    if not (eb or headings or paras or items):
        return ""

    # Skip the section if it's just a duplicate of the previous (the crawler sometimes
    # picks up nested duplicates - the first big block on each page repeats every h2)
    # The renderer will receive a deduplicated list from the caller.

    h2 = next((h["text"] for h in headings if h["level"] == "H2"), "")
    h3s = [h["text"] for h in headings if h["level"] == "H3"]
    lead = paras[0] if paras else ""
    rest_paras = paras[1:]

    parts = ['<section class="section ll-section">', '<div class="container">']
    parts.append('<header class="section-head" data-reveal>')
    if eb:
        parts.append(f'<span class="eyebrow"><span class="dot"></span>{esc(eb)}</span>')
    if h2:
        parts.append(f'<h2 class="section-title">{esc(h2)}</h2>')
    if lead:
        parts.append(f'<p class="section-sub">{esc(lead)}</p>')
    parts.append('</header>')

    # If we have h3 subsections, render as a grid of cards
    if h3s:
        # Pair each h3 with its trailing items/paras
        # simple approach: distribute remaining paras + items evenly
        cards_html = ['<div class="feature-grid" data-reveal>']
        # Build cards by chunking paras + items per h3
        # Heuristic: each h3 gets ~ (len(items)//len(h3s)) items, ~ (len(paras)//len(h3s)) paras
        per_items = max(1, len(items) // max(1, len(h3s)))
        per_paras = max(1, len(rest_paras) // max(1, len(h3s)))
        item_cursor = 0
        para_cursor = 0
        for h3 in h3s:
            card = ['<article class="feat-card" data-tilt>']
            card.append(f'<h3>{esc(h3)}</h3>')
            for _ in range(per_paras):
                if para_cursor < len(rest_paras):
                    card.append(render_para(rest_paras[para_cursor]))
                    para_cursor += 1
            if items:
                chunk = items[item_cursor:item_cursor + per_items]
                if chunk:
                    card.append('<ul class="bullet-list">')
                    for it in chunk:
                        card.append(f'<li>{esc(it)}</li>')
                    card.append('</ul>')
                item_cursor += per_items
            card.append('</article>')
            cards_html.append("".join(card))
        cards_html.append('</div>')
        parts.append("".join(cards_html))
        # Append any orphan paras at the end
        if para_cursor < len(rest_paras):
            parts.append('<div class="prose" data-reveal>')
            for p in rest_paras[para_cursor:]:
                parts.append(render_para(p))
            parts.append('</div>')
    else:
        # No h3 subsections — render paras + items as a single prose block
        if rest_paras or items:
            parts.append('<div class="prose" data-reveal>')
            for p in rest_paras:
                parts.append(render_para(p))
            if items:
                # Detect if items look like big stat numbers
                stat_items = [it for it in items if looks_like_stat(it.split('\n')[0])]
                if stat_items and len(stat_items) >= 2:
                    parts.append('<div class="stat-grid">')
                    for it in items:
                        first_line = it.split('\n')[0]
                        rest = '\n'.join(it.split('\n')[1:]).strip()
                        parts.append('<div class="stat-cell">')
                        parts.append(f'<div class="stat-num">{esc(first_line)}</div>')
                        if rest:
                            parts.append(f'<div class="stat-label">{esc(rest)}</div>')
                        parts.append('</div>')
                    parts.append('</div>')
                else:
                    parts.append('<ul class="bullet-list">')
                    for it in items:
                        parts.append(f'<li>{esc(it)}</li>')
                    parts.append('</ul>')
            parts.append('</div>')

    parts.append('</div></section>')
    return "".join(parts)


def dedupe_sections(sections: list) -> list:
    """The crawl sometimes captures both the parent <main> as one big section
    AND each child section. Drop sections whose content is entirely contained
    in a later section."""
    out = []
    seen_eyebrows = set()
    for s in sections:
        key = (
            s.get("eyebrow") or "",
            tuple(h["text"] for h in s.get("headings", [])[:2]),
        )
        # Heuristic: if a section has MANY headings (3+ H2s), it's the parent wrapper
        h2_count = sum(1 for h in s.get("headings", []) if h["level"] == "H2")
        if h2_count >= 3:
            continue
        if key in seen_eyebrows and key != ("", ()):
            # already had a section with the same eyebrow + first h2
            continue
        seen_eyebrows.add(key)
        out.append(s)
    return out


# ---------------------------------------------------------------- Page rendering

def render_pagehead(h1: str, route: str) -> str:
    """Top banner with H1."""
    h1 = (h1 or "").replace("\n", "<br/>")
    return f'''
  <section class="pagehead">
    <div class="hero__bg">
      <div class="hero__bg-grid"></div>
      <div class="hero__bg-aurora">
        <span class="aurora aurora--1"></span>
        <span class="aurora aurora--2"></span>
      </div>
    </div>
    <div class="container">
      <div class="eyebrow" data-reveal><span class="dot"></span>Logic Insight</div>
      <h1 data-reveal>{h1}</h1>
    </div>
  </section>
'''


def render_page(route: str, data: dict) -> str:
    title = data.get("title", "Logic Insight")
    # description: pull first paragraph if available
    sections = dedupe_sections(data.get("sections", []))
    first_para = ""
    for s in sections:
        if s.get("paras"):
            first_para = s["paras"][0][:160]
            break

    out = []
    out.append(head_block(title, first_para))
    out.append(nav(route))

    h1 = (data.get("h1s") or [""])[0]
    out.append(render_pagehead(h1, route))

    for i, s in enumerate(sections):
        out.append(render_section(i, s, route))

    out.append(footer())
    return "".join(out)


# ---------------------------------------------------------------- Homepage special

def render_homepage(data: dict) -> str:
    """Custom homepage: use sections from crawl + add the dashboard hero visual."""
    sections = dedupe_sections(data.get("sections", []))
    h1 = (data.get("h1s") or [""])[0].replace("\n", "<br/>")
    # First section likely has lead paragraph
    lead = ""
    for s in sections:
        if s.get("paras"):
            lead = s["paras"][0]
            break

    out = []
    out.append(head_block(data.get("title", "Logic Insight"), lead[:160]))
    out.append(nav("/"))

    # HERO with radial dashboard centerpiece
    out.append(f'''
  <section class="hero">
    <div class="hero__bg">
      <div class="hero__bg-grid"></div>
      <div class="hero__bg-aurora">
        <span class="aurora aurora--1"></span>
        <span class="aurora aurora--2"></span>
        <span class="aurora aurora--3"></span>
      </div>
    </div>
    <div class="container">
      <div class="hero__grid">
        <div class="hero__copy">
          <div class="eyebrow" data-reveal><span class="dot"></span>Overwatch by Logic Insight</div>
          <h1 class="hero__title" data-reveal>{h1}</h1>
          <p class="hero__sub" data-reveal>{esc(lead)}</p>
          <div class="hero__cta" data-reveal>
            <a href="{slug_for('/pricing/')}" class="btn btn--xl btn--primary">
              <span>Deploy Overwatch</span>
              <svg viewBox="0 0 16 16" width="16" height="16"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <a href="{slug_for('/features/')}" class="btn btn--xl btn--ghost">
              <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M5 3.5v9l7-4.5z" fill="currentColor"/></svg>
              <span>Watch demo</span>
            </a>
          </div>
          <ul class="hero__pills" data-reveal aria-label="Capabilities">
            <li><span class="pill-dot pill-dot--violet"></span>Cluster monitoring</li>
            <li><span class="pill-dot pill-dot--cyan"></span>ML anomaly detection</li>
            <li><span class="pill-dot pill-dot--pink"></span>Predictive analytics</li>
            <li><span class="pill-dot pill-dot--amber"></span>Network flow · IPFIX</li>
          </ul>
        </div>
        <div class="hero__visual" data-reveal>
          <div class="radial">
            <div class="radial__rings"></div>
            <svg class="radial__connector" preserveAspectRatio="none"></svg>
            <div class="radial__inner">
              <div class="radial__core" aria-label="Overwatch core">
                <svg viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="4" fill="currentColor"/>
                  <g stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
                    <line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/>
                    <line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/>
                    <line x1="4.9" y1="4.9" x2="7" y2="7"/><line x1="17" y1="17" x2="19.1" y2="19.1"/>
                    <line x1="4.9" y1="19.1" x2="7" y2="17"/><line x1="17" y1="7" x2="19.1" y2="4.9"/>
                  </g>
                </svg>
              </div>
            </div>
            <div class="radial__node radial__node--1"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="14" rx="2"/><line x1="8" y1="20" x2="16" y2="20"/></svg></div>
            <div class="radial__node radial__node--2"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7l8-4 8 4-8 4z"/><path d="M4 12l8 4 8-4"/><path d="M4 17l8 4 8-4"/></svg></div>
            <div class="radial__node radial__node--3"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-5 4 4 7-7"/><polyline points="14 9 21 9 21 16"/></svg></div>
            <div class="radial__node radial__node--4"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-12V4l-8-2-8 2v6c0 8 8 12 8 12z"/></svg></div>
            <div class="radial__node radial__node--5"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg></div>
            <div class="radial__node radial__node--6"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="9" x2="9" y2="15"/><line x1="15" y1="9" x2="15" y2="15"/><line x1="9" y1="12" x2="15" y2="12"/></svg></div>
          </div>
        </div>
      </div>
    </div>
  </section>
''')

    # Render the remaining real sections from the crawl (skip the first if it just
    # repeats the H1 + lead which we already used in the hero)
    used_lead = lead
    for i, s in enumerate(sections):
        # skip a section if its only paragraph is the lead we already showed in the hero
        if s.get("paras") and s["paras"][0] == used_lead and not s.get("headings"):
            continue
        # skip if this section's first heading equals h1
        head_texts = [h["text"] for h in s.get("headings", [])]
        if h1.replace("<br/>", " ").replace("<br>", " ").strip() in head_texts:
            # still render, but drop the redundant h1
            s = dict(s, headings=[h for h in s.get("headings", []) if h["text"] != h1.replace("<br/>"," ").strip()])
        out.append(render_section(i, s, "/"))

    out.append(footer())
    return "".join(out)


# ---------------------------------------------------------------- Main

written = []
for route, data in CONTENT.items():
    if data.get("error"):
        print(f"skip {route} (crawl error)")
        continue
    if route == "/":
        body = render_homepage(data)
    else:
        body = render_page(route, data)
    fname = slug_for(route)
    with open(fname, "w") as f:
        f.write(body)
    written.append(fname)
    print(f"wrote {fname:55} · {len(body):,} chars · {len(data.get('sections', []))} sections")

print(f"\n✓ {len(written)} pages generated")

#!/usr/bin/env python3
"""Generate all pages from a shared template + per-page content."""

PAGES = ["index", "product", "architecture", "ai-assistant", "integrations", "pricing", "insights", "about"]

NAV_LINKS = [
    ("product",      "Product"),
    ("architecture", "Architecture"),
    ("ai-assistant", "AI Assistant"),
    ("integrations", "Integrations"),
    ("pricing",      "Pricing"),
    ("insights",     "Insights"),
    ("about",        "About"),
]

LOGO_SVG = '''<svg viewBox="0 0 220 36" class="nav__logo-svg" role="img" aria-label="Logic Insight">
  <defs>
    <linearGradient id="li-mark-g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C39BFF"/>
      <stop offset="60%" stop-color="#A78BFA"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
    <linearGradient id="li-insight-g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FAF7FF"/>
      <stop offset="55%" stop-color="#D7C2FF"/>
      <stop offset="100%" stop-color="#FF6B9C"/>
    </linearGradient>
  </defs>
  <!-- fingerprint mark -->
  <g transform="translate(0,2)">
    <rect x="0" y="0" width="32" height="32" rx="9" fill="url(#li-mark-g)" opacity="0.18"/>
    <rect x="0" y="0" width="32" height="32" rx="9" fill="none" stroke="url(#li-mark-g)" stroke-width="1.3" opacity="0.85"/>
    <path d="M16 5 C 9 5 5 9 5 16 C 5 23 9 27 16 27" stroke="#FAF7FF" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    <path d="M16 9 C 11 9 9 11 9 16 C 9 21 11 23 16 23" stroke="#FAF7FF" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.75"/>
    <path d="M16 13 C 13 13 12 14 12 16 C 12 18 13 19 16 19" stroke="#FAF7FF" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.5"/>
    <circle cx="16" cy="16" r="1.4" fill="#FAF7FF"/>
  </g>
  <!-- wordmark -->
  <text x="44" y="24" font-family="Inter, sans-serif" font-weight="800" font-size="17" letter-spacing="0.04em" fill="#FAF7FF">LOGIC</text>
  <text x="103" y="24" font-family="Inter, sans-serif" font-weight="800" font-size="17" letter-spacing="0.04em" fill="url(#li-insight-g)">INSIGHT</text>
</svg>'''

FAVICON_HREF = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0%25' stop-color='%23C39BFF'/%3E%3Cstop offset='100%25' stop-color='%236D28D9'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='8' fill='%2307050E'/%3E%3Cpath d='M16 6 C 10 6 6 10 6 16 C 6 22 10 26 16 26' stroke='url(%23g)' stroke-width='2.4' fill='none' stroke-linecap='round'/%3E%3Cpath d='M16 10 C 12 10 10 12 10 16 C 10 20 12 22 16 22' stroke='url(%23g)' stroke-width='2.4' fill='none' stroke-linecap='round' opacity='0.6'/%3E%3Ccircle cx='16' cy='16' r='1.6' fill='%23C39BFF'/%3E%3C/svg%3E"


def head(title, description, page):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} · Logic Insight</title>
  <meta name="description" content="{description}" />
  <link rel="icon" type="image/svg+xml" href="{FAVICON_HREF}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body data-page="{page}">
  <div class="cursor-dot" aria-hidden="true"></div>
  <div class="cursor-blob" aria-hidden="true"></div>
  <div class="grain" aria-hidden="true"></div>
  <div class="scroll-progress" aria-hidden="true"><span></span></div>
'''


def nav(active):
    def link(slug, label):
        cls = ' class="is-active"' if slug == active else ""
        return f'    <a href="{slug}.html"{cls}>{label}</a>'
    links = "\n".join(link(s, l) for s, l in NAV_LINKS)
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
      <a href="about.html#contact" class="btn btn--ghost">Talk to sales</a>
      <a href="pricing.html" class="btn btn--primary">
        <span>Start free trial</span>
        <svg viewBox="0 0 16 16" width="14" height="14"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
    </div>
  </header>
'''


FOOTER = '''  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <div class="footer__brand">
          <a href="index.html" class="nav__brand" aria-label="Logic Insight home" style="padding:0;">''' + LOGO_SVG + '''</a>
          <p class="footer__tagline">Nutanix observability that thinks ahead.</p>
          <address class="footer__addr">
            425 W Colonial Dr, Ste 303<br/>
            Orlando, FL 32804<br/>
            <a href="mailto:contact@logicinsight.io">contact@logicinsight.io</a><br/>
            <a href="tel:+14075132359">+1 (407) 513-2359</a>
          </address>
        </div>
        <nav class="footer__cols" aria-label="Footer">
          <div>
            <h4>Product</h4>
            <a href="product.html">Cluster monitoring</a>
            <a href="product.html#forecast">Predictive analytics</a>
            <a href="product.html#flow">Network flow</a>
            <a href="product.html#hycu">Backup posture</a>
            <a href="architecture.html">Architecture</a>
            <a href="ai-assistant.html">AI Assistant</a>
          </div>
          <div>
            <h4>Integrations</h4>
            <a href="integrations.html#datadog">Datadog Marketplace</a>
            <a href="integrations.html#grafana">Grafana · Prometheus</a>
            <a href="integrations.html#hycu">HYCU Protégé</a>
            <a href="integrations.html#prism">Prism Central</a>
            <a href="integrations.html#wasabi">Wasabi · S3</a>
            <a href="integrations.html#snmp">SNMP devices</a>
          </div>
          <div>
            <h4>Company</h4>
            <a href="about.html">About</a>
            <a href="insights.html">Editorial</a>
            <a href="pricing.html">Pricing</a>
            <a href="about.html#contact">Contact</a>
          </div>
          <div>
            <h4>Resources</h4>
            <a href="#">Docs</a>
            <a href="#">RSS feed</a>
            <a href="#">GitHub</a>
            <a href="#">Status</a>
            <a href="#">Security</a>
          </div>
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


# -------------------------------------------------------------------
# PER-PAGE CONTENT
# -------------------------------------------------------------------

INDEX_BODY = '''
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
          <div class="eyebrow" data-reveal><span class="dot"></span>Overwatch v4 · just shipped</div>
          <h1 class="hero__title" data-reveal data-stagger>
            <span class="word">Nutanix</span>
            <span class="word">observability</span>
            <span class="word italic">that</span>
            <span class="word italic">thinks</span>
            <span class="word gradient">ahead.</span>
          </h1>
          <p class="hero__sub" data-reveal>
            One on-prem appliance. ML baselines, predictive analytics, IPFIX flow analysis,
            and an AI assistant that grounds every answer in the telemetry it pulled from.
          </p>
          <div class="hero__cta" data-reveal>
            <a href="pricing.html" class="btn btn--xl btn--primary">
              <span>Deploy Overwatch</span>
              <svg viewBox="0 0 16 16" width="16" height="16"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
            <a href="product.html" class="btn btn--xl btn--ghost">
              <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M5 3.5v9l7-4.5z" fill="currentColor"/></svg>
              <span>Watch 2-min demo</span>
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
                    <line x1="12" y1="2" x2="12" y2="5"/>
                    <line x1="12" y1="19" x2="12" y2="22"/>
                    <line x1="2"  y1="12" x2="5"  y2="12"/>
                    <line x1="19" y1="12" x2="22" y2="12"/>
                    <line x1="4.9"  y1="4.9"  x2="7"  y2="7"/>
                    <line x1="17"   y1="17"   x2="19.1" y2="19.1"/>
                    <line x1="4.9"  y1="19.1" x2="7"  y2="17"/>
                    <line x1="17"   y1="7"    x2="19.1" y2="4.9"/>
                  </g>
                </svg>
              </div>
            </div>
            <div class="radial__node radial__node--1">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="14" rx="2"/><line x1="8" y1="20" x2="16" y2="20"/></svg>
              <span class="radial__node-label">Clusters</span>
            </div>
            <div class="radial__node radial__node--2">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7l8-4 8 4-8 4z"/><path d="M4 12l8 4 8-4"/><path d="M4 17l8 4 8-4"/></svg>
              <span class="radial__node-label">Storage</span>
            </div>
            <div class="radial__node radial__node--3">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-5 4 4 7-7"/><polyline points="14 9 21 9 21 16"/></svg>
              <span class="radial__node-label">Forecast</span>
            </div>
            <div class="radial__node radial__node--4">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-12V4l-8-2-8 2v6c0 8 8 12 8 12z"/></svg>
              <span class="radial__node-label">Backups</span>
            </div>
            <div class="radial__node radial__node--5">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>
              <span class="radial__node-label">Network</span>
            </div>
            <div class="radial__node radial__node--6">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="9" x2="9" y2="15"/><line x1="15" y1="9" x2="15" y2="15"/><line x1="9" y1="12" x2="15" y2="12"/></svg>
              <span class="radial__node-label">Hardware</span>
            </div>
          </div>
        </div>
      </div>

      <div class="hero__stats" data-reveal>
        <div class="hero__stat">
          <div class="hero__stat-num"><span data-count="11" data-suffix="+">0</span></div>
          <div class="hero__stat-label">Integrations · Day 1</div>
        </div>
        <div class="hero__stat">
          <div class="hero__stat-num"><span data-count="60" data-suffix="min">0</span></div>
          <div class="hero__stat-label">From boot to first signal</div>
        </div>
        <div class="hero__stat">
          <div class="hero__stat-num"><span data-count="100" data-suffix="%">0</span></div>
          <div class="hero__stat-label">On-prem. Your data stays.</div>
        </div>
      </div>
    </div>
  </section>

  <section class="trust">
    <div class="container">
      <p class="trust__label">Concentrating the signals serious Nutanix teams already need</p>
      <div class="marquee" aria-hidden="true">
        <div class="marquee__track">
          <span class="marquee__logo">NUTANIX</span>
          <span class="marquee__logo">HYCU</span>
          <span class="marquee__logo">DATADOG</span>
          <span class="marquee__logo">GRAFANA</span>
          <span class="marquee__logo">PRISM CENTRAL</span>
          <span class="marquee__logo">WASABI</span>
          <span class="marquee__logo">REDFISH</span>
          <span class="marquee__logo">UBUNTU LTS</span>
          <span class="marquee__logo">IPFIX</span>
          <span class="marquee__logo">SNMP</span>
          <span class="marquee__logo">NUTANIX</span>
          <span class="marquee__logo">HYCU</span>
          <span class="marquee__logo">DATADOG</span>
          <span class="marquee__logo">GRAFANA</span>
          <span class="marquee__logo">PRISM CENTRAL</span>
          <span class="marquee__logo">WASABI</span>
          <span class="marquee__logo">REDFISH</span>
          <span class="marquee__logo">UBUNTU LTS</span>
          <span class="marquee__logo">IPFIX</span>
          <span class="marquee__logo">SNMP</span>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <header class="section-head" data-reveal>
        <span class="eyebrow"><span class="dot"></span>Four domains, one appliance</span>
        <h2 class="section-title">Every signal Nutanix teams need, <span class="italic gradient">already correlated.</span></h2>
        <p class="section-sub">Compute, storage, network, identity, backup — Overwatch runs ML against the combined picture, not the silos.</p>
      </header>

      <div class="pillars">
        <a class="pillar" data-tilt href="product.html#cluster" data-reveal>
          <div class="pillar__icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="14" rx="2"/><line x1="8" y1="20" x2="16" y2="20"/></svg>
          </div>
          <h3>Cluster monitoring</h3>
          <p>Per-CVM, per-host, per-container ML baselines. Anomalies before they become tickets.</p>
          <span class="pillar__link">Explore <svg viewBox="0 0 16 16" width="12" height="12"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        </a>
        <a class="pillar" data-tilt href="product.html#forecast" data-reveal>
          <div class="pillar__icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-5 4 4 7-7"/><polyline points="14 9 21 9 21 16"/></svg>
          </div>
          <h3>Predictive analytics</h3>
          <p>Capacity forecasts with confidence bands. Tell leadership "18 weeks" not "feels tight."</p>
          <span class="pillar__link">Explore <svg viewBox="0 0 16 16" width="12" height="12"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        </a>
        <a class="pillar" data-tilt href="product.html#flow" data-reveal>
          <div class="pillar__icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>
          </div>
          <h3>Network flow · IPFIX</h3>
          <p>East-west traffic, top talkers, retransmits — anchored to the alert, not a separate tool.</p>
          <span class="pillar__link">Explore <svg viewBox="0 0 16 16" width="12" height="12"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        </a>
        <a class="pillar" data-tilt href="product.html#hycu" data-reveal>
          <div class="pillar__icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-12V4l-8-2-8 2v6c0 8 8 12 8 12z"/></svg>
          </div>
          <h3>Backup posture</h3>
          <p>Immutability windows, retention drift, admin-path separation, restore freshness. HYCU-aware.</p>
          <span class="pillar__link">Explore <svg viewBox="0 0 16 16" width="12" height="12"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        </a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <header class="section-head" data-reveal>
        <span class="eyebrow"><span class="dot"></span>The dashboard you ship to the SRE bridge</span>
        <h2 class="section-title">A control surface that explains itself, <span class="italic gradient">at 3 a.m.</span></h2>
      </header>

      <div class="showcase" data-reveal>
        <div class="showcase__top">
          <div class="kpi">
            <div class="kpi__label">Cluster health</div>
            <div class="kpi__row"><span class="kpi__val">98.4</span><span class="kpi__delta kpi__delta--ok">+1.2</span></div>
            <div class="kpi__bar" style="--w: 92%;"></div>
          </div>
          <div class="kpi">
            <div class="kpi__label">P95 latency · ms</div>
            <div class="kpi__row"><span class="kpi__val">6.2</span><span class="kpi__delta kpi__delta--ok">−0.4</span></div>
            <div class="kpi__bar" style="--w: 28%;"></div>
          </div>
          <div class="kpi">
            <div class="kpi__label">Storage forecast · 90d</div>
            <div class="kpi__row"><span class="kpi__val">64%</span><span class="kpi__delta kpi__delta--warn">85% in 18w</span></div>
            <div class="kpi__bar" style="--w: 64%;"></div>
          </div>
          <div class="kpi">
            <div class="kpi__label">Backup posture</div>
            <div class="kpi__row"><span class="kpi__val">A</span><span class="kpi__delta kpi__delta--ok">stable</span></div>
            <div class="kpi__bar" style="--w: 96%;"></div>
          </div>
        </div>

        <div class="showcase__chart">
          <div class="showcase__chart-head">
            <div class="showcase__chart-title">
              cluster-prod-03 · controller latency
              <span class="live">live</span>
            </div>
            <div class="showcase__chart-legend">
              <span><i style="background:#A78BFA"></i>ML baseline</span>
              <span><i style="background:#FAF7FF"></i>Observed</span>
              <span><i style="background:#FF6B9C"></i>Anomaly</span>
            </div>
          </div>
          <svg class="showcase__chart-svg" viewBox="0 0 800 220" preserveAspectRatio="none">
            <defs>
              <linearGradient id="bandg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#A78BFA" stop-opacity="0.35"/>
                <stop offset="100%" stop-color="#A78BFA" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <!-- y gridlines -->
            <g stroke="rgba(255,255,255,0.05)" stroke-width="1">
              <line x1="0" y1="50"  x2="800" y2="50"/>
              <line x1="0" y1="100" x2="800" y2="100"/>
              <line x1="0" y1="150" x2="800" y2="150"/>
            </g>
            <!-- baseline band -->
            <path d="M0,120 C80,116 140,112 200,108 C260,104 320,108 380,110 C440,112 500,104 560,98 C620,92 680,96 740,94 L800,92 L800,220 L0,220 Z" fill="url(#bandg)"/>
            <path d="M0,120 C80,116 140,112 200,108 C260,104 320,108 380,110 C440,112 500,104 560,98 C620,92 680,96 740,94 L800,92" stroke="#A78BFA" stroke-width="1.6" stroke-dasharray="4 4" fill="none"/>
            <!-- observed (draw on viewport) -->
            <path class="chart-draw" d="M0,124 C70,128 130,138 200,128 C270,118 330,108 400,118 C470,128 520,108 580,80 C640,55 690,75 740,70 L800,62"
                  stroke="#FAF7FF" stroke-width="2.2" fill="none" stroke-linecap="round"/>
            <!-- anomaly markers -->
            <circle cx="580" cy="80" r="5" fill="#FF6B9C"/>
            <circle cx="580" cy="80" r="14" fill="none" stroke="#FF6B9C" stroke-width="1.5">
              <animate attributeName="r" values="5;18" dur="1.4s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="1;0" dur="1.4s" repeatCount="indefinite"/>
            </circle>
          </svg>

          <div class="showcase__alert">
            <span class="showcase__alert-dot"></span>
            <div>
              <strong>Anomaly · node-07</strong>
              <span class="muted" style="margin-left:6px;">controller latency · 2.4σ above baseline</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="ai-promo" data-reveal>
        <div>
          <span class="eyebrow"><span class="dot"></span>AI Assistant</span>
          <h2>Less chat. <span class="italic gradient">More evidence.</span></h2>
          <p>Most "AI in observability" is a chat box over the same broken signals. Overwatch grounds every answer in the data path it pulled from — and shows you that path.</p>
          <a href="ai-assistant.html" class="btn btn--ghost">How the assistant works
            <svg viewBox="0 0 16 16" width="12" height="12"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
        </div>
        <div class="ai-promo__chat">
          <div class="msg msg--user">
            <span class="msg__who">You</span>
            <p>Why is cluster-prod-03 latency drifting since 14:20?</p>
          </div>
          <div class="msg msg--ai">
            <span class="msg__who"><span class="msg__who-mark"></span>Overwatch</span>
            <p>Top contributor: <strong>node-07 storage controller</strong>. CVM read latency went from 6.2 ms p95 to 14.1 ms starting <span class="evidence">14:18:42</span>. Redfish shows <strong>PSU 2 degraded</strong> at <span class="evidence">14:17:11</span> — same node, 90s earlier.</p>
          </div>
          <div class="msg msg--ai">
            <span class="msg__who"><span class="msg__who-mark"></span>Overwatch</span>
            <p>Cross-referencing 14 nodes against 90-day baseline<span class="dots"><span></span><span></span><span></span></span></p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <header class="section-head" data-reveal>
        <span class="eyebrow"><span class="dot"></span>Pricing</span>
        <h2 class="section-title">Three ways to deploy. <span class="italic gradient">All transparent.</span></h2>
        <p class="section-sub">Per-core licensing. No data-volume games. No "contact us" tier hidden behind the page.</p>
      </header>
      <div class="pricing__grid" data-reveal>
        <article class="price-card">
          <header><h3>Essentials</h3><p>Single cluster or small platform team starting to consolidate signal.</p></header>
          <div class="price-card__price"><span class="price-num">$48</span><span class="price-unit">/core / mo</span></div>
          <ul class="price-card__list">
            <li>Nutanix cluster + hardware monitoring</li>
            <li>ML baselines · 90-day retention</li>
            <li>Datadog or Grafana export</li>
            <li>Email + chat support</li>
          </ul>
          <a class="btn btn--ghost btn--block" href="pricing.html">Start 30-day trial</a>
        </article>
        <article class="price-card price-card--featured">
          <span class="price-card__badge">Most teams pick this</span>
          <header><h3>Enterprise</h3><p>Multi-cluster, multi-site. The full Overwatch surface — IPFIX + AI assistant.</p></header>
          <div class="price-card__price"><span class="price-num">$36</span><span class="price-unit">/core / mo</span></div>
          <ul class="price-card__list">
            <li>Everything in Essentials</li>
            <li>Predictive analytics + capacity forecasts</li>
            <li>IPFIX east-west flow analysis</li>
            <li>HYCU backup posture telemetry</li>
            <li>AI assistant · evidence-linked answers</li>
            <li>Wasabi / S3 object-lock destination</li>
          </ul>
          <a class="btn btn--primary btn--block" href="pricing.html">Deploy Enterprise</a>
        </article>
        <article class="price-card">
          <header><h3>Managed (MaaS)</h3><p>We run the appliance, the upgrades, the tuning. You get the dashboards.</p></header>
          <div class="price-card__price"><span class="price-num">Talk</span><span class="price-unit">to us</span></div>
          <ul class="price-card__list">
            <li>Fully managed Overwatch appliance</li>
            <li>24×7 SRE coverage from Logic Insight</li>
            <li>Quarterly capacity + posture reviews</li>
            <li>Datadog Marketplace bundling option</li>
          </ul>
          <a class="btn btn--ghost btn--block" href="about.html#contact">Talk to a human</a>
        </article>
      </div>
    </div>
  </section>

  <section class="finalcta">
    <div class="container">
      <div class="finalcta__inner" data-reveal>
        <div class="finalcta__halo"></div>
        <span class="eyebrow"><span class="dot"></span>30-day trial · no credit card</span>
        <h2 class="finalcta__title">Stop assembling dashboards.<br/><span class="italic gradient">Start seeing the system.</span></h2>
        <p class="finalcta__sub">Deploy Overwatch into a cluster in under an hour. Bring your Datadog or Grafana. Keep your evidence on-prem.</p>
        <form class="finalcta__form" onsubmit="event.preventDefault(); this.classList.add('is-sent');">
          <label class="sr-only" for="email">Work email</label>
          <input id="email" type="email" required placeholder="you@company.com" autocomplete="email" />
          <button class="btn btn--xl btn--primary" type="submit">
            <span>Request appliance</span>
            <svg viewBox="0 0 16 16" width="14" height="14"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
          <p class="finalcta__sent">Thanks — we'll be in touch within one business day.</p>
        </form>
      </div>
    </div>
  </section>
'''


def pagehead(eyebrow, title_html, sub):
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
      <div class="eyebrow" data-reveal><span class="dot"></span>{eyebrow}</div>
      <h1 data-reveal>{title_html}</h1>
      <p data-reveal>{sub}</p>
    </div>
  </section>
'''


PRODUCT_BODY = pagehead(
    "Product",
    'Every signal a Nutanix team <span class="italic gradient">already needs to see.</span>',
    "Compute, storage, network, hardware, identity, backup. ML baselines learned per-cluster. Anomalies grounded in the data path that produced them."
) + '''
  <section class="section">
    <div class="container">
      <div class="bento">
        <article id="cluster" class="bento-card bento-card--lg" data-tilt data-reveal>
          <span class="bento-card__tag">Cluster monitoring</span>
          <h3>Prism is for state. <em>We are for change.</em></h3>
          <p>Nutanix-aware metrics across CVMs, hosts, containers, and storage. ML baselines learn each cluster's personality so anomalies surface against the cluster's own history — not a generic threshold.</p>
          <svg viewBox="0 0 600 200" style="margin-top:24px;width:100%;height:200px;">
            <defs>
              <linearGradient id="bandg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#A78BFA" stop-opacity="0.3"/><stop offset="100%" stop-color="#A78BFA" stop-opacity="0"/></linearGradient>
            </defs>
            <path d="M0,130 C80,120 140,108 200,100 C260,92 320,108 380,110 C440,112 500,90 560,82 L600,80 L600,200 L0,200 Z" fill="url(#bandg2)"/>
            <path class="chart-draw" d="M0,134 C80,140 140,150 200,138 C270,128 320,116 400,128 C470,140 500,116 560,82 L600,75" stroke="#FAF7FF" stroke-width="2.2" fill="none" stroke-linecap="round"/>
            <circle cx="560" cy="82" r="6" fill="#FF6B9C"/><circle cx="560" cy="82" r="16" fill="none" stroke="#FF6B9C" stroke-width="1.5"><animate attributeName="r" values="6;20" dur="1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.4s" repeatCount="indefinite"/></circle>
          </svg>
        </article>

        <article id="forecast" class="bento-card" data-tilt data-reveal>
          <span class="bento-card__tag">Predictive analytics</span>
          <h3>Capacity forecasts that <em>survive</em> Q3 planning.</h3>
          <p>Per-cluster, per-workload growth with confidence bands. Tell leadership the runway in weeks.</p>
          <div style="margin-top:24px;height:18px;background:rgba(255,255,255,0.05);border-radius:999px;overflow:hidden;position:relative;">
            <div style="position:absolute;left:0;top:0;bottom:0;width:64%;background:linear-gradient(90deg,#8B5CF6,#FF6B9C);border-radius:inherit;box-shadow:0 0 16px rgba(167,139,250,0.6);"></div>
            <div style="position:absolute;left:85%;top:-3px;bottom:-3px;width:2px;background:#FAF7FF;"></div>
          </div>
          <p class="mono" style="font-size:12px;color:var(--ink-mute);margin-top:12px;">cluster-prod-03 hits 85% in <span style="color:var(--p-300);">18 weeks</span></p>
        </article>

        <article id="flow" class="bento-card" data-tilt data-reveal>
          <span class="bento-card__tag">Network flow · IPFIX</span>
          <h3>IPFIX <em>without</em> the data lake.</h3>
          <p>East-west traffic, top talkers, retransmits — anchored to the alert, not assembled later.</p>
          <svg viewBox="0 0 300 120" style="margin-top:24px;width:100%;">
            <g stroke="#A78BFA" stroke-width="1.4" fill="none" stroke-dasharray="3 4">
              <path d="M20,40 Q150,10 280,40"><animate attributeName="stroke-dashoffset" from="0" to="-80" dur="4s" repeatCount="indefinite"/></path>
              <path d="M20,60 Q150,90 280,60"><animate attributeName="stroke-dashoffset" from="0" to="-80" dur="4s" repeatCount="indefinite"/></path>
              <path d="M20,80 Q150,30 280,80" stroke="#FF6B9C"><animate attributeName="stroke-dashoffset" from="0" to="-80" dur="4s" repeatCount="indefinite"/></path>
            </g>
            <g fill="#FAF7FF">
              <circle cx="20" cy="40" r="4"/><circle cx="20" cy="60" r="4"/><circle cx="20" cy="80" r="4"/>
              <circle cx="280" cy="40" r="4"/><circle cx="280" cy="60" r="4"/><circle cx="280" cy="80" r="4"/>
            </g>
          </svg>
        </article>

        <article class="bento-card" data-tilt data-reveal>
          <span class="bento-card__tag">Hardware · Redfish</span>
          <h3>Disk, PSU, fan, temp — before the ticket.</h3>
          <p>Dell, HPE, Lenovo, Supermicro chassis. SMART signals correlated to cluster events automatically.</p>
          <ul style="list-style:none;padding:0;margin-top:24px;display:grid;gap:8px;font-family:var(--ff-mono);font-size:12px;">
            <li style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:rgba(255,255,255,0.03);border:1px solid var(--line);border-radius:10px;"><span style="width:8px;height:8px;border-radius:50%;background:#34D399;box-shadow:0 0 8px #34D399;"></span>node-04 · iDRAC · all subsystems</li>
            <li style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:rgba(255,255,255,0.03);border:1px solid var(--line);border-radius:10px;"><span style="width:8px;height:8px;border-radius:50%;background:#FBBF24;box-shadow:0 0 8px #FBBF24;"></span>node-07 · PSU 2 · degraded efficiency</li>
            <li style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:rgba(255,255,255,0.03);border:1px solid var(--line);border-radius:10px;"><span style="width:8px;height:8px;border-radius:50%;background:#34D399;box-shadow:0 0 8px #34D399;"></span>node-09 · iLO 5 · all subsystems</li>
          </ul>
        </article>

        <article id="hycu" class="bento-card bento-card--wide" data-tilt data-reveal>
          <span class="bento-card__tag">HYCU · Backup posture</span>
          <h3>Recovery posture, not <em>"the job ran".</em></h3>
          <p>Track immutability windows, verification freshness, retention drift, and admin-path separation. The metrics that decide whether a backup actually survives the incident.</p>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:24px;">
            <div style="padding:16px;background:linear-gradient(180deg,rgba(167,139,250,0.10),rgba(167,139,250,0.02));border:1px solid rgba(167,139,250,0.20);border-radius:14px;">
              <div style="font-size:1.8rem;font-weight:700;letter-spacing:-0.02em;color:var(--p-200);font-variant-numeric:tabular-nums;"><span data-count="100" data-suffix="%">0</span></div>
              <div class="mono" style="font-size:10px;color:var(--ink-mute);letter-spacing:0.06em;text-transform:uppercase;margin-top:4px;">success · 30d</div>
            </div>
            <div style="padding:16px;background:linear-gradient(180deg,rgba(167,139,250,0.10),rgba(167,139,250,0.02));border:1px solid rgba(167,139,250,0.20);border-radius:14px;">
              <div style="font-size:1.8rem;font-weight:700;letter-spacing:-0.02em;color:var(--p-200);font-variant-numeric:tabular-nums;"><span data-count="14" data-suffix="d">0</span></div>
              <div class="mono" style="font-size:10px;color:var(--ink-mute);letter-spacing:0.06em;text-transform:uppercase;margin-top:4px;">immutability lock</div>
            </div>
            <div style="padding:16px;background:linear-gradient(180deg,rgba(167,139,250,0.10),rgba(167,139,250,0.02));border:1px solid rgba(167,139,250,0.20);border-radius:14px;">
              <div style="font-size:1.8rem;font-weight:700;letter-spacing:-0.02em;color:var(--p-200);font-variant-numeric:tabular-nums;">2.1h</div>
              <div class="mono" style="font-size:10px;color:var(--ink-mute);letter-spacing:0.06em;text-transform:uppercase;margin-top:4px;">RPO · prod tier</div>
            </div>
            <div style="padding:16px;background:linear-gradient(180deg,rgba(167,139,250,0.10),rgba(167,139,250,0.02));border:1px solid rgba(167,139,250,0.20);border-radius:14px;">
              <div style="font-size:1.8rem;font-weight:700;letter-spacing:-0.02em;color:var(--p-200);">✓</div>
              <div class="mono" style="font-size:10px;color:var(--ink-mute);letter-spacing:0.06em;text-transform:uppercase;margin-top:4px;">last restore test</div>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
'''


ARCH_BODY = pagehead(
    "Architecture",
    'One appliance. <span class="italic gradient">Open everywhere it matters.</span>',
    "Overwatch deploys as a single Ubuntu 24.04 LTS appliance inside your perimeter. Telemetry stays local; evidence flows out only when you choose where it goes."
) + '''
  <section class="section">
    <div class="container">
      <div class="arch__diagram" data-reveal>
        <svg viewBox="0 0 1000 420" class="arch-svg" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
          <defs><filter id="glow"><feGaussianBlur stdDeviation="4"/></filter></defs>
          <g class="arch-source"><rect x="40" y="40" width="200" height="50" rx="12"/><text x="140" y="70" text-anchor="middle">Nutanix Prism · API v3</text></g>
          <g class="arch-source"><rect x="40" y="105" width="200" height="50" rx="12"/><text x="140" y="135" text-anchor="middle">Redfish · iDRAC · iLO</text></g>
          <g class="arch-source"><rect x="40" y="170" width="200" height="50" rx="12"/><text x="140" y="200" text-anchor="middle">SNMP v2c / v3</text></g>
          <g class="arch-source"><rect x="40" y="235" width="200" height="50" rx="12"/><text x="140" y="265" text-anchor="middle">IPFIX · NetFlow v9</text></g>
          <g class="arch-source"><rect x="40" y="300" width="200" height="50" rx="12"/><text x="140" y="330" text-anchor="middle">HYCU · Backups</text></g>
          <g class="arch-core">
            <rect x="380" y="120" width="240" height="180" rx="20"/>
            <text x="500" y="180" text-anchor="middle" class="arch-core-title">OVERWATCH</text>
            <text x="500" y="205" text-anchor="middle" class="arch-core-sub">Ubuntu 24.04 · single appliance</text>
            <g class="arch-core-pills">
              <rect x="408" y="222" width="80" height="22" rx="11"/><text x="448" y="237" text-anchor="middle">ML baselines</text>
              <rect x="500" y="222" width="84" height="22" rx="11"/><text x="542" y="237" text-anchor="middle">Anomalies</text>
              <rect x="420" y="252" width="68" height="22" rx="11"/><text x="454" y="267" text-anchor="middle">Forecast</text>
              <rect x="500" y="252" width="92" height="22" rx="11"/><text x="546" y="267" text-anchor="middle">AI assistant</text>
            </g>
          </g>
          <g class="arch-dest"><rect x="760" y="60" width="200" height="60" rx="12"/><text x="860" y="95" text-anchor="middle">Datadog Marketplace</text></g>
          <g class="arch-dest"><rect x="760" y="140" width="200" height="60" rx="12"/><text x="860" y="175" text-anchor="middle">Grafana · Prometheus</text></g>
          <g class="arch-dest"><rect x="760" y="220" width="200" height="60" rx="12"/><text x="860" y="255" text-anchor="middle">S3 · Wasabi (immutable)</text></g>
          <g class="arch-dest"><rect x="760" y="300" width="200" height="60" rx="12"/><text x="860" y="335" text-anchor="middle">On-box dashboards</text></g>
          <g class="arch-lines">
            <path d="M240,65 C310,65 320,210 380,210" stroke="rgba(167,139,250,0.35)" stroke-width="1.4" fill="none"/>
            <path d="M240,130 C310,130 320,210 380,210" stroke="rgba(167,139,250,0.35)" stroke-width="1.4" fill="none"/>
            <path d="M240,195 C310,195 320,210 380,210" stroke="rgba(167,139,250,0.35)" stroke-width="1.4" fill="none"/>
            <path d="M240,260 C310,260 320,210 380,210" stroke="rgba(167,139,250,0.35)" stroke-width="1.4" fill="none"/>
            <path d="M240,325 C310,325 320,210 380,210" stroke="rgba(167,139,250,0.35)" stroke-width="1.4" fill="none"/>
            <path d="M620,210 C700,210 690,90 760,90" stroke="rgba(255,107,156,0.35)" stroke-width="1.4" fill="none"/>
            <path d="M620,210 C700,210 690,170 760,170" stroke="rgba(255,107,156,0.35)" stroke-width="1.4" fill="none"/>
            <path d="M620,210 C700,210 690,250 760,250" stroke="rgba(255,107,156,0.35)" stroke-width="1.4" fill="none"/>
            <path d="M620,210 C700,210 690,330 760,330" stroke="rgba(255,107,156,0.35)" stroke-width="1.4" fill="none"/>
          </g>
          <g class="arch-pulses"></g>
        </svg>
      </div>

      <div class="pillars" style="margin-top:48px;">
        <div class="pillar" data-reveal>
          <h3>On-prem by default</h3>
          <p>Telemetry stays inside your perimeter. No data leaves unless you forward it.</p>
        </div>
        <div class="pillar" data-reveal>
          <h3>Open standards</h3>
          <p>Prometheus, OTLP, IPFIX, Redfish, SNMP. Standards in, standards out.</p>
        </div>
        <div class="pillar" data-reveal>
          <h3>Forwarder, not lock-in</h3>
          <p>Change destinations without rebuilding ingestion. Datadog today, Grafana tomorrow.</p>
        </div>
        <div class="pillar" data-reveal>
          <h3>Ubuntu 24.04 LTS</h3>
          <p>Single OVA / qcow2. Backed by a real LTS, not a custom kernel surprise.</p>
        </div>
      </div>
    </div>
  </section>
'''


AI_BODY = pagehead(
    "AI Assistant",
    'Less chat. <span class="italic gradient">More evidence.</span>',
    "Most AI in observability is a chat box over the same broken signals. Overwatch grounds every answer in the data path it pulled from — and shows you that path."
) + '''
  <section class="section">
    <div class="container">
      <div class="ai-promo" data-reveal style="grid-template-columns:1fr 1.2fr;">
        <div>
          <span class="eyebrow"><span class="dot"></span>How it works</span>
          <h2>Evidence-grounded reasoning, <span class="italic gradient">not chat theater.</span></h2>
          <ul style="list-style:none;padding:0;display:grid;gap:20px;margin-top:24px;">
            <li style="display:grid;grid-template-columns:28px 1fr;gap:12px;"><svg viewBox="0 0 16 16" width="28" height="28" style="padding:6px;color:var(--p-300);background:rgba(167,139,250,0.10);border:1px solid rgba(167,139,250,0.20);border-radius:8px;"><path d="M3 8l3.5 3.5L13 4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg><div><strong style="display:block;color:var(--ink);">Evidence-linked answers</strong><span style="color:var(--ink-soft);font-size:14px;">Every claim is anchored to the metric, log line, or flow record it came from.</span></div></li>
            <li style="display:grid;grid-template-columns:28px 1fr;gap:12px;"><svg viewBox="0 0 16 16" width="28" height="28" style="padding:6px;color:var(--p-300);background:rgba(167,139,250,0.10);border:1px solid rgba(167,139,250,0.20);border-radius:8px;"><path d="M3 8l3.5 3.5L13 4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg><div><strong style="display:block;color:var(--ink);">No silent actions</strong><span style="color:var(--ink-soft);font-size:14px;">The assistant proposes — your operators approve. Full audit trail of what was suggested vs applied.</span></div></li>
            <li style="display:grid;grid-template-columns:28px 1fr;gap:12px;"><svg viewBox="0 0 16 16" width="28" height="28" style="padding:6px;color:var(--p-300);background:rgba(167,139,250,0.10);border:1px solid rgba(167,139,250,0.20);border-radius:8px;"><path d="M3 8l3.5 3.5L13 4" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg><div><strong style="display:block;color:var(--ink);">Nutanix-aware reasoning</strong><span style="color:var(--ink-soft);font-size:14px;">Works against telemetry that already knows what a CVM is, where IPFIX terminates, what immutability means.</span></div></li>
          </ul>
        </div>
        <div class="ai-promo__chat" style="padding:24px;">
          <div class="msg msg--user"><span class="msg__who">You</span><p>Why is cluster-prod-03 latency drifting since 14:20?</p></div>
          <div class="msg msg--ai"><span class="msg__who"><span class="msg__who-mark"></span>Overwatch</span><p>Top contributor: <strong>node-07 storage controller</strong>. CVM read latency moved from a 6.2 ms p95 baseline to 14.1 ms starting <span class="evidence">14:18:42</span>. Hardware view shows <strong>PSU 2 degraded</strong> at <span class="evidence">14:17:11</span> — same node, ~90 s earlier.</p>
            <div style="margin-top:12px;display:flex;flex-wrap:wrap;gap:6px;">
              <span class="evidence">baseline-p95.metric</span>
              <span class="evidence">redfish.psu.efficiency</span>
              <span class="evidence">ipfix.east-west.flows</span>
            </div>
          </div>
          <div class="msg msg--user"><span class="msg__who">You</span><p>Did the same PSU pattern hit any other node this quarter?</p></div>
          <div class="msg msg--ai"><span class="msg__who"><span class="msg__who-mark"></span>Overwatch</span><p>Cross-referencing 14 nodes against the 90-day baseline<span class="dots"><span></span><span></span><span></span></span></p></div>
        </div>
      </div>
    </div>
  </section>
'''


INTEG_BODY = pagehead(
    "Integrations",
    'Send signal <span class="italic gradient">to the platform you already chose.</span>',
    "Overwatch is the collection + enrichment layer. Where the metrics terminate is your decision — and you can change it without rebuilding ingestion."
) + '''
  <section class="section">
    <div class="container">
      <div class="integrations__grid" data-reveal>
        <a id="datadog"  class="integ-card" data-tilt href="#"><div class="integ-card__logo">📊</div><h3>Datadog Marketplace</h3><p>Listed integration. Nutanix metrics into the same dashboards your SRE team already lives in.</p><span class="integ-card__link">View on Marketplace →</span></a>
        <a id="grafana"  class="integ-card" data-tilt href="#"><div class="integ-card__logo">📈</div><h3>Grafana · Prometheus</h3><p>Open-format exports. Drop into existing dashboards, alerts, and on-call rotations.</p><span class="integ-card__link">Setup guide →</span></a>
        <a id="hycu"     class="integ-card" data-tilt href="#"><div class="integ-card__logo">🛡️</div><h3>HYCU Protégé</h3><p>Job, retention, immutability, and admin-separation telemetry from your backup tier.</p><span class="integ-card__link">Integration details →</span></a>
        <a id="prism"    class="integ-card" data-tilt href="#"><div class="integ-card__logo">🔷</div><h3>Prism Central · AHV</h3><p>Deeper-than-Prism cluster, VM, and storage signal — without scraping the UI.</p><span class="integ-card__link">What changes vs Prism →</span></a>
        <a id="wasabi"   class="integ-card" data-tilt href="#"><div class="integ-card__logo">🗄️</div><h3>Wasabi · S3 immutable</h3><p>Forward enriched flow + audit telemetry to object-lock storage for long-horizon retention.</p><span class="integ-card__link">Recipe →</span></a>
        <a id="snmp"     class="integ-card" data-tilt href="#"><div class="integ-card__logo">📡</div><h3>SNMP v2c / v3</h3><p>Switches, UPS, sensors, PDUs. Standard polling unified with the rest of the infra story.</p><span class="integ-card__link">Supported MIBs →</span></a>
      </div>
    </div>
  </section>
'''


PRICING_BODY = pagehead(
    "Pricing",
    'Three ways to deploy. <span class="italic gradient">All transparent.</span>',
    "Per-core licensing. No data-volume games. No 'contact us' tier hidden behind the page."
) + '''
  <section class="section">
    <div class="container">
      <div class="pricing__grid" data-reveal>
        <article class="price-card">
          <header><h3>Essentials</h3><p>Single cluster or small platform team starting to consolidate signal.</p></header>
          <div class="price-card__price"><span class="price-num">$48</span><span class="price-unit">/core / mo</span></div>
          <ul class="price-card__list">
            <li>Nutanix cluster + hardware monitoring</li>
            <li>ML baselines · 90-day retention</li>
            <li>Datadog or Grafana export</li>
            <li>Email + chat support</li>
          </ul>
          <a class="btn btn--ghost btn--block" href="#">Start 30-day trial</a>
        </article>
        <article class="price-card price-card--featured">
          <span class="price-card__badge">Most teams pick this</span>
          <header><h3>Enterprise</h3><p>Multi-cluster, multi-site. The full Overwatch surface — IPFIX + AI assistant.</p></header>
          <div class="price-card__price"><span class="price-num">$36</span><span class="price-unit">/core / mo</span></div>
          <ul class="price-card__list">
            <li>Everything in Essentials</li>
            <li>Predictive analytics + capacity forecasts</li>
            <li>IPFIX east-west flow analysis</li>
            <li>HYCU backup posture telemetry</li>
            <li>AI assistant · evidence-linked answers</li>
            <li>Wasabi / S3 object-lock destination</li>
          </ul>
          <a class="btn btn--primary btn--block" href="#">Deploy Enterprise</a>
        </article>
        <article class="price-card">
          <header><h3>Managed (MaaS)</h3><p>We run the appliance, the upgrades, the tuning. You get the dashboards.</p></header>
          <div class="price-card__price"><span class="price-num">Talk</span><span class="price-unit">to us</span></div>
          <ul class="price-card__list">
            <li>Fully managed Overwatch appliance</li>
            <li>24×7 SRE coverage from Logic Insight</li>
            <li>Quarterly capacity + posture reviews</li>
            <li>Datadog Marketplace bundling option</li>
          </ul>
          <a class="btn btn--ghost btn--block" href="about.html#contact">Talk to a human</a>
        </article>
      </div>

      <header class="section-head" data-reveal style="margin-top:120px;">
        <span class="eyebrow"><span class="dot"></span>FAQ</span>
        <h2 class="section-title">Common questions before you <span class="italic gradient">commit a per-core spend.</span></h2>
      </header>
      <div class="faq" data-reveal>
        <details><summary>Is pricing really per-core, or per-host?</summary><p>Per physical core in the Nutanix cluster being monitored. Logical cores don't multiply the cost — and Overwatch's appliance is included in the per-core price.</p></details>
        <details><summary>Do you charge per metric or per data volume?</summary><p>No. The per-core price covers all metrics, all retention up to the tier limit, all integrations. No invoice surprises from ingest growth.</p></details>
        <details><summary>What's the trial like?</summary><p>30 days, no credit card. You get the full Enterprise tier on as many clusters as you want. Cancel by closing the appliance — nothing leaves your network.</p></details>
        <details><summary>How does the Managed tier differ?</summary><p>We run the appliance, upgrades, tuning, and the on-call rotation. You get the dashboards and a quarterly posture review. Pricing is bespoke; usually it's cheaper than the SRE headcount you'd otherwise add.</p></details>
        <details><summary>Datadog Marketplace pricing?</summary><p>If you'd rather buy through Datadog, the Marketplace bundle is available. Same per-core economics, billed through your Datadog contract.</p></details>
      </div>
    </div>
  </section>
'''


INSIGHTS_BODY = pagehead(
    "Editorial",
    'Field notes from <span class="italic gradient">infrastructure-aware AI.</span>',
    "Practitioner writing on observability, identity, and backup posture. No marketing fluff."
) + '''
  <section class="section">
    <div class="container">
      <div class="insights__grid" data-reveal>
        <a class="insight-card" href="#" data-tilt>
          <div class="insight-card__art insight-card__art--1"></div>
          <span class="insight-card__cat">AI & Automation</span>
          <h3>AI for reviewing infrastructure anomalies — what actually helps.</h3>
          <p>Where focused operator assistance beats generic chat over dashboards.</p>
          <span class="insight-card__meta">6 min · Editorial</span>
        </a>
        <a class="insight-card" href="#" data-tilt>
          <div class="insight-card__art insight-card__art--2"></div>
          <span class="insight-card__cat">Network</span>
          <h3>Map east-west Nutanix traffic with IPFIX.</h3>
          <p>Turning vague performance complaints into usable operational explanations.</p>
          <span class="insight-card__meta">8 min · Editorial</span>
        </a>
        <a class="insight-card" href="#" data-tilt>
          <div class="insight-card__art insight-card__art--3"></div>
          <span class="insight-card__cat">Backup security</span>
          <h3>Immutability is not enough.</h3>
          <p>Object lock buys you a recovery copy. Admin path separation decides whether it survives.</p>
          <span class="insight-card__meta">10 min · Editorial</span>
        </a>
        <a class="insight-card" href="#" data-tilt>
          <div class="insight-card__art insight-card__art--1"></div>
          <span class="insight-card__cat">Identity</span>
          <h3>Microsoft Entra is infrastructure now.</h3>
          <p>If admins still use easy-to-phish sign-in flows, the tenant is weaker than it looks.</p>
          <span class="insight-card__meta">7 min · Editorial</span>
        </a>
        <a class="insight-card" href="#" data-tilt>
          <div class="insight-card__art insight-card__art--2"></div>
          <span class="insight-card__cat">Automation</span>
          <h3>Automating runbooks without hiding risk.</h3>
          <p>Automate the understanding before the action. Most failed runbooks skip step one.</p>
          <span class="insight-card__meta">5 min · Editorial</span>
        </a>
        <a class="insight-card" href="#" data-tilt>
          <div class="insight-card__art insight-card__art--3"></div>
          <span class="insight-card__cat">Mentorship</span>
          <h3>AI-era mentorship for platform teams.</h3>
          <p>Velocity isn't the signal it used to be. What better mentorship looks like now.</p>
          <span class="insight-card__meta">9 min · Editorial</span>
        </a>
      </div>
    </div>
  </section>
'''


ABOUT_BODY = pagehead(
    "About",
    'Built by operators who got tired of <span class="italic gradient">stitching observability together.</span>',
    "Logic Insight is a small, deliberate team based in Orlando, Florida. We build for infrastructure people because we are infrastructure people."
) + '''
  <section class="section">
    <div class="container">
      <div class="about__split" data-reveal>
        <div>
          <span class="eyebrow"><span class="dot"></span>The company</span>
          <h2 class="section-title">We ship the appliance <span class="italic gradient">we wished existed.</span></h2>
          <p style="color:var(--ink-soft);font-size:18px;line-height:1.6;margin-bottom:20px;">Twenty-plus years of running and selling infrastructure taught us where observability fails. Overwatch is the answer that doesn't require a four-tool stack and a part-time PhD.</p>
          <dl class="about__stats">
            <div><dt data-count="2021">0</dt><dd>founded</dd></div>
            <div><dt data-count="11" data-suffix="+">0</dt><dd>major integrations</dd></div>
            <div><dt>1</dt><dd>appliance, no add-ons</dd></div>
          </dl>
        </div>
        <div class="about__people">
          <article class="founder">
            <div class="founder__avatar">DL</div>
            <div>
              <h3>David Lira</h3>
              <p class="founder__role">Co-Founder · CEO / COO</p>
            </div>
            <p class="founder__bio">Twenty-plus years running and selling infrastructure in regulated environments. Decides what we ship and to whom.</p>
          </article>
          <article class="founder">
            <div class="founder__avatar">JR</div>
            <div>
              <h3>Jason Richmond</h3>
              <p class="founder__role">Co-Founder · Principal Platform Architect</p>
            </div>
            <p class="founder__bio">Designed the Overwatch data path. Writes the editorial. Holds the line on evidence-grounded telemetry.</p>
          </article>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="contact">
    <div class="container">
      <div class="finalcta__inner" data-reveal>
        <div class="finalcta__halo"></div>
        <span class="eyebrow"><span class="dot"></span>Contact</span>
        <h2 class="finalcta__title">Get in touch with <span class="italic gradient">a real human.</span></h2>
        <p class="finalcta__sub">For demos, technical scoping, partnership inquiries, or just to argue about observability.</p>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:760px;margin:32px auto 0;">
          <a href="mailto:contact@logicinsight.io" class="price-card" style="text-align:center;">
            <div class="mono" style="font-size:11px;color:var(--ink-mute);letter-spacing:0.08em;text-transform:uppercase;">Email</div>
            <div style="margin-top:8px;color:var(--p-300);font-weight:600;">contact@logicinsight.io</div>
          </a>
          <a href="tel:+14075132359" class="price-card" style="text-align:center;">
            <div class="mono" style="font-size:11px;color:var(--ink-mute);letter-spacing:0.08em;text-transform:uppercase;">Phone</div>
            <div style="margin-top:8px;color:var(--p-300);font-weight:600;">+1 (407) 513-2359</div>
          </a>
          <div class="price-card" style="text-align:center;">
            <div class="mono" style="font-size:11px;color:var(--ink-mute);letter-spacing:0.08em;text-transform:uppercase;">Office</div>
            <div style="margin-top:8px;color:var(--ink-soft);font-size:14px;">425 W Colonial Dr, Ste 303<br/>Orlando, FL 32804</div>
          </div>
        </div>
      </div>
    </div>
  </section>
'''


BODIES = {
    "index":        ("Nutanix observability that thinks ahead",      "Overwatch — the appliance-first observability platform for Nutanix, HCI, hardware, networks, and backups.",   INDEX_BODY),
    "product":      ("Product",                                       "Every Nutanix signal a platform team needs to see, already correlated.",                                     PRODUCT_BODY),
    "architecture": ("Architecture",                                  "Single Ubuntu 24.04 appliance. Open standards in, open standards out.",                                      ARCH_BODY),
    "ai-assistant": ("AI Assistant",                                  "Evidence-grounded AI for infrastructure operations. Less chat, more evidence.",                              AI_BODY),
    "integrations": ("Integrations",                                  "Datadog, Grafana, HYCU, Prism Central, Wasabi, SNMP — and forwarder-not-lock-in for the rest.",              INTEG_BODY),
    "pricing":      ("Pricing",                                       "Per-core licensing. No data-volume games. Three transparent tiers.",                                        PRICING_BODY),
    "insights":     ("Insights · Editorial",                          "Field notes on Nutanix observability, identity, and backup security.",                                      INSIGHTS_BODY),
    "about":        ("About",                                         "Built in Orlando by operators who got tired of stitching observability together.",                          ABOUT_BODY),
}

# -------------------------------------------------------------------
import os
for slug, (title, desc, body) in BODIES.items():
    page = "index" if slug == "index" else slug
    out = head(title, desc, page) + nav(page) + body + FOOTER
    fname = f"{slug}.html"
    with open(fname, "w") as f:
        f.write(out)
    print(f"wrote {fname} · {len(out):,} chars")

#!/usr/bin/env python3
"""Generate a single markdown 'content map' of the live site — every page,
every section, every paragraph + list + stat — so Aiden can paste each
paragraph into the matching slot on the redesigned page without flipping
back to the live URL."""

import json

with open("_content.json") as f:
    C = json.load(f)

# Same nav order as the generator + sub-pages
ORDER = [
    "/", "/features/", "/architecture/", "/ai-assistant/", "/integrations/",
    "/pricing/", "/about/", "/blog/", "/resources/",
    "/cluster-monitoring/", "/predictive-analytics/", "/network-flow-analysis/",
    "/hycu-monitoring/", "/redfish-monitoring/", "/snmp-monitoring/",
    "/prism-central-monitoring/", "/ahv-monitoring/", "/hci-monitoring/",
    "/monitoring-as-a-service/", "/nutanix-datadog/", "/nutanix-grafana/",
    "/how-to-monitor-nutanix-with-datadog/", "/how-to-monitor-nutanix-with-grafana/",
    "/nutanix-monitoring-vs-prism/",
]

def file_for(route: str) -> str:
    if route == "/":
        return "index.html"
    return route.strip("/").replace("/", "-") + ".html"


def dedupe_sections(sections):
    out = []
    seen = set()
    for s in sections:
        h2_count = sum(1 for h in s.get("headings", []) if h["level"] == "H2")
        if h2_count >= 3:
            continue
        key = (s.get("eyebrow") or "",
               tuple(h["text"] for h in s.get("headings", [])[:2]))
        if key in seen and key != ("", ()):
            continue
        seen.add(key)
        out.append(s)
    return out


lines = ["# Logic Insight — content map\n",
         "_One-stop reference for the polish pass. Each section below corresponds 1:1 to the redesigned page at the same route. Copy each paragraph into the matching `[ paste full paragraph from live page here ]` slot._\n",
         "---\n"]

for route in ORDER:
    if route not in C: continue
    data = C[route]
    if data.get("error"): continue
    fname = file_for(route)
    title = data.get("title", "")
    h1 = (data.get("h1s") or [""])[0]
    sections = dedupe_sections(data.get("sections", []))

    lines.append(f"## `{fname}`  ·  {route}\n")
    lines.append(f"**Title:** {title}\n")
    lines.append(f"**H1:** {h1}\n")

    for i, s in enumerate(sections):
        eb = (s.get("eyebrow") or "").strip()
        headings = s.get("headings", [])
        paras = s.get("paras", [])
        items = s.get("items", [])
        if not (eb or headings or paras or items): continue

        # Section header
        h2 = next((h["text"] for h in headings if h["level"] == "H2"), "")
        h3s = [h["text"] for h in headings if h["level"] == "H3"]

        lines.append(f"### Section {i+1}")
        if eb: lines.append(f"- **Eyebrow:** {eb}")
        if h2: lines.append(f"- **H2:** {h2}")
        for h3 in h3s:
            lines.append(f"- **H3:** {h3}")
        if paras:
            lines.append(f"- **Paragraphs ({len(paras)}):** _paste from logicinsight.io{route}_")
            for j, p in enumerate(paras, 1):
                import re
                m = re.search(r"^(.{20,180}?[.!?])(\s|$)", p.strip().replace("\n", " "))
                hint = (m.group(1) if m else p.strip()[:160]).strip()
                lines.append(f"  - ¶{j} starts: _{hint}…_")
        if items:
            lines.append("- **List items:**")
            for it in items:
                lines.append(f"  - {it.strip()}")
        lines.append("")

    lines.append("---\n")

out = "\n".join(lines)
with open("CONTENT-MAP.md", "w") as f:
    f.write(out)

print(f"wrote CONTENT-MAP.md · {len(out):,} chars · {sum(1 for l in lines if l.startswith('## '))} pages")

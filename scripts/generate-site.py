#!/usr/bin/env python3
"""
Generate the Supply Chain Guardian demonstration website.
Produces a professional dark-themed site with attack flow diagrams,
scanner module documentation, and links to generated reports.

Copyright (c) 2025-2026 Anshumaan Singh. All rights reserved.
"""
import os
import datetime

SITE_DIR = "public"
TOOLS_DIR = os.path.join(SITE_DIR, "tools", "supply-chain-guardian")
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

CSS = """
:root {
  --bg: #121318;
  --surface: #1a1b23;
  --surface-hover: #22232e;
  --border: #2a2b35;
  --text: #e0e0e6;
  --muted: #8b8d9a;
  --accent: #4f8cff;
  --accent-dim: rgba(79,140,255,0.12);
  --critical: #ef4444;
  --critical-dim: rgba(239,68,68,0.12);
  --high: #f97316;
  --high-dim: rgba(249,115,22,0.12);
  --medium: #eab308;
  --green: #22c55e;
  --green-dim: rgba(34,197,94,0.12);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Header */
.header {
  background: linear-gradient(135deg, #0f1019 0%, #1a1b2e 50%, #171825 100%);
  border-bottom: 1px solid var(--border);
  padding: 3.5rem 2rem 3rem;
}
.header-inner { max-width: 960px; margin: 0 auto; }
.header h1 {
  font-size: 2.25rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  margin-bottom: 0.5rem;
}
.header .subtitle {
  color: var(--muted);
  font-size: 1.05rem;
  max-width: 640px;
  line-height: 1.7;
}
.badges { margin-top: 1.25rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
.badge {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: 4px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}
.badge-critical { background: var(--critical-dim); color: var(--critical); }
.badge-high { background: var(--high-dim); color: var(--high); }
.badge-accent { background: var(--accent-dim); color: var(--accent); }
.badge-green { background: var(--green-dim); color: var(--green); }

/* Layout */
.container { max-width: 960px; margin: 0 auto; padding: 2rem; }

/* Stats Grid */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
.stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem;
  transition: border-color 0.2s;
}
.stat:hover { border-color: var(--accent); }
.stat-value { font-size: 1.6rem; font-weight: 700; }
.stat-label { color: var(--muted); font-size: 0.82rem; margin-top: 0.25rem; }

/* Section */
.section { margin: 2.5rem 0; }
.section h2 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}

/* Card */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: border-color 0.2s, background 0.2s;
}
.card:hover { border-color: var(--accent); background: var(--surface-hover); }
.card h3 { font-size: 1.05rem; margin-bottom: 0.5rem; }
.card p { color: var(--muted); font-size: 0.9rem; margin-bottom: 0.75rem; }
.card-link {
  font-weight: 600;
  font-size: 0.9rem;
}

/* Attack Flow */
.attack-flow {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 2rem 1.5rem;
  margin: 1rem 0;
}
.flow-step {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1.25rem;
  position: relative;
}
.flow-step:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 13px;
  top: 32px;
  bottom: -10px;
  width: 2px;
  background: var(--border);
}
.flow-num {
  width: 28px; height: 28px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700;
  flex-shrink: 0;
  margin-right: 1rem;
  margin-top: 1px;
  position: relative;
  z-index: 1;
}
.flow-num.red { background: var(--critical-dim); color: var(--critical); }
.flow-num.green { background: var(--green-dim); color: var(--green); }
.flow-content h4 { font-size: 0.95rem; margin-bottom: 0.15rem; }
.flow-content p { color: var(--muted); font-size: 0.85rem; margin: 0; }

/* Scanners Grid */
.scanners-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}
.scanner-item {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.85rem;
  font-size: 0.85rem;
  transition: border-color 0.15s;
}
.scanner-item:hover { border-color: var(--accent); }
.scanner-item strong { display: block; margin-bottom: 0.2rem; color: var(--text); }
.scanner-item span { color: var(--muted); }

/* Pipeline Stages */
.pipeline { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0; }
.pipeline-stage {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.6rem 1rem;
  font-size: 0.82rem;
  font-weight: 500;
}
.pipeline-stage .num {
  color: var(--accent);
  font-weight: 700;
  margin-right: 0.35rem;
}

/* Footer */
.footer {
  border-top: 1px solid var(--border);
  padding: 2rem;
  text-align: center;
  color: var(--muted);
  font-size: 0.85rem;
  margin-top: 3rem;
}
.footer a { color: var(--accent); }
.footer p + p { margin-top: 0.4rem; }
"""

SCANNERS = [
    ("Signature Scanner", "110+ known attack patterns"),
    ("Dependency Analyzer", "Compromised and malicious packages"),
    ("Permission Auditor", "Least-privilege enforcement"),
    ("Network Monitor", "Reverse shells, C2 callbacks"),
    ("Secret Detector", "Hardcoded credentials, API keys"),
    ("Workflow Analyzer", "Injection, unsafe triggers"),
    ("Cache Inspector", "Poisoning vectors"),
    ("Container Scanner", "Image pinning, privilege escalation"),
    ("OIDC Validator", "Token scope abuse, identity confusion"),
    ("Artifact Auditor", "Path traversal, overwrite, TOCTOU"),
    ("Binary Analyzer", "Executable detection, entropy analysis"),
    ("Runtime Monitor", "Process behavior, file access"),
    ("Egress Controller", "Unauthorized outbound connections"),
    ("Injection Scanner", "Script and expression injection"),
    ("CI Config Auditor", "Jenkins, GitLab, Azure, CircleCI"),
    ("Obfuscation Detector", "Base64, eval chains, encoded payloads"),
    ("Exception Engine", "Allowlist and override management"),
]

PIPELINE_STAGES = [
    "Signature Detection",
    "Deep Multi-Scanner Analysis",
    "Runtime Behavioral Monitoring",
    "Exception Engine",
    "Paranoid Zero-Trust Audit",
    "Security Tab Integration",
    "Report Deployment",
    "Pipeline Summary",
]

ATTACK_FLOW = [
    ("red", "Initial Compromise",
     "Attacker publishes a typosquatted package (reqeusts instead of requests) "
     "or compromises a popular GitHub Action (tj-actions/changed-files)."),
    ("red", "Silent Execution",
     "Malicious postinstall script runs during npm install. Obfuscated payload "
     "decodes via base64 and executes in the CI runner environment."),
    ("red", "Credential Theft",
     "Payload reads GITHUB_TOKEN, AWS keys, and CI secrets from environment "
     "variables. Data exfiltrated via DNS tunneling or HTTPS to attacker C2 server."),
    ("red", "Lateral Movement",
     "Stolen tokens used to access private repositories, modify package releases, "
     "and inject backdoors into downstream build artifacts."),
    ("green", "Supply Chain Guardian Detection",
     "SCG identifies the attack at multiple stages: compromised action reference, "
     "malicious package in manifest, obfuscated payload, network exfiltration, "
     "and runtime behavioral anomaly."),
]

def render_scanners():
    items = ""
    for name, desc in SCANNERS:
        items += f'<div class="scanner-item"><strong>{name}</strong><span>{desc}</span></div>\n'
    return items

def render_pipeline():
    stages = ""
    for i, name in enumerate(PIPELINE_STAGES, 1):
        stages += f'<div class="pipeline-stage"><span class="num">{i}</span>{name}</div>\n'
    return stages

def render_attack_flow():
    steps = ""
    for i, (color, title, desc) in enumerate(ATTACK_FLOW, 1):
        steps += f'''<div class="flow-step">
  <div class="flow-num {color}">{i}</div>
  <div class="flow-content"><h4>{title}</h4><p>{desc}</p></div>
</div>\n'''
    return steps

def build_page():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Supply Chain Guardian - Threat Detection Reports</title>
<style>{CSS}</style>
</head>
<body>
<div class="header">
  <div class="header-inner">
    <h1>Supply Chain Guardian</h1>
    <p class="subtitle">Enterprise-grade supply chain security scanner for CI/CD pipelines.
    Detects compromised dependencies, stolen credentials, network exfiltration, container escape,
    and 110+ real-world attack patterns across GitHub Actions, GitLab CI, Jenkins, and Azure DevOps.</p>
    <div class="badges">
      <span class="badge badge-critical">110+ Attack Patterns</span>
      <span class="badge badge-accent">17 Scanner Modules</span>
      <span class="badge badge-high">20 Attack Scenarios</span>
      <span class="badge badge-green">GitHub Marketplace</span>
    </div>
  </div>
</div>

<div class="container">
  <div class="stats">
    <div class="stat"><div class="stat-value" style="color:var(--critical)">110+</div><div class="stat-label">Attack Patterns</div></div>
    <div class="stat"><div class="stat-value" style="color:var(--accent)">17</div><div class="stat-label">Scanner Modules</div></div>
    <div class="stat"><div class="stat-value" style="color:var(--high)">37</div><div class="stat-label">Vulnerable Scenarios</div></div>
    <div class="stat"><div class="stat-value" style="color:var(--green)">8</div><div class="stat-label">Pipeline Stages</div></div>
  </div>

  <div class="section">
    <h2>Scan Reports</h2>
    <div class="card">
      <h3>Deep Multi-Scanner Analysis</h3>
      <p>Full scan with all 17 scanner modules, binary analysis, and dependency auditing.
      Covers workflow security, secret detection, network monitoring, permission auditing,
      container scanning, OIDC validation, and artifact integrity checks.</p>
      <span class="badge badge-accent">17 Scanners</span>
      <span class="badge badge-critical">Binary Analysis</span>
      <br><br>
      <a class="card-link" href="/supply-chain-guardian-demo/reports/deep-scan-report.html">View Deep Scan Report</a>
    </div>
    <div class="card">
      <h3>Paranoid Zero-Trust Audit</h3>
      <p>Maximum detection sensitivity with egress validation, /tmp and /dev/shm sweep,
      cross-platform CI/CD configuration audit, and strict fail thresholds.
      The most comprehensive scan mode available.</p>
      <span class="badge badge-critical">Paranoid Mode</span>
      <span class="badge badge-high">Zero Trust</span>
      <br><br>
      <a class="card-link" href="/supply-chain-guardian-demo/reports/paranoid-audit-report.html">View Paranoid Audit Report</a>
    </div>
  </div>

  <div class="section">
    <h2>Pipeline Stages</h2>
    <p style="color:var(--muted); font-size:0.9rem; margin-bottom:1rem;">
      The showcase pipeline runs 8 stages to demonstrate each capability of Supply Chain Guardian.
    </p>
    <div class="pipeline">
      {render_pipeline()}
    </div>
  </div>

  <div class="section">
    <h2>How a Supply Chain Attack Works</h2>
    <div class="attack-flow">
      {render_attack_flow()}
    </div>
  </div>

  <div class="section">
    <h2>Scanner Modules</h2>
    <div class="scanners-grid">
      {render_scanners()}
    </div>
  </div>

  <div class="section">
    <h2>Resources</h2>
    <div class="card">
      <p style="line-height:2">
        <a href="https://github.com/anshumaan-10/supply-chain-guardian">Source Code (GitHub)</a><br>
        <a href="https://github.com/marketplace/actions/supply-chain-guardian">GitHub Marketplace Listing</a><br>
        <a href="https://github.com/anshumaan-10/supply-chain-guardian-demo">Demo Repository</a>
      </p>
    </div>
  </div>

  <div class="footer">
    <p>Supply Chain Guardian v4 &middot; Built by <a href="https://github.com/anshumaan-10">Anshumaan Singh</a></p>
    <p><a href="https://github.com/anshumaan-10/supply-chain-guardian">Source</a> &middot;
    <a href="https://github.com/marketplace/actions/supply-chain-guardian">Marketplace</a> &middot;
    <a href="https://github.com/anshumaan-10/supply-chain-guardian-demo">Demo</a></p>
    <p>&copy; 2025-2026 Anshumaan Singh. All rights reserved.</p>
    <p style="margin-top:0.5rem; font-size:0.8rem;">Last updated: {NOW}</p>
  </div>
</div>
</body>
</html>'''


def main():
    os.makedirs(TOOLS_DIR, exist_ok=True)
    os.makedirs(os.path.join(SITE_DIR, "reports"), exist_ok=True)

    # Main page at /tools/supply-chain-guardian/
    page = build_page()
    with open(os.path.join(TOOLS_DIR, "index.html"), "w") as f:
        f.write(page)

    # Root redirect
    with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
        f.write(
            '<html><head>'
            '<meta http-equiv="refresh" content="0;url=/supply-chain-guardian-demo/tools/supply-chain-guardian/">'
            '</head><body>'
            '<p>Redirecting to <a href="/supply-chain-guardian-demo/tools/supply-chain-guardian/">Supply Chain Guardian</a>...</p>'
            '</body></html>'
        )

    print("Site generated successfully.")
    print(f"  Landing page: {TOOLS_DIR}/index.html")
    print(f"  Root redirect: {SITE_DIR}/index.html")


if __name__ == "__main__":
    main()

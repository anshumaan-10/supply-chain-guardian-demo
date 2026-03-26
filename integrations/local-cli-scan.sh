#!/usr/bin/env bash
# =============================================================================
#  Supply Chain Guardian — Local CLI Scanner
#  Copyright (c) 2025-2026 Anshumaan Singh. All rights reserved.
#
#  Run SCG locally from any developer machine or CI runner.
#
#  Usage:
#    ./local-cli-scan.sh                       # scan current directory
#    ./local-cli-scan.sh /path/to/project      # scan specific project
#    ./local-cli-scan.sh --mode paranoid .      # paranoid scan
#    ./local-cli-scan.sh --html report.html .   # generate HTML report
# =============================================================================
set -euo pipefail

# ─── Defaults ───────────────────────────────────────────────────────────────
SCG_REPO="https://github.com/anshumaan-10/supply-chain-guardian.git"
SCG_DIR="${HOME}/.supply-chain-guardian"
SCAN_MODE="deep"
FAIL_SEVERITY="high"
VERBOSE="true"
HTML_OUTPUT=""
JSON_OUTPUT=""
SARIF_OUTPUT="false"
TARGET_DIR=""

# ─── Colors ─────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ─── Banner ─────────────────────────────────────────────────────────────────
banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║   ⛨  Supply Chain Guardian — Local Scanner                 ║"
    echo "║      Detect supply chain attacks before they ship          ║"
    echo "║                                                            ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ─── Usage ──────────────────────────────────────────────────────────────────
usage() {
    cat <<USAGE
${BOLD}Usage:${NC}
  $(basename "$0") [options] [target-directory]

${BOLD}Options:${NC}
  --mode <quick|deep|paranoid>   Scan mode (default: deep)
  --fail <severity>              Fail threshold: low|medium|high|critical (default: high)
  --html <path>                  Generate HTML report at specified path
  --json <path>                  Generate JSON report at specified path
  --sarif                        Generate SARIF output (supply-chain-guardian.sarif)
  --quiet                        Reduce output verbosity
  --update                       Force re-download of SCG
  --help                         Show this help message

${BOLD}Examples:${NC}
  $(basename "$0")                                    # Deep scan current directory
  $(basename "$0") --mode paranoid /path/to/project   # Paranoid scan
  $(basename "$0") --html report.html --sarif .       # Full reports
  $(basename "$0") --mode quick --quiet .             # Fast, minimal output

USAGE
}

# ─── Parse arguments ───────────────────────────────────────────────────────
FORCE_UPDATE=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --mode)     SCAN_MODE="$2"; shift 2 ;;
        --fail)     FAIL_SEVERITY="$2"; shift 2 ;;
        --html)     HTML_OUTPUT="$2"; shift 2 ;;
        --json)     JSON_OUTPUT="$2"; shift 2 ;;
        --sarif)    SARIF_OUTPUT="true"; shift ;;
        --quiet)    VERBOSE="false"; shift ;;
        --update)   FORCE_UPDATE=true; shift ;;
        --help|-h)  banner; usage; exit 0 ;;
        -*)         echo -e "${RED}Unknown option: $1${NC}"; usage; exit 1 ;;
        *)          TARGET_DIR="$1"; shift ;;
    esac
done

# Default target to current directory
TARGET_DIR="${TARGET_DIR:-.}"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

# ─── Check Python ──────────────────────────────────────────────────────────
check_python() {
    if command -v python3 &>/dev/null; then
        PYTHON=python3
    elif command -v python &>/dev/null; then
        PYTHON=python
    else
        echo -e "${RED}Error: Python 3.9+ is required but not found.${NC}"
        echo "Install Python: https://www.python.org/downloads/"
        exit 1
    fi

    local version
    version=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local major minor
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)

    if [[ $major -lt 3 ]] || [[ $major -eq 3 && $minor -lt 9 ]]; then
        echo -e "${RED}Error: Python 3.9+ required, found ${version}${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} Python ${version} found"
}

# ─── Install/Update SCG ───────────────────────────────────────────────────
install_scg() {
    if [[ -d "$SCG_DIR" ]] && [[ "$FORCE_UPDATE" == "false" ]]; then
        echo -e "${GREEN}✓${NC} SCG already installed at ${SCG_DIR}"
        return
    fi

    echo -e "${YELLOW}↓${NC} Downloading Supply Chain Guardian..."
    rm -rf "$SCG_DIR"
    git clone --depth 1 "$SCG_REPO" "$SCG_DIR" 2>/dev/null
    echo -e "${GREEN}✓${NC} SCG installed"
}

# ─── Install Dependencies ──────────────────────────────────────────────────
install_deps() {
    local deps="pyyaml requests tabulate colorama jsonschema semver"
    echo -e "${YELLOW}↓${NC} Checking Python dependencies..."

    for dep in $deps; do
        if ! $PYTHON -c "import $dep" 2>/dev/null; then
            $PYTHON -m pip install --quiet "$dep" 2>/dev/null || true
        fi
    done
    echo -e "${GREEN}✓${NC} Dependencies ready"
}

# ─── Run Scan ──────────────────────────────────────────────────────────────
run_scan() {
    echo ""
    echo -e "${BOLD}Scanning:${NC}  ${TARGET_DIR}"
    echo -e "${BOLD}Mode:${NC}     ${SCAN_MODE}"
    echo -e "${BOLD}Fail on:${NC}  ${FAIL_SEVERITY}"
    echo ""

    local env_vars=(
        "INPUT_SCAN_MODE=${SCAN_MODE}"
        "INPUT_FAIL_ON_SEVERITY=${FAIL_SEVERITY}"
        "INPUT_VERBOSE=${VERBOSE}"
    )

    [[ -n "$JSON_OUTPUT" ]] && env_vars+=("INPUT_JSON_OUTPUT=${JSON_OUTPUT}")
    [[ -n "$HTML_OUTPUT" ]] && env_vars+=("INPUT_HTML_OUTPUT=true" "INPUT_HTML_OUTPUT_PATH=${HTML_OUTPUT}")
    [[ "$SARIF_OUTPUT" == "true" ]] && env_vars+=("INPUT_SARIF_OUTPUT=true")

    env "${env_vars[@]}" $PYTHON "${SCG_DIR}/src/main.py" --workspace "$TARGET_DIR"
    local exit_code=$?

    echo ""
    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  ✅  Supply chain scan PASSED        ║${NC}"
        echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
    else
        echo -e "${RED}╔══════════════════════════════════════╗${NC}"
        echo -e "${RED}║  🚨  Supply chain issues detected!   ║${NC}"
        echo -e "${RED}╚══════════════════════════════════════╝${NC}"
    fi

    # Report file locations
    echo ""
    [[ -n "$JSON_OUTPUT" && -f "$JSON_OUTPUT" ]] && echo -e "  📄 JSON report: ${JSON_OUTPUT}"
    [[ -n "$HTML_OUTPUT" && -f "$HTML_OUTPUT" ]] && echo -e "  🌐 HTML report: ${HTML_OUTPUT}"
    [[ "$SARIF_OUTPUT" == "true" && -f "supply-chain-guardian.sarif" ]] && echo -e "  🔍 SARIF report: supply-chain-guardian.sarif"

    return $exit_code
}

# ─── Main ──────────────────────────────────────────────────────────────────
main() {
    banner
    check_python
    install_scg
    install_deps
    run_scan
}

main

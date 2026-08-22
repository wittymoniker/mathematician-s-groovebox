#!/usr/bin/env bash
# ==============================================================================
# Filename: groovebox.sh
# Description: Primary shell launcher for the Equation of Reality (EQR) Ultimate Groovebox.
# ==============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}==============================================================${NC}"
echo -e "${CYAN}  Equation of Reality (EQR) - Ultimate Groovebox Launcher     ${NC}"
echo -e "${CYAN}==============================================================${NC}"

# 1. Environment Overrides & Master Configurations
export EQR_CORE_FREQ="432.0"
export EQR_SURVIVAL_MODE="1"
export EQR_CREATIVE_MODE="0"
export EQR_SPATIAL_DIMENSIONS="x,y,z"
export EQR_MODULAR_BAY_ACTIVE="1"
export PYTHONUNBUFFERED="1"

echo -e "${YELLOW}[*] Environment Initialized:${NC}"
echo -e "    - Reference Pitch    = ${GREEN}${EQR_CORE_FREQ} Hz${NC}"
echo -e "    - Spatial Space      = ${GREEN}${EQR_SPATIAL_DIMENSIONS}${NC}"
echo -e "    - Survival Mode      = ${GREEN}Active${NC}"
echo -e "    - Modular Patch Bay  = ${GREEN}Online${NC}"

# 2. Dependency Verification
echo -e "${YELLOW}[*] Checking Python dependencies (PyQt6)...${NC}"
if ! python3 -c "import PyQt6" &> /dev/null; then
    echo -e "${RED}[!] PyQt6 is missing. Installing required packages...${NC}"
    pip install --upgrade PyQt6
else
    echo -e "${GREEN}[+] PyQt6 dependency verified.${NC}"
fi

# 3. Target Script Validation
TARGET_SCRIPT="groovebox.py"

if [ ! -f "$TARGET_SCRIPT" ]; then
    echo -e "${RED}[!] Error: Ultimate suite script '${TARGET_SCRIPT}' not found.${NC}"
    echo -e "${YELLOW}[*] Please save the Python module script in the current directory before launching.${NC}"
    exit 1
fi

echo -e "${GREEN}[+] Ultimate suite located: ${TARGET_SCRIPT}${NC}"
echo -e "${CYAN}--------------------------------------------------------------${NC}"
echo -e "${GREEN}[*] Initializing GUI workstation and cross-tab wiring bay...${NC}"

# 4. Execute Master Suite
exec python3 "$TARGET_SCRIPT"

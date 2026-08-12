#!/bin/bash
# Load config and run Strix scan

cd /Users/aletatos/Documents/VDStrix/vdstrix

# Add Docker and uv to PATH
export PATH="/Volumes/Docker/Docker.app/Contents/Resources/bin:$HOME/.local/bin:$PATH"

# Load LLM config from cli-config.json
CONFIG_FILE="$HOME/.strix/cli-config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

# Extract values using Python
export STRIX_LLM=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['env']['STRIX_LLM'])")
export LLM_API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['env']['LLM_API_KEY'])")
export LLM_API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['env']['LLM_API_BASE'])")

# Run Strix with all arguments passed through
uv run strix "$@"

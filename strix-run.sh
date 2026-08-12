#!/bin/bash
# Strix wrapper script to handle Docker path from /Volumes/

# Add Docker to PATH
export PATH="/Volumes/Docker/Docker.app/Contents/Resources/bin:$HOME/.local/bin:$PATH"

# Load environment variables
if [ -f "$(dirname "$0")/.env" ]; then
    export $(cat "$(dirname "$0")/.env" | grep -v '^#' | xargs)
fi

# Run strix with all arguments
uv run strix "$@"

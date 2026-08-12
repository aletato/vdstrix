#!/bin/bash
# Quick alias to run Strix commands easily

# Source this file to add strix alias to your current shell:
# source ./strix-alias.sh

# Add Docker and uv to PATH
export PATH="/Volumes/Docker/Docker.app/Contents/Resources/bin:$HOME/.local/bin:$PATH"

# Create convenient alias
alias strix='cd /Users/aletatos/Documents/VDStrix/vdstrix && uv run strix'

echo "✅ Strix alias created!"
echo ""
echo "Usage examples:"
echo "  strix --help"
echo "  strix --target ./your-app"
echo "  strix view"

#!/bin/bash
# Setup script for Strix with DiodosAPI and Claude Sonnet 5

set -e

echo "🚀 Setting up Strix with DiodosAPI..."

# Check if API key is provided
if [ -z "$1" ]; then
    echo "❌ Error: API key required"
    echo "Usage: ./setup-diodos.sh YOUR_API_KEY"
    exit 1
fi

API_KEY="$1"

# Add uv to PATH
export PATH="$HOME/.local/bin:$PATH"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "⚠️  Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Create Strix config directory
mkdir -p ~/.strix

# Create CLI config
echo "📝 Creating Strix configuration..."
cat > ~/.strix/cli-config.json << EOF
{
  "llm": {
    "model": "anthropic/claude-sonnet-5",
    "api_key": "${API_KEY}",
    "api_base": "https://api.diodosapi.com/v1",
    "reasoning_effort": "high"
  },
  "telemetry": {
    "enabled": true
  },
  "runtime": {
    "image": "ghcr.io/usestrix/strix-sandbox:1.3.0",
    "backend": "docker"
  }
}
EOF

# Create .env file
cat > .env << EOF
# Strix Configuration for DiodosAPI with Claude Sonnet 5
STRIX_LLM=anthropic/claude-sonnet-5
LLM_API_KEY=${API_KEY}
LLM_API_BASE=https://api.diodosapi.com/v1
STRIX_REASONING_EFFORT=high
STRIX_RUNTIME_BACKEND=docker
STRIX_IMAGE=ghcr.io/usestrix/strix-sandbox:1.3.0
EOF

echo "✅ Configuration created successfully!"
echo ""
echo "📦 Installing dependencies (this may take a few minutes)..."
uv sync

echo ""
echo "🐳 Pulling Docker sandbox image..."
docker pull ghcr.io/usestrix/strix-sandbox:1.3.0

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Quick Start Commands:"
echo "   Test configuration:  uv run strix --help"
echo "   Scan a local app:    uv run strix --target ./your-app"
echo "   Scan a URL:          uv run strix --target https://example.com"
echo "   View results:        uv run strix view"
echo ""
echo "📚 Full documentation: https://docs.strix.ai"

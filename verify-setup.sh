#!/bin/bash
# Strix Setup Verification Script

echo "🔍 Verifying Strix Setup..."
echo ""

# Check uv
echo "1️⃣  Checking uv package manager..."
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    echo "   ✅ uv installed: $UV_VERSION"
else
    echo "   ❌ uv not found"
    exit 1
fi

# Check Python
echo ""
echo "2️⃣  Checking Python..."
PYTHON_VERSION=$(python3 --version)
echo "   ✅ $PYTHON_VERSION"

# Check Docker
echo ""
echo "3️⃣  Checking Docker..."
export PATH="/Volumes/Docker/Docker.app/Contents/Resources/bin:$HOME/.local/bin:$PATH"
if docker info &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "   ✅ Docker running: $DOCKER_VERSION"
else
    echo "   ❌ Docker not running or not accessible"
    exit 1
fi

# Check Docker image
echo ""
echo "4️⃣  Checking Strix sandbox image..."
if docker images | grep -q "usestrix/strix-sandbox"; then
    echo "   ✅ Strix sandbox image present"
else
    echo "   ⚠️  Strix sandbox image not found (may still be downloading)"
fi

# Check Strix installation
echo ""
echo "5️⃣  Checking Strix installation..."
cd "$(dirname "$0")"
export PATH="/Volumes/Docker/Docker.app/Contents/Resources/bin:$HOME/.local/bin:$PATH"
if uv run strix --version &> /dev/null; then
    STRIX_VERSION=$(uv run strix --version)
    echo "   ✅ Strix installed: $STRIX_VERSION"
else
    echo "   ❌ Strix not accessible"
    exit 1
fi

# Check configuration
echo ""
echo "6️⃣  Checking configuration..."
if [ -f "$HOME/.strix/cli-config.json" ]; then
    echo "   ✅ Configuration file exists: ~/.strix/cli-config.json"

    # Check if API key is configured
    if grep -q "sk-diodos" "$HOME/.strix/cli-config.json"; then
        echo "   ✅ DiodosAPI key configured"
    else
        echo "   ⚠️  API key may not be configured"
    fi

    # Check model configuration
    if grep -q "claude-sonnet-5" "$HOME/.strix/cli-config.json"; then
        echo "   ✅ Model: Claude Sonnet 5"
    fi

    # Check API base
    if grep -q "diodosapi.com" "$HOME/.strix/cli-config.json"; then
        echo "   ✅ API Base: DiodosAPI"
    fi
else
    echo "   ❌ Configuration file not found"
    exit 1
fi

echo ""
echo "================================================"
echo "✅ Setup verification complete!"
echo "================================================"
echo ""
echo "🎯 Ready to use Strix. Try these commands:"
echo ""
echo "   ./strix-run.sh --help"
echo "   ./strix-run.sh --target https://example.com"
echo "   ./strix-run.sh view"
echo ""
echo "Or with full PATH:"
echo "   export PATH=\"/Volumes/Docker/Docker.app/Contents/Resources/bin:\$HOME/.local/bin:\$PATH\""
echo "   uv run strix --target ./your-app"

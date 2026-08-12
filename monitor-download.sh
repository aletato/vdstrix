#!/bin/bash
# Monitor Docker image download progress

echo "🔍 Monitoring Docker image download..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

export PATH="/Volumes/Docker/Docker.app/Contents/Resources/bin:$HOME/.local/bin:$PATH"

# Check every 30 seconds
while true; do
    # Check if docker pull process is still running
    PULL_RUNNING=$(ps aux | grep "docker pull ghcr.io/usestrix/strix-sandbox" | grep -v grep | wc -l)

    # Check if image exists
    IMAGE_EXISTS=$(docker images | grep -c "strix-sandbox")

    if [ "$IMAGE_EXISTS" -gt 0 ]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✅ Docker image download complete!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        docker images | grep strix-sandbox
        echo ""
        echo "🚀 Strix is ready to use!"
        echo ""
        echo "Start a scan with:"
        echo "  ./strix-run.sh --target https://diodosapi.com"
        echo ""
        break
    elif [ "$PULL_RUNNING" -eq 0 ]; then
        echo ""
        echo "⚠️  Download process ended but image not found."
        echo "Check for errors in the download."
        break
    else
        echo -n "."
        sleep 30
    fi
done

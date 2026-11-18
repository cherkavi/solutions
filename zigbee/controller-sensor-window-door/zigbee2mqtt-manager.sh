
#!/usr/bin/env bash

set -euo pipefail

# Configuration
COMPOSE_DIR="/opt/zigbee2mqtt"
CONTAINER_NAME="zigbee2mqtt"
WEB_URL="http://localhost:8081"

# Check Docker Compose directory
if [[ ! -d "$COMPOSE_DIR" ]]; then
    echo "ERROR: Directory does not exist: $COMPOSE_DIR" >&2
    exit 1
fi

cd "$COMPOSE_DIR"

# Detect Docker Compose command
if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE=(docker-compose)
else
    echo "ERROR: Docker Compose is not installed." >&2
    exit 1
fi

case "${1:-}" in
    start)
        echo "Starting $CONTAINER_NAME..."
        "${DOCKER_COMPOSE[@]}" up -d
        ;;

    logs)
        echo "Showing logs for $CONTAINER_NAME..."
        docker logs -f "$CONTAINER_NAME"
        ;;

    stop|shutdown)
        echo "Stopping $CONTAINER_NAME..."
        "${DOCKER_COMPOSE[@]}" down
        ;;

    restart)
        echo "Restarting $CONTAINER_NAME..."
        "${DOCKER_COMPOSE[@]}" restart "$CONTAINER_NAME"
        ;;

    status)
        echo "Docker Compose status:"
        "${DOCKER_COMPOSE[@]}" ps
        ;;

    start-browser)
        echo "Opening Zigbee2MQTT: $WEB_URL"
        x-www-browser "$WEB_URL" &
        ;;

    *)
        echo "Usage: $0 {start|logs|stop|shutdown|restart|status|start-browser}"
        exit 1
        ;;
esac

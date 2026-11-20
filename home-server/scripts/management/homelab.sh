#!/usr/bin/env bash
# Script: homelab.sh
# Description: Manually manages independent Docker Compose projects.
# Usage:
#   homelab.sh list|status
#   homelab.sh up|down|restart|logs|pull|config PROJECT
# Projects: smart-home storage monitoring infrastructure development ai
# Notes: pull downloads images only; it does not recreate running containers.

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$ROOT/.env"
COMPOSE_ROOT="$ROOT/compose"

PROJECTS=(smart-home storage monitoring infrastructure development ai)

usage() {
  cat <<EOF
Usage: $0 COMMAND [PROJECT]
Commands:
  list                 List known projects
  status               Show containers across all projects
  up PROJECT           Start project
  down PROJECT         Stop and remove project containers (keeps bind-mounted data)
  restart PROJECT      Restart project
  logs PROJECT         Follow project logs
  pull PROJECT         Download images only
  config PROJECT       Validate and render Compose configuration
EOF
}

project_dir() {
  local p="$1" found=false
  for known in "${PROJECTS[@]}"; do
    if [[ "$p" == "$known" ]]; then found=true; break; fi
  done
  [[ "$found" == true ]] || { echo "Unknown project: $p" >&2; usage; exit 2; }
  [[ -f "$COMPOSE_ROOT/$p/compose.yaml" ]] || { echo "Missing compose file for $p" >&2; exit 1; }
  printf '%s' "$COMPOSE_ROOT/$p"
}

docker_cmd() {
  if docker info >/dev/null 2>&1; then
    docker "$@"
  else
    sudo docker "$@"
  fi
}

compose() {
  local p="$1"; shift
  local dir
  dir="$(project_dir "$p")"
  local args=(--project-directory "$dir" -f "$dir/compose.yaml")
  [[ ! -f "$ENV_FILE" ]] || args+=(--env-file "$ENV_FILE")
  docker_cmd compose "${args[@]}" "$@"
}

cmd="${1:-}"
case "$cmd" in
  list)
    printf '%s\n' "${PROJECTS[@]}"
    ;;
  status)
    docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
    ;;
  up|down|restart|logs|pull|config)
    [[ $# -eq 2 ]] || { usage; exit 2; }
    project="$2"
    case "$cmd" in
      up) compose "$project" up -d ;;
      down) compose "$project" down ;;
      restart) compose "$project" restart ;;
      logs) compose "$project" logs -f --tail=200 ;;
      pull) compose "$project" pull ;;
      config) compose "$project" config --quiet && echo "Compose configuration valid: $project" ;;
    esac
    ;;
  *) usage; exit 2 ;;
esac

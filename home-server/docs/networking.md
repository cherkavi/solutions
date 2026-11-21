# Networking

## Wi-Fi
```bash
ip -br link
nmcli device status
```

## Ports
| Service              | Port          | Exposure recommendation                    |
| ---                  | ---:          | ---                                        |
| SSH                  | 22/tcp        | LAN + Tailscale only                       |
| Home Assistant       | 8123/tcp      | LAN + Tailscale                            |
| Zigbee2MQTT frontend | 8081/tcp      | LAN + Tailscale                            |
| MQTT                 | 1883/tcp      | Host loopback only in this template        |
| Syncthing GUI        | 8384/tcp      | Host loopback; use SSH tunnel or Tailscale |
| Syncthing transfer   | 22000/tcp+udp | Trusted LAN / peers as required            |
| Uptime Kuma          | 3001/tcp      | LAN + Tailscale                            |
| AdGuard DNS          | 53/tcp+udp    | Only after careful router/DNS testing      |
| AdGuard UI           | 3000/tcp      | Admin network only                         |
| Gitea                | 3000/tcp      | Admin network only                         |
| Gitea SSH            | 2222/tcp      | Admin network only                         |
| PostgreSQL           | 5432/tcp      | Loopback only                              |
| Qdrant API           | 6333/tcp      | Loopback only                              |
| Ollama API           | 11434/tcp     | Loopback only                              |


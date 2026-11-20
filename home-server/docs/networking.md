# Networking

## Wi-Fi

- Reserve a stable DHCP address in the router.
- Prefer 5 GHz Wi-Fi for the mini PC if signal quality is reliable.
- Keep the Zigbee coordinator physically separated from the mini PC and USB 3 devices using a USB extension cable.
- Verify Wi-Fi reconnects after reboot and after an access-point restart.
- Consider a USB Ethernet adapter if reliability becomes an issue.

Do not guess the Wi-Fi interface name. Discover it with:

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

## Docker firewall caveat

Docker-published ports can bypass UFW rules. Do not assume `ufw deny` protects every published container port. Follow Docker's firewall documentation and enforce restrictions using the supported Docker firewall path (such as `DOCKER-USER` with iptables), or bind services to loopback where remote access is unnecessary.

Do not mix an independently managed nftables ruleset with Docker without understanding Docker's iptables integration.

## Tailscale

Install Tailscale on the Ubuntu host. This preserves administrative access when application containers are stopped. Avoid publishing services to the public Internet merely to access them remotely.

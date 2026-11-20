# Infrastructure

Optional AdGuard Home. DNS port 53 is published on all host interfaces by default. Do not start this project until you have planned DNS ownership, stable addressing, firewall access and a fallback resolver. Port 53 may already be in use by systemd-resolved or another DNS service; inspect first.

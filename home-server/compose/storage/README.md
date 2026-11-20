# Storage

Syncthing configuration is persistent under `/srv/homelab/data/syncthing`; synchronized content is under `/srv/homelab/files`.

The Web GUI binds to host loopback. Use an SSH tunnel, for example `ssh -L 8384:127.0.0.1:8384 USER@SERVER`, then browse to `http://127.0.0.1:8384`.

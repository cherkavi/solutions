# Publish this project to a public GitHub repository

This repository is designed to be public, but contains no real secrets by default.

## 1. Create the repository

On GitHub, create a new **public** repository named `homelab-ubuntu`.
Do not initialize it with a README, license or `.gitignore`, because this
project already contains those files.

## 2. Review before the first commit

From the project root:

```bash
git status --short
git diff --check
find . -type f | sort
```

Check that `.env`, credentials, private keys, MQTT password files, application
data and backups are not present. The `.gitignore` protects common paths, but
you must still inspect the files yourself.

## 3. Initialize and push

```bash
git init
git add .
git status
git diff --cached --check
git commit -m "Initial Ubuntu homelab infrastructure"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USER/homelab-ubuntu.git
git push -u origin main
```

Use GitHub's normal authentication (SSH keys or Git Credential Manager).
Never place a personal access token in a remote URL or script.

## 4. Normal manual workflow

```bash
git add docs scripts compose config
git commit -m "Describe the infrastructure change"
git push
```

On the server, deployment remains manual:

```bash
cd /opt/homelab-ubuntu
git pull --ff-only
# Review changes, validate Compose, back up data, then manually apply.
```

There is intentionally no GitHub Actions workflow that deploys to the server.

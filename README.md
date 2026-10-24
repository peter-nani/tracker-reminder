# Tracker Reminder

A standalone Python + Docker project that sends one randomly selected tracker-update
message to a Google Chat incoming webhook, with a randomly selected star-style emoji.

This project is independent and contains no scheduler integration or files from another project.

## Requirements

- Docker Engine and Docker Compose plugin
- A Google Chat incoming webhook URL

## Configure

```bash
cp .env.example .env
```

Edit `.env` and set `CHAT_WEBHOOK_URL` to your actual Google Chat incoming webhook URL.
Never commit `.env` or print the webhook URL in logs.

`CHAT_REQUEST_TIMEOUT_SECONDS` defaults to `30`; `LOG_LEVEL` defaults to `INFO`.

## Build and start

```bash
docker compose build
docker compose up -d
```

The container uses the requested command:

```dockerfile
CMD ["tail", "-f", "/dev/null"]
```

The container stays alive so the reminder script can be invoked on demand.

## Send a reminder manually

```bash
docker exec tracker-reminder python /app/tracker_reminder.py
```

The program sends one message each time it runs. Run the command again to send another.

## View logs

```bash
docker logs -f tracker-reminder
```

Logs include startup, selected-message count, success, missing configuration, invalid timeout,
and HTTP/network failures. The webhook URL is never logged.

## Missing webhook

The container can start without the webhook. When the script runs, it logs an error and exits
with status 1. After changing `.env`, recreate the container to load new environment values:

```bash
docker compose up -d --force-recreate
```

## Run without Docker (optional)

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app/tracker_reminder.py
```

Set `CHAT_WEBHOOK_URL` in your shell before running outside Docker.

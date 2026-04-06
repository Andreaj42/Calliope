# Calliope

**Calliope** is a tool designed to automate the analysis of Google Scholar alert emails.  
It retrieves incoming alerts via IMAP, processes them using a language model, and outputs structured insights based on a customizable research profile.

## Features

- Automatic retrieval of Google Scholar alerts from an email inbox (iCloud IMAP supported)
- Filtering and scoring of papers based on a user-defined research profile
- Integration with LLMs (via Ollama) for analysis
- Automated daily execution using Docker and systemd

## Requirements

- Python 3.12+
- Docker (for automated deployment)
- An email account with IMAP access (tested with iCloud)
- A running Ollama instance (local or remote)

---

## Installation

### Email Configuration

Create a mail rule that automatically moves all Google Scholar alert emails into a dedicated folder (e.g., `Papers`).

---

## Running from Source

```bash
python src/main.py
```

## Automated Execution (Debian VM)
### 1. Install Docker

### 2. Create Required Files  
#### a. Execution script  
```
sudo nano /usr/local/bin/calliope.sh
```

```
#!/usr/bin/env bash
set -euo pipefail

# --- Config ---
IMAGE="ghcr.io/andreaj42/calliope:latest"

docker pull "$IMAGE"

timeout 4h docker run --rm \
  --name calliope-$(date +%Y%m%d-%H%M%S) \
  --network host \
  --env-file /etc/calliope.env \
  "$IMAGE"
```
Set correct permissions:  
```
sudo chown root:root /usr/local/bin/calliope.sh 
sudo chmod 755 /usr/local/bin/calliope.sh
```

#### b. Environment variables  
```
sudo nano /etc/calliope.env
```
```
IMAP_HOST=imap.mail.me.com
IMAP_PORT=993
SMTP_HOST=smtp.mail.me.com
SMTP_PORT=587
EMAIL_ADDRESS=mymailaccount@icloud.com
EMAIL_PASSWORD=your_specific_password
RECIPIENT_MAIL=recipient_mail@domain.com
FOLDER=Papers

OLLAMA_URL=http://urls:ports/api/generate
OLLAMA_MODEL=llama3

RESEARCH_PROFILE=I am a PhD candidate working on deep learning for radio commun....
TASK="Score rubric (0-100):\n- 0-20: unrelated to radio signals or deep learnin...
```

#### c. Systemd service  
```
sudo nano /etc/systemd/system/calliope.service
```
```
[Unit]
Description=Daily Calliope Job
Wants=network-online.target
After=network-online.target docker.service
Requires=docker.service

[Service]
Type=oneshot

ExecStart=/usr/bin/flock -n /run/calliope.lock /usr/local/bin/calliope.sh

TimeoutStartSec=3h
KillMode=control-group

StandardOutput=journal
StandardError=journal
```

#### d. Systemd timer  
```
sudo nano /etc/systemd/system/calliope.timer
```
```
[Unit]
Description=Run Calliope Job

[Timer]
OnCalendar=*-*-* 03:15:00
Persistent=true

Unit=calliope.service

[Install]
WantedBy=timers.target
```

### 3. Enable and Start the Automation
```
sudo systemctl daemon-reload
sudo systemctl enable --now calliope.timer
sudo systemctl start calliope.service
```

### 4. Monitoring
```
systemctl status calliope.timer
sudo journalctl -xeu calliope.service
```

# Zohun Telegram Userbot - Deployment Guide

## Prerequisites

- Ubuntu/Debian VPS dengan minimal 1GB RAM
- Python 3.11 atau lebih baru
- Git installed

## Installation Steps

### 1. Clone Repository

```bash
cd /root
git clone https://github.com/zhelvano/rim.git rimbot
cd rimbot
```

### 2. Install Python Dependencies

```bash
# Install system dependencies
apt update
apt install -y python3-pip python3-venv ffmpeg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
nano .env
```

Required environment variables:
- `API_ID` - Get from https://my.telegram.org
- `API_HASH` - Get from https://my.telegram.org
- `BOT_TOKEN` - Get from @BotFather
- `OWNER_ID` - Your Telegram user ID
- `LOG_SELLER` - Channel/group ID for seller logs
- `LOG_BACKUP` - Channel/group ID for backup logs

Optional variables:
- `SUDO_OWNERS` - Space-separated user IDs
- `SPOTIFY_CLIENT_ID` & `SPOTIFY_CLIENT_SECRET` - For Spotify features
- `API_GEMINI` - For Gemini AI features

### 4. Test Run

```bash
# Activate venv if not already activated
source venv/bin/activate

# Run the bot
python -m Zohun
```

If everything works correctly, press `Ctrl+C` to stop and set up systemd service.

### 5. Setup Systemd Service

Create service file:

```bash
sudo nano /etc/systemd/system/zohunbot.service
```

Add the following content (adjust paths if needed):

```ini
[Unit]
Description=Zohun Telegram Userbot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/rimbot
Environment="PATH=/root/rimbot/venv/bin"
ExecStart=/root/rimbot/venv/bin/python -m Zohun
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable zohunbot
sudo systemctl start zohunbot
```

### 6. Check Status

```bash
# Check service status
sudo systemctl status zohunbot

# View logs
sudo journalctl -u zohunbot -f

# Restart bot
sudo systemctl restart zohunbot

# Stop bot
sudo systemctl stop zohunbot
```

## Troubleshooting

### Bot doesn't start

1. Check logs: `sudo journalctl -u zohunbot -n 50`
2. Verify all environment variables in `.env`
3. Ensure all dependencies installed: `pip install -r requirements.txt`

### Database errors

- Delete database files and restart: `rm -f *.db storage/*.session`
- Bot will create fresh databases on next start

### Permission errors

- Ensure bot is running as correct user
- Check file permissions: `chmod +x run_bot.sh`

## Updating

```bash
cd /root/rimbot
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart zohunbot
```

## Security Notes

- Keep your `.env` file secure
- Never share your `API_HASH` or `BOT_TOKEN`
- Use strong passwords for VPS access
- Enable firewall: `ufw allow ssh && ufw enable`

## Support

For issues, check GitHub repository or contact support.

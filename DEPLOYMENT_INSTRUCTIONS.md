# DEPLOYMENT INSTRUCTIONS

## Quick VPS Deployment Steps

### 1. Prerequisites Check
```bash
# Check Python version (must be 3.10+)
python3 --version

# Install system dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git
```

### 2. Extract and Setup
```bash
# Extract the uploaded ZIP
unzip rimarus-fixed.zip
cd rimarus

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# IMPORTANT: Edit .env with your actual credentials
nano .env
```

**Critical Variables to Set:**
- `API_ID`: Get from https://my.telegram.org
- `API_HASH`: Get from https://my.telegram.org  
- `BOT_TOKEN`: Create bot with @BotFather
- `BOT_ID`: Extract from BOT_TOKEN (numbers before colon)
- `OWNER_ID`: Your Telegram user ID (use @userinfobot)
- `LOG_SELLER`: Create a private channel, make bot admin, get ID
- `LOG_BACKUP`: Create another private channel for backups

### 4. Run the Bot

**Option A: Direct Run (for testing)**
```bash
cd Zohun
python __main__.py
```

**Option B: Using Start Script**
```bash
chmod +x start.sh
./start.sh
```

**Option C: Systemd Service (production)**
```bash
# Edit the service file first
sudo nano zohunbot.service
# Update User, WorkingDirectory, and ExecStart paths

# Install service
sudo cp zohunbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable zohunbot
sudo systemctl start zohunbot

# Check status
sudo systemctl status zohunbot

# View logs
journalctl -u zohunbot -f
```

### 5. Verify Installation
```bash
# Check if bot is running
ps aux | grep python

# Check logs for errors
tail -f Zohun/bot.log  # if logging to file

# Test bot
# Send /start to your bot on Telegram
```

## Troubleshooting

### Issue: Import Errors
**Solution**: All import errors (kb, ikb) have been fixed in this version

### Issue: Database Errors  
```bash
rm -rf Zohun/database/*.db
# Restart bot to recreate database
```

### Issue: Permission Denied
```bash
chmod +x *.sh
chmod -R 755 rimarus/
```

### Issue: Module Not Found
```bash
pip install -r requirements.txt --upgrade --force-reinstall
```

## Security Best Practices

1. Never share `.env` file
2. Never commit `token.json` to git
3. Use strong session secrets
4. Keep your VPS firewall configured
5. Regular backups of database folder

## Monitoring

```bash
# Watch logs in real-time
tail -f /path/to/logs

# Monitor system resources
htop

# Check bot process
systemctl status zohunbot
```

---
**Note**: This version includes all bug fixes for kb/ikb errors and CHAT_ID_INVALID issues.

# Zohun Ubot - Telegram Userbot

A powerful Telegram userbot built with Hydrogram framework.

## 🔧 Fixed Issues

This version fixes the following errors:
- ✅ Fixed `name 'kb' is not defined` error
- ✅ Fixed `name 'ikb' is not defined` error  
- ✅ Fixed `CHAT_ID_INVALID` error with improved error handling
- ✅ Added proper keyboard button imports and implementations
- ✅ Improved chat join error handling with delays and logging

## 📋 Prerequisites

- Python 3.10 or higher
- A Telegram account
- Telegram API credentials (API_ID and API_HASH)
- A Telegram Bot Token (from @BotFather)

## 🚀 VPS Deployment Setup

### 1. Upload and Extract

```bash
# Upload the ZIP file to your VPS
# Extract it
unzip rimarus-fixed.zip
cd rimarus
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install required packages
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your credentials
nano .env  # or use your preferred editor
```

**Required environment variables:**
- `API_ID`: Your Telegram API ID (get from https://my.telegram.org)
- `API_HASH`: Your Telegram API Hash
- `BOT_TOKEN`: Your bot token from @BotFather
- `BOT_ID`: Your bot's numeric ID
- `OWNER_ID`: Your Telegram user ID
- `LOG_SELLER`: Telegram channel ID for logs (format: -100xxxxxxxxxx)
- `LOG_BACKUP`: Telegram channel ID for backups

### 4. Start the Bot

#### Using Python directly:
```bash
cd Zohun
python __main__.py
```

#### Using the start script (recommended):
```bash
chmod +x start.sh
./start.sh
```

#### As a systemd service (for auto-restart):
```bash
# Copy the service file
sudo cp zohunbot.service /etc/systemd/system/

# Edit the service file with correct paths
sudo nano /etc/systemd/system/zohunbot.service

# Enable and start the service
sudo systemctl enable zohunbot
sudo systemctl start zohunbot

# Check status
sudo systemctl status zohunbot

# View logs
sudo journalctl -u zohunbot -f
```

## 📝 Configuration

### Environment Variables

Edit the `.env` file to configure:

- **API Configuration**: Your Telegram API credentials
- **Admin Settings**: Owner and sudo user IDs
- **Logging**: Channel IDs for logging and backups
- **API Keys**: Optional third-party API keys (Gemini, Spotify, etc.)
- **Payment**: Saweria integration (optional)

### Database

The bot uses SQLite database stored in `Zohun/database/`.
The database file will be created automatically on first run.

## 🛠️ Troubleshooting

### Common Issues:

**1. Import Errors (`kb` or `ikb` not defined)**
- ✅ Already fixed in this version
- The keyboard button functions are now properly imported

**2. CHAT_ID_INVALID Error**
- ✅ Already fixed with improved error handling
- The bot now handles chat joins with delays and proper logging

**3. Module Not Found Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**4. Permission Errors**
```bash
# Make scripts executable
chmod +x start.sh run_bot.sh setup.sh
```

**5. Database Errors**
```bash
# Remove existing database (WARNING: This deletes all data)
rm -rf Zohun/database/*.db
# Restart the bot to create a fresh database
```

## 📦 Project Structure

```
rimarus/
├── Zohun/              # Core bot framework
│   ├── clients/       # Client management
│   ├── database/      # Database operations
│   ├── helpers/       # Helper functions and utilities
│   └── logger/        # Logging system
├── assistant/         # Bot assistant commands
├── plugins/           # User bot plugins
├── storage/           # Cached files and assets
├── config/            # Configuration files
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (create from .env.example)
```

## 🔐 Security Notes

- Never share your `.env` file or `token.json`
- Keep your API credentials secure
- Don't commit sensitive data to git
- Use strong session security

## 📞 Support

For issues or questions:
- Check the logs in your LOG_SELLER channel
- Review the console output for error messages
- Ensure all environment variables are correctly set

## 📄 License

See LICENSE file for details.

## ⚠️ Disclaimer

This bot is for educational purposes. Use responsibly and comply with Telegram's Terms of Service.

---

**Version**: 1.0-fixed  
**Last Updated**: November 2025  
**Status**: Production Ready ✅

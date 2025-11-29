# Zohun Telegram Bot

## Overview
Telegram userbot built with Pyrogram 2.0 for advanced Telegram automation features. The bot includes HTML blockquote support fix and comprehensive plugin system.

## Recent Changes (November 27, 2025)
- **Fixed HTML blockquote**: Added patch for `reply_text` method (previously only `reply` was patched)
- **Fixed AFK MESSAGE_EMPTY error**: Added fallback text when AFK message is empty
- **Improved Autoreply**: Now replies to ALL messages in group (not just replies to userbot)
- **Fixed Chatbot Groq AI**: Changed model from array to string format
- Installed all required dependencies (pyrogram, aiohttp, google-generativeai, etc.)
- Bot successfully loads 201 modules

## Project Structure
```
Zohun/                  # Core bot framework
  __init__.py           # Main initialization with HTML patch (reply, reply_text, edit, edit_text)
  __main__.py           # Bot entry point
  clients/              # Pyrogram client management
  database/             # SQLite database handlers
  helpers/              # Utility functions (tools, buttons, commands, afk)
  logger.py             # Logging configuration

plugins/                # Bot command plugins
  autoreply.py          # Auto reply ALL messages with Groq AI
  chatbot.py            # Chatbot with Groq AI integration
  afk.py                # AFK mode with MESSAGE_EMPTY fix
  chibi.py              # Image generation with error handling
  ... (200+ plugins)

assistant/              # Bot assistant features
config/                 # Configuration management
storage/                # Session and data storage
```

## Key Features
- **HTML blockquote rendering** (auto-detects HTML tags in reply, reply_text, edit, edit_text)
- **Autoreply AI** - Replies to ALL messages in group using Groq AI
- **Chatbot AI** - Chat with Groq AI when someone replies to userbot
- Plugin system with 200+ commands
- Multi-userbot support
- Spotify integration
- YouTube downloader
- AI integrations (Gemini, Groq)

## Environment Variables Required
- API_ID, API_HASH: Telegram API credentials
- BOT_TOKEN: Bot token from BotFather
- GROQ_API_KEY: Groq API key for AI chatbot/autoreply
- API_GEMINI: Google Gemini API key
- OWNER_ID: Owner's Telegram ID
- Other optional: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

## Running the Bot
```bash
python3 run_bot.py
```

## Commands
- `.autoreply on` - Enable AI autoreply for all messages in group
- `.autoreply off` - Disable autoreply
- `.chatbot on` - Enable chatbot (replies when someone replies to userbot)
- `.chatbot off` - Disable chatbot
- `.afk <reason>` - Set AFK status (reply to a message)
- `.unafk` - Remove AFK status

## Technical Notes
- HTML patch is applied in Zohun/__init__.py using monkey-patching
- Patches applied: Message.reply, Message.reply_text, Message.edit, Message.edit_text
- pytgcalls modules (streaming, vctools) are optional due to dependency conflicts
- The bot uses SQLite for local database storage
- Groq AI model: llama-3.1-8b-instant

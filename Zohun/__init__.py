import importlib
import os
import re

try:
    import pyromod  # Enable conversation (.ask() method)
except (ImportError, TypeError, Exception):
    pyromod = None  # Will use custom conversation handler
from pyrogram import filters, enums
from pyrogram.handlers import (CallbackQueryHandler, DeletedMessagesHandler,
                               DisconnectHandler, EditedMessageHandler,
                               MessageHandler, UserStatusHandler)
from pyrogram.types import BotCommand, Message

def _apply_html_patch():
    """Apply HTML parse mode patch to Message class for blockquote support"""
    from functools import wraps
    
    def _has_html_tags(text):
        if not text or not isinstance(text, str):
            return False
        html_tags = ["<blockquote>", "<b>", "<i>", "<code>", "<pre>", 
                     "<a ", "<u>", "<s>", "<strike>", "<emoji", "<tg-emoji",
                     "<spoiler>", "</blockquote>", "</b>", "</i>", "</code>"]
        return any(tag in text for tag in html_tags)
    
    _original_reply = Message.reply
    _original_edit_text = Message.edit_text
    
    @wraps(_original_reply)
    async def patched_reply(self, text=None, *args, parse_mode=None, **kwargs):
        if text is not None and parse_mode is None:
            if _has_html_tags(str(text)):
                parse_mode = enums.ParseMode.HTML
        return await _original_reply(self, text, *args, parse_mode=parse_mode, **kwargs)
    
    @wraps(_original_edit_text)
    async def patched_edit_text(self, text, *args, parse_mode=None, **kwargs):
        if parse_mode is None:
            if _has_html_tags(str(text)):
                parse_mode = enums.ParseMode.HTML
        return await _original_edit_text(self, text, *args, parse_mode=parse_mode, **kwargs)
    
    Message.reply = patched_reply
    Message.edit_text = patched_edit_text
    
    # Also patch reply_text (alias for reply in some cases)
    if hasattr(Message, 'reply_text'):
        _original_reply_text = Message.reply_text
        @wraps(_original_reply_text)
        async def patched_reply_text(self, text=None, *args, parse_mode=None, **kwargs):
            if text is not None and parse_mode is None:
                if _has_html_tags(str(text)):
                    parse_mode = enums.ParseMode.HTML
            return await _original_reply_text(self, text, *args, parse_mode=parse_mode, **kwargs)
        Message.reply_text = patched_reply_text
    
    if hasattr(Message, 'edit'):
        _original_edit = Message.edit
        @wraps(_original_edit)
        async def patched_edit(self, text=None, *args, parse_mode=None, **kwargs):
            if text is not None and parse_mode is None:
                if _has_html_tags(str(text)):
                    parse_mode = enums.ParseMode.HTML
            return await _original_edit(self, text, *args, parse_mode=parse_mode, **kwargs)
        Message.edit = patched_edit

_apply_html_patch()

try:
    from pytgcalls import PyTgCalls
    from pytgcalls import filters as fl
    PYTGCALLS_AVAILABLE = True
except ImportError:
    PyTgCalls = None
    fl = None
    PYTGCALLS_AVAILABLE = False

from config import (AKSES_DEPLOY, API_HASH, API_ID, BOT_ID, BOT_NAME,
                    BOT_TOKEN, HELPABLE, OWNER_ID, SUDO_OWNERS)
from Zohun.clients import BaseClient
from Zohun.database import dB
from Zohun.logger import logger
from plugins import PLUGINS

if not os.path.exists("downloads"):
    os.makedirs("downloads")


list_error = []


class UserBot(BaseClient):
    __module__ = "pyrogram.client"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device_model = BOT_NAME
        if PYTGCALLS_AVAILABLE:
            self.group_call = PyTgCalls(self)
        else:
            self.group_call = None

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def on_edited_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(EditedMessageHandler(func, filters), group)
            return func

        return decorator

    def on_deleted_messages(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(DeletedMessagesHandler(func, filters), group)
            return func

        return decorator

    def on_disconnect(self):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(DisconnectHandler(func))
            return func

        return decorator

    def group_call_ends(self):
        def decorator(func):
            if PYTGCALLS_AVAILABLE:
                for ub in self._ubot:
                    if ub.group_call:
                        ub.group_call.on_update(fl.stream_end)(func)
            return func

        return decorator

    def user_prefix(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, client, message):
            if message.text:
                text = message.text.strip().encode("utf-8").decode("utf-8")
                username = client.me.username or ""
                prefixes = self.get_prefix(client.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix) :]

                    # Handle both string and filter objects
                    commands = cmd.split("|") if isinstance(cmd, str) else [str(cmd)]
                    for command in commands:
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        message.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True

                return False

        return filters.create(func)

    async def start(self):
        await super().start()
        if self.group_call and PYTGCALLS_AVAILABLE:
            try:
                await self.group_call.start()
            except Exception as e:
                logger.warning(f"Failed to start group call: {e}")
        prefixes = await dB.get_pref(self.me.id)
        if prefixes:
            self._prefix[self.me.id] = prefixes
        else:
            self._prefix[self.me.id] = [".", ",", "?", "+", "!"]
        self._ubot.append(self)
        self._get_my_id.append(self.me.id)
        logger.info(f"Starting Userbot {self.me.id}|@{self.me.username}")


class Bot(BaseClient):
    def __init__(self, **kwargs):
        super().__init__(
            name="Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            device_model=BOT_NAME,
            plugins=dict(root="assistant"),
            **kwargs,
        )

    def on_message(self, filters=None, group=-1):
        def decorator(function):
            self.add_handler(MessageHandler(function, filters), group)
            return function

        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(function):
            self.add_handler(CallbackQueryHandler(function, filters), group)
            return function

        return decorator

    async def add_reseller(self):
        for user in SUDO_OWNERS:
            if user not in await dB.get_list_from_var(BOT_ID, "SELLER"):
                await dB.add_to_var(BOT_ID, "SELLER", user)
        if OWNER_ID not in await dB.get_list_from_var(BOT_ID, "SELLER"):
            await dB.add_to_var(BOT_ID, "SELLER", OWNER_ID)
        for user in await dB.get_list_from_var(BOT_ID, "SELLER"):
            if user not in AKSES_DEPLOY:
                AKSES_DEPLOY.append(user)

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.fullname = f"{self.me.first_name} {self.me.last_name or ''}"
        self.username = self.me.username
        self.mention = self.me.mention
        
        # Register conversation handler if using custom implementation
        try:
            from Zohun.helpers.conversation import handle_response
            
            async def conversation_handler(client, message):
                # Check if message is a response to pending conversation
                if handle_response(message):
                    message.stop_propagation()
            
            # Add with high priority (group -2) to catch before other handlers
            self.add_handler(MessageHandler(conversation_handler), group=-2)
            logger.info("✅ Conversation handler registered")
        except ImportError:
            pass  # pyromod is handling it

        await self.set_bot_commands(
            [
                BotCommand("start", "Start the bot."),
                BotCommand("status", "Status account."),
                BotCommand("referral", "Information about Referral."),
                BotCommand("token", "Information about token."),
                BotCommand("close", "Close keyboard button."),
                BotCommand("restart", "Restart userbots."),
            ]
        )
        logger.info("🔄 Importing Modules")
        loaded_count = 0
        failed_count = 0
        skipped_count = 0
        for modul in PLUGINS:
            try:
                imported_module = importlib.import_module(f"plugins.{modul}")
                # Support both __MODULES__ (plural) and __MODULE__ (singular)
                module_name = getattr(imported_module, "__MODULES__", None)
                if not module_name:
                    module_name = getattr(imported_module, "__MODULE__", None)
                
                if module_name:
                    module_name = module_name.lower() if module_name else ""
                    HELPABLE[module_name] = imported_module
                    loaded_count += 1
                else:
                    # Skip modules without __MODULES__ or __MODULE__ (usually helper modules)
                    skipped_count += 1
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Failed to import {modul}: {e}")
                import traceback
                logger.debug(traceback.format_exc())
                # Continue loading other plugins instead of crashing
                continue
        logger.info(f"✅ Loaded {loaded_count} modules successfully")
        if skipped_count > 0:
            logger.info(f"ℹ️ Skipped {skipped_count} helper modules (no __MODULES__ attribute)")
        if failed_count > 0:
            logger.warning(f"⚠️ Failed to load {failed_count} modules")
        logger.info(f"🔥 {self.username} Bot Started 🔥")


zohun = UserBot(name="Clients")
bot = Bot()

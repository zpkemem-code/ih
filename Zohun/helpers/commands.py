import asyncio
import sys
import traceback
from functools import wraps

from pyrogram import enums, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

from config import BOT_ID, FAKE_DEVS, RIMZOHUN, LOG_BACKUP, OWNER_ID, SUDO_OWNERS
from Zohun import bot, zohun
from Zohun.database import dB

from .emoji_logs import Emoji

trigger = r"^(💬 Jawab Pesan|👤 Akun|❌ Batalkan|✨ Mulai Buat Userbot|❓ Status Akun|🔄 Reset Emoji|🔄 Reset Prefix|🔄 Restart Userbot|🔄 Reset Text|🚀 Updates|👥 Cek User|🛠️ Cek Fitur|🤔 Pertanyaan|↩️ Beranda|✨ Pembuatan Ulang Userbot|💬 Hubungi Admins|/copy|/close|/get|/restart|/id|/button|✅ Lanjutkan Buat Userbot|start|restart|/start|🎟️ Referral|🔑 Token)"
words = trigger.replace("^(", "").replace(")", "").split("|")
wrapped_words = [f'"{word}"' for word in words]
no_trigger = "[" + ", ".join(wrapped_words) + "]"
no_commands = [
    "💬 Jawab Pesan",
    "👤 Akun",
    "❌ Batalkan",
    "✨ Mulai Buat Userbot",
    "❓ Status Akun",
    "🔄 Reset Emoji",
    "🔄 Reset Prefix",
    "🔄 Restart Userbot",
    "✅ Lanjutkan Buat Userbot",
    "🔄 Reset Text",
    "🚀 Updates",
    "👥 Cek User",
    "🛠️ Cek Fitur",
    "🤔 Pertanyaan",
    "↩️ Beranda",
    "✨ Pembuatan Ulang Userbot",
    "💬 Hubungi Admins",
    "📃 Saya Setuju",
    "kontol",
    "close",
    "restart",
    "id",
    "button",
]


async def verified_sudo(_, client, message):
    # Import bot to access global permissions
    from Zohun import bot
    from Zohun.logger import logger
    
    # Get all permission lists from both client (per-userbot) and bot (global)
    # Check client-specific permissions (per-userbot)
    sudo_users = await dB.get_list_from_var(client.me.id, "SUDOERS")
    
    # The following global permission lists are for the main bot and should NOT
    # grant access to userbot commands. They are commented out to fix the issue.
    # Check global permissions (shared across all userbots)
    # prem_users = await dB.get_list_from_var(bot.me.id, "PREM_USERS")
    # seler_users = await dB.get_list_from_var(bot.me.id, "SELER_USERS")
    # admin_users = await dB.get_list_from_var(bot.me.id, "ADMIN_USERS")
    
    is_user = message.from_user if message.from_user else message.sender_chat
    is_self = bool(
        message.from_user
        and message.from_user.is_self
        or getattr(message, "outgoing", False)
    )
    
    # Get user ID and ensure it's an integer for comparison
    user_id = int(is_user.id) if is_user else None
    
    # Debug logging (commented out for production, uncomment to debug)
    # logger.debug(f"Permission check: user_id={user_id}, is_self={is_self}")
    # logger.debug(f"  sudo_users={sudo_users}")
    # logger.debug(f"  prem_users={prem_users}")
    # logger.debug(f"  seler_users={seler_users}")
    # logger.debug(f"  admin_users={admin_users}")
    
    # Check if user has permission:
    # 1. If the message is from the userbot itself (owner)
    # 2. If the user is in the specific userbot's sudoers list
    has_permission = (
        is_self or
        (user_id and user_id in sudo_users)
        # Global permissions for the main bot are no longer checked here
    )
    
    return has_permission


async def is_contact(_, client, message):
    is_user = message.from_user if message.from_user else None
    if not is_user.is_contact:
        return True
    return False


async def is_support(_, client, message):
    is_chat = message.chat if message.chat else None
    if not is_chat.is_support:
        return True
    return False


async def is_blocked(_, __, message):
    if message.sender_chat:
        return
    return bool(
        message.from_user and message.from_user.status == enums.UserStatus.LONG_AGO
    )


class FILTERS:
    PRIVATE = filters.private
    OWNER = filters.user(OWNER_ID)
    FAKE_DEV2 = filters.user(OWNER_ID)
    DEVELOPER = filters.user(RIMZOHUN) & ~filters.me
    FAKE_DEV = filters.user(FAKE_DEVS) & ~filters.me


class CMD:
    @staticmethod
    def split_limits(text):
        if len(text) < 2048:
            return [text]

        lines = text.splitlines(True)
        small_msg = ""
        result = []
        for line in lines:
            if len(small_msg) + len(line) < 2048:
                small_msg += line
            else:
                result.append(small_msg)
                small_msg = line
        else:
            result.append(small_msg)

        return result

    @staticmethod
    def capture_err(func):
        @wraps(func)
        async def capture(client, message):
            try:
                return await func(client, message)
            except Exception as err:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                errors = traceback.format_exception(exc_type, exc_value, exc_traceback)
                msg = message.chat or message.from_user
                error_feedback = CMD.split_limits(
                    "❌**ERROR** | `{}` | `{}`\n\n<pre>{}</pre>\n\n<pre>{}</pre>\n".format(
                        client.me.id,
                        msg.id,
                        message.text or message.caption,
                        "".join(errors),
                    ),
                )
                # Send error logs to LOG_BACKUP channel (with error handling)
                try:
                    for x in error_feedback:
                        await bot.send_message(LOG_BACKUP, x)
                except Exception as log_error:
                    # If logging fails, print to console instead of crashing
                    print(f"⚠️  Failed to send error log to LOG_BACKUP: {log_error}")
                    print(f"Original error: {err}")
                    # Log the actual error traceback to console for debugging
                    print("Error traceback:", "".join(errors))
                
                raise err

        return capture

    @staticmethod
    def FLOOD_HANDLER(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                return await func(*args, **kwargs)

        return wrapper

    @staticmethod
    def BOT(command, filter=None):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            @CMD.FLOOD_HANDLER
            @CMD.capture_err
            async def wrapped_func(client, message):
                user = message.from_user if message.from_user else message.sender_chat
                if user.id in await dB.get_list_from_var(client.me.id, "BANNED_USERS"):
                    return
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def UBOT(command, sudo=True):
        if sudo:
            filter = filters.create(verified_sudo)
        else:
            filter = filters.me

        def wrapper(func):
            @zohun.on_message(zohun.user_prefix(command) & filter)
            @CMD.FLOOD_HANDLER
            @CMD.capture_err
            async def wrapped_func(client, message):

                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def UBOT_REGEX(command, filter=None):
        if filter is None:
            filter = filters.create(verified_sudo)

        def wrapper(func):
            @zohun.on_message(filters.regex(command) & filters.me & filter)
            @CMD.FLOOD_HANDLER
            async def wrapped_func(client, message):
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def DELETED():
        def wrapper(func):
            @zohun.on_deleted_messages(filters.incoming & ~filters.me & ~filters.bot)
            async def wrapped_func(client, messages):
                return await func(client, messages)

            return wrapped_func

        return wrapper

    @staticmethod
    def CONNECT():
        def wrapper(func):
            @zohun.on_disconnect()
            async def wrapped_func(client):
                return await func(client)

            return wrapped_func

        return wrapper
        
    @staticmethod
    def USER_STATUS():
        def wrapper(func):
            @zohun.on_user_status()
            async def wrapped_func(client, users):
                return await func(client, users)

            return wrapped_func

        return wrapper

    @staticmethod
    def EDITED():
        def wrapper(func):
            @zohun.on_edited_message(
                (
                    filters.mentioned
                    & filters.incoming
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.me
                )
                | (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.service
                )
            )
            @CMD.capture_err
            async def wrapped_func(client, message):

                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def OWNER(func):
        async def function(client, message):
            user = message.from_user if message.from_user else message.sender_chat
            if user.id != OWNER_ID:
                return
            return await func(client, message)

        return function

    @staticmethod
    def NLX(func):
        async def function(client, message):
            user = message.from_user if message.from_user else message.sender_chat
            if user.id not in RIMZOHUN:
                return
            return await func(client, message)

        return function

    @staticmethod
    def FAKE_NLX(func):
        async def function(client, message):
            user = message.from_user if message.from_user else message.sender_chat
            if user.id not in SUDO_OWNERS:
                return
            return await func(client, message)

        return function

    @staticmethod
    def DEV_CMD(command, filter=FILTERS.DEVELOPER):
        def wrapper(func):
            @zohun.on_message(filters.command(command, "^") & filter)
            @CMD.FLOOD_HANDLER
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def FAKEDEV(command, filter=FILTERS.FAKE_DEV):
        def wrapper(func):
            @zohun.on_message(filters.command(command, "^") & filter)
            @CMD.FLOOD_HANDLER
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def INLINE(query=None):
        def wrapper(func):
            inline_filter = filters.regex(query) if query else filters.all
            @bot.on_inline_query(inline_filter)
            @CMD.FLOOD_HANDLER
            async def wrapped_func(client, inline_query):
                return await func(client, inline_query)

            return wrapped_func

        return wrapper

    @staticmethod
    def REGEX(command):
        def wrapper(func):
            @bot.on_message(filters.regex(command))
            @CMD.FLOOD_HANDLER
            async def wrapped_func(client, message):
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, callback_query):
                return await func(client, callback_query)

            return wrapped_func

        return wrapper

    @staticmethod
    def NO_CMD(result, client):
        query_mapping = {
            "PMPERMIT": {
                "query": (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.service
                ),
                "group": 1,
            },
            "MENTIONED": {
                "query": (
                    (filters.mentioned | filters.private)
                    & ~filters.bot
                    & ~filters.me
                    & filters.incoming
                ),
                "group": 2,
            },
            "FILTERS": {
                "query": (filters.group | filters.private)
                & ~filters.service
                & ~filters.bot
                & ~filters.me
                & filters.incoming,
                "group": 9,
            },
            "LOGS_GROUP": {
                "query": (
                    filters.mentioned
                    & filters.incoming
                    & ~filters.bot
                    & ~filters.via_bot
                    & ~filters.me
                )
                | (
                    filters.private
                    & filters.incoming
                    & ~filters.me
                    & ~filters.bot
                    & ~filters.service
                ),
                "group": 3,
            },
            "AFK": {
                "query": (
                    (filters.mentioned | filters.private)
                    & ~filters.bot
                    & ~filters.me
                    & filters.incoming
                ),
                "group": 4,
            },
            "REP_BLOCK": {
                "query": (
                    (filters.mentioned | filters.private)
                    & ~filters.bot
                    & ~filters.me
                    & filters.incoming
                    & filters.create(is_blocked)
                ),
                "group": 5,
            },
            "REPLY": {
                "query": (filters.reply & filters.me),
                "group": 6,
            },
            "ADD_ME": {
                "query": (filters.new_chat_members),
                "group": 7,
            },
            "KICK_ME": {
                "query": (filters.left_chat_member),
                "group": 8,
            },
            "CHATBOT": {
                "query": (~filters.bot & filters.incoming),
                "group": 10,
            },
            "AUTOREPLY_ALL": {
                "query": (
                    ~filters.private
                    & ~filters.channel
                    & ~filters.bot
                    & ~filters.me
                    & filters.incoming
                    & ~filters.service
                ),
                "group": 11,
            },
        }
        result_query = query_mapping.get(result)

        def decorator(func):
            if result_query:

                async def wrapped_func(client, message):
                    await func(client, message)

                client.on_message(
                    result_query["query"], group=int(result_query["group"])
                )(wrapped_func)
                return wrapped_func
            else:
                return func

        return decorator

    @staticmethod
    def IS_LOG(func):
        async def function(client, message):
            logs = await dB.get_var(client.me.id, "GRUPLOG")
            if logs:
                if message.chat.id != int(logs):
                    return
            else:
                pass
            return await func(client, message)

        return function

    @staticmethod
    def SELLER_AND_GC(func):
        async def function(client, message):
            user = message.from_user
            reseller = await dB.get_list_from_var(BOT_ID, "SELLER")
            if user.id not in reseller:
                return await message.reply("<b>Kamu bukan reseller!!</b>")

            return await func(client, message)

        return function

    @staticmethod
    def DB_BROADCAST(func):
        async def function(client, message):
            broadcast = await dB.get_list_from_var(client.me.id, "BROADCAST")
            user = message.from_user
            if user.id not in broadcast:
                await dB.add_to_var(client.me.id, "BROADCAST", user.id)
            return await func(client, message)

        return function

    @staticmethod
    def ADMIN(func):
        async def function(client, message):
            emo = Emoji(client)
            await emo.get()
            user = message.from_user if message.from_user else message.sender_chat
            if user.id not in await client.admin_list(message):
                return await message.reply(
                    f"<blockquote>{emo.gagal}<b>Anda bukan admin di grup ini.</b></blockquote>"
                )
            return await func(client, message)

        return function

    @staticmethod
    def ONLY_GROUP(func):
        async def function(client, message):
            if message.chat.type not in [
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP,
            ]:
                emo = Emoji(client)
                await emo.get()
                return await message.reply(
                    f"<blockquote>{emo.gagal}<b>Perintah ini hanya bisa digunakan di grup.</b></blockquote>"
                )
            return await func(client, message)

        return function

    @staticmethod
    def ONLY_PRIVATE(func):
        async def function(client, message):
            if message.chat.type != enums.ChatType.PRIVATE:
                emo = Emoji(client)
                await emo.get()
                return await message.reply(
                    f"<blockquote>{emo.gagal}<b>Perintah ini hanya bisa digunakan di chat pribadi.</b></blockquote>"
                )
            return await func(client, message)

        return function

    @staticmethod
    def INLINE_QUERY(func):
        async def wrapper(client, iq):
            users = zohun._get_my_id
            if iq.from_user.id not in users:
                return await client.answer_inline_query(
                    iq.id,
                    cache_time=0,
                    results=[
                        InlineQueryResultArticle(
                            title=f"Anda Belum Melakukan Pembelian @{client.me.username}",
                            input_message_content=InputTextMessageContent(
                                f"Kamu Bisa Melakukan Pembelian @{client.me.username} Agar Bisa Menggunakan"
                            ),
                        )
                    ],
                )
            else:

                return await func(client, iq)

        return wrapper

    @staticmethod
    def CALLBACK_DATA(func):
        async def wrapper(client, cq):
            users = zohun._get_my_id
            if cq.from_user.id not in users:
                return await cq.answer(
                    f"Silakan Order Bot @{client.me.username} Agar Bisa Menggunakan Bot Ini",
                    True,
                )
            else:

                return await func(client, cq)

        return wrapper


class PY:
    """Pyrogram bot decorator wrappers - Complete version"""
    
    @staticmethod
    def START(func):
        """Decorator for start command - passthrough"""
        return func
    
    @staticmethod
    def PRIVATE(func):
        """Decorator for private chat filter - passthrough"""
        return func
    
    @staticmethod
    def GROUP(func):
        """Decorator for group chat filter - passthrough"""
        return func
    
    @staticmethod
    def OWNER(func):
        """Decorator for owner-only commands"""
        def decorator_wrapper(func_inner):
            @bot.on_callback_query(filters.user(OWNER_ID))
            async def wrapped_func(client, callback_query):
                return await func_inner(client, callback_query)
            return wrapped_func
        # If used as @PY.OWNER without (), return the filter
        if callable(func):
            return decorator_wrapper(func)
        return decorator_wrapper
    
    @staticmethod
    def ADMIN(func):
        """Decorator for admin commands (OWNER + SUDO_OWNERS)"""
        admin_users = [OWNER_ID] + (SUDO_OWNERS if isinstance(SUDO_OWNERS, list) else [])
        
        def decorator_wrapper(func_inner):
            @bot.on_callback_query(filters.user(admin_users))
            async def wrapped_func(client, callback_query):
                return await func_inner(client, callback_query)
            return wrapped_func
        
        if callable(func):
            return decorator_wrapper(func)
        return decorator_wrapper
    
    @staticmethod
    def SELLER(func):
        """Decorator for seller/reseller commands"""
        # Seller filter - passthrough for now, can be customized
        return func
    
    @staticmethod
    def RIM(func):
        """Decorator for RIM user filter"""
        def decorator_wrapper(func_inner):
            @bot.on_callback_query(filters.user(RIMZOHUN))
            async def wrapped_func(client, callback_query):
                return await func_inner(client, callback_query)
            return wrapped_func
        
        if callable(func):
            return decorator_wrapper(func)
        return decorator_wrapper
    
    @staticmethod
    def NO_CMD_UBOT(key, ubot_instance):
        """Decorator to exclude from ubot commands - with key and ubot instance
        
        Usage: @PY.NO_CMD_UBOT("PMPERMIT", ubot)
        """
        def decorator(func):
            # Register event handler on ubot instance
            if hasattr(ubot_instance, 'on_message'):
                # This is a special decorator that registers on ubot
                @ubot_instance.on_message()
                async def wrapped_func(client, message):
                    return await func(client, message)
                return wrapped_func
            return func
        return decorator
    
    @staticmethod
    def CALLBACK(data):
        """Decorator for callback query handlers"""
        def decorator(func):
            @bot.on_callback_query(filters.regex(f"^{data}$"))
            async def wrapped_func(client, callback_query):
                return await func(client, callback_query)
            return wrapped_func
        return decorator

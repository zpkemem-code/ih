import asyncio
import os

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import (
    ChannelPrivate,
    ChatRestricted,
    ChatWriteForbidden,
    FloodWait,
    Forbidden,
    PeerIdInvalid,
    SlowmodeWait,
    UserBannedInChannel,
)

from config import OWNER_ID, LOG_SELLER
from Zohun import bot, zohun
from Zohun.database import dB
from Zohun.helpers import CMD, FILTERS, Tools
from Zohun.logger import logger


@CMD.BOT("broadcast", FILTERS.PRIVATE)
async def broadcast_command(client, message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return await message.reply("<blockquote><b>This command is only for owner!</b></blockquote>")
    
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply(
            "<b>Usage:</b>\n"
            "<code>/broadcast [text]</code> - Broadcast to all users\n"
            "<code>/broadcast</code> (reply to message) - Forward message to all users"
        )
    
    proses = await message.reply("<blockquote><b>Starting broadcast...</b></blockquote>")
    
    broadcast_list = await dB.get_list_from_var(client.me.id, "BROADCAST")
    
    if not broadcast_list:
        return await proses.edit("<blockquote><b>No users in broadcast list!</b></blockquote>")
    
    text = None
    if message.reply_to_message:
        text = message.reply_to_message
    elif len(message.command) > 1:
        text = message.text.split(None, 1)[1]
    
    done, failed = 0, 0
    
    for user in broadcast_list:
        try:
            if message.reply_to_message:
                await text.copy(user)
            else:
                await client.send_message(user, text)
            done += 1
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if message.reply_to_message:
                    await text.copy(user)
                else:
                    await client.send_message(user, text)
                done += 1
            except Exception:
                failed += 1
        except Exception as e:
            failed += 1
            logger.warning(f"Failed to send broadcast to {user}: {e}")
    
    return await proses.edit(
        f"<b>Broadcast completed!</b>\n"
        f"<b>Success:</b> {done}\n"
        f"<b>Failed:</b> {failed}"
    )


@CMD.BOT("bcgroup", FILTERS.PRIVATE)
async def broadcast_group_command(client, message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return await message.reply("<b>This command is only for owner!</b>")
    
    if not zohun._ubot:
        return await message.reply("<b>No userbots available!</b>")
    
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply(
            "<b>Usage:</b>\n"
            "<code>/bcgroup [text]</code> - Broadcast to all groups via userbot\n"
            "<code>/bcgroup</code> (reply to message) - Forward to all groups"
        )
    
    proses = await message.reply("<b>Starting group broadcast via userbots...</b>")
    
    total_done, total_failed = 0, 0
    
    for ubot in zohun._ubot:
        try:
            chats = await ubot.get_chat_id("group")
            
            for chat_id in chats:
                try:
                    if message.reply_to_message:
                        await ubot.copy_message(
                            chat_id=chat_id,
                            from_chat_id=message.chat.id,
                            message_id=message.reply_to_message.id
                        )
                    else:
                        text = message.text.split(None, 1)[1]
                        await ubot.send_message(chat_id, text)
                    total_done += 1
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception:
                    total_failed += 1
        except Exception as e:
            logger.error(f"Error broadcasting with userbot {ubot.me.id}: {e}")
    
    return await proses.edit(
        f"<b>Group Broadcast completed!</b>\n"
        f"<blockquote><b>Success:</b> {total_done}\n"
        f"<b>Failed:</b> {total_failed}</blockquote>"
    )


@CMD.BOT("stats", FILTERS.PRIVATE)
async def stats_command(client, message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return await message.reply("<blockquote><b>This command is only for owner!</b></blockquote>")
    
    broadcast_list = await dB.get_list_from_var(client.me.id, "BROADCAST")
    prem_users = await dB.get_list_from_var(client.me.id, "PREM_USERS")
    seller_users = await dB.get_list_from_var(client.me.id, "SELER_USERS")
    admin_users = await dB.get_list_from_var(client.me.id, "ADMIN_USERS")
    
    total_ubots = len(zohun._ubot)
    
    return await message.reply(
        f"<b>Bot Statistics</b>\n\n"
        f"<blockquote><b>Total Userbots:</b> {total_ubots}\n"
        f"<b>Broadcast Users:</b> {len(broadcast_list)}\n"
        f"<b>Premium Users:</b> {len(prem_users)}\n"
        f"<b>Sellers:</b> {len(seller_users)}\n"
        f"<b>Admins:</b> {len(admin_users)}</blockquote>"
    )


@CMD.BOT("listuser", FILTERS.PRIVATE)
async def listuser_command(client, message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return await message.reply("<blockquote><b>This command is only for owner!</b></blockquote>")
    
    ubots = zohun._ubot
    if not ubots:
        return await message.reply("<b>No userbots running!</b>")
    
    text = "<b>Active Userbots:</b>\n\n"
    for i, ubot in enumerate(ubots, 1):
        try:
            text += f"{i}. <a href='tg://user?id={ubot.me.id}'>{ubot.me.first_name}</a> | <code>{ubot.me.id}</code>\n"
        except Exception:
            text += f"{i}. Unknown | Error\n"
    
    return await message.reply(text)


@CMD.BOT("sendlog", FILTERS.PRIVATE)
async def sendlog_command(client, message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return await message.reply("<blockquote><b>This command is only for owner!</b></blockquote>")
    
    if len(message.command) < 2:
        return await message.reply("<b>Usage: /sendlog [message]</b>")
    
    text = message.text.split(None, 1)[1]
    
    try:
        await client.send_message(LOG_SELLER, text)
        return await message.reply("<b>Message sent to log channel!</b>")
    except Exception as e:
        return await message.reply(f"<b>Failed: {e}</b>")


@CMD.BOT("ping", FILTERS.PRIVATE)
async def ping_command(client, message):
    import time
    start = time.time()
    msg = await message.reply("<b>Pong!</b>")
    end = time.time()
    await msg.edit(f"<b>Pong!</b> <code>{round((end - start) * 1000, 2)}ms</code>")

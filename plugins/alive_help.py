import random
import re
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from time import time

import psutil
from pyrogram.raw.functions import Ping
from pyrogram.types import (
    InlineQueryResultArticle, InlineKeyboardMarkup, InlineKeyboardButton,
    InputTextMessageContent
)
from pyrogram.utils import unpack_inline_message_id as unpackInlineMessage

from config import OWNER_ID, HELPABLE
from Zohun.helpers import *
from Zohun.database import dB
from Zohun import bot, zohun

ubot = zohun
HELP_COMMANDS = HELPABLE


__MODULES__ = "Alive Help"


@CMD.INLINE("^alive")
async def _(client, inline_query):
    psr = await EMO.PASIR(client)
    get_id = inline_query.query.split()
    for my in ubot._ubot:
        if int(get_id[2]) == my.me.id:
            try:
                peer = my._get_my_peer[my.me.id]
                users = len(peer["pm"])
                group = len(peer["gc"])
            except Exception:
                users = random.randrange(await my.get_dialogs_count())
                group = random.randrange(await my.get_dialogs_count())
            get_exp = await get_expired_date(my.me.id)
            exp = get_exp.strftime("%d-%m-%Y") if get_exp else "None"
            if my.me.id in await dB.get_list_from_var(client.me.id, "ULTRA_PREM"):
                status = "SuperUltra"
            else:
                status = "Premium"
            button = BTN.ALIVE(get_id)
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime = await get_time((time() - start_time))
            psr = await EMO.PASIR(client)
            msg = f"""
<blockquote>{bot.me.mention}
    status: {status} 
       {psr} expired_on: {exp} 
        dc_id: {my.me.dc_id}
        ping_dc: {ping} ms
        peer_users: {users} users
        peer_group: {group} group
        start_uptime: {uptime}</blockquote>
        <blockquote>☛   <a href=https://t.me/ZonaHunterNew>𝐙𝐎𝐍𝐀 𝐇𝐔𝐍𝐓𝐄𝐑</a>   ☚</blockquote>
"""
            await client.answer_inline_query(
                inline_query.id,
                cache_time=300,
                results=[
                    (
                        InlineQueryResultArticle(
                            title="💬",
                            reply_markup=InlineKeyboardMarkup(button),
                            input_message_content=InputTextMessageContent(msg),
                        )
                    )
                ],
            )


@PY.CALLBACK("alv_cls")
async def _(client, callback_query):
    get_id = callback_query.data.split()
    if not callback_query.from_user.id == int(get_id[2]):
        return
    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for my in ubot._ubot:
        if callback_query.from_user.id == int(my.me.id):
            await my.delete_messages(
                unPacked.chat_id, [int(get_id[1]), unPacked.message_id]
            )


@CMD.BOT("anu")
async def _(client, message):
    buttons = BTN.BOT_HELP(message)
    sh = await message.reply("help menu information", reply_markup=InlineKeyboardMarkup(buttons))
    

@PY.CALLBACK("balik")
async def _(client, callback_query):
    buttons = BTN.BOT_HELP(callback_query)
    sh = await callback_query.message.edit("help menu information", reply_markup=InlineKeyboardMarkup(buttons))

@PY.CALLBACK("reboot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await dB.get_list_from_var(client.me.id, "ADMIN_USERS"):
        return await callback_query.answer("tombol ini bukan untuk lu", True)
    await callback_query.answer("system berhasil di restart", True)
    subprocess.call(["bash", "start.sh"])

@PY.CALLBACK("update")
async def _(client, callback_query):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    user_id = callback_query.from_user.id
    if not user_id == OWNER_ID:
        return await callback_query.answer("tombol ini bukan untuk lu", True)
    if "Already up to date." in str(out):
        return await callback_query.answer("sudah terupdate", True)
    else:
        await callback_query.answer("sedang memproses update.....", True)
    os.execl(sys.executable, sys.executable, "-m", "kingzubot-prem")


@CMD.INLINE("^user_help")
async def user_help_inline(client, inline_query):
    SH = await ubot.get_prefix(inline_query.from_user.id)
    msg = f"<blockquote><b>✣ menu inline <a href=tg://user?id={inline_query.from_user.id}>{inline_query.from_user.first_name} {inline_query.from_user.last_name or ''}</a>\n  total modules: {len(HELP_COMMANDS)}\n  prefix: {' '.join(SH)}</b></blockquote>"
    results = [InlineQueryResultArticle(
        title="Help Menu!",
        reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
        input_message_content=InputTextMessageContent(msg),
    )]
    await client.answer_inline_query(inline_query.id, cache_time=60, results=results)

@PY.CALLBACK("^close_user")
async def close_usernya(client, callback_query):
    unPacked = unpackInlineMessage(callback_query.inline_message_id)
    for x in ubot._ubot:
        if callback_query.from_user.id == int(x.me.id):
            await x.delete_messages(
                unPacked.chat_id, unPacked.message_id
            )

@PY.CALLBACK("help_(.*?)")
async def help_callback(client, callback_query):
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
    next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
    tutup_match = re.match(r"help_tutup\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    SH = await ubot.get_prefix(callback_query.from_user.id)
    top_text = f"<blockquote><b>✣ menu inline <a href=tg://user?id={callback_query.from_user.id}>{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}</a>\n  total modules: {len(HELP_COMMANDS)}\n  prefix: {' '.join(SH)}</b></blockquote>"

    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = HELP_COMMANDS[module].__HELP__.format(next((p) for p in SH))
        button = [[InlineKeyboardButton("⊲ back", callback_data="help_back")]]
        await callback_query.edit_message_text(
            text=text 
            + '\n<blockquote>☛<b><a href=https://t.me/ZonaHunterNew>    𝐙𝐎𝐍𝐀 𝐇𝐔𝐍𝐓𝐄𝐑    </a></b>☚</blockquote>',
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await callback_query.edit_message_text(
            top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )
    elif next_match:
        next_page = int(next_match.group(1))
        await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(next_page + 1, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )
    elif back_match:
        await callback_query.edit_message_text(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")),
            disable_web_page_preview=True,
        )


# ============================================================
# .help Command - Show modules and help
# ============================================================

@CMD.UBOT("help")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    
    # Get argument (module name)
    arg = None
    if len(message.command) > 1:
        arg = message.command[1]
    
    if not arg:
        # Show all modules using inline
        query = "help"
        chat_id = message.chat.id
        
        try:
            inline = await ButtonUtils.send_inline_bot_result(
                message,
                chat_id,
                bot.me.username,
                query,
            )
            if inline:
                return await message.delete()
        except Exception as error:
            return await message.reply(f"{em.gagal}Error: {str(error)}")
    else:
        # Show specific module help
        from config import HELPABLE
        
        nama = arg
        pref = client.get_prefix(client.me.id)
        x = next(iter(pref)) if pref else "."
        text_help2 = f"<blockquote>☛<b><a href=https://t.me/ZonaHunterNew>    𝐙𝐎𝐍𝐀 𝐇𝐔𝐍𝐓𝐄𝐑    </a></b>☚</blockquote>"
        
        if nama in HELPABLE:
            return await message.reply(
                f"{HELPABLE[nama].__HELP__.format(x, text_help2)}",
            )
        else:
            return await message.reply(
                f"{em.gagal}<b>Tidak ada modul bernama <code>{nama}</code></b>"
            )

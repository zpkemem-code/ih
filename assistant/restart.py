import asyncio
import importlib

# from pyrogram.helpers import kb
from pyrogram.types import ReplyKeyboardMarkup

from config import BOT_NAME
from Zohun import UserBot, bot, zohun
from Zohun.database import dB
from Zohun.helpers import CMD, FILTERS, Emoji
from plugins import PLUGINS

keyboard = ReplyKeyboardMarkup([["↩️ Beranda"]], resize_keyboard=True, one_time_keyboard=True)


async def reset_costum_text(client, message):
    user_id = message.from_user.id
    proses = await message.reply("<b>Processing...</b>")
    if user_id not in zohun._get_my_id:
        return await proses.edit(
            f"<blockquote><b>You are not user @{bot.me.username}!!</b></blockquote>", reply_markup=keyboard
        )
    try:
        await dB.set_var(user_id, "text_ping", "Ping")
        await dB.set_var(user_id, "text_uptime", "Uptime")
        owner_name = f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
        await dB.set_var(user_id, "text_owner", f"Owner: {owner_name}")
        await dB.set_var(user_id, "text_ubot", f"{BOT_NAME}")
        await dB.set_var(user_id, "text_gcast", "Proses")
        await dB.set_var(user_id, "text_sukses", "Gcast Sukses")
        await asyncio.sleep(1)
        return await proses.edit(
            "<blockquote><b>Your costum text has been reset</b></blockquote>", reply_markup=keyboard
        )
    except Exception as er:
        return await proses.edit(f"<b>ERROR: `{str(er)}`</b>", reply_markup=keyboard)


async def reset_emoji(client, message):
    user_id = message.from_user.id
    proses = await message.reply("<b>Processing...</b>")
    if user_id not in zohun._get_my_id:
        return await proses.edit(
            f"<blockquote><b>You are not user @{bot.me.username}!!</b></blockquote>", reply_markup=keyboard
        )
    for User in zohun._ubot:
        if user_id == User.me.id:
            try:
                em = Emoji(User)
                await em.reset_emoji()
                await asyncio.sleep(1)
                return await proses.edit(
                    "<blockquote><b>Your costum emoji has been reset.!!</b></blockquote>", reply_markup=keyboard
                )
            except Exception as er:
                return await proses.edit(
                    f"<b>ERROR: `{str(er)}`</b>", reply_markup=keyboard
                )


async def reset_prefix(client, message):
    mepref = [".", ",", "?", "+", "!"]
    proses = await message.reply("<b>Processing...</b>")
    user_id = message.from_user.id
    if user_id not in zohun._get_my_id:
        return await proses.edit(
            f"<blockquote><b>You are not user @{bot.me.username}!!</b></blockquote>", reply_markup=keyboard
        )
    for x in zohun._ubot:
        if x.me.id == user_id:
            x.set_prefix(x.me.id, mepref)
            await dB.set_pref(x.me.id, mepref)
            return await proses.edit(
                f"<blockquote><b>Your prefix has been reset to: `{' '.join(mepref)}` .</b></blockquote>",
                reply_markup=keyboard,
            )


async def restart_userbot(client, message):
    proses = await message.reply("<b>Processing...</b>")
    user_id = message.from_user.id
    if user_id not in zohun._get_my_id:
        return await proses.edit(
            f"<blockquote><b>You are not user @{bot.me.username}!!</b></blockquote>", reply_markup=keyboard
        )
    for X in await dB.get_userbots():
        if user_id == int(X["name"]):
            try:
                ubot = UserBot(**X)
                await ubot.start()
                for modul in PLUGINS:
                    importlib.reload(importlib.import_module(f"plugins.{modul}"))
                return await proses.edit(
                    f"<blockquote><b>✅ Userbot has been restarted {ubot.me.first_name} {ubot.me.last_name or ''} | {ubot.me.id}.</b></blockquote>",
                    reply_markup=keyboard,
                )
            except Exception as error:
                return await proses.edit(f"<b>{error}</b>", reply_markup=keyboard)


@CMD.BOT("restart", FILTERS.PRIVATE)
async def _(client, message):
    return await restart_userbot(client, message)

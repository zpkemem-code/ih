import random
from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping

from Zohun import dB
from Zohun.helpers import CMD, Emoji, get_time, start_time
from Zohun.database import dB

__MODULES__ = "Settings"
__HELP__ = """<blockquote>Command Help **Settings**</blockquote>

<blockquote>**Set text ping message**</blockquote>
    **You can set costum text ping**
        `{0}set_text ping` (text/reply text)

<blockquote>**Set text uptime message**</blockquote>
    **You can set costum text uptime**
        `{0}set_text uptime` (text/reply text)

<blockquote>**Set text owner message**</blockquote>
    **You can set costum text owner**
        `{0}set_text owner` (text/reply text)

<blockquote>**Set text ubot message**</blockquote>
    **You can set costum text ubot**
        `{0}set_text ubot` (text/reply text)

<blockquote>**Set text sukses message**</blockquote>
    **You can set costum text sukses gcast**
        `{0}set_text sukses` (text/reply text)

<blockquote>**Set text proses message**</blockquote>
    **You can set costum text proses**
        `{0}set_text proses` (text/reply text)

<blockquote>**Set text help message**</blockquote>
    **You can set costum text inline help**
        `{0}set_text help` (text/reply text)

<blockquote>**Note:** Use `{0}ping` to check the changes and `{0}help`</blockquote>

<b>   {1}</b>
"""


async def set_pong_message(user_id, new_message):
    await dB.set_var(user_id, "text_ping", new_message)
    return


async def set_utime_message(user_id, new_message):
    await dB.set_var(user_id, "text_uptime", new_message)
    return


async def set_owner_message(user_id, new_message):
    await dB.set_var(user_id, "text_owner", new_message)
    return


async def set_ubot_message(user_id, new_message):
    await dB.set_var(user_id, "text_ubot", new_message)
    return


async def set_gcast_message(user_id, new_message):
    await dB.set_var(user_id, "text_gcast", new_message)
    return


async def set_sukses_message(user_id, new_message):
    await dB.set_var(user_id, "text_sukses", new_message)
    return


async def set_help_message(user_id, new_message):
    await dB.set_var(user_id, "text_help", new_message)
    return


costumtext_query = {
    "ping": set_pong_message,
    "uptime": set_utime_message,
    "owner": set_owner_message,
    "ubot": set_ubot_message,
    "proses": set_gcast_message,
    "sukses": set_sukses_message,
    "help": set_help_message,
}


@CMD.UBOT("set_text")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    pros = await message.reply(f"{em.proses}**{proses_}**")

    args = message.text.split(maxsplit=2)
    variable = args[1]
    # if len(args) >= 3:
    new_message = client.new_arg(message)
    if variable in costumtext_query:
        await costumtext_query[variable](client.me.id, new_message)
        return await pros.edit(
            f"{em.sukses}**Successfully updated custom text: <u>{variable}</u>**"
        )
    else:
        return await pros.edit(
            f"{em.gagal}**Please given text for this query: {variable}!**"
        )
    # else:
    # return await pros.edit(
    #    f"{em.gagal}**No query: <code>{variable}</code>. Please provide the correct query!**"
    # )


@CMD.UBOT("ping")
@CMD.DEV_CMD("mping")
@CMD.FAKEDEV("mping")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    upnya = await get_time((time() - start_time))
    duration = round((end - start).microseconds / 100000, 2)
    _ping = f"<b>{em.ping}{pong_}:</b> <u>{duration}ms</u>\n<b>{em.uptime}{uptime_}:</b> <u>{upnya}</u>\n<b>{em.owner}{owner_}</b>"
    return await message.reply(_ping)


async def add_absen(client, text):
    auto_text = await dB.get_var(client.me.id, "TEXT_ABSEN") or []
    auto_text.append(text)
    await dB.set_var(client.me.id, "TEXT_ABSEN", auto_text)


@CMD.FAKEDEV("absen")
@CMD.DEV_CMD("absen")
async def _(client, message):
    txt = await dB.get_var(client.me.id, "TEXT_ABSEN")
    if len(message.command) == 1:
        if not txt:
            return
        try:
            psn = random.choice(txt)
            return await message.reply(psn)
        except:
            pass
    else:
        command, variable = message.command[:2]
        if variable.lower() == "text":
            for x in client._ubot:
                value = " ".join(message.command[2:])
                await add_absen(x, value)

        else:
            return

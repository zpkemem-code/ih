from asyncio import sleep

from pyrogram import raw
from pyrogram.errors import FloodWait

from Zohun.helpers import CMD, Emoji

__MODULES__ = "Spambot"
__HELP__ = """<blockquote>Command Help **Spambot**</blockquote> 

<blockquote>**Check spambot**</blockquote>
    **Check your status account from limit @spambot**
        `{0}limit`

<b>   {1}</b>
"""


@CMD.UBOT("limit")
@CMD.FAKEDEV("limit")
async def _(client, message):
    return await spam_bot(client, message)


async def spam_bot(client, message):
    em = Emoji(client)
    await em.get()
    await client.unblock_user("SpamBot")
    xin = await client.resolve_peer("SpamBot")
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    msg = await message.reply(f"{em.proses}**{proses_}**")
    await client.send_message("SpamBot", "/start")
    await sleep(1)
    async for status in client.search_messages("SpamBot", limit=1):
        isdone = status.text
        break
    else:
        isdone = None
    if isdone:
        result = status.text
        emoji = None
        if "Good news" in result or "Kabar baik" in result:
            emoji = f"{em.sukses}"
        if "afraid" in result or "khawatir" in result:
            emoji = f"{em.warn}"
        await client.send_message(
            message.chat.id,
            f"{emoji}**{result}**\n\n ~ {em.owner} **{client.me.first_name}**",
        )
        try:
            await client.invoke(
                raw.functions.messages.DeleteHistory(peer=xin, max_id=0, revoke=True)
            )
        except FloodWait as e:
            await sleep(e.value)
            await client.invoke(
                raw.functions.messages.DeleteHistory(peer=xin, max_id=0, revoke=True)
            )
    return await msg.delete()

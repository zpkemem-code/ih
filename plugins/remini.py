__MODULES__ = "Remini"
__HELP__ = """<blockquote>Command Help **Remini**</blockquote>

<blockquote>**Enchancer image** </blockquote>
    **Change image to hd with this command**
        `{0}remini` (reply image)

<b>   {1}</b>
"""


from config import API_MAELYN
from Zohun.helpers import CMD, Emoji, Tools


@CMD.UBOT("remini")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    prs = await message.reply_text(f"{em.proses}**{proses_[4]}**")
    rep = message.reply_to_message or message
    if len(message.command) < 2 and not rep:
        return await prs.edit(f"{em.gagal}**Please reply to image or give link.!!**")
    if rep and rep.media:
        arg = await Tools.upload_media(message)
    else:
        arg = client.get_text(message)
        if not arg.startswith("https://"):
            return await prs.edit(
                f"{em.gagal}**Please give valid link or reply media**"
            )
    url = f"https://api.maelyn.tech/api/img2img/remini?url={arg}&apikey={API_MAELYN}"
    respon = await Tools.fetch.get(url)
    await prs.edit(f"{em.proses}**Scanning of image...**")
    if respon.status_code == 200:
        data = respon.json()["result"]
        try:
            await prs.delete()
            url = data.get("url")
            type = data.get("type")
            size = data.get("size")
            expired = data.get("expired")
            return await message.reply_photo(
                url,
                caption=f"{em.sukses}**Type**: {type}\n**Size**: {size}\n**Expired**: {expired}",
            )
        except Exception as er:
            await prs.delete()
            return await message.reply(f"{em.gagal}**ERROR:** {str(er)}")
    else:
        return await prs.edit(f"**{em.gagal}Please try again: {respon.status_code}!**")

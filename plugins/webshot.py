from Zohun.helpers import CMD, Emoji, Tools

__MODULES__ = "Webshot"
__HELP__ = """<blockquote>Command Help **Webshot** </blockquote>

<blockquote>**View webpage capture**</blockquote>
    **Get screenshot web from url**
        `{0}webss` (url)
    
<b>   {1}</b>
"""


@CMD.UBOT("webss")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_[4]}**")
    if len(message.command) < 2:
        return await proses.edit(
            f"{em.gagal}**Please give valid link! Example: `{message.text.split()[0]}webss https://youtube.com`**"
        )
    url = (
        message.text.split(None, 1)[1]
        if len(message.command) < 3
        else message.text.split(None, 2)[1]
    )
    if "https://" not in url:
        return await proses.edit(f"{em.gagal}**Please give valid link!**")
    full = False if len(message.command) < 3 else True
    try:
        photo = await Tools.screen_web(url, full)
        if not photo:
            return await proses.edit(
                f"{em.gagal}**Something went wrong, please try again!**"
            )

        await proses.delete()
        upload = await message.reply(f"{em.proses}**Uploading media...**")
        if not full:
            await message.reply_photo(photo)
        else:
            await message.reply_document(photo)
        return await upload.delete()
    except Exception as r:
        return await upload.edit(f"{em.gagal}**ERROR:** {str(r)}")

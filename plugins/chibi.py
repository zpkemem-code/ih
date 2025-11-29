from pyrogram.types import InputMediaPhoto

from config import API_MAELYN
from Zohun.helpers import CMD, Emoji, Tools

__MODULES__ = "Chibi"
__HELP__ = """<blockquote>Command Help **Chibi**</blockquote>

<blockquote>**Generate image** </blockquote>
    **You can generate image with effect chibi**
        `{0}chibi` (prompt)

<b>   {1}</b>
"""


@CMD.UBOT("chibi")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_[4]}**")
    prompt = client.get_text(message)
    if not prompt:
        return await proses.edit(
            f"{em.gagal}**Please reply to a message containing the prompt!\n"
            f"Example: `{message.text.split()[0]} beautiful japanese girl`**"
        )
    headers = {"mg-apikey": API_MAELYN}
    params = {"prompt": prompt, "resolution": "Square"}
    url = "https://api.maelyn.tech/api/txt2img/chibi"
    
    try:
        response = await Tools.fetch.get(url, headers=headers, params=params)
    except Exception as e:
        return await proses.edit(
            f"{em.gagal}<b>Koneksi error: {str(e)[:100]}\nPastikan internet aktif dan API tersedia!</b>"
        )
    
    media_group = []
    if response.status_code == 200:
        data = response.json()["result"]
        for bahan in data:
            img = await Tools.get_media_data(bahan, "jpg")
            caption = f"{em.sukses}<b>Successfully generate image:</b>"
            media_group.append(InputMediaPhoto(media=img, caption=caption))
        if media_group:
            await client.send_media_group(
                chat_id=message.chat.id,
                media=media_group,
                reply_to_message_id=message.id,
            )
            return await proses.delete()
        else:
            return await proses.edit(
                f"{em.gagal}<b>Failed to generate image. Please try again later.</b>"
            )
    else:
        return await proses.edit(
            f"{em.gagal}<b>Failed to generate image. Please try again later.</b>"
        )

from config import API_MAELYN
from Zohun.helpers import CMD, Emoji, Tools

__MODULES__ = "Dalle"
__HELP__ = """<blockquote>Command Help **Dalle**</blockquote>

<blockquote>**Basic command** </blockquote>
    **You can generate image with dalle**
        `{0}dalle` (prompt)

<b>   {1}</b>
"""


@CMD.UBOT("dalle")
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
    url = "https://api.maelyn.tech/api/txt2img/dallexl"
    response = await Tools.fetch.get(url, headers=headers, params=params)
    if response.status_code == 200:
        try:
            data = response.json()["result"].get("url")
            img = await Tools.get_media_data(data, "jpg")
            caption = f"{em.sukses}<b>Successfully generate image:</b>"
            await message.reply_photo(img, caption=caption)
            return await proses.delete()
        except Exception:
            return await proses.edit(
                f"{em.gagal}<b>Failed to generate image. Please try again later.</b>"
            )
    else:
        return await proses.edit(
            f"{em.gagal}<b>Failed to generate image. Please try again later.</b>"
        )

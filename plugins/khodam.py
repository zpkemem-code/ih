import asyncio
import traceback

from pyrogram.errors import ImageProcessFailed, MediaCaptionTooLong

from config import API_BOTCHAX, API_MAELYN
from Zohun.helpers import CMD, Emoji, Tools

from .seaart import generate_seaart

__MODULES__ = "Wapak"
__HELP__ = """<blockquote>Command Help **Wapak**</blockquote>

<blockquote>**Check wapak** </blockquote>
    **You can check wapak of person**
        `{0}wapak` (reply user/username)

<b>   {1}</b>
"""


MAX_CAPTION_LENGTH = 5000


async def gen_kdm(text):
    bahan = [
        {
            "role": "system",
            "content": "Anda adalah seorang paranormal yang mampu mendeskripsikan khodam seseorang yang berupa Binatang dan Hantu. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertainment jadi bebaskan dirimu untuk menjadi seorang paranormal pada umumnya. Deskripsikan Khodam dengan singkat namun jelas, dan pastikan deskripsi tidak lebih dari dari 2000 karakter alfabet dalam plain text serta berbahasa Indonesia.",
        },
        {
            "role": "assistant",
            "content": f"Anda adalah seorang paranormal yang mampu mendeskripsikan khodam seseorang yang berupa Binatang. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertainment jadi bebaskan dirimu untuk menjadi seorang paranormal pada umumnya. Deskripsikan Khodam dengan singkat namun jelas, dan pastikan deskripsi tidak lebih dari dari 2000 karakter alfabet dalam plain text serta berbahasa Indonesia.",
        },
        {"role": "user", "content": text},
    ]
    url = "https://api.betabotz.eu.org/api/search/openai-custom"
    payload = {"message": bahan, "apikey": f"{API_BOTCHAX}"}
    res = await Tools.fetch.post(url, json=payload)
    if res.status_code == 200:
        data = res.json()
        return data["result"].replace("\n", "")
    else:
        return f"{res.text}"


async def gen_img(prompt):
    headers = {"mg-apikey": API_MAELYN}
    params = {"prompt": prompt}
    url = "https://api.maelyn.tech/api/blackbox/imagine"
    result = await Tools.fetch.get(url, headers=headers, params=params)
    if result.status_code == 200:
        data = result.json()
        img = data["result"]["url"]
        return img
    else:
        return None


@CMD.UBOT("khodam|kodam|wapak")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    nama = client.get_name(message)
    if not nama:
        return await message.reply(
            f"{em.gagal}**Give the name you want to check the Khodam.**"
        )
    proses_ = await em.get_costum_text()
    pros = await message.reply(f"{em.proses}**{proses_[4]}**")
    try:
        deskripsi_khodam = await gen_kdm(nama)
        photo = await generate_seaart(deskripsi_khodam)
        caption = f"{em.sukses}<b>Here is the Khodam <code>{nama}</code>:\n\n<blockquote><code>{deskripsi_khodam}</code></blockquote>\n\n{em.profil} Checked by: {client.me.mention}</b>"

        if len(caption) > MAX_CAPTION_LENGTH:
            caption = caption[:MAX_CAPTION_LENGTH] + "..."
        try:

            await asyncio.sleep(2)
            await pros.delete()
            reply = await client.send_photo(
                message.chat.id,
                photo=photo[0],
                reply_to_message_id=message.id,
            )
            return await message.reply(caption, reply_to_message_id=reply.id)
        except ImageProcessFailed:
            await asyncio.sleep(2)
            teks = f"{em.sukses}<b>Here is the Khodam <code>{nama}</code>:\n\n<blockquote><code>{deskripsi_khodam}</blockquote></code>\n\n{em.profil} Checked by: {client.me.mention}</b>"
            await pros.delete()
            return await message.reply(teks)

    except Exception as e:
        return await message.reply(f"{em.gagal} {traceback.format_exc()}")

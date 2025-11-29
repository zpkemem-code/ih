import asyncio
import aiohttp
import os
import time
import traceback
import uuid

from config import API_BOTCHAX
from Zohun.helpers import CMD, Emoji, Tools

__MODULES__ = "Brat"
__HELP__ = """
 Brat
 • `{0}brat` [Reply chat]: Teks bikin stiker 
 • `{0}bratvi`: Teks bikin video
 {1} 
"""


@CMD.UBOT("brat")
async def _(client, message):
    em = Emoji(client)
    await em.get()

    # Ambil teks dari argumen atau reply
    args = message.text.split(" ", 1)
    if len(args) >= 2:
        teks = args[1]
    elif message.reply_to_message and message.reply_to_message.text:
        teks = message.reply_to_message.text
    else:
        return await message.reply(f"**{em.gagal} Gunakan `.brat ` atau reply ke pesan teks.**")

    proses = await message.reply(f"**{em.proses} Sedang membuat gambar...**")

    try:
        url = f"https://api.botcahx.eu.org/api/maker/brat?text={teks}&apikey={API_BOTCHAX}"
        response = await Tools.fetch.get(url)

        if response.status_code != 200 or not response.headers.get("Content-Type", "").startswith("image/"):
            return await proses.edit(f"**{em.gagal} Gagal membuat gambar.**")

        # Simpan sebagai file stiker (webp)
        file_path = f"brat_{uuid.uuid4().hex}.webp"
        with open(file_path, "wb") as f:
            f.write(response.content)

        await client.send_sticker(
            chat_id=message.chat.id,
            sticker=file_path
        )
        await proses.delete()
        os.remove(file_path)

    except Exception as e:
        await proses.edit(f"**{em.gagal} Terjadi kesalahan:**\n{e}")


@CMD.UBOT("bratvi")
async def _(client, message):
    em = Emoji(client)
    await em.get()

    args = message.text.split(" ", 1)

    if len(args) >= 2:
        teks = args[1]
    elif message.reply_to_message and message.reply_to_message.text:
        teks = message.reply_to_message.text
    else:
        return await message.reply_text(f"**{em.gagal} Gunakan `.bratvideo ` atau reply ke pesan teks.**")

    proses = await message.reply_text(f"**{em.proses} Sedang membuat video...**")

    try:
        url = f"https://api.botcahx.eu.org/api/maker/brat-video?text={teks}&apikey={API_BOTCHAX}"
        response = await Tools.fetch.get(url)

        if response.status_code == 200 and response.headers.get("Content-Type", "").startswith("video/"):
            file_path = f"bratvideo_{uuid.uuid4().hex}.mp4"
            with open(file_path, "wb") as f:
                f.write(response.content)

            await client.send_video(
                chat_id=message.chat.id,
                video=file_path,
                caption=f"{em.sukses} Video berhasil dibuat!",
                supports_streaming=True
            )
            await proses.delete()
            os.remove(file_path)
        else:
            await proses.edit(f"**{em.gagal} Gagal membuat video.**")
    except Exception as e:
        await proses.edit(f"**{em.gagal} Terjadi kesalahan:**\n{e}")

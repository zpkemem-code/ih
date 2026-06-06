import os
from io import BytesIO

import aiohttp
import filetype

from PyroUbot import *

__MODULE__ = "ᴛᴏᴜʀʟ"
__HELP__ = """
<blockquote><b>Bantuan untuk tourl

perintah : <code>{0}tourl</code> [reply media/text]
    mengapload media/text ke catbox.moe</b></blockquote>
"""

CATBOX_API = "https://catbox.moe/user/api.php"
LITTERBOX_API = "https://litterbox.catbox.moe/resources/internals/api.php"
CATBOX_USERHASH = "4e0ca6489f98d21d9e4590af7"


async def _post_to_catbox(buffer: BytesIO, filename: str, mime_type: str) -> str:
    buffer.seek(0)
    form = aiohttp.FormData()
    form.add_field("reqtype", "fileupload")
    form.add_field("userhash", CATBOX_USERHASH)
    form.add_field("fileToUpload", buffer.read(), filename=filename, content_type=mime_type)

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Accept": "text/plain,*/*",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(CATBOX_API, data=form, timeout=90) as response:
            body = (await response.text()).strip()
            if response.status != 200 or not body.startswith("http"):
                raise Exception(f"Catbox upload gagal ({response.status}): {body}")
            return body


async def _post_to_litterbox(buffer: BytesIO, filename: str, mime_type: str) -> str:
    buffer.seek(0)
    form = aiohttp.FormData()
    form.add_field("reqtype", "fileupload")
    form.add_field("time", "72h")
    form.add_field("fileToUpload", buffer.read(), filename=filename, content_type=mime_type)

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Accept": "text/plain,*/*",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(LITTERBOX_API, data=form, timeout=90) as response:
            body = (await response.text()).strip()
            if response.status != 200 or not body.startswith("http"):
                raise Exception(f"Litterbox upload gagal ({response.status}): {body}")
            return body


async def upload_file(buffer: BytesIO, default_name: str = "file") -> str:
    kind = filetype.guess(buffer.getvalue())
    ext = kind.extension if kind else "bin"
    mime = kind.mime if kind else "application/octet-stream"
    filename = f"{default_name}.{ext}"

    try:
        return await _post_to_catbox(buffer, filename, mime)
    except Exception:
        return await _post_to_litterbox(buffer, filename, mime)


@PY.UBOT("tourl|tg")
async def _(client, message):
    reply_message = message.reply_to_message
    if not reply_message:
        return await message.reply("Please reply ke media atau teks untuk diupload.")

    try:
        if reply_message.media:
            downloaded_file = await reply_message.download()
            with open(downloaded_file, "rb") as f:
                buffer = BytesIO(f.read())
            try:
                default_name = os.path.splitext(os.path.basename(downloaded_file))[0] or "file"
                media_url = await upload_file(buffer, default_name=default_name)
            finally:
                if downloaded_file and os.path.exists(downloaded_file):
                    os.remove(downloaded_file)
            return await message.reply(
                f"<b>Berhasil diupload ke: <a href='{media_url}'>{media_url}</a></b>"
            )

        if reply_message.text:
            buffer = BytesIO(reply_message.text.encode("utf-8"))
            media_url = await upload_file(buffer, default_name="message")
            return await message.reply(
                f"<b>Teks berhasil diupload ke: <a href='{media_url}'>{media_url}</a></b>"
            )

        return await message.reply("Reply media atau teks yang valid.")
    except Exception as e:
        await message.reply(f"Error: {e}")

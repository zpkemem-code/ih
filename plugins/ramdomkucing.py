from Zohun.helpers import *
import random
import requests
from pyrogram.enums import *
from pyrogram import *
from pyrogram.types import *
from io import BytesIO

__MODULE__ = "Random Kucing"
__HELP__ = """
<blockquote><b>『 ғoto random kucing 』</b>

<b>⌲ perintah:</b> <code>{0}random [kucing]</code></b></blockquote>
"""

URLS = {
    "kucing": "https://api.siputzx.my.id/api/r/cats"
}

@CMD.UBOT("random")
async def _(client, message):
    # Extract query from message
    query = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if query not in URLS:
        valid_queries = ", ".join(URLS.keys())
        await message.reply(f"Query tidak valid. Gunakan salah satu dari: {valid_queries}.")
        return

    processing_msg = await message.reply("Processing Kingz...")
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        response = requests.get(URLS[query])
        response.raise_for_status()
        
        photo = BytesIO(response.content)
        photo.name = 'image.jpg'
        
        await client.send_photo(message.chat.id, photo)
        await processing_msg.delete()
    except requests.exceptions.RequestException as e:
        await processing_msg.edit_text(f"Gagal mengambil gambar cecan Error: {e}")

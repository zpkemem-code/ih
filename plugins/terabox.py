from pyrogram import Client, filters
import requests
from Zohun.helpers import *

__MODULE__ = "Terabox"
__HELP__ = """
<blockquote> <b>bantuan untuk terabox

perintah : <code>{0}terabox</code> terabox <b>[link nya]</b>
penjelasan : download video terabox.</b></blockquote>

"""

@CMD.UBOT("terabox")
async def terabox_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text("Gunakan perintah contoh: .terabox link vidieo <url>")
        return
    
    url = message.command[1]
    api_url = f"https://api.botcahx.eu.org/api/download/terabox?url={url}&apikey=045705b1"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        await message.reply_text("Gagal mengambil data dari Terabox API.")
        return
    
    data = response.json()
    if not data.get("status"):
        await message.reply_text("Terabox API mengembalikan respons gagal.")
        return
    
    result_text = "📂 **Daftar File Terabox:**\n\n"
    for item in data.get("result", []):
        name = item.get("name", "Tidak diketahui")
        created = item.get("created", "Tidak diketahui")
        files = item.get("files", [])
        
        result_text += f"📁 **{name}** (Dibuat: {created})\n"
        for file in files:
            filename = file.get("filename", "Tidak diketahui")
            size = file.get("size", "Tidak diketahui")
            url = file.get("url", "Tidak tersedia")
            result_text += f"  ├ 🎬 {filename} ({size} bytes)\n  └ 🔗 [Download]({url})\n\n"
    
    await message.reply_text(result_text, disable_web_page_preview=True)

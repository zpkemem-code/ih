from Zohun.helpers import *
import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message

__MODULE__ = "Turbo Gpt"
__HELP__ = """
<blockquote><b>✮ Bantuan Untuk Turbo Gpt ✮

perintah : <code>{0}turbo</code>
    buat menjawab pertanyaan <code>{0}claude</code> haii</b></blockquote>
"""

@CMD.UBOT("turbo")
async def chat_gpt(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji>mohon gunakan format\ncontoh : .turbo hai"
            )
        else:
            prs = await message.reply_text(f"<emoji id=6226405134004389590>🔍</emoji>Turbo Sedang Menjawab Pesan Anda....")
            hai = message.text.split(' ', 1)[1]
            response = requests.get(f'https://vapis.my.id/api/turbov1?q={hai}')

            try:
                if "result" in response.json():
                    x = response.json()["result"]                  
                    await prs.edit(
                      f"<blockquote>{x}</blockquote>"
                    )
                else:
                    await message.reply_text("No 'results' key found in the response.")
            except KeyError:
                await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")
      

import random
from Zohun.helpers import *
from pyrogram.types import InputMediaPhoto

__MODULE__ = "Gifsearch"
__HELP__ = """
<blockquote><b>Bantuan Untuk GifSearch

Perintah : <code>{0}gif</code> [ǫuery]
  Untuk Mencari gift/animation Random Dari Google</b></blockquote>
"""

@CMD.UBOT("gif")
async def gif_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply(f"<code>{message.text}</code> [ǫuery]")
    TM = await message.reply("<b>memproses...</b>")
    try:
        x = await client.get_inline_bot_results(
            message.command[0], message.text.split(None, 1)[1]
        )
        saved = await client.send_inline_bot_result(
            client.me.id, x.query_id, x.results[random.randrange(len(x.results))].id
        )
    except:
        await message.reply("<b>❌ gif tidak ditemukan</b>")
        return await TM.delete()
    saved = await client.get_messages(client.me.id, int(saved.updates[1].message.id))
    await client.send_animation(
        message.chat.id, saved.animation.file_id, reply_to_message_id=message.id
    )
    await TM.delete()
    return await saved.delete()

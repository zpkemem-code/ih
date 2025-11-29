import asyncio

from pyrogram import Client
from pyrogram.types import Message

from Zohun import bot
from Zohun.helpers import CMD, Emoji

__MODULE__ = "Colong"
__HELP__ = """
<blockquote><b>Bantuan Untuk Colong

perintah : <code>{0}colong</code>
Untuk Mengambil Media/vidio Yang 1x Lihat</b></blockquote>
"""


@CMD.UBOT("colong")
async def _(client: Client, message: Message):
    """Command to copy/steal one-time view media"""
    emo = Emoji(client)
    await emo.get()
    
    rep = message.reply_to_message
    
    if not rep:
        return await message.reply(
            f"{emo.gagal}<b>Reply to a one-time view media message!</b>"
        )
    
    if not (rep.photo or rep.video or rep.voice or rep.video_note):
        return await message.reply(
            f"{emo.gagal}<b>The replied message doesn't contain viewable media!</b>"
        )
    
    pros = await message.reply(f"{emo.proses}<b>Copying media...</b>")
    
    try:
        # Copy the message to bot's saved messages
        await rep.copy(bot.me.username)
        
        # Get the copied message
        async for msg in client.search_messages(bot.me.username, limit=1):
            try:
                # Forward back to current chat
                await msg.copy(message.chat.id, reply_to_message_id=message.id)
                await pros.delete()
                
                # Delete from saved messages
                await msg.delete()
                
            except Exception as e:
                await pros.edit(
                    f"{emo.gagal}<b>Failed to send media: {str(e)}</b>"
                )
                return
        
    except Exception as e:
        await pros.edit(
            f"{emo.gagal}<b>Failed to copy media: {str(e)}</b>"
        )

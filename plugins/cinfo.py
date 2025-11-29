from Zohun import bot 
from Zohun.helpers import CMD, ButtonUtils 
 
 
__MODULES__ = "Cinfo"

@CMD.UBOT("cardinfo|cid") 
async def _(client, message): 
    result = await ButtonUtils.send_inline_bot_result( 
        message, 
        message.chat.id, 
        bot.me.username, 
        f"inline_card_info {id(message)}", 
    ) 
    if result: 
        return await message.delete() 
    else: 
        return await message.reply_text(f"**Failed to send inline result.**")
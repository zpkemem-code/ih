__MODULES__ = "Seaart" 
__HELP__ = """Command Help **Sea Art** 
 
**Basic commands**  
    **You can generate image to seaart** 
        `{0}seaart` (prompt) 
 
   {1} 
""" 
 
import traceback 
 
from pyrogram.types import InputMediaPhoto 
 
import config 
from Zohun.helpers import CMD, Emoji, Tools 
from Zohun.logger import logger 
 
SEA_URL = "https://api.maelyn.tech/api/seaart" 
 
 
async def generate_seaart(prompt): 
    headers = {"mg-apikey": config.API_MAELYN} 
    params = {"prompt": prompt, "cookie": ""} 
    response = await Tools.fetch.get(SEA_URL, headers=headers, params=params) 
    try: 
        data = response.json() 
        img_url = data["result"] 
        media = [] 
        for img in img_url: 
            media.append(img["url"]) 
            print(media) 
            return media 
    except Exception: 
        logger.error(traceback.format_exc()) 
        return None 
 
 
@CMD.UBOT("seaart") 
async def _(client, message): 
    em = Emoji(client) 
    await em.get() 
    pros = await em.get_costum_text() 
    proses = await message.reply(f"{em.proses}**{pros[4]}**") 
    prompt = client.get_text(message) 
    try: 
        if not prompt: 
            return await proses.edit( 
                f"{em.gagal}**Please reply to a message containing the prompt!\nExample: `{message.text.split()[0]} cute cats`**" 
            ) 
        media = await generate_seaart(prompt) 
        if media is None: 
            return await proses.edit(f"{em.gagal}**Please try again later..**") 
        media_group = [] 
        for data in media: 
            img = await Tools.get_media_data(data, "jpg") 
            caption = f"{em.sukses}Successfully generate image" 
            media_group.append(InputMediaPhoto(media=img, caption=caption)) 
        if media_group: 
            await client.send_media_group( 
                chat_id=message.chat.id, 
                media=media_group, 
                reply_to_message_id=message.id, 
            ) 
            return await proses.delete() 
        else: 
            return await proses.edit( 
                f"{em.gagal}Failed to generate image. Please try again later." 
            ) 
    except Exception as e: 
        logger.error(traceback.format_exc()) 
        return await proses.edit(f"{em.gagal}**Terjadi kesalahan:**\n`{e}`")
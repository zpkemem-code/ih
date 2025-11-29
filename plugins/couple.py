import aiohttp
import random
import os
from pyrogram import enums
from Zohun.helpers import CMD, EMO
from pyrogram.types import InputMediaPhoto

__MODULE__ = "Couple"
__HELP__ = """
<blockquote><b>『 couple 』</b>

  <b>➢ perintah:</b> <code>{0}couple</code>
   <i>penjelasan: untuk mencari photo couple secara random</i></blockquote>
"""

COUPLE_SOURCES = [
    "https://raw.githubusercontent.com/RhymenBillworworx/couple/main/pp{}.jpg",
    "https://avatars.mds.yandex.net/get-pdb/{}",
]

async def get_random_couple_images():
    male_id = random.randint(1, 50)
    female_id = random.randint(51, 100)
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://api.waifu.pics/sfw/waifu") as resp:
                if resp.status == 200:
                    data1 = await resp.json()
                    male_url = data1.get("url")
                else:
                    male_url = None
        except:
            male_url = None
            
        try:
            async with session.get(f"https://api.waifu.pics/sfw/neko") as resp:
                if resp.status == 200:
                    data2 = await resp.json()
                    female_url = data2.get("url")
                else:
                    female_url = None
        except:
            female_url = None
    
    return male_url, female_url

async def download_image(session, url, filename):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                content = await resp.read()
                with open(filename, 'wb') as f:
                    f.write(content)
                return filename
    except:
        pass
    return None

@CMD.UBOT("couple")
async def couple_command(client, message):
    prs = await EMO.PROSES(client)
    err = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    
    jalan = await message.reply(f"{prs}<b>Mencari gambar couple...</b>")
    chat_id = message.chat.id
    
    try:
        male_url, female_url = await get_random_couple_images()
        
        if not male_url or not female_url:
            await jalan.edit(f"{err}<b>Gagal mengambil gambar couple. Coba lagi nanti.</b>")
            return
        
        async with aiohttp.ClientSession() as session:
            male_file = await download_image(session, male_url, f"couple_male_{chat_id}.jpg")
            female_file = await download_image(session, female_url, f"couple_female_{chat_id}.jpg")
            
            if not male_file or not female_file:
                await jalan.edit(f"{err}<b>Gagal mendownload gambar. Coba lagi nanti.</b>")
                return
            
            media_group = [
                InputMediaPhoto(media=male_file, caption="<b>👦 Male</b>"),
                InputMediaPhoto(media=female_file, caption="<b>👧 Female</b>")
            ]
            
            await client.send_media_group(chat_id, media_group)
            await jalan.delete()
            
            if os.path.exists(male_file):
                os.remove(male_file)
            if os.path.exists(female_file):
                os.remove(female_file)
                
    except Exception as e:
        await jalan.edit(f"{err}<b>Terjadi kesalahan:</b> <code>{str(e)}</code>")
        for f in [f"couple_male_{chat_id}.jpg", f"couple_female_{chat_id}.jpg"]:
            if os.path.exists(f):
                os.remove(f)

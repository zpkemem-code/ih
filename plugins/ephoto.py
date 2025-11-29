import os
from Zohun.helpers import *
import requests

__MODULE__ = "Ephoto"
__HELP__ = """**「 BANTUAN UNTUK MODULE EPHOTO 」**

𖠇➛ **perintah: .television (text)**
𖠇➛ **penjelasan: untuk membuat text television**

𖠇➛ **perintah: .glasse (text)**
𖠇➛ **penjelasan: untuk membuat text glasse**

𖠇➛ **perintah: .blackpink (text)**
𖠇➛ **penjelasan: untuk membuat text blackpink**

𖠇➛ **perintah: .blackpink2 (text)**
𖠇➛ **penjelasan: untuk membuat text blackpink2**

𖠇➛ **perintah: .coverpubg (text)**
𖠇➛ **penjelasan: untuk membuat membuat text blackpink2**

𖠇➛ **perintah: .hororr (text)**
𖠇➛ **penjelasan: untuk membuat text hororrr**"""

def tweet(text):
    url = "https://api.botcahx.eu.org/api/ephoto/televisi"
    params = {
        "text": text,
        "apikey": "045705b1"
    }   
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None
        
def rob(text):
    url = "https://api.botcahx.eu.org/api/ephoto/coverpubg"
    params = {
        "text": text,
        "apikey": "045705b1"
    }   
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None
        
def robottt(text):
    url = "https://api.botcahx.eu.org/api/ephoto/horor"
    params = {
        "text": text,
        "apikey": "045705b1"
    }   
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None

          
@CMD.UBOT("hororr")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("contoh : .hororrr peno")
        return

    request_text = args[1]
    processing_msg = await message.edit("loadiiing..........")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▱▱▱▱▱ 𝟸𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▱▱▱▱ 𝟺𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▱▱▱ 𝟼𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▱▱ 𝟾𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▰▰ 𝟷𝟶𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("✦ successғully ✦")
    await asyncio.sleep(0.1)
    image_content = robottt(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("apikey sedang bermasalah")
                                  
@CMD.UBOT("coverpubg")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("contoh : .coverpubg peno")
        return

    request_text = args[1]
    processing_msg = await message.edit("loadiiing..........")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▱▱▱▱▱ 𝟸𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▱▱▱▱ 𝟺𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▱▱▱ 𝟼𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▱▱ 𝟾𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▰▰ 𝟷𝟶𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("✦ successғully ✦")
    await asyncio.sleep(0.1)
    image_content = rob(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("apikey sedang bermasalah")
                                  
@CMD.UBOT("blackpink")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("contoh : .blackpink peno")
        return

    request_text = args[1]
    processing_msg = await message.edit("loadiiing..........")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▱▱▱▱▱ 𝟸𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▱▱▱▱ 𝟺𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▱▱▱ 𝟼𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▱▱ 𝟾𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▰▰ 𝟷𝟶𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("✦ successғully ✦")
    await asyncio.sleep(0.1)
    image_content = fb(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("apikey sedang bermasalah")
@CMD.UBOT("blackpink2")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("contoh : .blackpink peno")
        return

    request_text = args[1]
    processing_msg = await message.edit("loadiiing..........")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▱▱▱▱▱ 𝟸𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▱▱▱▱ 𝟺𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▱▱▱ 𝟼𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▱▱ 𝟾𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▰▰ 𝟷𝟶𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("✦ successғully ✦")
    await asyncio.sleep(0.1)
    image_content = fbs(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("apikey sedang bermasalah")
@CMD.UBOT("television")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("contoh : .television peno")
        return

    request_text = args[1]
    processing_msg = await message.edit("loadiiing..........")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▱▱▱▱▱ 𝟸𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▱▱▱▱ 𝟺𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▱▱▱ 𝟼𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▱▱ 𝟾𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▰▰ 𝟷𝟶𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("✦ successғully ✦")
    await asyncio.sleep(0.1)
    image_content = tweet(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("apikey sedang bermasalah")

@CMD.UBOT("glasse")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("contoh : .gllaases peno")
        return

    request_text = args[1]
    processing_msg = await message.edit("loadiiing..........")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▱▱▱▱▱ 𝟸𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▱▱▱▱ 𝟺𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▱▱▱ 𝟼𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▱▱ 𝟾𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("▰▰▰▰▰▰▰ 𝟷𝟶𝟶%")
    await asyncio.sleep(0.1)
    processing_msg = await message.edit("✦ successғully ✦")
    await asyncio.sleep(0.1)
    image_content = tweets(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("apikey sedang bermasalah")
                                                                                                                              
import asyncio
import random

from plugins import truth_and_dare_string as tod

from Zohun.helpers import *


@CMD.UBOT("apakah")
async def apakah(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.AP)}")


@CMD.UBOT("kenapa")
async def kenapa(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.KN)}")


@CMD.UBOT("bagaimana")
async def bagaimana(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.BG)}")


@CMD.UBOT("dare")
async def dare(client, message):
    try:        
        await message.edit(f"{random.choice(tod.DARE)}")
    except BaseException:
        pass

@CMD.UBOT("truth")
async def truth(client, message):
    try:
        await message.edit(f"{random.choice(tod.TRUTH)}")
    except Exception:
        pass


__MODULE__ = "Truth & Dare"
__HELP__ = """
<b>⦪ bantuan untuk truth & dare ⦫</b>

<blockquote><b>⎆ perintah :
ᚗ <code>{0}dare</code>
⊷ coba aja

ᚗ <code>{0}truth</code>
⊷ coba aja

ᚗ <code>{0}apakah</code>
⊷ coba aja

ᚗ <code>{0}bagaimana</code>
⊷ coba aja

ᚗ <code>{0}kenapa</code>
⊷ coba aja</b></blockquote>
  """

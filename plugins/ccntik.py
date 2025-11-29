import asyncio
import random

from Zohun.helpers import *

__MODULE__ = "Cekcantik"
__HELP__ = """**「 BANTUAN UNTUK MODULE CEK CANTIK 」**

𖠇➛ **perintah: .cekcantik**
𖠇➛ **penjelasan: untuk melihat cantik nama orang**"""


@CMD.UBOT("cekcantik")
async def cekkhodam(client, message):
    try:
        nama = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
        if not nama:
            await message.edit("namanya mana")
            return

        def pick_random(options):
            return random.choice(options)

        hasil = f"""
 <b>𖤐 hasil cek cantik:</b>
╭───────────────────────
├ •nama : {nama}
├ •cantik : {pick_random(['ga seberapa', 'dikit', 'banyak', 'setengah', 'seperapat', 'se tete'])}
├ •ngeri bet jir
╰────────────────────────
  **next cek siapa lagi.**       
      """
        await message.edit(hasil)
    except BaseException:
        pass

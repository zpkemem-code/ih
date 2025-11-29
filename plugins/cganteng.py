import asyncio
import random

from Zohun.helpers import *

__MODULE__ = "Cekganteng"
__HELP__ = """**「 BANTUAN UNTUK MODULE CEK GANTENG 」**

𖠇➛ **perintah: .cekganteng**
𖠇➛ **penjelasan: untuk melihat ganteng nama orang**"""


@CMD.UBOT("cekganteng")
async def cekkhodam(client, message):
    try:
        nama = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
        if not nama:
            await message.edit("namanya mana")
            return

        def pick_random(options):
            return random.choice(options)

        hasil = f"""
 <b>𖤐 hasil cek ganteng:</b>
╭───────────────────────
├ •nama : {nama}
├ •ganteng : {pick_random(['kaya ktl', 'dikit', 'banyak', 'setengah', 'seperapat', 'se tete'])}
├ •ngeri bet jir
╰────────────────────────
  **next cek ganteng siapa lagi.**       
      """
        await message.edit(hasil)
    except BaseException:
        pass

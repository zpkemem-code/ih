import random
from pyrogram import *
from pyrogram import Client, filters
from Zohun.helpers import *

__MODULE__ = "Cek Agama"
__HELP__ = """
<blockquote><b>Bantuan Untuk Cek Agama</b>

Perintah:
<code>{0}cekagama [nama]</code> → DETEKSI AGAMA DARI NAMA  

Sumber: Random generator berdasarkan nama.</blockquote></b>
"""

AGAMA_LIST = [
    "HINDU","ATEIS (GAK PUNYA AGAMA","ISLAM","KRISTEN","BUDHA","KATOLIK","KRISTEN PROTESTAN","ISLAM KTP","KONGHUCU",
]

@CMD.UBOT("cekagama")
async def cek_agama(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text("<blockquote><b>⚠️ Gunakan format: .cekagama [nama]</blockquote></b>")

    nama = args[1]
    agama = random.choice(AGAMA_LIST)
    hasil = f'''<blockquote><b>
    HASIL DETEKSI AGAMA DARI {nama}
    ╭───────────────────────
    ├ nama : `{nama}`
    ├ agama: `{agama}`
    ├ selamat ya agama nya cocok kok
    ╰────────────────────────
    note maaғ ya {nama} cuma becanda kok 😁
    
    </blockquote></b>'''
    await message.reply_text(hasil)

import random
from pyrogram import *
from pyrogram import Client, filters
from Zohun.helpers import *

__MODULE__ = "Cek Kecantikan"
__HELP__ = """
<blockquote><b>Bantuan Untuk Cek Kecantikan</b>

Perintah:
<code>{0}cekkctkn [nama]</code> → Ratting berapa persen kecantikan nama  

Sumber: Random generator berdasarkan nama.</blockquote></b>
"""

KHODAM_LIST = [
    "1% (JELEK BINGIT)🤮", "55% (MAYAN)🙂", "30% (DEMPUL)🙃", "70% (CANTIK TAPI AGAK IRENG)😉",
    "90% (CANTIKNYA PAS)😎", "100% (CANTIK+TOBRUT)🤯", "4% (IRENG)🤢", "10% (IRENG+TEPOS)😖", "1000% (CANTIK+TOBRUT+MANIS)😱"
]

@CMD.UBOT("cekkctkn")
async def cek_khodam(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text("⚠️ Gunakan format: cekkctkn [nama]")

    nama = args[1]
    khodam = random.choice(KHODAM_LIST)
    hasil = f"<blockquote><b>🤭HASIL KECANTIKAN🤭\n\n=👩 Nama: `{nama}`\n Persen: `{khodam}`</blockquote></b>"
    await message.reply_text(hasil)
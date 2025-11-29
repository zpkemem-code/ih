import random
from pyrogram import *
from pyrogram import Client, filters
from Zohun.helpers import *

__MODULE__ = "Cek Khodam"
__HELP__ = """
<blockquote><b>Bantuan Untuk Cek Khodam</b>

Perintah:
<code>{0}cekkhodam [nama]</code> → Melihat jenis khodam berdasarkan nama  

Sumber: Random generator berdasarkan nama.</blockquote></b>
"""

KHODAM_LIST = [
    "🐉 Naga Emas", "🔥 Macan Putih", "🌊 Siluman Air", "🦅 Garuda Sakti",
    "⚡ Harimau Petir", "🌓 Jin Penjaga", "🌿 Roh Alam", "🪨 Batu Bertuah", "🖕 Kontol Pukinak", "👽 Alien Ngocok", " Sandal Jepit", " Jin coklat batangan", " Batu Bata", "kancing baju", " es krim", " ketoprak ", " soto madura", "Remot Tv", "Knalpot Racing", "Bihun", "Kuyang", "Nyi Blorong", "satpam komplek", "tusuk sate", "Tutup Odol", "Bebek sumbing", "Sapi Sumbing", "ultraman pink", "sabun bolong", "tai ayam", "Burung Puyuh", "Roti aoka"
]

@CMD.UBOT("cekkhodam")
async def cek_khodam(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text("⚠️ Gunakan format: cekkhodam [nama]")

    nama = args[1]
    khodam = random.choice(KHODAM_LIST)
    hasil = f"<blockquote><b>🔮 **Hasil Cek Khodam** 🔮\n\n🧑 Nama: `{nama}`\n🪄 Khodam: `{khodam}`</blockquote></b>"
    await message.reply_text(hasil)
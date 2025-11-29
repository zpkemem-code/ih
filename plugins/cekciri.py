import asyncio
import random

from Zohun.helpers import *

@CMD.UBOT("cekkontol|cekkntl")
async def cekkhodam(client, message):
    try:
        nama = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
        if not nama:
            await message.edit("<blockquote><b>namanya mana anjeng<emoji id=6325790754543241229>🪨</emoji></b></blockquote>")
            return

        def pick_random(options):
            return random.choice(options)

        hasil = f"""
<b>𖤐 cek kontol {nama} </b>
<blockquote><b>╭───「 hasil cek kontol 」───</b>
<b>┆• warna kontol : {pick_random(['irenk', 'pink', 'rainbow', 'itam cok', 'kuning'])}</b>
<b>┆• warna jembut : {pick_random(['irenk', 'pink', 'rainbow', 'itam cok', 'kuning'])}</b>
<b>┆• ukuran kontol : {pick_random(['16 cm', '10 cm', '15 cm', '6 cm', '1 cm', '3 cm'])}</b>
<b>┆• ciri cirinya : {pick_random(['bengkok', 'bengkok dikit', 'lurus', 'panjang kecil', 'lebar', 'tumpul'])}</b>
<b>╰──────────────────────</b></blockquote>   
      """
        await message.edit(hasil)
    except BaseException:
        pass

@CMD.UBOT("cekmemek|cekmmk")
async def cekkhodam(client, message):
    try:
        nama = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
        if not nama:
            await message.edit("<blockquote><b>namanya mana anjeng<emoji id=6325790754543241229>🪨</emoji></b></blockquote>")
            return

        def pick_random(options):
            return random.choice(options)

        hasil = f"""
<b>𖤐 cek memek {nama} </b>
<blockquote><b>╭───「 hasil cek memek 」───</b>
<b>┆• warna memek : {pick_random(['irenk', 'pink', 'rainbow', 'itam cok', 'kuning'])}</b>
<b>┆• warna jembut : {pick_random(['irenk', 'pink', 'rainbow', 'itam cok', 'kuning'])}</b>
<b>┆• ukuran lobang : {pick_random(['16 inc', '10 inc', '15 inc', '6 inc', '1 inc', '3 inc'])}</b>
<b>┆• ciri cirinya : {pick_random(['berjembut', 'dah jebol', 'bau trasi', 'berlendir', 'lebar itam', 'sempit'])}</b>
<b>╰──────────────────────</b></blockquote>   
      """
        await message.edit(hasil)
    except BaseException:
        pass

@CMD.UBOT("ceksange|ceksagne")
async def cekkhodam(client, message):
    try:
        nama = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
        if not nama:
            await message.edit("<blockquote><b>namanya mana anjeng<emoji id=6325790754543241229>🪨</emoji></b></blockquote>")
            return

        def pick_random(options):
            return random.choice(options)

        hasil = f"""
<b>𖤐 cek sange</b>
<blockquote><b>╭───「 hasil cek sange 」───</b>
<b>┆• nama :  {nama} </b>
<b>┆• sange : {pick_random(['90%', '95%', '75%', '85%', '100%'])}</b>
<b>┆• sangean kontol </b>
<b>╰──────────────────────</b></blockquote>   
      """
        await message.edit(hasil)
    except BaseException:
        pass
__MODULE__ = "Cek Ciri"
__HELP__ = """<blockquote><b>「 BANTUAN UNTUK MODULE CEK CIRI 」</b>

<b>♛ perintah: .cekkontol</b>
<b>卍 penjelasan: cek kontol dengan nama orangnya</b>

<b>♛ perintah: .cekmemek</b>
<b>卍 penjelasan: cek memek dengan nama orangnya</b>

<b>♛ perintah: .ceksange</b>
<b>卍 penjelasan: cek sange dengan nama orangnya</b></blockquote>
  """

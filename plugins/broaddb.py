import asyncio
import random

from gc import get_objects
from asyncio import sleep
from pyrogram.raw.functions.messages import DeleteHistory, StartBot

from pyrogram.errors.exceptions import FloodWait

from Zohun.helpers import *
from Zohun.database import dB

__MODULE__ = "Broaddb"
__HELP__ = """
<blockquote>Bantuan Untuk Broaddb

perintah : <code>{0}gikesdb</code> 
    mengirim pesan siaran grup/pesan database

perintah : <code>{0}adddb</code> 
    menambahkan database broadcast 

perintah : <code>{0}undb</code> 
    menghapus database broadcast

perintah : <code>{0}listdb</code> 
    melihat total database broadcast

perintah : <code>{0}ralldb</code> 
    menghapus semua database broadcast</blockquote></b>
    
"""

@CMD.UBOT("gikesdb")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    _msg = f"{prs}proccesing..."
    gcs = await message.reply(_msg)
    if not message.reply_to_message:
        return await gcs.edit(f"**{ggl} mohon balas ke pesan !**")
    text = message.reply_to_message
    database = await dB.get_list_from_var(client.me.id, "DB_ID")
    done = 0
    failed = 0
    for chat_id in database:
        try:
            await text.copy(chat_id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await text.copy(chat_id)
            done += 1
        except Exception:
            failed += 1
            pass
    if client.me.is_premium:
        await gcs.delete()
        _gcs = f"""
{brhsl} berrhasil kirim ke {done} chat database
{ggl} gagal kirim ke {failed} chat database

"""
    else:
        await gcs.delete()
        _gcs = f"""
gcast telah selesai
berrhasil {done} chat database
gagal {failed} chat database
"""
    return await message.reply(_gcs)

@CMD.UBOT("adddb")
async def _(client, message):
    prs = await EMO.PROSES(client)
    grp = await EMO.BERHASIL(client)
    _msg = f"{prs}processing..."

    msg = await message.reply(_msg)
    try:
        chat_id = message.chat.id
        database = await dB.get_list_from_var(client.me.id, "DB_ID")

        if chat_id in database:
            txt = f"""
{grp}sudah ada dalam database broadcast
"""
        else:
            await add_to_vars(client.me.id, "DB_ID", chat_id)
            txt = f"""
{grp}berhasil di tambahkan ke database broadcast
"""

        return await msg.edit(txt)
    except Exception as error:
        return await msg.edit(str(error))


@CMD.UBOT("undb")
async def _(client, message):
    prs = await EMO.PROSES(client)
    grp = await EMO.BERHASIL(client)
    _msg = f"{prs}processing..."

    msg = await message.reply(_msg)
    try:
        chat_id = get_arg(message) or message.chat.id
        database = await dB.get_list_from_var(client.me.id, "DB_ID")

        if chat_id not in database:
            response = f"""
{grp}tidak ada dalam database broadcast
"""
        else:
            await remove_from_vars(client.me.id, "DB_ID", chat_id)
            response = f"""
{grp}berhasil di hapus dalam database broadcast
"""

        return await msg.edit(response)
    except Exception as error:
        return await msg.edit(str(error))


@CMD.UBOT("listdb")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    _msg = f"{prs}processing..."
    mzg = await message.reply(_msg)

    database = await dB.get_list_from_var(client.me.id, "DB_ID")
    total_database = len(database)

    list = f"{brhsl} daftar database\n"

    for chat_id in database:
        try:
            chat = await client.get_chat(chat_id)
            list += f" ├ {chat.title} | {chat.id}\n"
        except:
            list += f" ├ {chat_id}\n"

    list += f"{ktrng} total database {total_database}"
    return await mzg.edit(list)


@CMD.UBOT("ralldb")
async def _(client, message):
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    brhsl = await EMO.BERHASIL(client)
    _msg = f"{prs}processing..."

    msg = await message.reply(_msg)
    databases = await dB.get_list_from_var(client.me.id, "DB_ID")

    if not databases:
        return await msg.edit(f"{ggl}database broadcast anda kosong")

    for chat_id in databases:
        await remove_from_vars(client.me.id, "DB_ID", chat_id)

    await msg.edit(f"{brhsl}semua database broadcast berhasil di hapus")

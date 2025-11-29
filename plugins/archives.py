from Zohun.helpers.tools import get_data_id
from Zohun.helpers import *
__MODULE__ = "Archive"
__HELP__ = """
<b>⦪ bantuan untuk archive ⦫<b>

<blockquote><b>⎆ perintah :
ᚗ <code>{0}arch</code>
⊷ mengarchivekan group chat pribadi maupun channel

ᚗ <code>{0}unarch</code>
⊷ mengunarchivekan group chat pribadi maupun channel</b></blockquote>
"""
@CMD.UBOT("arch")
async def archive_user(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    if len(message.command) <2:
        return await message.reply(f"{ggl}mohon gunakan arch all, users, group")
    anjai = await message.reply(f"{prs}proccesing...")
    anjir = message.command[1]
    xx = await client.get_chat_id( anjir)
    for anu in xx:
        await client.archive_chats(anu)
    
    await anjai.edit(f"{brhsl}berhasil mengarchivekan semua {anjir}")

@CMD.UBOT("unarch")
async def unarchive_user(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    if len(message.command) <2:
        return await message.reply(f"{ggl}mohon gunakan arch all, users, group")
    anjai = await message.reply(f"{prs}proccesing...")
    anjir = message.command[1]
    xx = await client.get_chat_id( anjir)
    for anu in xx:
        await client.unarchive_chats(anu)
    await anjai.edit(f"{brhsl}berhasil mengunarchivekan semua {anjir}")

import os
import asyncio
import random

from os import remove
from asyncio import sleep, gather

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.enums import ChatType

from Zohun.helpers import *


__MODULE__ = "Profiles"
__HELP__ = """
<blockquote>Bantuan Untuk Profiles

perintah : <code>{0}setbio</code>
    mengubah bio pada akun anda

perintah : <code>{0}setname</code>
    mengubah nama pada akun anda:

perintah : <code>{0}block</code>
    memblokir pengguna

perintah : <code>{0}unblock</code>
    membuka pemblokiran pada pengguna

perintah : <code>{0}sg</code>
    memeriksa histori name pengguna telegram

perintah : <code>{0}info</code>
    melihat informasi data akun telegram

perintah : <code>{0}cinfo</code>
    melihat informasi data group/channel telegram</blockquote>
"""


@CMD.UBOT("sg")
async def _(client, message):
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    get_user = await extract_user(message)
    lol = await message.reply(f"{prs}processing...")
    if not get_user:
        return await lol.edit(f"{ggl}user tidak ditemukan")
    try:
        user_id = (await client.get_users(get_user)).id
    except Exception:
        try:
            user_id = int(message.command[1])
        except Exception as error:
            return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    getbot = random.choice(bot)
    await client.unblock_user(getbot)
    txt = await client.send_message(getbot, user_id)
    await asyncio.sleep(4)
    await txt.delete()
    await lol.delete()
    async for name in client.search_messages(getbot, limit=2):
        if not name.text:
            await message.reply(
                f"{ggl}{getbot} tidak dapat merespon permintaan", quote=True
            )
        else:
            await message.reply(name.text, quote=True)
    user_info = await client.resolve_peer(getbot)
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))


@CMD.UBOT("info")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"{prs}processing . . .")
    if not user_id:
        return await Tm.edit(
            f"{ggl}berikan userid/username/reply untuk mendapatkan info pengguna tersebut.>"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""
<blockquote><b>{brhsl} user information:</blockquote></b>

<blockquote><b><emoji id=6030656587830399914>🆔</emoji> user id: {user.id}
<emoji id=5260399854500191689>😀</emoji> first name: {first_name}
<emoji id=5257969839313526622>📂</emoji> last name: {last_name}
<emoji id=5258331647358540449>✍️</emoji> username: {username}
<emoji id=5260268501515377807>📣</emoji> dc id: {dc_id}
<emoji id=5258093637450866522>😀</emoji> is bot: {user.is_bot}
<emoji id=5219805369806629055>😀</emoji> is scam: {user.is_scam}
<emoji id=6003779240837780921>🚫</emoji> restricted: {user.is_restricted}
<emoji id=5260341314095947411>👀</emoji> verified: {user.is_verified}
<emoji id=5258185631355378853>⭐️</emoji> premium: {user.is_premium}
<emoji id=5292226786229236118>🔄</emoji> user bio: {bio}</blockquote></b>

<blockquote><b><emoji id=5220070652756635426>😀</emoji> same groups seen: {len(common)}
<emoji id=5253959125838090076>😀</emoji> last seen: {status}
<emoji id=4942990428317156193>😅</emoji> userbot: <a href=tg://user?id={user.id}>{fullname}</a></blockquote></b>
"""
        
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Tm.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"info: {e}")


@CMD.UBOT("cinfo")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    Tm = await message.reply(f"{prs}processing . . .")
    try:
        if len(message.text.split()) > 1:
            chat_u = message.text.split()[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await Tm.edit(
                    f"{ggl}gunakan perintah ini di dalam grup atau gunakan cinfo [group username atau id]"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""
{brhsl}chat information:

🆔 chat id: {chat.id}
👥 title: {chat.title}
👥 username: {username}
📩 type: {type}
🏛️ dc id: {dc_id}
🗣️ is scam: {chat.is_scam}
🎭 is fake: {chat.is_fake}
✅ verified: {chat.is_verified}
🚫 restricted: {chat.is_restricted}
🔰 protected: {chat.has_protected_content}

🚻 total members: {chat.members_count}
📝 description: {description}
"""
        
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Tm.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=message.id,
                ),
            )
            remove(photo)
        else:
            await Tm.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(f"info: `{e}`")


@CMD.UBOT("id")
async def _(client, message):
    text = f"<blockquote><b><emoji id=6026218958900695642>💎</emoji> message id: `{message.id}`\n</blockquote></b>"

    if message.chat.type == ChatType.CHANNEL:
        text += f"<blockquote><b><emoji id=6026056450223116307>⏺</emoji> chat id: `{message.sender_chat.id}`\n</blockquote></b>"
    else:
        text += f"<blockquote><b><emoji id=6026292029179301727>👑</emoji> your id: `{message.from_user.id}`\n</blockquote></b>"

        if len(message.command) > 1:
            try:
                user = await client.get_chat(message.text.split()[1])
                text += f"<blockquote><b><emoji id=6026056450223116307>⏺</emoji> user id: `{user.id}`\n</blockquote></b>\n"
            except:
                return await message.reply("<emoji id=6113891550788324241>❌</emoji>pengguna tidak ditemukan")

        text += f"<blockquote><b><emoji id=6026056450223116307>⏺</emoji> chat id: `{message.chat.id}`\n</blockquote></b>"

    if message.reply_to_message:
        id_ = (
            message.reply_to_message.from_user.id
            if message.reply_to_message.from_user
            else message.reply_to_message.sender_chat.id
        )
        file_info = get_file_id(message.reply_to_message)
        if file_info:
            text += f"media id: {file_info.file_id}\n\n"
        text += (
            f"<blockquote><b><emoji id=6026257381678124710>✅</emoji> replied message id: `{message.reply_to_message.id}` </blockquote></b>\n"
            f"<blockquote><b><emoji id=6026257381678124710>✅</emoji> replied user id: `{id_}` </blockquote></b>"
        )

    return await message.reply(text, disable_web_page_preview=True)


@CMD.UBOT("setbio")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    tex = await message.reply(f"{prs}processing...")
    if len(message.command) == 1:
        return await tex.edit(f"{ggl}{message.text.split()[0]} [text]")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await tex.edit(f"{brhsl}berhasil mengubah bio menjadi {bio}")
        except Exception as e:
            await tex.edit(f"ERROR: {e}")
    else:
        return await tex.edit(f"{ggl}berikan teks untuk ditetapkan sebagai bio")


@CMD.UBOT("setname")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    tex = await message.reply(f"{prs}processing...")
    if len(message.command) == 1:
        return await tex.edit(f"{ggl}{message.text.split()[0]} [text]")
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await tex.edit(
                f"{brhsl}berhasil mengubah nama menjadi {name}"
            )
        except Exception as e:
            await tex.edit(f"ERROR: {e}")
    else:
        return await tex.edit(f"{ggl}berikan teks untuk ditetapkan sebagai nama anda")


@CMD.UBOT("block")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    tex = await message.reply(f"{prs}processing...")
    if not user_id:
        return await tex.edit(f"{ggl}{message.text.split()[0]} [reply to user]")
    if user_id == client.me.id:
        return await tex.edit(f"{brhsl}ok done")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"{brhsl}berhasil diblokir {umention}")
  

@CMD.UBOT("unblock")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user_id = await extract_user(message)
    tex = await message.reply(f"{prs}processing...")
    if not user_id:
        return await tex.edit(f"{ggl}{message.text.split()[0]} [reply to user]")
    if user_id == client.me.id:
        return await tex.edit(f"{brhsl}ok done.")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"{brhsl}berhasil dibebaskan {umention}")

@CMD.UBOT("idm")
async def _(client, message):
    if not message.reply_to_message:
        return
    id = message.reply_to_message.entities[0].custom_emoji_id
    await message.reply(f"`{id}`")


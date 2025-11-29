from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from config import OWNER_ID
from Zohun.helpers import *
from Zohun.database import dB
from Zohun import bot



__MODULES__ = "Owner Bot"

@CMD.UBOT("addprem")
@CMD.UBOT("prem")
async def _(client, message):
    user = message.from_user
    seller_id = await dB.get_list_from_var(bot.me.id, "SELER_USERS")
    if user.id != OWNER_ID and user.id not in seller_id:
        return await message.reply("❌ Tidak ada izin! Command ini untuk Owner dan Reseller.")
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("memproses...")
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username - bulan</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    if not get_bulan:
        get_bulan = 1

    prem_users = await dB.get_list_from_var(bot.me.id, "PREM_USERS")

    if user.id in prem_users:
        return await msg.edit(f"""
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> sudah premium
▎<b>expired:</b> {get_bulan} bulan
"""
        )

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(bot.me.id, "PREM_USERS", user.id)
        await msg.edit(f"""
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>expired:</b> {get_bulan} bulan
▎<b>silahkan buka @{bot.me.username} untuk membuat userbot</b>

▎<b>cara buat userbot:</b>
▎ • silahkan /start dulu bot @ZoHunUbot
▎ • kalau sudah start bot abis itu pencet tombol buat userbot
▎ • nah nanti ada arahan dari bot nya itu ikutin

▎<b>note:</b> jangan lupa baca arahan dari bot nya
"""
        )
        return await bot.send_message(
            OWNER_ID,
            f"• id-seller: `{message.from_user.id}`\n\n• id-customer: `{user_id}`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⁉️ seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "customer ⁉️", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)


@CMD.UBOT("unprem")
async def _(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/username</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    prem_users = await dB.get_list_from_var(bot.me.id, "PREM_USERS")

    if user.id not in prem_users:
        return await msg.edit(f"""
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> tidak terdaftar
"""
        )
    try:
        await remove_from_vars(bot.me.id, "PREM_USERS", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> telah di hapus dari database
"""
        )
    except Exception as error:
        return await msg.edit(error)
        

@CMD.UBOT("getprem")
async def _(client, message):
    text = ""
    count = 0
    user = message.from_user
    seller_id = await dB.get_list_from_var(bot.me.id, "SELER_USERS")
    if user.id != OWNER_ID and user.id not in seller_id:
        return await message.reply("❌ Tidak ada izin! Command ini untuk Owner dan Reseller.")
    prem = await dB.get_list_from_var(bot.me.id, "PREM_USERS")
    prem_users = []

    for user_id in prem:
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"▎ • {count}: <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a> » <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        await message.reply_text("tidak ada pengguna yang ditemukan")
    else:
        await message.reply_text(text)


@CMD.UBOT("addseller")
@CMD.UBOT("addseles")
@CMD.UBOT("seles")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("❌ Tidak ada izin! Command ini hanya untuk Owner.")
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/username</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await dB.get_list_from_var(bot.me.id, "SELER_USERS")

    if user.id in sudo_users:
        return await msg.edit(f"""
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> sudah reseller
"""
        )

    try:
        await add_to_vars(bot.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> reseller
▎<b>silahkan buka @{bot.me.username}</b>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@CMD.UBOT("unseles")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("❌ Tidak ada izin! Command ini hanya untuk Owner.")
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/username</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await dB.get_list_from_var(bot.me.id, "SELER_USERS")

    if user.id not in seles_users:
        return await msg.edit(f"""
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> tidak terdaftar
"""
        )

    try:
        await remove_from_vars(bot.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> telah di hapus dari database
"""
        )
    except Exception as error:
        return await msg.edit(error)


@CMD.UBOT("getseles")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("❌ Tidak ada izin! Command ini hanya untuk Owner.")
    Sh = await message.reply("sedang memproses...")
    seles_users = await dB.get_list_from_var(bot.me.id, "SELER_USERS")

    if not seles_users:
        return await Sh.edit("daftar seller kosong")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f"▎ 👤 <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a> • <code>{user.id}</code>"
            )
        except:
            continue

    if seles_list:
        response = (
            "📋 daftar reseller:\n\n"
            + "\n".join(seles_list)
            + f"\n\n• total reseller: {len(seles_list)}"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar seller")


@CMD.UBOT("time")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("❌ Tidak ada izin! Command ini hanya untuk Owner.")
    Tm = await message.reply("processing . . .")
    bajingan = message.command
    if len(bajingan) != 3:
        return await Tm.edit(f"gunakan /set_time user_id hari")
    user_id = int(bajingan[1])
    get_day = int(bajingan[2])
    print(user_id , get_day)
    try:
        get_id = (await client.get_users(user_id)).id
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"""
▎💬 <b>INFORMATION</b>
▎<b>name:</b> {user.mention}
▎<b>id:</b> <code>{get_id}</code>
▎<b>aktifkan selama:</b> {get_day} hari
"""
    )


@CMD.UBOT("cek")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("❌ Tidak ada izin! Command ini hanya untuk Owner.")
    Sh = await message.reply("processing . . .")
    user_id = await extract_user(message)
    if not user_id:
        return await Sh.edit("pengguna tidak temukan")
    try:
        get_exp = await get_expired_date(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.ediit(error)
    if get_exp is None:
        await Sh.edit(f"""
▎<b>name:</b> {sh.mention}
▎<b>id:</b> <code>{user_id}</code>
▎<b>plan:</b> none
▎<b>prefix:</b> .
▎<b>expired:</b> nonaktif
""")
    else:
        SH = await ubot.get_prefix(user_id)
        exp = get_exp.strftime("%d-%m-%Y")
        if user_id in await dB.get_list_from_var(bot.me.id, "ULTRA_PREM"):
            status = "SuperUltra"
        else:
            status = "Premium"
        await Sh.edit(f"""
▎<b>name:</b> {sh.mention}
▎<b>id:</b> <code>{user_id}</code>
▎<b>plan:</b> {status}
▎<b>prefix:</b> {' '.join(SH)}
▎<b>expired:</b> {exp}
"""
        )


@CMD.UBOT("addadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("❌ Tidak ada izin! Command ini hanya untuk Owner.")
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await dB.get_list_from_var(bot.me.id, "ADMIN_USERS")

    if user.id in admin_users:
        return await msg.edit(f"""
▎💬 <b>INFORMATION</b>
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> sudah dalam daftar
"""
        )

    try:
        await add_to_vars(bot.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
▎💬 <b>INFORMATION</b>
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> admin
"""
        )
    except Exception as error:
        return await msg.edit(error)


@CMD.UBOT("unadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("❌ Tidak ada izin! Command ini hanya untuk Owner.")
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await dB.get_list_from_var(bot.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
▎💬 <b>INFORMATION</b>
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> tidak dalam daftar
"""
        )

    try:
        await remove_from_vars(bot.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
▎💬 <b>INFORMATION</b>
▎<b>name:</b> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>
▎<b>id:</b> <code>{user.id}</code>
▎<b>keterangan:</b> unadmin
"""
        )
    except Exception as error:
        return await msg.edit(error)


@CMD.UBOT("getadmin")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply("❌ Tidak ada izin! Command ini hanya untuk Owner.")
    Sh = await message.reply("sedang memproses...")
    admin_users = await dB.get_list_from_var(bot.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("<s>daftar admin kosong</s>")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f"▎ 👤 <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a> • <code>{user.id}</code>"
            )
        except:
            continue

    if admin_list:
        response = (
            "📋 daftar admin:\n\n"
            + "\n".join(admin_list)
            + f"\n\n⚜️ total admin: {len(admin_list)}"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar admin")

@CMD.UBOT("addultra")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply_text(f"{ggl}mau ngapain kamu ?")
    msg = await message.reply(f"{prs}sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{ggl}{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await dB.get_list_from_var(bot.me.id, "ULTRA_PREM")

    if user.id in ultra_users:
        return await msg.edit(f"{ggl}sudah menjadi superultra!")

    try:
        await add_to_vars(bot.me.id, "ULTRA_PREM", user.id)
        return await msg.edit(f"{brhsl}berhasil menjadi superultra")
    except Exception as error:
        return await msg.edit(error)

@CMD.UBOT("rmultra")
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    user = message.from_user
    if user.id != OWNER_ID:
        return await message.reply_text(f"{ggl}mau ngapain kamu ?")
    msg = await message.reply(f"{prs}sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{ggl}{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await dB.get_list_from_var(bot.me.id, "ULTRA_PREM")

    if user.id not in ultra_users:
        return await msg.edit(f"{ggl}tidak ada di dalam database superultra")

    try:
        await remove_from_vars(bot.me.id, "ULTRA_PREM", user.id)
        return await msg.edit(f"{brhsl}berhasil di hapus dari daftar superultra")
    except Exception as error:
        return await msg.edit(error)

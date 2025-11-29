import asyncio
import importlib
from datetime import datetime

import pyrogram
from dateutil.relativedelta import relativedelta
from pyrogram.types import (InlineKeyboardMarkup, KeyboardButton,
                            ReplyKeyboardMarkup, ReplyKeyboardRemove)
from pytz import timezone

from config import API_HASH, API_ID, LOG_SELLER, MAX_BOT, SUDO_OWNERS
from Zohun import AKSES_DEPLOY, BOT_ID, UserBot, bot, dB, zohun
from Zohun.database import state
from Zohun.helpers import CMD, ButtonUtils, Message, TokenReferal, ikb, no_trigger
from Zohun.logger import logger
from plugins import PLUGINS


async def setExpiredUser(user_id):
    if user_id in SUDO_OWNERS:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=12)
        await dB.set_expired_date(user_id, expired)
    else:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=1)
        await dB.set_expired_date(user_id, expired)


async def mari_buat_userbot(client, message):
    try:
        user_id = message.from_user.id
        
        # Send immediate feedback
        await message.reply("Memproses permintaan...")
        
        if user_id in zohun._get_my_id:
            return await client.send_message(
                user_id,
                "<b><blockquote>Anda telah memasang userbot</blockquote></b>",
                reply_markup=ReplyKeyboardRemove(),
            )
        if len(zohun._ubot) == MAX_BOT:
            buttons = ReplyKeyboardMarkup(
                [["💬 Hubungi Admins"]], resize_keyboard=True, one_time_keyboard=True
            )
            return await message.reply(
                f"""
<b>❌ Tidak dapat membuat Userbot !</b>

<b>📚 Karena Telah Mencapai Yang Telah Di Tentukan : {len(zohun._ubot)}</b>

<b>👮‍♂ Silakan Hubungi Admins . </b>
""",
                reply_markup=buttons,
            )
        # Check if user has permission from ANY permission list
        # Use BOT_ID directly to ensure consistency
        prem_users = await dB.get_list_from_var(BOT_ID, "PREM_USERS")
        seler_users = await dB.get_list_from_var(BOT_ID, "SELER_USERS")
        admin_users = await dB.get_list_from_var(BOT_ID, "ADMIN_USERS")
        
        has_access = (
            user_id in AKSES_DEPLOY or
            user_id in prem_users or
            user_id in seler_users or
            user_id in admin_users
        )
        
        if not has_access:
            buttons = ikb([[("📃 Saya Setuju", "go_payment")], [("❌ Tutup", "closed")]])
            text = f"<blockquote>{await Message.policy_message()}</blockquote>"
            return await message.reply(
                text,
                disable_web_page_preview=True,
                reply_markup=buttons,
            )
        else:
            return await create_userbots(client, message)
    
    except Exception as e:
        # Comprehensive error reporting
        logger.error(f"ERROR in mari_buat_userbot: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Send error to user
        try:
            error_msg = "<b>Terjadi Error:</b>\n\n<code>" + str(e) + "</code>\n\n<b>Silahkan screenshot dan kirim ke admin.</b>\n\n<b>Error Type:</b> " + type(e).__name__
            await message.reply(error_msg)
        except:
            pass


async def create_userbots(client, message):
    tokenref = await TokenReferal.create()
    try:
        user_id = message.from_user.id
        anu = ReplyKeyboardMarkup(
            [
                [KeyboardButton(text="Kontak Saya", request_contact=True)],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        try:
            ref_kode = await client.ask(
                user_id,
                "<b>Apakah kamu mempunyai kode Referral ? Jika iya, Silahkan kirim kode Referral. Jika tidak kamu bisa melakukan /skip.</b>",
                timeout=300,
            )
            if ref_kode.text in ["skip", "Skip", "/skip", "start", "/start"]:
                kode_referal = None
            else:
                kode_referal = ref_kode.text
        except asyncio.TimeoutError:
            kode_referal = None
        try:
            phone = await client.ask(
                user_id,
                f"<blockquote><b>Silahkan klik tombol <u>Kontak Saya</u> untuk mengirimkan Nomor Telepon Telegram Anda.</b></blockquote>\n<b>Ads: {await Message._ads()}</b>",
                reply_markup=anu,
            )
            phone_number = phone.contact.phone_number
        except AttributeError:
            try:
                phone = await client.ask(
                    user_id,
                    f"<blockquote><b>Silahkan klik tombol <u>Kontak Saya</u> untuk mengirimkan Nomor Telepon Telegram Anda.</b></blockquote>\n<b>Ads: {await Message._ads()}</b>",
                    reply_markup=anu,
                )
                phone_number = phone.contact.phone_number
            except Exception:
                return await bot.send_message(
                    user_id,
                    "<blockquote><b>PEA, punya mata dipake buat baca!! jangan BOKEP mulu.</b></blockquote>",
                    reply_markup=ButtonUtils.start_menu(is_admin=False),
                )
        new_client = pyrogram.Client(
            name=str(user_id),
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True,
        )
        await asyncio.sleep(2)
        get_otp = await client.send_message(
            user_id,
            f"<b><blockquote>Sedang Mengirim Kode OTP...</blockquote></b>\n<b>Ads: {await Message._ads()}</b>",
            reply_markup=ReplyKeyboardRemove(),
        )
        await new_client.connect()
        try:
            code = await new_client.send_code(phone_number.strip())
        except pyrogram.errors.ApiIdInvalid as AID:
            await get_otp.delete()
            return await client.send_message(user_id, AID)
        except pyrogram.errors.PhoneNumberInvalid as PNI:
            await get_otp.delete()
            return await client.send_message(user_id, PNI)
        except pyrogram.errors.PhoneNumberFlood as PNF:
            await get_otp.delete()
            return await client.send_message(user_id, PNF)
        except pyrogram.errors.PhoneNumberBanned as PNB:
            await get_otp.delete()
            return await client.send_message(user_id, PNB)
        except pyrogram.errors.PhoneNumberUnoccupied as PNU:
            await get_otp.delete()
            return await client.send_message(user_id, PNU)
        except Exception as error:
            await get_otp.delete()
            return await client.send_message(
                user_id,
                f"<b>ERROR:</b> {error}",
                reply_markup=ButtonUtils.start_menu(is_admin=False),
            )
        await get_otp.delete()
        otp = await client.ask(
            user_id,
            f"<b><blockquote>Silakan Periksa Kode OTP dari <a href=tg://openmessage?user_id=777000>Akun Telegram</a> Resmi. Kirim Kode OTP ke sini setelah membaca Format di bawah ini.</b>\n\nJika Kode OTP adalah <code>12345</code> Tolong <b>[ TAMBAHKAN SPASI ]</b> kirimkan Seperti ini <code>1 2 3 4 5</code>.</blockquote></b>\n<b>Ads: {await Message._ads()}</b>",
        )
        if otp.text in no_trigger:
            return await client.send_message(
                user_id,
                f"<blockquote><b>Proses di batalkan.</b></blockquote>\n<b>Ads: {await Message._ads()}</b>",
                reply_markup=ButtonUtils.start_menu(is_admin=False),
            )
        otp_code = otp.text
        try:
            await new_client.sign_in(
                phone_number.strip(),
                code.phone_code_hash,
                phone_code=" ".join(str(otp_code)),
            )
        except pyrogram.errors.PhoneCodeInvalid as PCI:
            return await client.send_message(user_id, PCI)
        except pyrogram.errors.PhoneCodeExpired as PCE:
            return await client.send_message(user_id, PCE)
        except pyrogram.errors.BadRequest as error:
            return await client.send_message(
                user_id,
                f"<b>ERROR:</b> {error}",
                reply_markup=ButtonUtils.start_menu(is_admin=False),
            )
        except pyrogram.errors.SessionPasswordNeeded:
            two_step_code = await client.ask(
                user_id,
                f"<b><blockquote>Akun anda Telah mengaktifkan Verifikasi Dua Langkah. Silahkan Kirimkan Passwordnya.</blockquote></b>\n<b>Ads: {await Message._ads()}</b>",
            )
            if two_step_code.text in no_trigger:
                return await client.send_message(
                    user_id,
                    f"<blockquote><b>Proses di batalkan.</b></blockquote>\n<b>Ads: {await Message._ads()}</b>",
                    reply_markup=ButtonUtils.start_menu(is_admin=False),
                )
            new_code = two_step_code.text
            try:
                await new_client.check_password(new_code)
                await dB.set_var(user_id, "PASSWORD", new_code)
            except Exception as error:
                return await client.send_message(
                    user_id,
                    f"<b>ERROR:</b> {error}",
                    reply_markup=ButtonUtils.start_menu(is_admin=False),
                )
        session_string = await new_client.export_session_string()
        await new_client.disconnect()
        new_client.storage.session_string = session_string
        new_client.in_memory = False
        bot_msg = await client.send_message(
            user_id,
            f"<b><blockquote>Tunggu proses selama 1-5 menit...\nKami sedang menghidupkan Userbot Anda.</blockquote></b>\n<b>Ads: {await Message._ads()}</b>",
            disable_web_page_preview=True,
        )
        await asyncio.sleep(2)
        kn_client = UserBot(
            name=str(user_id),
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            in_memory=True,
        )
        try:
            await kn_client.start()
        except Exception as e:
            logger.error(f"Error Client: {str(e)}")
        if not await dB.get_expired_date(kn_client.me.id):
            await setExpiredUser(kn_client.me.id)
        await dB.add_ubot(
            user_id=int(kn_client.me.id),
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
        )
        if not user_id == kn_client.me.id:
            zohun._ubot.remove(kn_client)
            await dB.remove_ubot(kn_client.me.id)
            await kn_client.log_out()
            return await bot_msg.edit(
                f"<blockquote><b>Gunakan akun anda sendiri, bukan orang lain!!</b></blockquote>\n<b>Ads: {await Message._ads()}</b>"
            )
        Referral = await tokenref.register_user(
            user_id=str(kn_client.me.id),
            api_id=API_ID,
            api_hash=API_HASH,
            phone=phone_number.strip(),
            referral_code=kode_referal,
        )
        user_token = Referral["token"]
        user_referal = Referral["referral_code"]
        referal_from = Referral["referred_by"] or None
        await asyncio.sleep(1)
        for mod in PLUGINS:
            importlib.reload(importlib.import_module(f"plugins.{mod}"))
        seles = await dB.get_list_from_var(BOT_ID, "SELLER")
        if kn_client.me.id not in seles:
            try:
                AKSES_DEPLOY.remove(kn_client.me.id)
            except Exception:
                pass
        try:
            await kn_client.join_chat("ZonaDewasaNew")
            await kn_client.join_chat("ZonaShareNew")
            await kn_client.join_chat("WarungRimNew")
        except Exception:
            pass
        prefix = zohun.get_prefix(kn_client.me.id)
        keyb = ButtonUtils.start_menu(is_admin=False)
        exp = await dB.get_expired_date(kn_client.me.id)
        expir = exp.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
        text_done = f"""
<blockquote><b>🔥 {bot.me.mention} Berhasil Di Aktifkan
➡️ Akun: <a href=tg://openmessage?user_id={kn_client.me.id}>{kn_client.me.first_name} {kn_client.me.last_name or ''}</a>
➡️ ID: <code>{kn_client.me.id}</code>
➡️ Prefixes: {' '.join(prefix)}
➡️ Token: <code>{user_token}</code>
➡️ Kode Referral Anda: <code>{user_referal}</code>
➡️ Kode Referral dari: {referal_from}
➡️ Masa Aktif: {expir}</b></blockquote>

<blockquote><b>Kode Referral kamu berfungsi untuk mengajak pengguna lain menggunakan bot ini. Dan jika kode Referral kamu sudah digunakan 10 kali, maka kamu bisa menambahkan masa aktif userbot selama 1 bulan atau memasang userbot gratis menggunakan akun kamu yang lain.
Kamu bisa mengecek status Referral kamu dengan cara mengetik /status dibot ini.
 
Token kamu berfungsi untuk mengklaim garansi ubot, jika kamu ingin berpindah akun atau akunmu dibanned oleh pihak Telegram. Mohon simpan Token kamu dengan aman.</b></blockquote>

<b>Ads: {await Message._ads()}</b>"""
        await bot_msg.edit(text_done, disable_web_page_preview=True, reply_markup=keyb)
        who_seller = state.get(kn_client.me.id, "seller")
        if who_seller:
            count = await dB.get_var(int(who_seller), "penjualan") or 0
            new_data = count + 1
            await dB.set_var(int(who_seller), "penjualan", new_data)
        return await client.send_message(
            LOG_SELLER,
            f"""
    <b>❏ Notifikasi Userbot Aktif</b>
    <b> ├ Akun :</b> <a href=tg://user?id={kn_client.me.id}>{kn_client.me.first_name} {kn_client.me.last_name or ''}</a> 
    <b> ╰ ID :</b> <code>{kn_client.me.id}</code>
    """,
            reply_markup=ikb(
                [
                    [
                        (
                            "Cek Kadaluarsa",
                            f"cek_masa_aktif {kn_client.me.id}",
                            "callback_data",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    except Exception as er:
        logger.error(f"{str(er)}")


@CMD.CALLBACK("^cek_masa_aktif")
async def _(client, cq):
    user_id = int(cq.data.split()[1])
    try:
        expired = await dB.get_expired_date(user_id)
        habis = expired.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
        return await cq.answer(f"⏳ Waktu: {habis}", True)
    except Exception:
        return await cq.answer("✅ Sudah tidak aktif", True)


@CMD.CALLBACK("^closed")
async def _(client, cq):
    await cq.answer()
    return await cq.message.delete()

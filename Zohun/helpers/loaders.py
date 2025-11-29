import asyncio
import os
import sys
import traceback
import zipfile
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from pyrogram import enums
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup
from pytz import timezone

from config import (AKSES_DEPLOY, BOT_ID, BOT_NAME, LOG_BACKUP, LOG_SELLER,
                    OWNER_ID, SAWERIA_USERID)
from Zohun import bot, zohun
from Zohun.logger import logger
from Zohun.database import dB

from ..database import DB_PATH, dB, state
from .auto_referal import TokenReferal
from .message import Message
from .tools import Tools

waktu_jkt = timezone("Asia/Jakarta")


def kb(rows=None, resize_keyboard=True, one_time_keyboard=False):
    """Local kb function for this module."""
    if rows is None:
        rows = []
    keyboard = []
    for row in rows:
        button_row = []
        for button in row:
            if isinstance(button, str):
                button_row.append(KeyboardButton(text=button))
            elif isinstance(button, tuple) and len(button) >= 1:
                button_row.append(KeyboardButton(text=button[0]))
        if button_row:
            keyboard.append(button_row)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard
    )


def find_env_file():
    for file in os.listdir():
        if file.endswith(".env"):
            return os.path.abspath(file)
    return None


async def add_transaction(user_id, month):
    expired = await dB.get_expired_date(user_id)
    if not expired:
        now = datetime.now(waktu_jkt)
        expired = now + relativedelta(months=month)
        await dB.set_expired_date(user_id, expired)


async def get_receive(payment_id):
    receipt_url = f"https://api-sparkle.vercel.app/api/saweria/checkPayment/{SAWERIA_USERID}/{payment_id}"
    try:
        response = await Tools.fetch.get(receipt_url)
        if response.status_code == 200:
            resp = response.json()
            teks = resp["msg"]
            if teks == "BERHASIL":
                return "Berhasil"
            return "Pending"

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


async def get_user_progres(ids):
    data = state.get(ids, "USER_PAYMENT")
    logger.info(f"cek data: {data}")
    if not data:
        return None, None, None

    idpay = data.get("idpay")
    userid = data.get("userid")
    month = data.get("month")

    if not all([idpay, userid, month]):
        return None, None, None

    return idpay, int(userid), int(month)


async def check_payment():
    logger.info("Menjalankan auto cek payment")
    while True:
        await asyncio.sleep(10)
        try:
            data_id = await dB.get_var(BOT_ID, "PAYMENT") or []
            if not data_id:
                continue

            for ids in data_id:
                try:
                    teks = await get_receive(ids)
                    idpay, target, month = await get_user_progres(ids)

                    if None in (idpay, target, month):
                        logger.error(f"Invalid payment data for ID: {ids}")
                        data_id.remove(ids)
                        await dB.set_var(BOT_ID, "PAYMENT", data_id)
                        continue

                    if ids == idpay:
                        user = await bot.get_users(target)
                        mention = user.mention
                        userid = user.id
                        if teks == "Berhasil":
                            await add_transaction(userid, month)
                            expired = await dB.get_expired_date(userid)
                            data_id.remove(ids)
                            await dB.set_var(BOT_ID, "PAYMENT", data_id)
                            state.delete(ids, "USER_PAYMENT")
                            msg = f"""
<b><blockquote>#New Order User Added To Access!!

User: {mention}
User ID: `{userid}`

Payment ID: `{ids}`
Month: {month}

Expired at: `{expired.astimezone(waktu_jkt).strftime("%Y-%m-%d %H:%M")}`
Payment status: <u>Succesed</u>

Message: Payment has been successful, [Click here](https://saweria.co/receipt/{ids})</blockquote></b>"""
                            if userid not in AKSES_DEPLOY:
                                AKSES_DEPLOY.append(userid)
                                try:
                                    await bot.send_message(
                                        userid,
                                        f"Selamat ! Akun anda sudah memiliki akses untuk pembuatan Userbot",
                                        reply_markup=kb(
                                            [["✅ Lanjutkan Buat Userbot"]],
                                            resize_keyboard=True,
                                            one_time_keyboard=True,
                                        ),
                                    )
                                except Exception:
                                    pass
                            await bot.send_message(LOG_SELLER, msg)
                    else:
                        await bot.send_message(LOG_SELLER, f"**ERROR:** {teks}")
                except Exception as er:
                    logger.error(f"Error processing payment ID {ids}: {str(er)}")
                    data_id.remove(ids)
                    await dB.set_var(BOT_ID, "PAYMENT", data_id)
                    logger.error(f"Check_Payment error: {traceback.format_exc()}")
        except Exception as e:
            await bot.send_message(
                LOG_SELLER, f"Check_Payment error: {traceback.format_exc()}"
            )
            await bot.send_message(LOG_SELLER, f"Check_Payment error: {str(e)}")
        await asyncio.sleep(5)


async def load_user_allchats(client):
    private = []
    group = []
    globall = []
    all = []
    bots = []
    try:
        async for dialog in client.get_dialogs():
            try:
                if dialog.chat.type == enums.ChatType.PRIVATE:
                    private.append(dialog.chat.id)
                elif dialog.chat.type in (
                    enums.ChatType.GROUP,
                    enums.ChatType.SUPERGROUP,
                ):
                    group.append(dialog.chat.id)
                elif dialog.chat.type in (
                    enums.ChatType.GROUP,
                    enums.ChatType.SUPERGROUP,
                    enums.ChatType.CHANNEL,
                ):
                    globall.append(dialog.chat.id)
                elif dialog.chat.type in (
                    enums.ChatType.GROUP,
                    enums.ChatType.SUPERGROUP,
                    enums.ChatType.PRIVATE,
                ):
                    all.append(dialog.chat.id)
                if dialog.chat.type == enums.ChatType.BOT:
                    bots.append(dialog.chat.id)
            except Exception:
                continue
    except Exception:
        pass
    return private, group, globall, all, bots


async def installing_user(client):
    private, group, globall, all, bots = await load_user_allchats(client)
    client_id = client.me.id
    client._get_my_peer[client_id] = {
        "private": private,
        "group": group,
        "global": globall,
        "all": all,
        "bot": bots,
    }


async def installPeer():
    try:
        for client in zohun._ubot:
            await installing_user(client)
    except Exception as er:
        await bot.send_message(
            OWNER_ID, f"Error installPeer {str(er)}, {sys.exc_info()[-1].tb_lineno}"
        )
    await bot.send_message(OWNER_ID, "✅ Sukses Install Data Pengguna.")


async def sending_user(user_id):
    try:
        return await bot.send_message(
            user_id,
            f"<blockquote><b>Akun anda tidak dapat memberikan Respon!!\n\nHarap Hentikan Sesi Perangkat dengan nama <code>{BOT_NAME}</code>. Lalu, lakukan Re-Deploy atau klik Lanjut Pembuatan Ulang Userbot di bawah (JIKA MERASA ANDA MASIH MEMILIKI SISA WAKTU EXPIRED USERBOT).</b></blockquote>",
            reply_markup=kb(
                [["✨ Pembuatan Ulang Userbot"]],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
    except Exception:
        return


async def CheckUsers():
    while True:
        total = await dB.get_var(BOT_ID, "total_users")
        try:
            if len(zohun._ubot) != total:
                now = datetime.now(timezone("Asia/Jakarta"))
                timestamp = now.strftime("%Y-%m-%d_%H:%M")
                zip_filename = f"{BOT_NAME}_{timestamp}.zip"
                with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                    if os.path.exists(".env"):
                        env_path = os.path.abspath(".env")
                        zipf.write(env_path, os.path.basename(env_path))
                    if os.path.exists(DB_PATH):
                        zipf.write(DB_PATH, os.path.basename(DB_PATH))
                    token_path = os.path.abspath("token.json")
                    if os.path.exists(token_path):
                        zipf.write(token_path, os.path.basename(token_path))
                caption = now.strftime("%d %B %Y %H:%M")
                if LOG_BACKUP and LOG_BACKUP != 0:
                    await bot.send_document(LOG_BACKUP, zip_filename, caption=caption)
                if os.path.exists(zip_filename):
                    os.remove(zip_filename)
                return
        except Exception as e:
            if LOG_SELLER and LOG_SELLER != 0:
                try:
                    await bot.send_message(LOG_SELLER, f"CheckUsers error: {str(e)}")
                except Exception:
                    pass
            return
        await asyncio.sleep(360)


async def ExpiredUser():
    while True:
        for X in zohun._ubot:
            tokenref = await TokenReferal.create()
            try:
                wkt = datetime.now(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
                exp = await dB.get_expired_date(X.me.id)
                expir = exp.astimezone(timezone("Asia/Jakarta")).strftime(
                    "%Y-%m-%d %H:%M"
                )
                if expir == wkt:
                    msg = Message.expired_message(X)
                    await bot.send_message(LOG_SELLER, msg)
                    await X.unblock_user(bot.me.username)
                    await bot.send_message(X.me.id, msg)
                    await dB.remove_ubot(X.me.id)
                    await dB.rem_pref(X.me.id)
                    await dB.rem_expired_date(X.me.id)
                    zohun._get_my_id.remove(X.me.id)
                    await tokenref.delete_user_data(str(X.me.id))
                    zohun._ubot.remove(X)
                    await X.log_out()
                    os.execl("/bin/bash", "bash", "start.sh")
            except Exception:
                pass
                # await bot.send_message(
                #    LOG_SELLER, f"Delete user {X.me.mention}: {str(e)}"
                # )
                # tokenref.delete_user_data(str(X.me.id))
                # await dB.remove_ubot(X.me.id)
                # await dB.rem_pref(X.me.id)
                # os.execl("/bin/bash", "bash", "start.sh")
        await asyncio.sleep(1)


async def CleanAcces():
    while True:
        for org in AKSES_DEPLOY:
            try:
                seles = await dB.get_list_from_var(BOT_ID, "SELLER")
                if org not in seles:
                    AKSES_DEPLOY.remove(org)
            except Exception as e:
                await bot.send_message(LOG_SELLER, f"Clean_Accses error: {str(e)}")
        await asyncio.sleep(3600)


async def stoped_ubot(userid):
    for client in zohun._ubot:
        if client.me.id == userid:
            await dB.remove_ubot(client.me.id)
            await dB.rem_expired_date(client.me.id)
            zohun._get_my_id.remove(client.me.id)
            zohun._ubot.remove(client)
            await client.stop()
            await client.log_out()
            break


async def CheckSellerCount():
    while True:
        try:
            now = datetime.now(ZoneInfo("Asia/Jakarta"))
            last_check_str = await dB.get_var(BOT_ID, "last_check_seller")
            if last_check_str:
                last_check = datetime.fromisoformat(last_check_str).astimezone(
                    ZoneInfo("Asia/Jakarta")
                )
            else:
                last_check = now - timedelta(days=31)
            if (now - last_check).days >= 30:
                reseller_list = await dB.get_list_from_var(BOT_ID, "SELLER") or []
                for sellerid in reseller_list:

                    penjualan = int(await dB.get_var(sellerid, "penjualan") or 0)
                    if penjualan < 5:
                        logger.info(f"Hapus akses seller {sellerid}")
                        await dB.remove_from_var(BOT_ID, "SELLER", sellerid)
                    else:
                        logger.info(f"Reset data seller {sellerid}")
                        await dB.set_var(sellerid, "penjualan", 0)
                await dB.set_var(BOT_ID, "last_check_seller", now.isoformat())
            await asyncio.sleep(86400)
        except Exception as e:
            logger.error(f"[CheckSellerCount] Error: {e}")
            await asyncio.sleep(60)

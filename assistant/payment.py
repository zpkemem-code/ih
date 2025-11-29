import base64
import io
import sys
import time
import traceback

from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            ReplyKeyboardRemove, WebAppInfo)

from config import LOG_SELLER, SAWERIA_EMAIL, SAWERIA_USERID
from Zohun.database import dB, state
from Zohun.helpers import CMD, ButtonUtils, Message, Tools
from Zohun.logger import logger

last_generated_time = {}


@CMD.CALLBACK("^go_payment")
async def user_aggre(client, callback_query):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    del_ = await client.send_message(
        user_id, "<b>Please wait...</b>", reply_markup=ReplyKeyboardRemove()
    )
    await del_.delete()
    await callback_query.message.delete()
    buttons = ButtonUtils.plus_minus(0, user_id)
    return await client.send_message(
        user_id,
        Message.TEXT_PAYMENT(0, 0, 0),
        disable_web_page_preview=True,
        reply_markup=buttons,
    )


@CMD.CALLBACK("^(kurang|tambah)")
async def _(client, callback_query):
    await callback_query.answer()
    BULAN = int(callback_query.data.split()[1])
    HARGA = 25000
    QUERY = callback_query.data.split()[0]
    try:
        if QUERY == "kurang":
            if BULAN > 1:
                BULAN -= 1
                TOTAL_HARGA = HARGA * BULAN
        elif QUERY == "tambah":
            if BULAN < 12:
                BULAN += 1
                TOTAL_HARGA = HARGA * BULAN
        buttons = ButtonUtils.plus_minus(BULAN, TOTAL_HARGA)
        await callback_query.edit_message_text(
            Message.TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN),
            disable_web_page_preview=True,
            reply_markup=buttons,
        )
    except Exception:
        pass


@CMD.CALLBACK("^confirm")
async def _(client, callback_query):
    await callback_query.answer()
    amount = int(callback_query.data.split()[1])
    month = callback_query.data.split()[2]
    user_id = callback_query.from_user.id
    full = f"{callback_query.from_user.first_name}"
    await callback_query.message.delete()

    if amount == user_id:
        return await client.send_message(user_id, "<b>Harga tidak boleh kosong.</b>")
    current_time = time.time()
    if user_id in last_generated_time:
        elapsed_time = current_time - last_generated_time[user_id]
        if elapsed_time < 1800:
            remaining_time = 1800 - elapsed_time
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            await callback_query.message.reply(
                f"⚠️ Tunggu {minutes} menit {seconds} detik sebelum membuat QRIS baru."
            )
            return
    try:
        wait = await client.send_message(
            user_id, "<b>Tunggu sebentar sedang menyiapkan metode pembayaran anda!!</b>"
        )
        logger.info(f"Harga: {amount}")
        get_data = await dB.get_var(client.me.id, "PAYMENT") or []
        logger.info(f"user id: {user_id}")
        thanks = "Thank you and happy shopping"
        params = {
            "user_id": SAWERIA_USERID,
            "amount": amount,
            "name": full,
            "email": SAWERIA_EMAIL,
            "msg": thanks,
        }
        url = "https://rimzohun.vercel.app/api/saweria/createPayment"
        result = await Tools.fetch.post(url, json=params)
        if result.status_code == 200:
            response = result.json()
            data = response["data"]
            payment_info = {
                "amount": data["amount"],
                "amount_to_display": data["etc"]["amount_to_display"],
                "created_at": data["created_at"],
                "id": data["id"],
                "message": data["message"],
                "status": data["status"],
                "expired_at": data["expired_at"],
                "receipt": data["receipt"],
                "url": data["url"],
                "qr_image": data["qr_image"],
            }
            idpay = payment_info["id"]
            get_data.append(idpay)
            await dB.set_var(client.me.id, "PAYMENT", get_data)
            logger.info(f"payment id : {idpay}")
            progres = {"idpay": idpay, "userid": user_id, "month": month}
            logger.info(f"progress: {progres}")
            state.set(idpay, "USER_PAYMENT", progres)
            msg = f"""
<blockquote><b>Please scan the barcode!!

Amount: {payment_info['amount']}
Display Amount: {payment_info['amount_to_display']}

ID: `{payment_info['id']}`
Created: {payment_info['created_at']}
Status: {payment_info['status']}

Expired at: {payment_info['expired_at']}
Message: {payment_info['message']}
Check Payment Status: [Click here]({payment_info['receipt']})</b></blockquote>"""

            bahan = payment_info["qr_image"].replace("data:image/png;base64,", "")
            qr_image = io.BytesIO(base64.b64decode(bahan))
            qr_image.name = f"{payment_info['amount']}.jpg"
            # await message.reply_photo(qr_image, caption=msg)
            button = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Click Here Scan QR",
                            web_app=WebAppInfo(url=payment_info["url"]),
                        )
                    ]
                ]
            )
            await client.send_photo(user_id, qr_image, caption=msg, reply_markup=button)
            mention = (await client.get_users(user_id)).mention
            await client.send_message(
                LOG_SELLER,
                f"<b>User {mention} create payment, waiting for payment.</b>",
            )
            return await wait.delete()
        else:
            return await client.send_message(
                user_id, f"**ERROR**: {result.status_code}"
            )
    except Exception as er:
        logger.error(f"ERROR: {traceback.format_exc()}")
        logger.error(f"ERROR: {sys.exc_info()[-1].tb_lineno}")
        return await client.send_message(user_id, "<b>Please try again.</b>")

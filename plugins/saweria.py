__MODULES__ = "Saweria"
__HELP__ = """<blockquote>Command Help **Saweria** </blockquote>

<blockquote>**Saweria login**</blockquote>
    **You can login to saweria with this command**
        `{0}saweria login` (reply message with format email and password)

<blockquote>**Saweria check payment**</blockquote>
    **If you have id payment saweria, you can check with this command**
        `{0}saweria cekpay` (id payment)

<blockquote>**Saweria check balance**</blockquote>
    **You can check balance from your saweria account**
        `{0}saweria balance`

<blockquote>**Saweria create payment**</blockquote>
    **You can create a new payment with amount**
        `{0}saweria payment` (amount) 
 
<blockquote>**Note**: if you want use this feature, please login first.</blockquote>
 
<b>   {1}</b>
"""
import base64
import io

from Zohun.database import dB
from Zohun.helpers import CMD, Emoji, Tools


@CMD.UBOT("saweria")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_[4]}**")
    args = ["login", "payment", "balance", "cekpay", "transaksi"]
    command = message.command
    if len(command) < 2 or command[1] not in args:
        return await proses.edit(
            f"{em.gagal}**Please give me valid query, only supported `login`, `payment`, `balance`, and `cekpay`]**"
        )
    if command[1] == "login":
        reply = message.reply_to_message
        if not reply:
            return await proses.edit(
                f"{em.gagal}**Please reply to message with format: aku1244haha@gmail.com pasword123**"
            )
        mail, pw = Tools.parse_text(reply)
        params = {"email": mail, "password": pw}
        url = "https://rimzohun.vercel.app/api/saweria/login"
        result = await Tools.fetch.post(url, json=params)
        if result.status_code == 200:
            resp = result.json()
            msg = f"""
<blockquote>{em.sukses}**Succesfully login saweria!!

user_id: `{resp['data']['user_id']}`
token: `{resp['data']['token']}`

Please dont share this data!!**</blockquote>"""
            kwarg = {
                "email": mail,
                "pw": pw,
                "user_id": resp["data"]["user_id"],
                "token": resp["data"]["token"],
            }
            await dB.set_var(client.me.id, "SAWERIA_LOGIN", kwarg)
            return await proses.edit(msg)
        else:
            return await proses.edit(
                f"{em.gagal}**Failed to fetch data**: {result.status_code}"
            )
    elif command[1] == "balance":
        info = await dB.get_var(client.me.id, "SAWERIA_LOGIN")
        if not info:
            return await proses.edit(
                f"{em.gagal}**Please login first to check balance!!**"
            )
        mail = info["email"]
        pw = info["pw"]
        params = {"email": mail, "password": pw}
        url = "https://rimzohun.vercel.app/api/saweria/balance"
        result = await Tools.fetch.post(url, json=params)
        if result.status_code == 200:
            resp = result.json()
            msg = f"""
<blockquote>{em.sukses}**Your balance in saweria!!

Saldo Pending: `{resp['data']['pending']}`
Saldo Available: `{resp['data']['available']}`**</blockquote>"""
            return await proses.edit(msg)
        else:
            return await proses.edit(
                f"{em.gagal}**Failed to fetch data**: {result.status_code}"
            )
    elif command[1] == "cekpay":
        info = await dB.get_var(client.me.id, "SAWERIA_LOGIN")
        if not info:
            return await proses.edit(
                f"{em.gagal}**Please login first to check payment!!**"
            )
        if len(message.command) < 3:
            return await proses.edit(
                f"{em.gagal}**Please give me id payment. Example: `{message.text.split()[0]} cekpay 5f694d83-4b60-4640-a22c-1da47d224a63`**"
            )
        id_pay = message.text.split(None, 2)[2]
        url = f"https://rimzohun.vercel.app/api/saweria/checkPayment/{info['user_id']}/{id_pay}"
        result = await Tools.fetch.get(url)
        if result.status_code == 200:
            resp = result.json()
            status = resp["status"]
            teks = resp["msg"]
            msg = f"""
<b><blockquote>{em.sukses}Status Payment!!
ID: `{id_pay}`
Status: {status}
Message: {teks}</blockquote></b>"""
            return await proses.edit(msg)
        else:
            return await proses.edit(
                f"{em.gagal}**Failed to fetch data**: {result.status_code}"
            )
    elif command[1] == "payment":
        info = await dB.get_var(client.me.id, "SAWERIA_LOGIN")
        if not info:
            return await proses.edit(
                f"{em.gagal}**Please login first to make payment!!**"
            )
        if len(message.command) < 3:
            return await proses.edit(
                f"{em.gagal}**Please give me amount. Example: `{message.text.split()[0]} payment 5000`**"
            )
        reply = message.reply_to_message
        amount = reply.text.split()[0] if reply else message.text.split(None, 3)[2]
        thanks = "Thanks for payment." if not reply else reply.text.split(maxsplit=1)[1]
        email = info["email"]
        user_id = info["user_id"]
        full = f"{client.me.id}"
        params = {
            "user_id": user_id,
            "amount": amount,
            "name": full,
            "email": email,
            "msg": thanks,
        }
        url = "https://rimzohun.vercel.app/api/saweria/createPayment"
        result = await Tools.fetch.post(url, json=params)
        if result.status_code == 200:
            response = result.json()
            resp = response["data"]
            if resp:
                payment_info = {
                    "amount": resp["amount"],
                    "amount_to_display": resp["etc"]["amount_to_display"],
                    "created_at": resp["created_at"],
                    "id": resp["id"],
                    "message": resp["message"],
                    "status": resp["status"],
                    "expired_at": resp["expired_at"],
                    "receipt": resp["receipt"],
                    "url": resp["url"],
                    "qr_image": resp["qr_image"],
                }
            else:
                return await proses.edit(f"{em.gagal}**ERROR**: {resp}")
            msg = f"""
<blockquote><b>{em.sukses}Successed Generate Payment!!
Amount: {payment_info['amount']}
Display Amount: {payment_info['amount_to_display']}

ID: `{payment_info['id']}`
Created: {payment_info['created_at']}
Status: {payment_info['status']}

Expired at: {payment_info['expired_at']}
Message: {payment_info['message']}
Check Payment Status: [Click here]({payment_info['receipt']})

[Click here to pay]({payment_info['url']})</b></blockquote>"""
            bahan = payment_info["qr_image"].replace("data:image/png;base64,", "")
            qr_image = io.BytesIO(base64.b64decode(bahan))
            qr_image.name = f"{payment_info['amount']}.jpg"
            await message.reply_photo(qr_image, caption=msg)
            # if os.path.exists(qr_image):
            # os.remove(qr_image)
            return await proses.delete()
        else:
            return await proses.edit(
                f"{em.gagal}**Failed to fetch data**: {result.status_code}"
            )

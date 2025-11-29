import asyncio
import datetime

from Zohun.helpers import *

__MODULE__ = "Done"
__HELP__ = """
<blockquote> <b>Bantuan Untuk Done</b>

• <b>Perintah</b> : <code>{0}done</code> <b>[name item],[harga] [pembayaran]</b>
• <b>Penjelasan : konfirmasi pembayaran.</b></blockquote>

"""


@CMD.UBOT("done")
async def done_command(client, message):
    izzy_ganteng = await message.reply("<blockquote>memproses...</blockquote>")
    await asyncio.sleep(5)
    try:
        args = message.text.split(" ", 1)
        if len(args) < 2 or "," not in args[1]:
            await message.reply_text("<blockquote>Penggunaan: .done name item,price,payment</blockquote>")
            return

        parts = args[1].split(",", 2)

        if len(parts) < 2:
            await message.reply_text("<blockquote>Penggunaan: .done name item,price,payment</blockquote>")
            return

        name_item = parts[0].strip()
        price = parts[1].strip()
        payment = parts[2].strip() if len(parts) > 2 else "Lainnya"
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = (
            f"<blockquote>「 𝗧𝗥𝗔𝗡𝗦𝗔𝗞𝗦𝗜 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 」\n</blockquote>"
            f"<blockquote>📦 <b>barang : {name_item}</b>\n"
            f"💸 <b>nominal : {price}</b>\n"
            f"🕰️ <b>waktu : {time}</b>\n"
            f"💳 <b>payment : {payment}</b>\n</blockquote>"
            f"<blockquote>terimakasih telah order</blockquote>"
        )
        await izzy_ganteng.edit(response)

    except Exception as e:
        await izzy_ganteng.edit(f"error: {e}")
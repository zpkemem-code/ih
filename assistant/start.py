from config import LOG_SELLER, SUDO_OWNERS
from Zohun.database import dB, state
from Zohun.helpers import CMD, FILTERS, ButtonUtils, Message, Tools
from Zohun.logger import logger


async def gen_image(client):
    image = None
    file_id = await dB.get_var(client.me.id, "IMAGE_START")
    if file_id:
        image = {"photo": file_id} if file_id.startswith("AgAC") else {"video": file_id}
        return image
    return None


@CMD.BOT("setimg", FILTERS.PRIVATE)
@CMD.NLX
async def _(client, message):
    if message.reply_to_message:
        proses = await message.reply("<blockquote>**Tunggu sebentar..**</blockquote>")
        reply = message.reply_to_message
        if not reply.media:
            return await proses.edit(
                "<blockquote>**Silahkan balas ke pesan foto atau video**</blockquote>"
            )
        file_id = Tools.get_file_id(reply).get("file_id")
        await dB.set_var(client.me.id, "IMAGE_START", file_id)
        return await proses.edit(
            f"<blockquote>**Berhasil mengatur media start ke: <a href='{reply.link}'>pesan ini</a>**</blockquote>",
            disable_web_page_preview=True,
        )
    else:
        if len(message.command) == 2:
            args = message.command[1]
            if args in ["off", "disable"]:
                await dB.remove_var(client.me.id, "IMAGE_START")
                return await message.reply(
                    "<blockquote>**Media start dinon-aktifkan**</blockquote>"
                )
            else:
                return await message.reply(
                    "<blockquote>**Silahkan balas ke media jika ingin mengatur pesan start media, atau ketik `/setimg off` untuk menon-aktifkan pesan media start.**</blockquote>"
                )
        else:
            return await message.reply(
                "<blockquote>**Silahkan balas ke media jika ingin mengatur pesan start media, atau ketik `/setimg off` untuk menon-aktifkan pesan media start.**</blockquote>"
            )


@CMD.BOT("setads", FILTERS.PRIVATE)
@CMD.NLX
async def _(client, message):
    if not message.reply_to_message:
        return await message.reply("**Silahkan balas ke teks**")
    proses = await message.reply("**Tunggu sebentar..**")
    reply = message.reply_to_message
    text = reply.text or reply.caption or ""
    await dB.set_var(client.me.id, "ads", text)
    return await proses.edit(
        f"**Pesan ads berhasil diatur ke: <a href='{reply.link}'>pesan ini</a>**"
    )


@CMD.BOT("start", FILTERS.PRIVATE)
@CMD.DB_BROADCAST
async def start_home(client, message):
    image_start = await gen_image(client)
    if message.from_user.id in SUDO_OWNERS:
        buttons = ButtonUtils.start_menu(is_admin=True)
    else:
        buttons = ButtonUtils.start_menu(is_admin=False)
        sender_id = message.from_user.id
        sender_mention = message.from_user.mention
        sender_name = message.from_user.first_name
        # Send notification to LOG_SELLER with error handling
        try:
            await client.send_message(
                LOG_SELLER,
                f"<b>User: {sender_mention}\nID: `{sender_id}`\nName: {sender_name}\nHas started your bot.</b>",
            )
        except Exception as e:
            # If LOG_SELLER channel is invalid or bot doesn't have access, log to console
            logger.warning(f"Failed to send notification to LOG_SELLER: {e}")
    text = await Message.welcome_message(client, message)
    if image_start:
        if "video" in image_start:
            return await message.reply_video(
                video=image_start["video"],
                caption=text,
                reply_markup=buttons,
            )
        elif "photo" in image_start:
            return await message.reply_photo(
                photo=image_start["photo"],
                caption=text,
                reply_markup=buttons,
            )
    else:
        return await message.reply(
            text=text,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )


@CMD.BOT("button")
async def _(client, message):
    link = message.text.split(None, 1)[1]
    tujuan, _id = Tools.extract_ids_from_link(link)
    txt = state.get(message.from_user.id, "edit_reply_markup")
    teks, button = ButtonUtils.parse_msg_buttons(txt)
    if button:
        button = ButtonUtils.create_inline_keyboard(button)
    return await client.edit_message_reply_markup(
        chat_id=tujuan, message_id=_id, reply_markup=button
    )


@CMD.BOT("id")
async def _(client, message):
    if len(message.command) < 2:
        return
    query = message.text.split()[1]
    try:
        reply = message.reply_to_message
        media = Tools.get_file_id(reply)
        data = {"file_id": media["file_id"], "type": media["message_type"]}
        state.set(message.from_user.id, query, data)
        return
    except Exception as er:
        logger.error(f"{str(er)}")

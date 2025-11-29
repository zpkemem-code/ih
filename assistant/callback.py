import asyncio
import os
import sys
import traceback
from gc import get_objects
from uuid import uuid4

import requests
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton as Ikb
from pyrogram.types import (InlineKeyboardMarkup, InputMediaAnimation,
                            InputMediaAudio, InputMediaDocument,
                            InputMediaPhoto, InputMediaVideo)
from pyrogram.utils import unpack_inline_message_id

from config import API_BOTCHAX, API_MAELYN, COPY_ID, SUDO_OWNERS
from Zohun import bot, zohun
from Zohun.database import dB, state
from Zohun.helpers import (CMD, ButtonUtils, Tools, gens_font, ikb,
                          query_fonts, trigger)
from Zohun.logger import logger
from plugins.pmpermit import LIMIT

from .create_users import mari_buat_userbot
from .eval import eval_tasks, update_kode
from .help import cek_plugins
from .restart import (reset_costum_text, reset_emoji, reset_prefix,
                      restart_userbot)
from .start import start_home
from .status import cek_status_akun
from .support import pengguna_nanya
from .tokenref import referal_command, token_command

MESSAGE_DICT = {}
CONVERSATIONS = {}


@CMD.REGEX(trigger)
async def _(client, message):
    try:
        text = message.text
        if text in [
            "✨ Mulai Buat Userbot",
            "✨ Pembuatan Ulang Userbot",
            "✅ Lanjutkan Buat Userbot",
        ]:
            return await mari_buat_userbot(client, message)
        elif text == "❓ Status Akun":
            return await cek_status_akun(client, message)
        elif text.startswith("🔄 Reset"):
            data = text.split(" ")[2]
            if data == "Emoji":
                return await reset_emoji(client, message)
            elif data == "Prefix":
                return await reset_prefix(client, message)
            elif data == "Text":
                return await reset_costum_text(client, message)
        elif text == "🔄 Restart Userbot":
            return await restart_userbot(client, message)
        elif text == "🚀 Updates":
            return await update_kode(client, message)
        elif text == "🛠️ Cek Fitur":
            return await cek_plugins(client, message)
        elif text == "🤔 Pertanyaan":
            return await pengguna_nanya(client, message)
        elif text == "💬 Hubungi Admins":
            return await contact_admins(client, message)
        elif text == "↩️ Beranda":
            return await start_home(client, message)
        elif text == "🎟️ Referral":
            return await referal_command(client, message)
        elif text == "🔑 Token":
            return await token_command(client, message)
    except Exception as er:
        logger.error(f"Terjadi error: {str(er)}")


@CMD.CALLBACK("^Canceleval")
async def _(_, callback_query):
    await callback_query.answer()
    reply_message_id = callback_query.message.reply_to_message_id
    if not reply_message_id:
        return

    def cancel_task(task_id) -> bool:
        task = eval_tasks.get(task_id, None)
        if task and not task.done():
            task.cancel()
            return True
        return False

    canceled = cancel_task(reply_message_id)
    if not canceled:
        return


async def contact_admins(client, message):
    new_msg = """
<b>Dibawah ini adalah Admin Saya. Kamu dapat menghubungi salah satu dari mereka.</b>"""
    tombol = []
    row = []
    for admin in SUDO_OWNERS:
        try:
            try:
                user = await client.get_users(admin)
            except Exception:
                continue
            owner_name = user.first_name
            row.append(Ikb(owner_name, user_id=f"{user.id}"))
            if len(row) == 2:
                tombol.append(row)
                row = []
        except Exception as e:
            continue
    if row:
        tombol.append(row)
    last_row = [
        Ikb(text="❌ Tutup", callback_data="closed"),
    ]
    tombol.append(last_row)

    markup = InlineKeyboardMarkup(tombol)
    return await message.reply(new_msg, reply_markup=markup)


@CMD.CALLBACK("^close")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        user = callback_query.from_user
        split = callback_query.data.split(maxsplit=1)[1]
        # logger.info(f"ini split {split}")
        data = state.get(user.id, split)
        # logger.info(f"ini data {data}")
        if not data:
            return await callback_query.answer("This button not for you fvck!!", True)
        message = next(
            (obj for obj in get_objects() if id(obj) == int(data["idm"])), None
        )
        c = message._client
        state.clear_client(c.me.id)
        return await c.delete_messages(int(data["chat"]), int(data["_id"]))
    except Exception as er:
        logger.error(f"{str(er)}")


@CMD.CALLBACK("^cb_pm")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        data = callback_query.data.split()
        user = callback_query.from_user.id
        maling = int(data[3])
        polisi = int(data[2])
        pm_ok = await dB.get_list_from_var(polisi, "PM_OKE")
        if data[1] == "ok":
            if user != polisi:
                return await callback_query.answer(
                    "This button not for you fvck!!", True
                )
            if maling not in pm_ok:
                await dB.add_to_var(polisi, "PM_OKE", maling)
                return await callback_query.edit_message_text(
                    "<b>User has been approved to send message.</b>"
                )
            else:
                return await callback_query.edit_message_text(
                    "<b>This user is already approved</b>"
                )
        elif data[1] == "no":
            if user != polisi:
                return await callback_query.answer(
                    "This button not for you fvck!!", True
                )
            if maling in pm_ok:
                await dB.remove_from_var(polisi, "PM_OKE", maling)
                return await callback_query.edit_message_text(
                    "<b>User has been disapproved to send message.</b>"
                )
            else:
                return await callback_query.edit_message_text(
                    "<b>This user is already disapproved</b>"
                )
        elif data[1] == "warn":
            Flood = state.get(polisi, maling)
            pm_warns = await dB.get_var(polisi, "PMLIMIT") or LIMIT
            return await callback_query.answer(
                f"⚠️ You have a chance {Flood}/{pm_warns} ❗\n\nIf you insist on sending messages continuously then you will be ⛔ blocked automatically and we will 📢 report your account as spam",
                True,
            )
    except Exception as er:
        logger.error(f"ERROR: {str(er)}, line: {sys.exc_info()[-1].tb_lineno}")


@CMD.CALLBACK("^getbio_")
async def _(client, callback_query):
    getid = int(callback_query.data.split("_")[1])
    data = state.get(getid, "bio")
    if not data:
        return await callback_query.answer("Bio not found", True)
    return await callback_query.answer(data, True)


@CMD.CALLBACK("^cb_gc_info")
async def _(client, callback_query):
    await callback_query.answer()
    cek = state.get(client.me.id, "gc_info")
    state.set(client.me.id, "desc_gc", cek)
    usr = cek["username"]
    if usr is None:
        keyb = ikb([[("Desc", f"cb_desc {cek['id']}", "callback_data")]])
    else:
        keyb = ikb(
            [
                [
                    ("Chat", f"https://t.me/{usr}", "url"),
                    ("Desc", f"cb_desc {cek['id']}", "callback_data"),
                ]
            ]
        )
    cdesc = cek["desc"]
    if cdesc is None:
        pass
    else:
        pass
    msg = f"""
<b>ChatInfo:</b>
   <b>name:</b> <b>{cek['name']}</b>
      <b>id:</b> <code>{cek['id']}</code>
      <b>type:</b> <b>{cek['type']}</b>
      <b>dc_id:</b> <b>{cek['dc_id']}</b>
      <b>username:</b> <b>@{cek['username']}</b>
      <b>member:</b> <b>{cek['member']}</b>
      <b>protect:</b> <b>{cek['protect']}</b>
"""
    return await callback_query.edit_message_text(msg, reply_markup=keyb)


@CMD.CALLBACK("^cb_desc")
async def _(client, callback_query):
    await callback_query.answer()
    query = callback_query.data.split(None, 1)
    id_gc = query[1]
    data = state.get(client.me.id, "gc_info")
    if int(id_gc) == int(data["id"]):
        return await callback_query.answer(f"{data['desc']}", True)
    else:
        return await callback_query.answer("Tidak ada perasaan ini", True)


@CMD.CALLBACK("^copymsg")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id = int(callback_query.data.split("_", 1)[1])
        message = [obj for obj in get_objects() if id(obj) == get_id][0]
        await message._client.unblock_user(bot.me.username)
        await callback_query.edit_message_text("<b>Proses Upload...</b>")
        copy = await message._client.send_message(
            bot.me.username, f"/kontol {message.text.split()[1]}"
        )
        msg = message.reply_to_message or message
        await asyncio.sleep(1.5)
        await copy.delete()
        async for get in message._client.search_messages(bot.me.username, limit=1):
            await message._client.copy_message(
                message.chat.id, bot.me.username, get.id, reply_to_message_id=msg.id
            )
            await message._client.delete_messages(
                message.chat.id, COPY_ID[message._client.me.id]
            )
            await get.delete()
    except Exception as error:
        await callback_query.edit_message_text(f"**ERROR:** <code>{error}</code>")


async def close_user(callback_query, user_id):
    pass


@CMD.CALLBACK("^cb")
async def _(client, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    btn_close = state.get("close_notes", "get_note")
    dia = callback_query.from_user
    type_mapping = {
        "photo": InputMediaPhoto,
        "video": InputMediaVideo,
        "animation": InputMediaAnimation,
        "audio": InputMediaAudio,
        "document": InputMediaDocument,
    }
    try:
        notetag = data[-2].replace("cb_", "")
        gw = data[-1]
        item = [x for x in zohun._ubot if int(gw) == x.me.id]
        noteval = await dB.get_var(int(gw), notetag, "notes")

        if not noteval:
            await callback_query.answer("Catatan tidak ditemukan.", True)
            return

        full = (
            f"<a href=tg://user?id={dia.id}>{dia.first_name} {dia.last_name or ''}</a>"
        )
        await dB.add_userdata(
            dia.id,
            dia.first_name,
            dia.last_name,
            dia.username,
            dia.mention,
            full,
            dia.id,
        )

        for me in item:
            tks = noteval["result"].get("text")
            note_type = noteval["type"]
            file_id = noteval.get("file_id")
            note, button = ButtonUtils.parse_msg_buttons(tks)
            teks = await Tools.escape_tag(bot, dia.id, note, Tools.parse_words)
            button = ButtonUtils.create_inline_keyboard(button, int(gw))
            for row in btn_close.inline_keyboard:
                button.inline_keyboard.append(row)
            try:
                if note_type == "text":
                    await callback_query.edit_message_text(
                        text=teks, reply_markup=button
                    )

                elif note_type in type_mapping and file_id:
                    InputMediaType = type_mapping[note_type]
                    media = InputMediaType(media=file_id, caption=teks)
                    await callback_query.edit_message_media(
                        media=media, reply_markup=button
                    )

                else:
                    await callback_query.edit_message_caption(
                        caption=teks, reply_markup=button
                    )

            except FloodWait as e:
                return await callback_query.answer(
                    f"FloodWait {e}, Please Waiting!!", True
                )
            except MessageNotModified:
                pass

    except Exception as e:
        print(f"Error in notes callback: {str(e)}")
        return await callback_query.answer(
            "Terjadi kesalahan saat memproses catatan.", True
        )


@CMD.CALLBACK("^get_font")
async def _(_, callback_query):
    await callback_query.answer()
    try:
        data = int(callback_query.data.split()[1])
        new = str(callback_query.data.split()[2])
        text = state.get(data, "FONT")
        get_new_font = gens_font(new, text)
        await callback_query.answer("Wait a minute!!", True)
        return await callback_query.edit_message_text(
            f"<b>Result:\n<code>{get_new_font}</code></b>"
        )
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^prev_font")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id, current_batch = map(int, callback_query.data.split()[1:])
        prev_batch = current_batch - 1

        if prev_batch < 0:
            prev_batch = len(query_fonts) - 1

        keyboard = ButtonUtils.create_font_keyboard(
            query_fonts[prev_batch], get_id, prev_batch
        )

        buttons = InlineKeyboardMarkup(keyboard)
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^next_font")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id, current_batch = map(int, callback_query.data.split()[1:])
        next_batch = current_batch + 1

        if next_batch >= len(query_fonts):
            next_batch = 0

        keyboard = ButtonUtils.create_font_keyboard(
            query_fonts[next_batch], get_id, next_batch
        )

        buttons = InlineKeyboardMarkup(keyboard)
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^refresh_cat")
async def _(client, callback_query):

    await callback_query.answer("Please wait a minute", True)
    buttons = ikb([[("Refresh cat", "refresh_cat")], [("Close", "close inline_cat")]])
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            await callback_query.edit_message_animation(
                cat_url,
                caption="<blockquote><b>Meow 😽</b></blockquote>",
                reply_markup=buttons,
            )
        else:
            await callback_query.edit_message_media(
                InputMediaPhoto(
                    media=cat_url, caption="<blockquote><b>Meow 😽</b></blockquote>"
                ),
                reply_markup=buttons,
            )
    else:
        await callback_query.edit_message_text("Failed to refresh cat picture 🙀")


@CMD.CALLBACK("^prev_textpro")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id, current_batch = map(int, callback_query.data.split()[1:])
        prev_batch = current_batch - 1

        if prev_batch < 0:
            prev_batch = len(Tools.query_textpro) - 1

        keyboard = ButtonUtils.create_buttons_textpro(
            Tools.query_textpro[prev_batch], get_id, prev_batch
        )

        buttons = InlineKeyboardMarkup(keyboard)
        state.set(get_id, "page_textpro", prev_batch)
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^next_textpro")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id, current_batch = map(int, callback_query.data.split()[1:])
        next_batch = current_batch + 1

        if next_batch >= len(Tools.query_textpro):
            next_batch = 0

        keyboard = ButtonUtils.create_buttons_textpro(
            Tools.query_textpro[next_batch], get_id, next_batch
        )

        buttons = InlineKeyboardMarkup(keyboard)
        state.set(get_id, "page_textpro", next_batch)
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^genpro")
async def _(client, callback_query):
    await callback_query.answer()
    await callback_query.answer("Wait a minute!!", True)
    query = callback_query.data.split()
    userid = int(query[1])
    command = str(query[2])
    text = state.get(userid, "TEXT_PRO")
    result_image = await Tools.gen_text_pro(text, command)
    page = state.get(userid, "page_textpro")
    keyboard = ButtonUtils.create_buttons_textpro(
        Tools.query_textpro[0], userid, current_batch=int(page)
    )
    buttons = InlineKeyboardMarkup(keyboard)
    if not result_image.startswith("ERROR"):
        logger.info(f"Result TextPro: {result_image}")
        try:
            image = InputMediaPhoto(
                media=result_image,
                caption=f"<blockquote>**Costum text:**\n\n{text}</blockquote>",
            )
            await callback_query.edit_message_media(media=image, reply_markup=buttons)
        except Exception as e:

            logger.error(f"Line 656: {traceback.format_exc()}")
            await callback_query.edit_message_text(f"Failed to send image: {str(e)}")
    else:
        logger.error(f"Line 659: {traceback.format_exc()}")
        await callback_query.edit_message_text(
            f"Failed to generate text pro:\n{result_image}"
        )


@CMD.CALLBACK("^nxttsearch")
async def _(_, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    userid = int(data[2])
    page = int(data[1])
    uniq = str(data[3])
    videos = state.get(userid, uniq)
    if videos is None:
        await callback_query.answer("Tidak ada halaman berikutnya.", show_alert=True)
        return
    await callback_query.answer()
    buttons = []
    for video in videos[page * 5 : (page + 1) * 5]:
        title = video["title"]
        video_link = video["play"]
        caption = f"<blockquote>{title}</blockquote>"

    if page > 0:
        buttons.append(
            [
                Ikb(
                    "Prev video", callback_data=f"nxttsearch_{page - 1}_{userid}_{uniq}"
                ),
                Ikb(
                    "Next video", callback_data=f"nxttsearch_{page + 1}_{userid}_{uniq}"
                ),
            ]
        )
        buttons.append([Ikb("Close", callback_data=f"close inline_ttsearch {uniq}")])
    else:
        buttons.append(
            [
                Ikb(
                    "Next video", callback_data=f"nxttsearch_{page + 1}_{userid}_{uniq}"
                ),
            ]
        )
        buttons.append([Ikb("Close", callback_data=f"close inline_ttsearch {uniq}")])
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_media(
        media=InputMediaVideo(
            media=video_link,
            caption=caption,
        ),
        reply_markup=reply_markup,
    )


@CMD.CALLBACK("^cqtiktok")
async def _(client, callback_query):
    await callback_query.answer()

    try:
        data = callback_query.data.split("_")
        userid = int(data[2])
        query = str(data[1])
        results = state.get(userid, "result_ttdownload")
        get_id = state.get(userid, "idm_ttdownload")
        message = [obj for obj in get_objects() if id(obj) == get_id][0]
        name = f"{str(uuid4())}"
        if query == "videodl":
            video_link = results["video"][0]
            caption = results["title"]
            logger.info(f"Video tiktok link: {video_link}")
            await callback_query.edit_message_text(
                "**Please wait, trying to send the video...**"
            )
            video = f"downloads/{name.split('-')[1]}.mp4"
            await Tools.bash(f"curl -L {video_link} -o {video}")
            await message.reply_video(video, caption=caption)
            if os.path.exists(video):
                os.remove(video)
            await asyncio.sleep(2)
            ids = (unpack_inline_message_id(callback_query.inline_message_id)).id
            return await message._client.delete_messages(message.chat.id, ids)
        elif query == "audiodl":
            audio_link = results["audio"][0]
            caption = results["title"]
            logger.info(f"Audio tiktok link: {audio_link}")
            await callback_query.edit_message_text(
                "**Please wait, trying to send the audio...**"
            )
            audio = f"downloads/{name.split('-')[1]}.mp3"
            await Tools.bash(f"curl -L {audio_link} -o {audio}")
            await message.reply_audio(audio, caption=caption)
            await asyncio.sleep(2)
            if os.path.exists(audio):
                os.remove(audio)
            ids = (unpack_inline_message_id(callback_query.inline_message_id)).id
            return await message._client.delete_messages(message.chat.id, ids)
    except Exception as er:
        logger.error(f"Cq tiktok dl: {traceback.format_exc()}")
        return await callback_query.edit_message_text(f"**An errror:** {str(er)}")


@CMD.CALLBACK("^nxtspotify")
async def _(_, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    userid = int(data[2])
    page = int(data[1])
    uniq = str(data[3])
    audios = state.get(userid, uniq)
    if audios is None:
        await callback_query.answer("Tidak ada halaman berikutnya.", show_alert=True)
        return
    await callback_query.answer()
    buttons = []
    for audio in audios[page * 5 : (page + 1) * 5]:
        caption = f"""<blockquote>
🎶 **Title:** {audio['title']}
👥 **Popularity:** {audio['popularity']}
⏳ **Duration:** {audio['duration']}
🖇️ **Spotify URL:** <a href='{audio['url']}'>here</a></blockquote>"""
        state.set(userid, "fordlspotify", audio["url"])
        logger.info(f"Url line 796: {audio['url']}")
    buttons.append([Ikb("Download audio", callback_data=f"dlspot_{userid}_{uniq}")])
    if page > 0:
        buttons.append(
            [
                Ikb(
                    "Prev audio", callback_data=f"nxtspotify_{page - 1}_{userid}_{uniq}"
                ),
                Ikb(
                    "Next audio", callback_data=f"nxtspotify_{page + 1}_{userid}_{uniq}"
                ),
            ]
        )
        buttons.append([Ikb("Close", callback_data=f"close inline_spotify {uniq}")])
    else:
        buttons.append(
            [
                Ikb(
                    "Next audio", callback_data=f"nxtspotify_{page + 1}_{userid}_{uniq}"
                ),
            ]
        )
        buttons.append([Ikb("Close", callback_data=f"close inline_spotify {uniq}")])
    # state.set(userid, "fordlspotify", audio["url"])
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_text(
        caption, reply_markup=reply_markup, disable_web_page_preview=True
    )


@CMD.CALLBACK("^dlspot")
async def _(_, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    userid = int(data[1])
    uniq = str(data[2])
    data = state.get(userid, uniq)
    get_id = state.get(userid, "idm_spotdl")
    message = [obj for obj in get_objects() if id(obj) == get_id][0]
    link = data[0]["url"]
    audio, caption = await Tools.download_spotify(link)
    await callback_query.edit_message_text(
        "**Please wait, trying to send the audio...**"
    )
    await message.reply_audio(audio, caption=caption)
    await asyncio.sleep(2)
    ids = (unpack_inline_message_id(callback_query.inline_message_id)).id
    if os.path.exists(audio):
        os.remove(audio)
    try:
        return await message._client.delete_messages(
            message.chat.id,
            ids,
        )
    except Exception:
        logger.error(f"Cant delete inline_message_id: {traceback.format_exc()}")


@CMD.CALLBACK("^nxpinsearch")
async def _(_, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    page = int(data[1])
    uniq = str(data[2])
    photos = state.get(uniq, uniq)

    if not photos:
        await callback_query.answer(
            "Tidak ada foto untuk ditampilkan.", show_alert=True
        )
        return

    total_photos = len(photos)

    if page < 0 or page >= total_photos:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return

    buttons = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            Ikb("⬅️ Prev", callback_data=f"nxpinsearch_{page - 1}_{uniq}")
        )
    if page < total_photos - 1:
        nav_buttons.append(
            Ikb("➡️ Next", callback_data=f"nxpinsearch_{page + 1}_{uniq}")
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([Ikb("❌ Close", callback_data=f"close inline_pinsearch {uniq}")])

    reply_markup = InlineKeyboardMarkup(buttons)

    await callback_query.edit_message_media(
        media=InputMediaPhoto(media=photos[page]), reply_markup=reply_markup
    )


@CMD.CALLBACK("^bola_date")
async def _(client, callback_query):
    await callback_query.answer()
    split = callback_query.data.split()
    if len(split) > 1:
        state_key = split[1]
        stored_data = state.get(state_key, state_key)

        buttons = []
        temp_row = []
        for liga_date in stored_data:
            button = Ikb(
                text=liga_date["LigaDate"],
                callback_data=f"bola_matches {state_key} {liga_date['LigaDate']}",
            )
            temp_row.append(button)

            if len(temp_row) == 3:
                buttons.append(temp_row)
                temp_row = []

        if temp_row:
            buttons.append(temp_row)

        buttons.append([Ikb(text="Close", callback_data="close inline_bola")])
        keyboard = InlineKeyboardMarkup(buttons)

        return await callback_query.edit_message_text(
            text="<b>Select a date to view football matches:</b>",
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
    else:
        return await callback_query.edit_message_text("No data found.")


@CMD.CALLBACK("^bola_matches")
async def _(client, callback_query):
    await callback_query.answer()
    split = callback_query.data.split()
    if len(split) > 2:
        state_key = split[1]
        selected_date = split[2]
        stored_data = state.get(state_key, state_key)

        date_matches = next(
            (
                date
                for date in stored_data
                if date["LigaDate"].split()[0] == selected_date.split()[0]
            ),
            None,
        )

        if date_matches:
            text = f"Football Matches on {selected_date}\n\n"
            for league in date_matches["LigaItem"]:
                text += f"🏆 {league['NameLiga']}\n"
                for match in league["Match"]:
                    text += f"⚽ {match['team']} at {match['time']}\n"

            buttons = [
                [Ikb(text="« Back", callback_data=f"bola_date {state_key}")],
                [Ikb(text="Close", callback_data="close inline_bola")],
            ]
            keyboard = InlineKeyboardMarkup(buttons)

            return await callback_query.edit_message_text(
                text=f"<blockquote><b>{text}</b></blockquote>",
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
        else:
            return await callback_query.answer("Silahkan ulangi fitur bola!!", True)


@CMD.CALLBACK("^restanime_")
async def _(client, callback_query):
    data = callback_query.data.split("_")
    page = int(data[1])
    uniq = str(data[2])
    berita = state.get(uniq, uniq)
    if not berita:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    total_photos = len(berita)
    if page < 0 or page >= total_photos:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    buttons = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(Ikb("⬅️ Prev", callback_data=f"restanime_{page - 1}_{uniq}"))
    if page < total_photos - 1:
        nav_buttons.append(Ikb("➡️ Next", callback_data=f"restanime_{page + 1}_{uniq}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([Ikb("❌ Close", callback_data=f"close inline_anime {uniq}")])
    title = berita[page].get("title")
    episode = berita[page].get("episode")
    date = Tools.jakartaTime(berita[page].get("updatedAt", "-"))
    url = berita[page].get("url")
    judul = f"**Title:** {title}\n**Episode:** {episode}\n**Link:** {url}\n**Uploaded:** {date}"
    await Tools.bash(f"wget {berita[page].get('thumbnail')} -O {uniq}.jpg")
    thumb = await Tools.upload_thumb(f"{uniq}.jpg")
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_media(
        media=InputMediaPhoto(media=thumb, caption=judul),
        reply_markup=reply_markup,
    )


@CMD.CALLBACK("^restdonghua_")
async def _(client, callback_query):
    data = callback_query.data.split("_")
    page = int(data[1])
    uniq = str(data[2])
    berita = state.get(uniq, uniq)
    if not berita:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    total_photos = len(berita)
    if page < 0 or page >= total_photos:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    buttons = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            Ikb("⬅️ Prev", callback_data=f"restdonghua_{page - 1}_{uniq}")
        )
    if page < total_photos - 1:
        nav_buttons.append(
            Ikb("➡️ Next", callback_data=f"restdonghua_{page + 1}_{uniq}")
        )
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([Ikb("❌ Close", callback_data=f"close inline_donghua {uniq}")])
    title = berita[page].get("title")
    episode = berita[page].get("episode")
    date = Tools.jakartaTime(berita[page].get("updatedAt", "-"))
    url = berita[page].get("url")
    judul = f"**Title:** {title}\n**Episode:** {episode}\n**Link:** {url}\n**Uploaded:** {date}"
    await Tools.bash(f"wget {berita[page].get('thumbnail')} -O {uniq}.jpg")
    thumb = await Tools.upload_thumb(f"{uniq}.jpg")
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_media(
        media=InputMediaPhoto(media=thumb, caption=judul),
        reply_markup=reply_markup,
    )


@CMD.CALLBACK("^restcomic_")
async def _(client, callback_query):
    data = callback_query.data.split("_")
    page = int(data[1])
    uniq = str(data[2])
    berita = state.get(uniq, uniq)
    if not berita:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    total_photos = len(berita)
    if page < 0 or page >= total_photos:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    buttons = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(Ikb("⬅️ Prev", callback_data=f"restcomic_{page - 1}_{uniq}"))
    if page < total_photos - 1:
        nav_buttons.append(Ikb("➡️ Next", callback_data=f"restcomic_{page + 1}_{uniq}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([Ikb("❌ Close", callback_data=f"close inline_comic {uniq}")])
    title = berita[page].get("title")
    chapter = berita[page].get("chapters", [{}])[0]
    episode = chapter.get("title", "-")
    date = chapter.get("date", "-")
    chapter_url = chapter.get("url", "")
    if "https://komiku.id" in chapter_url and not chapter_url.startswith(
        "https://komiku.id/"
    ):
        chapter_url = chapter_url.replace("https://komiku.id", "https://komiku.id/")
    target = berita[page].get("cover")
    await Tools.bash(f"wget {target} -O {uniq}.jpg")
    thumb = await Tools.upload_thumb(f"{uniq}.jpg")
    judul = f"**Title:** {title}\n**Chapters:** {episode}\n**Link:** {chapter_url}\n**Uploaded:** {date}"
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_media(
        media=InputMediaPhoto(media=thumb, caption=judul),
        reply_markup=reply_markup,
    )


@CMD.CALLBACK("^gnews_")
async def _(client, callback_query):
    data = callback_query.data.split("_")
    page = int(data[1])
    uniq = str(data[2])
    berita = state.get(uniq, uniq)
    if not berita:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    total_photos = len(berita)
    if page < 0 or page >= total_photos:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    buttons = []
    nav_buttons = []
    buttons.append([Ikb("📮 Link", url=f"{berita[page].get('link')}")])
    if page > 0:
        nav_buttons.append(Ikb("⬅️ Prev", callback_data=f"gnews_{page - 1}_{uniq}"))
    if page < total_photos - 1:
        nav_buttons.append(Ikb("➡️ Next", callback_data=f"gnews_{page + 1}_{uniq}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([Ikb("❌ Close", callback_data=f"close inline_gnews {uniq}")])
    title = berita[page].get("title")
    source = berita[page].get("source")
    date = Tools.jakartaTime(berita[page].get("datetime", "-"))
    time = berita[page].get("time")
    arType = berita[page].get("topicFeatured")
    thumb = berita[page].get("image")
    judul = f"""
**Title:** {title}
**Source:** {source}
**Uploaded:** {date}
**Time:** {time}
**articleType:** {arType}"""
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_media(
        media=InputMediaPhoto(media=thumb, caption=judul),
        reply_markup=reply_markup,
    )


@CMD.CALLBACK("^news_")
async def _(client, callback_query):
    data = callback_query.data.split("_")
    page = int(data[1])
    uniq = str(data[2])
    berita = state.get(uniq, uniq)
    if not berita:
        await callback_query.answer(
            "Tidak ada berita untuk ditampilkan.", show_alert=True
        )
        return
    total_photos = len(berita)
    if page < 0 or page >= total_photos:
        await callback_query.answer("Halaman tidak ditemukan.", show_alert=True)
        return
    buttons = []
    nav_buttons = []
    buttons.append([Ikb("📮 Link", url=f"{berita[page]['berita_url']}")])
    if page > 0:
        nav_buttons.append(Ikb("⬅️ Prev", callback_data=f"news_{page - 1}_{uniq}"))
    if page < total_photos - 1:
        nav_buttons.append(Ikb("➡️ Next", callback_data=f"news_{page + 1}_{uniq}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([Ikb("❌ Close", callback_data=f"close inline_news {uniq}")])
    title = berita[page]["berita"]
    date = berita[page].get("berita_diupload", "-")
    thumb = berita[page]["berita_thumb"]
    judul = f"""
**Title:** {title}
**Uploaded:** {date}"""
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_media(
        media=InputMediaPhoto(media=thumb, caption=judul),
        reply_markup=reply_markup,
    )


@CMD.CALLBACK("^selectmodel_")
async def _(client, query):
    uniq = str(query.data.split("_")[1])
    msg = "**Please choose model for AI:**"
    buttons = ikb(
        [
            [
                ("ChatGpt", f"chatai_chatgpt_{uniq}"),
                ("DeepSeek", f"chatai_deepseek_{uniq}"),
            ],
            [
                ("Gemini", f"chatai_gemini_{uniq}"),
                ("BlackBox", f"chatai_blackbox_{uniq}"),
            ],
        ]
    )
    return await query.edit_message_text(msg, reply_markup=buttons)


@CMD.CALLBACK("^chatai_")
async def _(client, query):
    model = query.data.split("_")[1]
    uniq = query.data.split("_")[2]
    if model == "chatgpt":
        return await chatai_with_chatgpt(client, query, uniq)
    elif model == "gemini":
        return await chatai_with_gemini(client, query, uniq)
    elif model == "deepseek":
        return await chatai_with_deepseek(client, query, uniq)
    elif model == "blackbox":
        return await chatai_with_blackbox(client, query, uniq)


async def chatai_with_deepseek(client, query, uniq):
    data = state.get(uniq, uniq)
    if not data:
        return await query.answer(
            "Data not found, please create new conversation.", True
        )
    question = data["prompt"]
    get_id = data["idm"]
    message = [obj for obj in get_objects() if id(obj) == get_id][0]
    chat_id = message.chat.id
    user_id = message.from_user.id
    ids = (unpack_inline_message_id(query.inline_message_id)).id
    try:
        await message._client.delete_messages(
            message.chat.id,
            ids,
        )
    except Exception:
        logger.error(traceback.format_exc())
    if user_id not in CONVERSATIONS:
        CONVERSATIONS[user_id] = []
    while True:
        try:
            headers = {"mg-apikey": API_MAELYN}
            params = {
                "q": question,
                "roleplay": "Kamu adalah asisten paling canggih yang berbahasa Indonesia gaul, dan jangan gunakan bahasa inggris sebelum saya memulai duluan",
                "uuid": chat_id,
            }
            url = "https://api.maelyn.tech/api/deepseek/chat"
            r = await Tools.fetch.get(url, headers=headers, params=params)
            CONVERSATIONS[user_id].append(question)
            if r.status_code == 200:
                result = r.json()["result"].get("content")
                CONVERSATIONS[user_id].append(result)
                if len(CONVERSATIONS[user_id]) > 20:
                    CONVERSATIONS[user_id] = (
                        CONVERSATIONS[user_id][:2] + CONVERSATIONS[user_id][-18:]
                    )
                if len(result) > 4096:
                    with open(f"{question.split()[1]}.txt", "wb") as file:
                        file.write(result.encode("utf-8"))
                    reply = await message._client.send_document(
                        chat_id, f"{question.split()[1]}.txt"
                    )
                    next_message = await message._client.ask(
                        chat_id,
                        f"**<u>Chat with DeepSeek</u>**\n<b>Question:</b>\n<blockquote>{question}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                        reply_to_message_id=reply.id,
                        timeout=300,
                    )
                else:
                    next_message = await message._client.ask(
                        chat_id,
                        f"<b><u>Chat with DeepSeek</u></b>\n<b>Question:\n<blockquote>{question}</blockquote>\n\nAnswer:\n</b><blockquote>{result}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                    )
                if next_message.text.lower() == "stopped ask":
                    del CONVERSATIONS[user_id]
                    await next_message.reply(f"**Conversation ended.**")
                    break
                question = next_message.text
            else:
                return await message.reply("<b>Please try again later..</b>")
        except Exception:
            logger.error(traceback.format_exc())
            return await message.reply("<b>Please try again later..</b>")


async def chatai_with_blackbox(client, query, uniq):
    data = state.get(uniq, uniq)
    if not data:
        return await query.answer(
            "Data not found, please create new conversation.", True
        )
    prompt = data["prompt"]
    get_id = data["idm"]
    message = [obj for obj in get_objects() if id(obj) == get_id][0]
    chat_id = message.chat.id
    user_id = message.from_user.id
    ids = (unpack_inline_message_id(query.inline_message_id)).id
    try:
        await message._client.delete_messages(
            message.chat.id,
            ids,
        )
    except Exception:
        logger.error(traceback.format_exc())
    if user_id not in CONVERSATIONS:
        CONVERSATIONS[user_id] = []
    BLACKBOX_CHAT_URL = "https://api.maelyn.tech/api/blackbox/chat"
    BLACKBOX_IMAGE_URL = "https://api.maelyn.tech/api/blackbox/image"
    BLACKBOX_IMAGINE_URL = "https://api.maelyn.tech/api/blackbox/imagine"
    while True:
        try:
            headers = {"mg-apikey": API_MAELYN}
            if message.reply_to_message and message.reply_to_message.photo:
                photo_url = await Tools.upload_media(message)
                params = {"url": photo_url, "q": prompt}
                CONVERSATIONS[user_id].append(prompt)
                r = await Tools.fetch.get(
                    BLACKBOX_IMAGE_URL, headers=headers, params=params
                )
                data = r.json()
                next_message = await message._client.ask(
                    chat_id,
                    f"**<u>Chat with BlackBox</u>**\n<b>Question:</b>\n<blockquote>{prompt}</blockquote>\n\nAnswer:\n</b><blockquote>{data.get('result')}</blockquote>\n\n**Type** `stopped ask` **to end the conversation.**",
                    timeout=300,
                )
                CONVERSATIONS[user_id].append(data.get("result"))
                if next_message.text.lower() == "stopped ask":
                    del CONVERSATIONS[user_id]
                    await next_message.reply(f"**Conversation ended.**")
                    break
                prompt = next_message.text
            elif prompt.lower().startswith("generate "):
                prompt = prompt[9:].strip()
                params = {"prompt": prompt}
                r = await Tools.fetch.get(
                    BLACKBOX_IMAGINE_URL, headers=headers, params=params
                )
                CONVERSATIONS[user_id].append(prompt)
                data = r.json()
                img_url = data["result"]["url"]
                await message._client.send_photo(chat_id, img_url)
                next_message = await message._client.ask(
                    chat_id,
                    f"**<u>Chat with BlackBox</u>**\n<b>Question:</b>\n<blockquote>{prompt}</blockquote>\n\n**Generated by BlackBox**\n\n**Type** `stopped ask` **to end the conversation.**",
                    timeout=300,
                )
                CONVERSATIONS[user_id].append(img_url)
                if next_message.text.lower() == "stopped ask":
                    del CONVERSATIONS[user_id]
                    await next_message.reply(f"**Conversation ended.**")
                    break
                prompt = next_message.text
            else:
                CONVERSATIONS[user_id].append(prompt)
                params = {"q": prompt}
                r = await Tools.fetch.get(
                    BLACKBOX_CHAT_URL, headers=headers, params=params
                )
                data = r.json()
                CONVERSATIONS[user_id].append(data.get("result"))
                if len(CONVERSATIONS[user_id]) > 20:
                    CONVERSATIONS[user_id] = (
                        CONVERSATIONS[user_id][:2] + CONVERSATIONS[user_id][-18:]
                    )
                result = data.get("result")
                if len(result) > 4096:
                    with open(f"{prompt.split()[1]}.txt", "wb") as file:
                        file.write(result.encode("utf-8"))
                    reply = await message._client.send_document(
                        chat_id, f"{prompt.split()[1]}.txt"
                    )
                    next_message = await message._client.ask(
                        chat_id,
                        f"**<u>Chat with BlackBox</u>**\n<b>Question:</b>\n<blockquote>{prompt}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                        reply_to_message_id=reply.id,
                        timeout=300,
                    )
                else:
                    next_message = await message._client.ask(
                        chat_id,
                        f"<b><u>Chat with BlackBox</u></b>\n<b>Question:\n<blockquote>{prompt}</blockquote>\n\nAnswer:\n</b><blockquote>{result}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                    )
                if next_message.text.lower() == "stopped ask":
                    del CONVERSATIONS[user_id]
                    await next_message.reply(f"**Conversation ended.**")
                    break
                prompt = next_message.text
        except Exception:
            logger.error(traceback.format_exc())
            return await message.reply("<b>Please try again later..</b>")


async def chatai_with_gemini(client, query, uniq):
    data = state.get(uniq, uniq)
    if not data:
        return await query.answer(
            "Data not found, please create new conversation.", True
        )
    question = data["prompt"]
    get_id = data["idm"]
    message = [obj for obj in get_objects() if id(obj) == get_id][0]
    chat_id = message.chat.id
    user_id = message.from_user.id
    ids = (unpack_inline_message_id(query.inline_message_id)).id
    try:
        await message._client.delete_messages(
            message.chat.id,
            ids,
        )
    except Exception:
        logger.error(traceback.format_exc())
    if user_id not in CONVERSATIONS:
        CONVERSATIONS[user_id] = []
    GEMINI_IMAGE_URL = "https://api.maelyn.tech/api/gemini/image"
    GEMINI_CHAT = f"https://api.maelyn.tech/api/gemini/chat"
    headers = {"mg-apikey": API_MAELYN}
    while True:
        if message.reply_to_message and message.reply_to_message.photo:
            photo_url = await Tools.upload_media(message)
            params = {"url": photo_url, "q": question}
            CONVERSATIONS[user_id].append(question)
            try:
                r = await Tools.fetch.get(
                    GEMINI_IMAGE_URL, headers=headers, params=params
                )
                data = r.json()
                next_message = await message._client.ask(
                    chat_id,
                    f"{data.get('result')}\n\n**Type** `stopped ask` **to end the conversation.**",
                    timeout=300,
                )
                CONVERSATIONS[user_id].append(data.get("result"))
                if next_message.text.lower() == "stopped ask":
                    del CONVERSATIONS[user_id]
                    await next_message.reply(f"**Conversation ended.**")
                    break
                question = next_message.text
            except Exception:
                logger.error(traceback.format_exc())
                return await message.reply("<b>Please try again later..</b>")
        else:
            params = {"q": question}
            CONVERSATIONS[user_id].append(question)
            try:
                r = await Tools.fetch.get(GEMINI_CHAT, headers=headers, params=params)
                if r.status_code == 200:
                    result = r.json()["result"]
                    CONVERSATIONS[user_id].append(result)
                    if len(CONVERSATIONS[user_id]) > 20:
                        CONVERSATIONS[user_id] = (
                            CONVERSATIONS[user_id][:2] + CONVERSATIONS[user_id][-18:]
                        )
                    if len(result) > 4096:
                        with open(f"{question.split()[1]}.txt", "wb") as file:
                            file.write(result.encode("utf-8"))
                        reply = await message._client.send_document(
                            chat_id, f"{question.split()[1]}.txt"
                        )
                        next_message = await message._client.ask(
                            chat_id,
                            f"**<u>Chat with Gemini</u>**\n<b>Question:</b>\n<blockquote>{question}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                            reply_to_message_id=reply.id,
                            timeout=300,
                        )
                    else:
                        next_message = await message._client.ask(
                            chat_id,
                            f"<b><u>Chat with Gemini</u></b>\n<b>Question:\n<blockquote>{question}</blockquote>\n\nAnswer:\n</b><blockquote>{result}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                        )
                    if next_message.text.lower() == "stopped ask":
                        del CONVERSATIONS[user_id]
                        await next_message.reply(f"**Conversation ended.**")
                        break
                    question = next_message.text
                else:
                    return await message.reply("<b>Please try again later..</b>")
            except Exception:
                logger.error(traceback.format_exc())
                return await message.reply("<b>Please try again later..</b>")


async def chatai_with_chatgpt(client, query, uniq):
    buttons = ikb(
        [
            [
                ("ChatGpt Normal", f"chatgpt_normal_{uniq}"),
                ("ChatGpt Audio", f"chatgpt_audio_{uniq}"),
            ],
            [
                ("« Select model", f"selectmodel_{uniq}"),
                ("Close", f"close inline_chatai {uniq}"),
            ],
        ]
    )
    msg = "<b>If you want to get an answer with an audio reply, please select the ChatGpt Audio button. Or if you want an answer with plain text, then you select ChatGpt Normal</b>"
    return await query.edit_message_text(msg, reply_markup=buttons)


async def chatai_with_chatgpt_normal(client, query, uniq):
    data = state.get(uniq, uniq)
    prompt = data["prompt"]
    get_id = data["idm"]
    message = [obj for obj in get_objects() if id(obj) == get_id][0]
    user_id = message.from_user.id
    chat_id = message.chat.id
    ids = (unpack_inline_message_id(query.inline_message_id)).id
    try:
        await message._client.delete_messages(
            message.chat.id,
            ids,
        )
    except Exception:
        logger.error(traceback.format_exc())
    if user_id not in CONVERSATIONS:
        CONVERSATIONS[user_id] = [
            {
                "role": "system",
                "content": "Kamu adalah asisten paling canggih yang berbahasa Indonesia gaul, dan jangan gunakan bahasa inggris sebelum saya memulai duluan.",
            },
            {
                "role": "assistant",
                "content": "Kamu adalah asisten paling canggih yang berbahasa Indonesia gaul",
            },
        ]
    while True:
        url = "https://api.betabotz.eu.org/api/search/openai-custom"
        payload = {"message": CONVERSATIONS[user_id], "apikey": API_BOTCHAX}
        try:
            r = await Tools.fetch.post(url, json=payload)
            if r.status_code == 200:
                result = r.json()["result"]
                CONVERSATIONS[user_id].append({"role": "assistant", "content": result})
                if len(CONVERSATIONS[user_id]) > 20:
                    CONVERSATIONS[user_id] = (
                        CONVERSATIONS[user_id][:2] + CONVERSATIONS[user_id][-18:]
                    )
                if len(result) > 4096:
                    with open(f"{prompt.split()[1]}.txt", "wb") as file:
                        file.write(result.encode("utf-8"))
                    reply = await message._client.send_document(
                        chat_id, f"{prompt.split()[1]}.txt"
                    )
                    next_message = await message._client.ask(
                        chat_id,
                        f"<b><u>Chat with ChatGpt</u></b>\nQuestion:</b>\n<blockquote>{prompt}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                        reply_to_message_id=reply.id,
                        timeout=300,
                    )
                else:
                    next_message = await message._client.ask(
                        chat_id,
                        f"<b><u>Chat with ChatGpt</u></b>\n<b>Question:\n<blockquote>{prompt}</blockquote>\n\nAnswer:\n</b><blockquote>{result}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                    )
                    if next_message.text.lower() == "stopped ask":
                        del CONVERSATIONS[user_id]
                        await next_message.reply(f"**Conversation ended.**")
                        break
                    prompt = next_message.text
            else:
                return await message.reply("<b>Please try again later..</b>")
        except Exception:
            logger.error(traceback.format_exc())
            return await message.reply("<b>Please try again later..</b>")


@CMD.CALLBACK("^chatgpt_")
async def _(client, query):
    mode = str(query.data.split("_")[1])
    uniq = str(query.data.split("_")[2])
    data = state.get(uniq, uniq)
    if not data:
        return await query.answer(
            "Data not found, please create new conversation.", True
        )
    if mode == "normal":
        return await chatai_with_chatgpt_normal(client, query, uniq)
    elif mode == "audio":
        msg = "<b>Please select model voice first.</b>"
        models = [
            "alloy",
            "echo",
            "fable",
            "onyx",
            "nova",
            "shimmer",
            "coral",
            "verse",
            "ballad",
            "ash",
            "sage",
            "amuch",
            "dan",
            "elan",
        ]

        buttons = []
        row = []
        for idx, model in enumerate(models, 1):
            row.append(
                Ikb(model.capitalize(), callback_data=f"gptvoice_{model}_{uniq}")
            )
            if idx % 3 == 0:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        reply_markup = InlineKeyboardMarkup(buttons)
        return await query.edit_message_text(msg, reply_markup=reply_markup)


@CMD.CALLBACK("^gptvoice_")
async def _(client, callback_query):
    data = callback_query.data.split("_")
    args = str(data[1])
    uniq = str(data[2])
    query = state.get(uniq, uniq)
    if not query:
        return await callback_query.answer(
            "Data telah usang. Silahkan jalankan ulang fitur nya.", True
        )
    prompt = query["prompt"]
    get_id = query["idm"]
    message = [obj for obj in get_objects() if id(obj) == get_id][0]
    chat_id = message.chat.id
    user_id = message.from_user.id
    ids = (unpack_inline_message_id(callback_query.inline_message_id)).id
    try:
        await message._client.delete_messages(
            message.chat.id,
            ids,
        )
    except Exception:
        logger.error(traceback.format_exc())
    if user_id not in CONVERSATIONS:
        CONVERSATIONS[user_id] = []
    while True:
        try:
            headers = {"mg-apikey": API_MAELYN}
            params = {"q": prompt, "model": args}
            url = "https://api.maelyn.tech/api/chatgpt/audio"
            response = await Tools.fetch.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()["result"]
                audio = data.get("url")
                CONVERSATIONS[user_id].append(audio)
                reply = await message._client.send_audio(chat_id, audio)
                next_message = await message._client.ask(
                    chat_id,
                    f"**Model: {args}**\n\n<b>Question:\n<blockquote>{prompt}</blockquote>\n\n**Type `stopped ask` to end the conversation.**",
                    reply_to_message_id=reply.id,
                )
                if next_message.text.lower() == "stopped ask":
                    del CONVERSATIONS[user_id]
                    await next_message.reply(f"**Conversation ended.**")
                    break
                prompt = next_message.text
            else:
                return await message.reply("<b>Please try again later..</b>")
        except Exception:
            logger.error(traceback.format_exc())
            return await message.reply("<b>Please try again later..</b>")

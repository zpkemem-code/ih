import asyncio
import io
import os
import random
import sys
import tempfile
import traceback
from datetime import datetime
from gc import get_objects
from time import time
from uuid import uuid4

import requests
from pyrogram import enums
from pyrogram.enums import ParseMode
from pyrogram.errors import (ChannelInvalid, PeerIdInvalid, UserIdInvalid,
                             UsernameNotOccupied, UserNotParticipant)
from pyrogram.file_id import FileId, FileType, ThumbnailSource
from pyrogram.raw.functions import Ping
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.types import (Chat, InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultAnimation,
                            InlineQueryResultArticle,
                            InlineQueryResultCachedAnimation,
                            InlineQueryResultCachedDocument,
                            InlineQueryResultCachedPhoto,
                            InlineQueryResultCachedSticker,
                            InlineQueryResultCachedVideo,
                            InlineQueryResultCachedVoice,
                            InlineQueryResultPhoto, InlineQueryResultVideo,
                            InputTextMessageContent, User)

from config import (API_MAELYN, BOT_ID, BOT_NAME, HELPABLE, SUDO_OWNERS,
                    URL_LOGO)
from Zohun import bot, zohun
from Zohun.database import dB, state
from Zohun.helpers import (CMD, ButtonUtils, Message, Tools, get_time, ikb,
                          paginate_modules, query_fonts, start_time)
from Zohun.helpers.card import generate_profile_card
from Zohun.logger import logger
from plugins.pmpermit import DEFAULT_TEXT, LIMIT


@CMD.INLINE()
async def _(client, inline_query):
    try:
        text = inline_query.query.strip().lower()
        if not text:
            return
        answers = []
        if text.split()[0] == "help":
            answerss = await get_inline_help(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id, results=answerss, cache_time=0
            )
        elif text.split()[0] == "alive":
            answerss = await alive_inline(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_send":
            tuju = text.split()[1]
            answerss = await send_inline(answers, inline_query, int(tuju))
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_copy":
            tuju = text.split()[1]
            answerss = await copy_inline(answers, inline_query, int(tuju))
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "make_button":
            tuju = text.split()[1]
            answerss = await button_inline(answers, inline_query, int(tuju))
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "pmpermit_inline":
            answerss = await pmpermit_inline(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "copy_inline":
            answerss = await copy_inline_msg(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "user_info":
            answerss = await user_inline(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "gc_info":
            answerss = await gc_inline(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "get_note":
            answerss = await get_inline_note(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_eval":
            answerss = await inline_eval(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_font":
            answerss = await inline_font(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_cat":
            answerss = await inline_cat(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_bola":
            answerss = await inline_bola(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "get_users":
            answerss = await get_zohun_user(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_textpro":
            answerss = await inline_textpro(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_ttsearch":
            answerss = await inline_ttsearch(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_ttdownload":
            answerss = await inline_ttdownload(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_spotify":
            answerss = await inline_spotify(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_pinsearch":
            answerss = await inline_pinsearch(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_news":
            answerss = await inline_news(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_anime":
            answerss = await inline_anime(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_donghua":
            answerss = await inline_donghua(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_comic":
            answerss = await inline_comic(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_gnews":
            answerss = await inline_gnews(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_chatai":
            answerss = await inline_chatai(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_cekid":
            answerss = await inline_cekid(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_info":
            answerss = await inline_info(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_card_info":
            answerss = await inline_card_info(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )

    except Exception:
        logger.error(f"{traceback.format_exc()}")


async def inline_card_info(results, inline):
    try:
        _id = inline.query.split()[1]
        message = next((obj for obj in get_objects() if id(obj) == int(_id)), None)
        if message:
            buttons = []

            def add_button(name, value):
                if value:
                    buttons.append(InlineKeyboardButton(name, callback_data=str(value)))

            client = message._client
            chat = message.chat
            your_id = message.from_user or message.sender_chat
            message_id = message.id
            reply = message.reply_to_message
            replied_user_id = None
            mentioned = None
            photo_id = video_id = sticker_id = animation_id = document_id = emoji_id = (
                None
            )
            if reply:
                replied_user_id = (
                    reply.from_user.id
                    if reply.from_user
                    else reply.sender_chat.id if reply.sender_chat else None
                )
                if reply.entities:
                    for entity in reply.entities:
                        if entity.custom_emoji_id:
                            emoji_id = entity.custom_emoji_id
                if reply.photo:
                    photo_id = reply.photo.file_id
                elif reply.video:
                    video_id = reply.video.file_id
                elif reply.sticker:
                    sticker_id = reply.sticker.file_id
                elif reply.animation:
                    animation_id = reply.animation.file_id
                elif reply.document:
                    document_id = reply.document.file_id

            if len(message.command) == 2:
                try:
                    split = message.text.split(None, 1)[1].strip()
                    entity = await client.get_chat(split)

                    if entity.type in [
                        enums.ChatType.GROUP,
                        enums.ChatType.SUPERGROUP,
                        enums.ChatType.CHANNEL,
                    ]:
                        mentioned = entity.id

                    else:
                        mentioned = entity.id
                except Exception:
                    return await message.reply_text(f"**User not found.**")
            add_button("Message ID", message_id)
            add_button("Your ID", your_id.id)
            add_button("Chat ID", chat.id)
            add_button("Reply Message ID", reply.id if reply else None)
            add_button("Reply User ID", replied_user_id)
            add_button("Mentioned ID", mentioned)
            add_button("Emoji ID", emoji_id)
            add_button("Photo File ID", photo_id)
            add_button("Video File ID", video_id)
            add_button("Sticker File ID", sticker_id)
            add_button("GIF File ID", animation_id)
            add_button("Document File ID", document_id)

            keyboard = InlineKeyboardMarkup(
                [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
            )

            user_to_fetch = replied_user_id or mentioned or your_id.id
            profile_card_path = None

            if user_to_fetch:
                try:
                    target = await client.get_chat(user_to_fetch)
                    if target.type == enums.ChatType.PRIVATE:
                        user = await client.get_users(user_to_fetch)
                        profile_card_path = await generate_profile_card(client, user)
                    elif target.type in [
                        enums.ChatType.GROUP,
                        enums.ChatType.SUPERGROUP,
                        enums.ChatType.CHANNEL,
                    ]:
                        user = await client.get_chat(user_to_fetch)
                        profile_card_path = await generate_profile_card(client, user)
                except Exception:
                    logger.error(f"Error: {traceback.format_exc()}")
                    profile_card_path = None
            text = f"<b><blockquote>Generated Card Info By {bot.me.mention}</blockquote></b>"
            if profile_card_path and os.path.exists(profile_card_path):
                uploaded_url = await Tools.upload_thumb(profile_card_path)
                os.remove(profile_card_path)
                results.append(
                    InlineQueryResultPhoto(
                        photo_url=uploaded_url,
                        title="User ID Info",
                        caption=text,
                        reply_markup=keyboard,
                    )
                )
            else:
                results.append(
                    InlineQueryResultArticle(
                        title="User ID Info",
                        input_message_content=InputTextMessageContent(text),
                        reply_markup=keyboard,
                    )
                )

            return results

    except Exception:
        logger.error(f"Inline ID Info Error:\n{traceback.format_exc()}")
        return results


async def inline_info(results, inline):
    _id = inline.query.split()[1]
    message = next((obj for obj in get_objects() if id(obj) == int(_id)), None)
    if message:
        client = message._client
        from_user = None
        from_user_id, from_user_name, user = Tools.extract_user(message)

        small_user = None
        full_user = None
        profile_vid = None

        if user or isinstance(user, User):
            try:
                from_user = await client.invoke(
                    GetFullUser(id=(await client.resolve_peer(from_user_id)))
                )
            except UserIdInvalid:
                pass
            except PeerIdInvalid as error:
                return await message.reply(str(error))

            if from_user:
                small_user = from_user.users[0]
                full_user = from_user.full_user
                premium = small_user.premium
                dc_id = small_user.photo.dc_id
                gbanned = small_user.id in await dB.get_list_from_var(
                    client.me.id, "GBANNED"
                )
                is_bot = small_user.bot
                from_user = User._parse(client, small_user)

        if not from_user and user or isinstance(user, Chat):
            try:
                from_user = await client.invoke(
                    GetFullChannel(channel=(await client.resolve_peer(from_user_id)))
                )
            except (ChannelInvalid, UsernameNotOccupied) as error:
                return await message.reply(str(error))

            small_user = from_user.chats[0]
            full_user = from_user.full_chat
            dc_id = from_user.full_chat.chat_photo.dc_id
            from_user = Chat._parse_channel_chat(client, small_user)

        if not from_user and user == True:
            return await message.reply("**Please check again.**")

        first_name = getattr(from_user, "title", getattr(from_user, "first_name", " "))
        last_name = getattr(from_user, "last_name", "")
        username = from_user.username or ""
        msg = ""

        if isinstance(from_user, User):
            msg += "<blockquote><b>UserInfo:</b>\n"
            msg += f"   <b>name:</b> <b><a href='tg://user?id={from_user.id}'>{first_name} {last_name or ''}</a></b>\n"
            msg += f"      <b>id:</b> <code>{from_user.id}</code>\n"
            msg += f"      <b>dc_id:</b> <code>{dc_id}</code>\n"
            msg += f"      <b>is_bot:</b> <code>{is_bot}</code>\n"
            msg += f"      <b>is_gbanned:</b> <code>{gbanned}</code>\n"
            msg += f"      <b>is_premium:</b> <b>{premium}</b>\n"

            if username:
                buttons = ikb(
                    [
                        [("User Link", f"https://t.me/{username}", "url")],
                        [("User Bio", f"getbio_{from_user.id}")],
                    ]
                )
            else:
                buttons = ikb(
                    [
                        [("User Link", f"{from_user_id}", "user_id")],
                        [("User Bio", f"getbio_{from_user.id}")],
                    ]
                )
        if isinstance(from_user, Chat):
            msg += "<blockquote><b>ChatInfo:</b>\n"
            msg += f"   <b>name:</b> <b><a href='https://t.me/c/{full_user.id}'>{first_name}</a></b>\n"
            msg += f"      <b>dc_id:</b> <code>{dc_id}</code>\n"
            msg += f"      <b>id:</b> <code>{from_user.id}</code>\n"
            if username:
                buttons = ikb(
                    [
                        [("Chat Link", f"https://t.me/{username}", "url")],
                        [("Chat Bio", f"getbio_{from_user.id}")],
                    ]
                )
            else:
                buttons = ikb(
                    [
                        [("Chat Link", f"https://t.me/c/{full_user.id}", "url")],
                        [("Chat Bio", f"getbio_{from_user.id}")],
                    ]
                )
        if getattr(full_user, "about", None):
            state.set(from_user.id, "bio", full_user.about)

        if getattr(full_user, "common_chats_count", None):
            msg += f"      <b>same_group:</b> <code>{full_user.common_chats_count}</code>\n"

        if isinstance(from_user, User) and message.chat.type in [
            enums.ChatType.SUPERGROUP,
            enums.ChatType.CHANNEL,
        ]:
            try:
                chat_member_p = await message.chat.get_member(small_user.id)
                joined_date = (
                    chat_member_p.joined_date or datetime.fromtimestamp(time())
                ).strftime("%d-%m-%Y %H:%M:%S")
                msg += f"      <b>joinned:</b> <code>{joined_date}</code>\n"
            except UserNotParticipant:
                pass

        if len(msg) < 334:
            polos = getattr(
                full_user, "settings", getattr(full_user, "available_reactions", None)
            )
            if polos:
                msg += f"      <b>reactions:</b> <code>{len(polos)}</code>\n"

        if getattr(full_user, "online_count", None):
            online_count = full_user.online_count
            msg += f"      <b>online_count:</b> <code>{online_count}</code>\n"

        if getattr(full_user, "pinned_msg_id", None):
            pinned_message = f"<a href='https://t.me/c/{full_user.id}/{full_user.pinned_msg_id}'>Pinned Message</a>"
            msg += f"      <b>pinned:</b> <b>{pinned_message}</b>\n"

        if getattr(full_user, "linked_chat_id", None):
            linked_chat = (
                f"<a href='https://t.me/c/{full_user.linked_chat_id}/1'>Linked Chat</a>"
            )
            msg += f"      <b>linked_chat:</b> <b>{linked_chat}</b>\n"

        chat_photo = from_user.photo

        if chat_photo:
            p_p_u_t = None
            tepos = getattr(
                full_user, "profile_photo", getattr(full_user, "chat_photo", None)
            )
            if tepos:
                profile_vid = tepos.video_sizes[0] if tepos.video_sizes else None
                p_p_u_t = datetime.fromtimestamp(tepos.date).strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            if p_p_u_t:
                msg += f"      <b>upload_date:</b> <code>{p_p_u_t}</code>\n"
            if profile_vid:
                file_obj = io.BytesIO()
                async for chunk in client.stream_media(
                    message=FileId(
                        file_type=FileType.PHOTO,
                        dc_id=tepos.dc_id,
                        media_id=tepos.id,
                        access_hash=tepos.access_hash,
                        file_reference=tepos.file_reference,
                        thumbnail_source=ThumbnailSource.THUMBNAIL,
                        thumbnail_file_type=FileType.PHOTO,
                        thumbnail_size=profile_vid.type,
                        volume_id=0,
                        local_id=0,
                    ).encode(),
                ):
                    file_obj.write(chunk)
                    suffix = ".mp4"
            else:
                file_obj = io.BytesIO()
                async for chunk in client.stream_media(
                    message=chat_photo.big_file_id,
                ):
                    file_obj.write(chunk)
                suffix = ".jpg"
            if file_obj:
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=suffix
                ) as tmp_file:
                    tmp_file.write(file_obj.getvalue())
                    tmp_file_path = tmp_file.name

                link = await Tools.upload_thumb(tmp_file_path)
            media = (
                InlineQueryResultVideo
                if link.endswith(".mp4")
                else InlineQueryResultPhoto
            )
            msg += "</blockquote>"
            url_ling = (
                {"video_url": link, "thumb_url": link}
                if link.endswith(".mp4")
                else {"photo_url": link}
            )
            results.append(
                media(
                    **url_ling,
                    title="Inline Info",
                    caption=msg,
                    reply_markup=buttons,
                )
            )
    else:
        results.append(
            InlineQueryResultArticle(
                title="Inline Info",
                input_message_content=InputTextMessageContent(msg),
                reply_markup=buttons,
            )
        )
    return results


async def inline_cekid(results, inline):
    try:
        _id = inline.query.split()[1]
    except IndexError:
        return results

    message = next((obj for obj in get_objects() if id(obj) == int(_id)), None)
    if not message:
        return results

    chat = message.chat
    your_id = message.from_user if message.from_user else message.sender_chat
    message_id = message.id
    reply = message.reply_to_message

    # FIXED: Display IDs directly in message text instead of copy_text buttons
    text = f"""**📊 Message Information**

<blockquote>📌 **Message ID:** `{message_id}`
👤 **Your ID:** `{your_id.id}`
💬 **Chat ID:** `{chat.id}`</blockquote>"""
    
    # Simple close button instead of copy_text buttons
    buttons = [[InlineKeyboardButton("❌ Close", callback_data="close_inline")]]
    
    if reply:
        replied_user_id = (
            reply.from_user.id if reply.from_user
            else reply.sender_chat.id if reply.sender_chat else None
        )
        text += f"""

**↩️ Replied Message Information**
📩 **Reply Message ID:** `{reply.id}`"""
        
        if replied_user_id:
            text += f"\n👥 **Replied User ID:** `{replied_user_id}`"
        
        # Add file IDs to text if present
        if reply.photo:
            text += f"\n🖼️ **Photo File ID:** `{reply.photo.file_id}`"
        if reply.video:
            text += f"\n🎥 **Video File ID:** `{reply.video.file_id}`"
        if reply.sticker:
            text += f"\n🎨 **Sticker File ID:** `{reply.sticker.file_id}`"
        if reply.animation:
            text += f"\n🎬 **Animation File ID:** `{reply.animation.file_id}`"
        if reply.document:
            text += f"\n📄 **Document File ID:** `{reply.document.file_id}`"
        if reply.entities:
            for entity in reply.entities:
                if entity.custom_emoji_id:
                    text += f"\n😊 **Custom Emoji ID:** `{entity.custom_emoji_id}`"
        
    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await message._client.get_users(split)).id
            buttons.append(
                [InlineKeyboardButton("Mentioned User ID", callback_data=str(user_id))]
            )
        except Exception:
            pass

    results.append(
        InlineQueryResultArticle(
            title="Inline CheckID",
            input_message_content=InputTextMessageContent(text),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    )
    return results


async def inline_chatai(results, inline):
    uniq = str(inline.query.split()[1])
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
    results.append(
        InlineQueryResultArticle(
            title="Inline Chat AI",
            input_message_content=InputTextMessageContent(msg),
            reply_markup=(buttons),
        )
    )
    return results


async def inline_gptaudio(results, inline):
    uniq = str(inline.query.split()[1])
    msg = "<b>Please select model first.</b>"
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
            InlineKeyboardButton(
                model.capitalize(), callback_data=f"gptvoice_{model}_{uniq}"
            )
        )
        if idx % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    results.append(
        InlineQueryResultArticle(
            title="GPT Voice Models",
            input_message_content=InputTextMessageContent(msg),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    )
    return results


async def inline_gnews(results, inline):
    uniq = str(inline.query.split()[1])
    data = state.get(uniq, uniq)
    try:
        title = data[0].get("title")
        source = data[0].get("source")
        date = Tools.jakartaTime(data[0].get("datetime", "-"))
        time = data[0].get("time")
        arType = data[0].get("articleType")
        thumb = data[0].get("image")
        judul = f"""
**Title:** {title}
**Source:** {source}
**Uploaded:** {date}
**Time:** {time}
**articleType:** {arType}"""
        buttons = ikb(
            [
                [("📮 Link", f"{data[0].get('link')}", "url")],
                [("》 Next", f"gnews_1_{uniq}")],
            ]
        )
        results.append(
            InlineQueryResultPhoto(
                photo_url=thumb,
                caption=judul,
                title="Inline News",
                reply_markup=buttons,
            )
        )
        return results
    except Exception:
        logger.error(f"Inline news: {traceback.format_exc()}")


async def inline_comic(results, inline):
    uniq = str(inline.query.split()[1])
    data = state.get(uniq, uniq)
    try:
        buttons = ikb([[("》 Next", f"restcomic_1_{uniq}")]])
        title = data[0].get("title")
        chapter = data[0].get("chapters", [{}])[0]
        episode = chapter.get("title", "-")
        date = chapter.get("date", "-")
        chapter_url = chapter.get("url", "")
        if "https://komiku.id" in chapter_url and not chapter_url.startswith(
            "https://komiku.id/"
        ):
            chapter_url = chapter_url.replace("https://komiku.id", "https://komiku.id/")
        target = data[0].get("cover")
        await Tools.bash(f"wget {target} -O {uniq}.jpg")
        thumb = await Tools.upload_thumb(f"{uniq}.jpg")

        judul = f"**Title:** {title}\n**Chapters:** {episode}\n**Link:** {chapter_url}\n**Uploaded:** {date}"
        results.append(
            InlineQueryResultPhoto(
                photo_url=thumb,
                caption=judul,
                title="Inline Donghua",
                reply_markup=buttons,
            )
        )
        return results
    except Exception:
        logger.error(f"Inline comic: {traceback.format_exc()}")


async def inline_donghua(results, inline):
    uniq = str(inline.query.split()[1])
    data = state.get(uniq, uniq)
    try:
        buttons = ikb([[("》 Next", f"restdonghua_1_{uniq}")]])
        title = data[0].get("title")
        episode = data[0].get("episode")
        target = data[0].get("thumbnail")
        await Tools.bash(f"wget {target} -O {uniq}.jpg")
        thumb = await Tools.upload_thumb(f"{uniq}.jpg")
        date = Tools.jakartaTime(data[0].get("updatedAt", "-"))
        url = data[0].get("url")
        judul = f"**Title:** {title}\n**Episode:** {episode}\n**Link:** {url}\n**Uploaded:** {date}"
        results.append(
            InlineQueryResultPhoto(
                photo_url=thumb,
                caption=judul,
                title="Inline Donghua",
                reply_markup=buttons,
            )
        )
        return results
    except Exception:
        logger.error(f"Inline donghua: {traceback.format_exc()}")


async def inline_anime(results, inline):
    uniq = str(inline.query.split()[1])
    data = state.get(uniq, uniq)
    try:
        buttons = ikb([[("》 Next", f"restanime_1_{uniq}")]])
        title = data[0].get("title")
        episode = data[0].get("episode")
        target = data[0].get("thumbnail")
        await Tools.bash(f"wget {target} -O {uniq}.jpg")
        thumb = await Tools.upload_thumb(f"{uniq}.jpg")
        date = Tools.jakartaTime(data[0].get("updatedAt", "-"))
        url = data[0].get("url")
        judul = f"**Title:** {title}\n**Episode:** {episode}\n**Link:** {url}\n**Uploaded:** {date}"
        results.append(
            InlineQueryResultPhoto(
                photo_url=thumb,
                caption=judul,
                title="Inline Anime",
                reply_markup=buttons,
            )
        )
        return results
    except Exception:
        logger.error(f"Inline anime: {traceback.format_exc()}")


async def inline_news(results, inline):
    uniq = str(inline.query.split()[1])
    data = state.get(uniq, uniq)
    try:
        buttons = ikb(
            [
                [("📮 Link", f"{data[0]['berita_url']}", "url")],
                [("》 Next", f"news_1_{uniq}")],
            ]
        )
        date = data[0].get("berita_diupload", "-")
        foto = data[0]["berita_thumb"]
        judul = f"**Title:** {data[0]['berita']}\n**Link:** {data[0]['berita_url']}\n**Uploaded:** {date}"
        results.append(
            InlineQueryResultPhoto(
                photo_url=foto,
                thumb_url=foto,
                caption=judul,
                title="Inline News",
                reply_markup=buttons,
            )
        )
        return results
    except Exception:
        logger.error(f"Inline news: {traceback.format_exc()}")


async def inline_pinsearch(results, inline):
    uniq = str(inline.query.split()[1])
    data = state.get(uniq, uniq)
    try:
        buttons = ikb([[("》 Next", f"nxpinsearch_1_{uniq}")]])
        results.append(
            InlineQueryResultPhoto(
                photo_url=data[0],
                title="Inline Pinterest",
                reply_markup=buttons,
            )
        )
        return results
    except Exception:
        logger.error(f"Inline result pindl: {traceback.format_exc()}")


async def inline_ttdownload(results, inline):
    userid = inline.from_user.id
    keyboard = ikb(
        [
            [
                ("Download Video", f"cqtiktok_videodl_{userid}"),
                ("Download Audio", f"cqtiktok_audiodl_{userid}"),
            ]
        ]
    )
    results.append(
        InlineQueryResultArticle(
            title="Tiktok Inline Download!",
            reply_markup=keyboard,
            input_message_content=InputTextMessageContent(
                "<blockquote><b>Please select the button below you want to download!</b></blockquote>"
            ),
        )
    )
    return results


async def inline_spotify(results, inline):
    userid = inline.from_user.id
    uniq = str(inline.query.split()[1])
    data = state.get(userid, uniq)
    state.set(userid, "fordlspotify", data[0]["url"])
    try:
        for audio in data:
            caption = f"""
<blockquote>🎶 **Title:** {audio['title']}
👥 **Popularity:** {audio['popularity']}
⏳ **Duration:** {audio['duration']}
🖇️ **Spotify URL:** <a href='{audio['url']}'>here</a></blockquote>"""
            buttons = ikb(
                [
                    [("Download audio", f"dlspot_{userid}_{uniq}")],
                    [("Next audio", f"nxtspotify_1_{userid}_{uniq}")],
                ]
            )
            results.append(
                InlineQueryResultArticle(
                    title="Tiktok Inline Download!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(
                        caption, disable_web_page_preview=True
                    ),
                )
            )
        return results
    except Exception:
        logger.error(f"Inline result spotify: {traceback.format_exc()}")


async def inline_ttsearch(results, inline):
    userid = inline.from_user.id
    uniq = str(inline.query.split()[1])
    data = state.get(userid, uniq)
    try:
        for video in data:
            title = video["title"] or "-"
            video_link = video["play"]
            buttons = ikb([[("Next video", f"nxttsearch_1_{userid}_{uniq}")]])
            caption = f"<blockquote>{title}</blockquote>"
            results.append(
                InlineQueryResultVideo(
                    thumb_url=video_link,
                    video_url=video_link,
                    title=title,
                    caption=caption,
                    reply_markup=buttons,
                )
            )
        return results
    except Exception:
        logger.error(f"Inline result ttdl: {traceback.format_exc()}")


async def inline_bola(resultss, inline_query):
    url = f"https://api.maelyn.tech/api/jadwalbola?apikey={API_MAELYN}"
    result = await Tools.fetch.get(url)
    uniq = f"{str(uuid4())}"
    if result.status_code == 200:
        data = result.json()
        if data["status"] == "Success":
            buttons = []
            temp_row = []
            state.set(uniq.split("-")[0], uniq.split("-")[0], data["result"])
            for liga_date in data["result"]:
                button = InlineKeyboardButton(
                    text=liga_date["LigaDate"],
                    callback_data=f"bola_matches {uniq.split('-')[0]} {liga_date['LigaDate']}",
                )
                temp_row.append(button)

                if len(temp_row) == 3:
                    buttons.append(temp_row)
                    temp_row = []

            if temp_row:
                buttons.append(temp_row)
            last_row = [
                InlineKeyboardButton(
                    text="« Back", callback_data=f"bola_date {uniq.split('-')[0]}"
                ),
                InlineKeyboardButton(text="Close", callback_data="close inline_bola"),
            ]
            buttons.append(last_row)
            keyboard = InlineKeyboardMarkup(buttons)

            resultss.append(
                InlineQueryResultArticle(
                    title="Football Schedule",
                    reply_markup=keyboard,
                    input_message_content=InputTextMessageContent(
                        "<b>Select a date to view football matches:</b>"
                    ),
                )
            )
    return resultss


async def get_zohun_user(result, inline_query):
    try:
        msg = await Message.userbot(0)
        buttons = ButtonUtils.userbot(zohun._ubot[0].me.id, 0)
        result.append(
            InlineQueryResultArticle(
                title="get user Inline!",
                reply_markup=buttons,
                input_message_content=InputTextMessageContent(msg),
            )
        )

        return result
    except Exception:
        logger.error(f"Line 209:\n {traceback.format_exc()}")


async def inline_textpro(result, inline):
    try:
        userid = inline.from_user.id
        text = state.get(userid, "TEXT_PRO")
        image_data = await Tools.gen_text_pro(text, "water-color")
        keyboard = ButtonUtils.create_buttons_textpro(
            Tools.query_textpro[0], userid, current_batch=0
        )
        state.set(userid, "page_textpro", 0)
        buttons = InlineKeyboardMarkup(keyboard)
        result.append(
            InlineQueryResultPhoto(
                photo_url=image_data,
                title="Text Pro Inline!",
                reply_markup=buttons,
                caption=f"<blockquote>**Costum text:**\n\n{text}</blockquote>",
            )
        )

        return result
    except Exception:
        logger.error(f"Line 180:\n {traceback.format_exc()}")


async def inline_cat(result, inline_query):
    buttons = ikb([[("Refresh cat", "refresh_cat")], [("Close", "close inline_cat")]])
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            result.append(
                InlineQueryResultAnimation(
                    animation_url=cat_url,
                    title="cat Inline!",
                    reply_markup=buttons,
                    caption="<blockquote><b>Meow 😽</b></blockquote>",
                )
            )
        else:
            result.append(
                InlineQueryResultPhoto(
                    photo_url=cat_url,
                    title="cat Inline!",
                    reply_markup=buttons,
                    caption="<blockquote><b>Meow 😽</b></blockquote>",
                )
            )

    return result


async def inline_font(result, inline_query):
    get_id = inline_query.from_user.id

    keyboard = ButtonUtils.create_font_keyboard(query_fonts[0], get_id, current_batch=0)

    buttons = InlineKeyboardMarkup(keyboard)
    result.append(
        InlineQueryResultArticle(
            title="Font Inline!",
            reply_markup=buttons,
            input_message_content=InputTextMessageContent(
                "<blockquote><b>Please choice fonts:</b></blockquote>"
            ),
        )
    )
    return result


async def inline_eval(result, inline_query):
    uniq = str(inline_query.query.split()[1])
    data = state.get(BOT_ID, uniq)
    if len(data) == 1:
        msg = data["time"]
        button = ikb([[("Close", f"close inline_eval {uniq}")]])
    else:
        msg = data["time"]
        button = ikb([[("Output", f"{data['url']}", "url")]])
    result.append(
        InlineQueryResultArticle(
            title="Inline Eval",
            input_message_content=InputTextMessageContent(
                msg, disable_web_page_preview=True
            ),
            reply_markup=button,
        )
    )
    return result


async def gc_inline(result, inline_query):
    ids = inline_query.from_user.id
    data = state.get(ids, "gc_info")
    state.set(BOT_ID, "gc_info", data)
    usr = data["username"]
    if usr is None:
        keyb = ikb([[("Desc", f"cb_desc {data['id']}", "callback_data")]])
    else:
        keyb = ikb(
            [
                [
                    ("Chat", f"https://t.me/{usr}", "url"),
                    ("Desc", f"cb_desc {data['id']}", "callback_data"),
                ]
            ]
        )
    msg = f"""
<blockquote><b>ChatInfo:</b>
   <b>name:</b> <b>{data['name']}</b>
      <b>id:</b> <code>{data['id']}</code>
      <b>type:</b> <b>{data['type']}</b>
      <b>dc_id:</b> <b>{data['dc_id']}</b>
      <b>username:</b> <b>@{data['username']}</b>
      <b>member:</b> <b>{data['member']}</b>
      <b>protect:</b> <b>{data['protect']}</b>
      <b>is_creator:</b> <b>{data['is_creator']}</b>
      <b>is_admin:</b> <b>{data['is_admin']}</b>
      <b>is_restricted:</b> <b>{data['is_restricted']}</b></blockquote>
"""
    result.append(
        InlineQueryResultArticle(
            title="gc info!",
            input_message_content=InputTextMessageContent(
                msg, disable_web_page_preview=True
            ),
            reply_markup=keyb,
        )
    )
    return result


async def user_inline(result, inline_query):
    ids = inline_query.from_user.id
    data = state.get(ids, "user_info")
    try:
        org = await bot.get_users(int(data["id"]))
        keyb = ikb([[("User", f"{org.id}", "user_id")]])
    except Exception:
        org = f"tg://openmessage?user_id={int(data['id'])}"
        keyb = ikb([[("User", f"{org}", "url")]])
    msg = f"""
<blockquote><b>UserInfo:</b>
   <b>name:</b> <b>{data['name']}</b>
      <b>id:</b> <code>{data['id']}</code>
      <b>created:</b> <code>{data['create']}</code>
      <b>is_contact:</b> <b>{data['contact']}</b>
      <b>is_premium:</b> <b>{data['premium']}</b>
      <b>is_deleted:</b> <b>{data['deleted']}</b>
      <b>is_bot:</b> <b>{data['isbot']}</b>
      <b>is_gbanned:</b> <b>{data['gbanned']}</b>
      <b>dc_id:</b> <b>{data['dc_id']}</b></blockquote>
"""
    result.append(
        InlineQueryResultArticle(
            title="user info!",
            input_message_content=InputTextMessageContent(
                msg, disable_web_page_preview=True
            ),
            reply_markup=keyb,
        )
    )
    return result


async def pmpermit_inline(result, inline_query):
    him = int(inline_query.query.split()[1])
    mee = inline_query.from_user.id
    gtext = await dB.get_var(mee, "PMTEXT")
    pm_text = gtext if gtext else DEFAULT_TEXT
    pm_warns = await dB.get_var(mee, "PMLIMIT") or LIMIT
    Flood = state.get(mee, him)
    teks, button = ButtonUtils.parse_msg_buttons(pm_text)
    button = ButtonUtils.create_inline_keyboard(button, mee)
    def_button = ikb(
        [
            [
                ("Approve", f"cb_pm ok {mee} {him}", "callback_data"),
                ("Disapprove", f"cb_pm no {mee} {him}", "callback_data"),
            ],
            [
                (
                    f"You have a warning {Flood} of {pm_warns} !!",
                    f"cb_pm warn {mee} {him}",
                    "callback_data",
                )
            ],
        ]
    )
    if button:
        for row in def_button.inline_keyboard:
            button.inline_keyboard.append(row)
    else:
        button = def_button
    tekss = await Tools.escape_tag(bot, him, teks, Tools.parse_words)
    media = await dB.get_var(mee, "PMMEDIA")
    if media:
        file_id = str(media["file_id"])
        type = str(media["type"])
        type_mapping = {
            "photo": InlineQueryResultCachedPhoto,
            "video": InlineQueryResultCachedVideo,
            "animation": InlineQueryResultCachedAnimation,
            "audio": InlineQueryResultCachedDocument,
            "document": InlineQueryResultCachedDocument,
            "sticker": InlineQueryResultCachedSticker,
            "voice": InlineQueryResultCachedVoice,
        }
        result_class = type_mapping[type]
        kwargs = {
            "id": str(uuid4()),
            "caption": tekss,
            "reply_markup": button,
        }
        if type == "photo":
            kwargs["photo_file_id"] = file_id
        elif type == "video":
            kwargs.update({"video_file_id": file_id, "title": "Video with Button"})
        elif type == "animation":
            kwargs["animation_file_id"] = file_id
        elif type == "audio":
            kwargs.update(
                {"document_file_id": file_id, "title": "Document with Button"}
            )
        elif type == "document":
            kwargs.update(
                {"document_file_id": file_id, "title": "Document with Button"}
            )
        elif type == "sticker":
            kwargs["sticker_file_id"] = file_id
        elif type == "voice":
            kwargs.update({"voice_file_id": file_id, "title": "Voice with Button"})
        result.append(result_class(**kwargs))
    else:
        result.append(
            InlineQueryResultArticle(
                title="PMPermit NOn-Media",
                input_message_content=InputTextMessageContent(
                    tekss,
                    disable_web_page_preview=True,
                ),
                reply_markup=button,
            )
        )
    return result


async def copy_inline(result, inline_query, user_id):
    try:
        _id = state.get(user_id, "inline_copy")
        message = next((obj for obj in get_objects() if id(obj) == int(_id)), None)
        if message:
            button = message.reply_to_message.reply_markup
            caption = (
                message.reply_to_message.text or message.reply_to_message.caption or ""
            )
            entities = (
                message.reply_to_message.entities
                or message.reply_to_message.caption_entities
                or ""
            )
            if message.reply_to_message.media:
                client = message._client
                reply = message.reply_to_message
                copy = await reply.copy(bot.me.username)
                sent = await client.send_message(
                    bot.me.username, "/id copy_media", reply_to_message_id=copy.id
                )
                await asyncio.sleep(1)
                await sent.delete()
                await copy.delete()
                data = state.get(user_id, "copy_media")
                file_id = str(data["file_id"])
                type = str(data["type"])
                type_mapping = {
                    "photo": InlineQueryResultCachedPhoto,
                    "video": InlineQueryResultCachedVideo,
                    "animation": InlineQueryResultCachedAnimation,
                    "audio": InlineQueryResultCachedDocument,
                    "document": InlineQueryResultCachedDocument,
                    "sticker": InlineQueryResultCachedSticker,
                    "voice": InlineQueryResultCachedVoice,
                }
                result_class = type_mapping[type]
                kwargs = {
                    "id": str(uuid4()),
                    "caption": caption,
                    "caption_entities": entities,
                    "reply_markup": button,
                }

                if type == "photo":
                    kwargs["photo_file_id"] = file_id
                elif type == "video":
                    kwargs.update(
                        {"video_file_id": file_id, "title": "Video with Button"}
                    )
                elif type == "animation":
                    kwargs["animation_file_id"] = file_id
                elif type == "audio":
                    kwargs.update(
                        {"document_file_id": file_id, "title": "Document with Button"}
                    )
                elif type == "document":
                    kwargs.update(
                        {"document_file_id": file_id, "title": "Document with Button"}
                    )
                elif type == "sticker":
                    kwargs["sticker_file_id"] = file_id
                elif type == "voice":
                    kwargs.update(
                        {"voice_file_id": file_id, "title": "Voice with Button"}
                    )

                result.append(result_class(**kwargs))
            else:
                result.append(
                    InlineQueryResultArticle(
                        id=str(uuid4()),
                        title="Send Inline!",
                        reply_markup=button,
                        input_message_content=InputTextMessageContent(
                            caption,
                            entities=entities,
                        ),
                    )
                )
        return result
    except Exception as er:
        logger.error(f"ERROR: {str(er)}, line: {sys.exc_info()[-1].tb_lineno}")


async def send_inline(result, inline_query, user_id):
    try:
        _id = state.get(user_id, "inline_send")
        message = next((obj for obj in get_objects() if id(obj) == int(_id)), None)
        if message:
            button = message.reply_to_message.reply_markup
            caption = (
                message.reply_to_message.text or message.reply_to_message.caption or ""
            )
            entities = (
                message.reply_to_message.entities
                or message.reply_to_message.caption_entities
                or ""
            )
            if message.reply_to_message.media:
                client = message._client
                reply = message.reply_to_message
                copy = await reply.copy(bot.me.username)
                sent = await client.send_message(
                    bot.me.username, "/id send_media", reply_to_message_id=copy.id
                )
                await asyncio.sleep(1)
                await sent.delete()
                await copy.delete()
                data = state.get(user_id, "send_media")
                file_id = str(data["file_id"])
                type = str(data["type"])
                type_mapping = {
                    "photo": InlineQueryResultCachedPhoto,
                    "video": InlineQueryResultCachedVideo,
                    "animation": InlineQueryResultCachedAnimation,
                    "audio": InlineQueryResultCachedDocument,
                    "document": InlineQueryResultCachedDocument,
                    "sticker": InlineQueryResultCachedSticker,
                    "voice": InlineQueryResultCachedVoice,
                }
                result_class = type_mapping[type]
                kwargs = {
                    "id": str(uuid4()),
                    "caption": caption,
                    "reply_markup": button,
                    "caption_entities": entities,
                }

                if type == "photo":
                    kwargs["photo_file_id"] = file_id
                elif type == "video":
                    kwargs.update(
                        {"video_file_id": file_id, "title": "Video with Button"}
                    )
                elif type == "animation":
                    kwargs["animation_file_id"] = file_id
                elif type == "audio":
                    kwargs.update(
                        {"document_file_id": file_id, "title": "Document with Button"}
                    )
                elif type == "document":
                    kwargs.update(
                        {"document_file_id": file_id, "title": "Document with Button"}
                    )
                elif type == "sticker":
                    kwargs["sticker_file_id"] = file_id
                elif type == "voice":
                    kwargs.update(
                        {"voice_file_id": file_id, "title": "Voice with Button"}
                    )

                result.append(result_class(**kwargs))
            else:
                result.append(
                    InlineQueryResultArticle(
                        id=str(uuid4()),
                        title="Send Inline!",
                        reply_markup=button,
                        input_message_content=InputTextMessageContent(
                            caption, entities=entities
                        ),
                    )
                )
        return result
    except Exception as er:
        logger.error(f"ERROR: {str(er)}, line: {sys.exc_info()[-1].tb_lineno}")


async def button_inline(result, inline_query, user_id):
    try:
        data = state.get(user_id, "button")
        text, button = ButtonUtils.parse_msg_buttons(data)
        if button:
            button = ButtonUtils.create_inline_keyboard(button, user_id)

        data2 = state.get(user_id, "button_media")
        if not data2:
            result.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="Text Button!",
                    input_message_content=InputTextMessageContent(
                        text, disable_web_page_preview=True
                    ),
                    reply_markup=button,
                )
            )
        else:
            file_id = str(data2["file_id"])
            type = str(data2["type"])
            type_mapping = {
                "photo": InlineQueryResultCachedPhoto,
                "video": InlineQueryResultCachedVideo,
                "animation": InlineQueryResultCachedAnimation,
                "audio": InlineQueryResultCachedDocument,
                "document": InlineQueryResultCachedDocument,
                "sticker": InlineQueryResultCachedSticker,
                "voice": InlineQueryResultCachedVoice,
            }

            if type in type_mapping:
                result_class = type_mapping[type]
                kwargs = {
                    "id": str(uuid4()),
                    "caption": text,
                    "reply_markup": button,
                }

                if type == "photo":
                    kwargs["photo_file_id"] = file_id
                elif type == "video":
                    kwargs.update(
                        {"video_file_id": file_id, "title": "Video with Button"}
                    )
                elif type == "animation":
                    kwargs["animation_file_id"] = file_id
                elif type == "audio":
                    kwargs.update(
                        {"document_file_id": file_id, "title": "Document with Button"}
                    )
                elif type == "document":
                    kwargs.update(
                        {"document_file_id": file_id, "title": "Document with Button"}
                    )
                elif type == "sticker":
                    kwargs["sticker_file_id"] = file_id
                elif type == "voice":
                    kwargs.update(
                        {"voice_file_id": file_id, "title": "Voice with Button"}
                    )

                result.append(result_class(**kwargs))

        return result
    except Exception as er:
        logger.error(f"ERROR: {str(er)}, line: {sys.exc_info()[-1].tb_lineno}")


async def copy_inline_msg(result, inline_query):
    result.append(
        InlineQueryResultArticle(
            title="Copy Inline!",
            reply_markup=ikb(
                [
                    [
                        (
                            "🔐 Unlock Message 🔐",
                            f"copymsg_{int(inline_query.query.split()[1])}",
                            "callback_data",
                        )
                    ]
                ]
            ),
            input_message_content=InputTextMessageContent(
                "<b>🔒 This is private content</b>"
            ),
        )
    )
    return result


async def get_inline_help(result, inline_query):
    user_id = inline_query.from_user.id
    prefix = zohun.get_prefix(user_id)
    text_help = (
        await dB.get_var(user_id, "text_help") or f"**☛   <a href=https://t.me/ZonaHunterNew>𝐙𝐎𝐍𝐀 𝐇𝐔𝐍𝐓𝐄𝐑</a>   ☚**"
    )
    full = f"<a href=tg://user?id={inline_query.from_user.id}>{inline_query.from_user.first_name} {inline_query.from_user.last_name or ''}</a>"
    msg = """
<b>Inline Help
    Prefixes: <code>{}</code>
    Plugins: <code>{}</code>
    {}</b>
<blockquote>{}</blockquote>""".format(
        " ".join(prefix),
        len(HELPABLE),
        full,
        text_help,
    )
    result.append(
        InlineQueryResultArticle(
            title="Help Menu!",
            description=" Command Help",
            thumb_url=URL_LOGO,
            reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")),
            input_message_content=InputTextMessageContent(msg),
        )
    )
    return result


async def alive_inline(result, inline_query):
    self = inline_query.from_user.id
    pmper = None
    status = None
    start = datetime.now()
    ping = (datetime.now() - start).microseconds / 1000
    upnya = await get_time((time() - start_time))
    me = next((x for x in zohun._ubot), None)
    try:
        peer = zohun._get_my_peer[self]
        users = len(peer["pm"])
        group = len(peer["gc"])
    except Exception:
        users = random.randrange(await me.get_dialogs_count())
        group = random.randrange(await me.get_dialogs_count())
    await me.invoke(Ping(ping_id=0))
    seles = await dB.get_list_from_var(bot.me.id, "SELLER")
    if self in SUDO_OWNERS:
        status = "[Admins]"
    elif self in seles:
        status = "[Seller]"
    else:
        status = "[Costumer]"
    cekpr = await dB.get_var(self, "PMPERMIT")
    if cekpr:
        pmper = "enable"
    else:
        pmper = "disable"
    get_exp = await dB.get_expired_date(self)
    exp = get_exp.strftime("%d-%m-%Y")
    txt = f"""
<b>{BOT_NAME}</b>
    <b>status:</b> {status} 
      <b>dc_id:</b> <code>{me.me.dc_id}</code>
      <b>ping_dc:</b> <code>{str(ping).replace('.', ',')} ms</code>
      <b>anti_pm:</b> <code>{pmper}</code>
      <b>peer_users:</b> <code>{users} users</code>
      <b>peer_group:</b> <code>{group} group</code>
      <b>peer_ubot:</b> <code>{len(zohun._ubot)} ubot</code>
      <b>uptime:</b> <code>{upnya}</code>
      <b>expires:</b> <code>{exp}</code>
"""
    msge = f"<blockquote>{txt}</blockquote>"
    button = ikb([[("Close", "close alive")]])
    cekpic = await dB.get_var(self, "ALIVE_PIC")
    if not cekpic:
        result.append(
            InlineQueryResultArticle(
                title=BOT_NAME,
                description="Get Alive Of Bot.",
                input_message_content=InputTextMessageContent(msge),
                thumb_url=URL_LOGO,
                reply_markup=button,
            )
        )
    else:
        media = (
            InlineQueryResultVideo
            if cekpic.endswith(".mp4")
            else InlineQueryResultPhoto
        )
        url_ling = (
            {"video_url": cekpic, "thumb_url": cekpic}
            if cekpic.endswith(".mp4")
            else {"photo_url": cekpic}
        )
        result.append(
            media(
                **url_ling,
                title=BOT_NAME,
                description="Get Alive Of Bot.",
                thumb_url=URL_LOGO,
                caption=msge,
                reply_markup=button,
            )
        )
    return result


async def get_inline_note(result, inline_query):
    q = inline_query.query.split(None, 1)
    note = q[1]
    logger.info(f"{note}")
    gw = inline_query.from_user.id
    _id = state.get(gw, "in_notes")
    message = next((obj for obj in get_objects() if id(obj) == int(_id)), None)
    noteval = await dB.get_var(gw, note, "notes")
    if not noteval:
        return
    btn_close = ikb([[("Close", f"close get_note {note}")]])
    state.set("close_notes", "get_note", btn_close)
    try:
        tks = noteval["result"].get("text")
        type = noteval["type"]
        file_id = noteval["file_id"]
        note, button = ButtonUtils.parse_msg_buttons(tks)
        teks = await Tools.escape_filter(message, note, Tools.parse_words)
        button = ButtonUtils.create_inline_keyboard(button, gw)
        for row in btn_close.inline_keyboard:
            button.inline_keyboard.append(row)
        if type != "text":
            type_mapping = {
                "photo": InlineQueryResultCachedPhoto,
                "video": InlineQueryResultCachedVideo,
                "animation": InlineQueryResultCachedAnimation,
                "audio": InlineQueryResultCachedDocument,
                "document": InlineQueryResultCachedDocument,
                "sticker": InlineQueryResultCachedSticker,
                "voice": InlineQueryResultCachedVoice,
            }
            result_class = type_mapping[type]
            kwargs = {
                "id": str(uuid4()),
                "caption": teks,
                "reply_markup": button,
                "parse_mode": ParseMode.HTML,
            }

            if type == "photo":
                kwargs["photo_file_id"] = file_id
            elif type == "video":
                kwargs.update({"video_file_id": file_id, "title": "Video with Button"})
            elif type == "animation":
                kwargs["animation_file_id"] = file_id
            elif type == "audio":
                kwargs.update(
                    {"document_file_id": file_id, "title": "Document with Button"}
                )
            elif type == "document":
                kwargs.update(
                    {"document_file_id": file_id, "title": "Document with Button"}
                )
            elif type == "sticker":
                kwargs["sticker_file_id"] = file_id
            elif type == "voice":
                kwargs.update({"voice_file_id": file_id, "title": "Voice with Button"})

            result.append(result_class(**kwargs))
        else:
            result.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="Send Inline!",
                    reply_markup=button,
                    input_message_content=InputTextMessageContent(
                        teks,
                        parse_mode=ParseMode.HTML,
                    ),
                )
            )
        return result
    except Exception:
        logger.error(f"Error notes: {traceback.format_exc()}")

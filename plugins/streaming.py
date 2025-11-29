import asyncio
import os
from uuid import uuid4

from pyrogram.errors import FloodWait
from pytgcalls.exceptions import NotInCallError

from config import URL_LOGO
from Zohun import dB, zohun
from Zohun.database import state
from Zohun.helpers import (CMD, Emoji, Spotify, Tools, YoutubeSearch,
                          gen_qthumb, stream, telegram, youtube)
from Zohun.logger import logger
from Zohun import zohun
from Zohun.database import dB
from Zohun.helpers import CMD

__MODULES__ = "Music"
__HELP__ = """<blockquote>Command Help **Music**</blockquote>

<blockquote>**Basic command**</blockquote>
    **Use `v` for play video**
        `{0}play` (title)
        `{0}vplay` (title)
    **Resume playing**
        `{0}resume`
    **Pause playing**
        `{0}pause`
    **Skip playing**
        `{0}skip`
    **End playing**
        `{0}end`
        
<blockquote>**Channelplay command**</blockquote>
    **Playing to channel, use `v` for playing video**
        `{0}cplay` (title) 
        `{0}cvplay` title
    **Resume playing channel**
        `{0}cresume`
    **Pause playing channel**
        `{0}cpause`
    **Skip playing channel**
        `{0}cskip`
    **End playing channel**
        `{0}cend`
    **Linked channel to chat**
        `{0}channelplay linked`
    **Disable linked channel**
        `{0}channelplay disable`
    **Check linked playback channel**
        `{0}channelplay status`
    
<blockquote>**Other command**</blockquote>
    **Set volume playing, then try leave voice chat and join again**
        `{0}volume` (1-200)
    **Get playlist playing now**
        `{0}playlist`
    
<b>   {1}</b>"""


async def skip_songs(client, chat_id):
    emo = Emoji(client)
    await emo.get()
    await Tools.get_logo()
    group_calls = stream.get_active_call(chat_id, client.me.id)
    queue = stream.get_queue(chat_id, client.me.id)

    if not group_calls:
        return await client.send_message(
            chat_id, f"{emo.gagal}<b>No media is currently playing.</b>"
        )

    if not queue or len(queue) <= 1:
        return await client.send_message(
            chat_id, f"{emo.gagal}<b>No next track available.</b>"
        )
    pros = await client.send_message(
        chat_id, f"{emo.proses}<b>Processing next media...</b>"
    )
    next_song = stream.skip(chat_id, client.me.id)
    mode_ = next_song["mode"]
    type_ = next_song["media_type"]
    name_ = next_song["song_name"]
    singer_ = next_song["singer"]
    dur = next_song["dur"]
    media_link = next_song["url"]
    thumb_ = next_song["thumb"]
    file_path = next_song["file_name"]
    title_song = f'<a href="{media_link}">{name_}</a>'
    req_id = f"<a href='tg://user?id={client.me.id}'>{client.me.first_name} {client.me.last_name or ''}</a>"
    status = "5258077307985207053" if mode_ == "Video" else "5258020476977946656"

    try:
        streaming = await stream.run_stream(file_path, type_, quality="480p")
        await client.group_call.play(chat_id, streaming)
    except Exception as e:
        if "timed out" in str(e).lower() and type_ == "Video":
            try:
                logger.info(f"⚠️ 480p timeout, trying 360p...")
                streaming = await stream.run_stream(file_path, type_, quality="360p")
                await client.group_call.play(chat_id, streaming)
            except Exception as e2:
                if "timed out" in str(e2).lower():
                    try:
                        logger.info(f"⚠️ 360p timeout, using audio-only...")
                        streaming = await stream.run_stream(file_path, "Audio")
                        await client.group_call.play(chat_id, streaming)
                    except Exception as e3:
                        return await pros.edit(f"{emo.gagal}<b>Failed (tried 480p→360p→audio): {e3}</b>")
                else:
                    return await pros.edit(f"{emo.gagal}<b>Failed at 360p: {e2}</b>")
        else:
            return await pros.edit(f"{emo.gagal}<b>Failed: {str(e)}</b>")

    if thumb_:
        try:
            await client.send_photo(
                chat_id,
                photo=thumb_,
                caption=stream.play_text.format(
                    mode_, type_, status, title_song, singer_, dur, req_id
                ),
            )
        except Exception:
            await client.send_message(
                chat_id,
                stream.play_text.format(
                    mode_,
                    type_,
                    status,
                    title_song,
                    singer_,
                    dur,
                    req_id,
                ),
                disable_web_page_preview=True,
            )
            await pros.delete()
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(thumb_):
                os.remove(thumb_)


@zohun.group_call_ends()
async def _(client, update):
    chat_id = update.chat_id
    try:
        group_calls_data = stream.get_active_call(chat_id, client.mtproto_client.me.id)
    except Exception as e:
        logger.error(f"Failed to get active call data: {e}")
        return

    if not group_calls_data:
        stream.clear_queue(chat_id, client.mtproto_client.me.id)
        stream.remove_active_call(chat_id, client.mtproto_client.me.id)
        return await client.leave_call(chat_id)

    try:
        c, m = group_calls_data
        play_list = stream.get_queue(chat_id, c.me.id)
    except Exception as e:
        logger.error(f"Error fetching queue: {e}")
        return

    if not play_list or len(play_list) <= 1:
        stream.clear_queue(chat_id, c.me.id)
        stream.remove_active_call(chat_id, c.me.id)
        return await client.leave_call(chat_id)
    try:
        return await skip_songs(c, m.chat.id)
    except Exception as e:
        logger.error(f"Error in skip_cmd: {e}")


async def handle_spotify(client, message, emo, pros, media_link, mode):
    if not await Spotify.valid(media_link):
        await pros.edit(f"<blockquote>{emo.gagal} Link Spotify tidak valid!")
        return None

    if "track" in media_link:
        results = await Spotify.track(media_link)
        return results

    elif "playlist" in media_link:
        playlist = await Spotify.playlist(media_link)
        if not playlist:
            await pros.edit(
                f"<blockquote>{emo.gagal} Playlist kosong atau tidak ditemukan."
            )
            return None

        result = []
        for media in playlist:
            track_title = media["title"]
            yt_search = YoutubeSearch(track_title, max_results=1)
            await yt_search.fetch_results()
            track = {
                "file_path": yt_search.get_link(),
                "title": yt_search.get_title(),
                "uploader": yt_search.get_channel(),
                "duration": yt_search.get_duration(),
                "thumb": (yt_search.get_thumbnail()) or URL_LOGO,
                "url": yt_search.get_link(),
                "mode": mode,
            }
            result.append(track)

        return result

    elif "album" in media_link:
        album = await Spotify.album(media_link)
        if not album:
            await pros.edit(
                f"<blockquote>{emo.gagal} Album kosong atau tidak ditemukan."
            )
            return None
        return album

    elif "artist" in media_link:
        artist = await Spotify.artist(media_link)
        if not artist:
            await pros.edit(
                f"<blockquote>{emo.gagal} Tidak ada top tracks untuk artis ini."
            )
            return None
        return artist

    else:
        await pros.edit(f"<blockquote>{emo.gagal} Jenis link Spotify tidak dikenali!")
        return None


@CMD.UBOT("play|vplay|cplay|cvplay")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    audio_original = None
    uploade_r = None
    thumb_media = None
    media_title = None
    dur = None
    thumbs = None
    views = None
    pref = client.get_prefix(client.me.id)
    x = next(iter(pref), None)
    rep = message.reply_to_message
    if len(message.command) < 2 and not rep:
        return await message.reply(
            f"{emo.gagal}<b>Use the command by replying to a Music, Video, or provide a youtube title/link</b>"
        )

    pros = await message.reply(f"{emo.proses}<b>Processing media playback ..</b>")

    user_mention = (
        message.sender_chat.title if message.sender_chat else message.from_user.mention
    )

    cmd = message.command[0].lower()
    is_channel_mode = cmd.startswith("c") or cmd.startswith("cv")
    chat_id = (
        await dB.get_var(client.me.id, "CHANNEL")
        if is_channel_mode
        else message.chat.id
    )
    as_video = cmd.startswith("v") or cmd.startswith("cv")
    type_media = "Video" if as_video else "Audio"
    if is_channel_mode:
        chat = await dB.get_var(client.me.id, "CHANNEL")
        if not chat:
            return await pros.edit(
                f"{emo.gagal}<b>You have not linked a Channel for {message.chat.title or 'this Group'}.\n\nUse the following command to link a Channel:\n<code>{x}channelplay linked</code></b>"
            )

    mode = "Channel" if is_channel_mode or message.sender_chat else "Group"

    await pros.edit(f"{emo.proses}<b>Downloading {type_media} for mode: {mode} ..</b>")
    duration_limit = 5500000000
    size_limit = 2147483648
    audio_telegram = (rep.audio or rep.voice) if rep else None
    video_telegram = (rep.video or rep.document) if rep else None
    if audio_telegram:
        type_media = "Audio"
        if audio_telegram.file_size > size_limit:
            await pros.edit(
                f"{emo.warn}<b>Audio size is too large! The maximum media size limit is 2GB.</b>"
            )
            return
        if audio_telegram.duration > duration_limit:
            await pros.edit(
                f"{emo.warn}<b>Audio duration is too long! The maximum media duration limit is 3 hours.</b>"
            )
            return
        file_path = await telegram.get_filepath(audio=audio_telegram)
        try:
            if await telegram.download(client, message, pros, file_path):
                audio_original = file_path
            else:
                audio_original = file_path
        except Exception as e:
            await pros.edit(
                f"{emo.gagal}<b>Error occurred while downloading Telegram Audio:\n\n<code>{e}</code></b>"
            )
            return
        media_link = await telegram.get_link(message)
        media_title = await telegram.get_filename(audio_telegram, audio=True)
        dur = await telegram.get_duration(audio_telegram, file_path)
        file = (
            await client.download_media(rep.audio.thumbs[-1].file_id)
            if rep.audio and rep.audio.thumbs
            else None
        )
        thumbs = await Tools.upload_thumb(file) if file else URL_LOGO
        vidid = int(uuid4())
        views = Tools.gen_views()
        uploade_r = f"[Here]({rep.link})"

    elif video_telegram:
        type_media = "Video"
        if rep.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in Tools.formats:
                    await pros.edit(
                        f"{emo.warn}<b>Unknown media format! Here is the list of supported media Tools.formats: {' | '.join(Tools.formats)}</b>"
                    )
                    return
            except Exception as e:
                await pros.edit(
                    f"{emo.gagal}<b>Error occurred while downloading Telegram Video:\n\n<code>{e}</code></b>"
                )
                return
        if video_telegram.duration > size_limit:
            await pros.edit(
                f"{emo.warn}<b>Video size is too large! The maximum media size limit is 2GB.</b>"
            )
            return
        file_path = await telegram.get_filepath(video=video_telegram)
        try:
            if await telegram.download(client, message, pros, file_path):
                audio_original = file_path
            else:
                audio_original = file_path
        except Exception as e:
            await pros.edit(
                f"{emo.gagal}<b>Error occurred while downloading Telegram Video:\n\n<code>{e}</code></b>"
            )
            return
        media_link = await telegram.get_link(message)
        media_title = await telegram.get_filename(video_telegram)
        dur = await telegram.get_duration(video_telegram, file_path)
        file = (
            await client.download_media(rep.video.thumbs[-1].file_id)
            if rep.video and rep.video.thumbs
            else None
        )
        thumbs = await Tools.upload_thumb(file) if file else URL_LOGO
        uploade_r = f"[Here]({rep.link})"
        vidid = int(uuid4())
        views = Tools.gen_views()

    else:
        gt_txt = client.get_text(message)
        if await Spotify.valid(gt_txt):
            if "track" in gt_txt:
                data_spotify = await Spotify.track(gt_txt)
                if data_spotify is None:
                    return await pros.edit(f"{emo.gagal}**Sorry, try another url!!**")
                media_title = data_spotify.get("title")
                audio_original = data_spotify.get("file_path")
                vidid = data_spotify.get("vidid")
                dur = data_spotify.get("duration")
                thumbs = data_spotify.get("thumbs")
                uploade_r = data_spotify.get("uploader")
                uploade_r = ", ".join(uploade_r)
                media_link = data_spotify.get("url")
                views = Tools.gen_views()
            elif "playlist" in gt_txt:
                playlist = await Spotify.playlist(gt_txt)
                if playlist is None:
                    return await pros.edit(f"{emo.gagal}**Sorry, try another url!!**")
                await pros.edit(
                    f"{emo.proses}**Processing playlist with `{len(playlist)}` songs...**"
                )
                first_song = playlist[0]
                track_title = first_song["title"]
                yt_search = YoutubeSearch(track_title, max_results=1)
                await yt_search.fetch_results()
                media_title = yt_search.get_title()
                audio_original = yt_search.get_link()
                dur = yt_search.get_duration()
                uploade_r = yt_search.get_channel()
                media_link = yt_search.get_link()
                vidid = first_song["track_id"]
                thumbs = yt_search.get_thumbnail() or URL_LOGO
                views = Tools.gen_views()

                async def process_remaining_songs():
                    try:
                        await asyncio.sleep(5)
                        for media in playlist[1:]:
                            track_title = media["title"]
                            yt_search = YoutubeSearch(track_title, max_results=1)
                            await yt_search.fetch_results()
                            f_info = {
                                "song_name": yt_search.get_title(),
                                "file_name": yt_search.get_link(),
                                "singer": yt_search.get_channel(),
                                "dur": yt_search.get_duration(),
                                "url": yt_search.get_link(),
                                "thumb": yt_search.get_thumbnail() or URL_LOGO,
                                "mode": mode,
                                "media_type": type_media,
                            }
                            stream.add_to_queue(chat_id, client.me.id, f_info)
                            await asyncio.sleep(0.5)
                        await message.reply(
                            f"{emo.sukses}**Successfully added `{len(playlist)-1}` more songs to queue from playlist**"
                        )
                    except Exception as e:
                        logger.error(f"Error processing playlist: {str(e)}")

                asyncio.create_task(process_remaining_songs())
        elif await youtube.valid(gt_txt):
            (
                audio_original,
                _,
                media_title,
                duration,
                views,
                uploade_r,
                media_link,
                vidid,
                thumbs,
                _,
            ) = await youtube.download(gt_txt, as_video=as_video)
            dur = Tools.seconds_to_min(duration)
        else:
            yt_search = YoutubeSearch(gt_txt, max_results=1)
            await yt_search.fetch_results()
            media_link = yt_search.get_link()
            audio_original = yt_search.get_link()
            media_title = yt_search.get_title()
            uploade_r = yt_search.get_channel()
            dur = yt_search.get_duration()
            thumbs = yt_search.get_thumbnail()
            views = yt_search.get_views()
            vidid = yt_search.get_id()
            logger.info(f"Apa itu vidid: {vidid}")

    data = {
        "title": media_title,
        "duration": dur,
        "thumbnail": thumbs,
        "views": views,
        "channel": uploade_r,
    }
    state.set(client.me.id, "GEN_THUMB", data)
    thumb_media = await gen_qthumb(client, vidid)

    jadul = f"<a href='{media_link}'>{media_title}</a>"
    f_info = {
        "song_name": media_title,
        "file_name": audio_original,
        "singer": uploade_r,
        "dur": dur,
        "url": media_link,
        "thumb": thumb_media,
        "mode": mode,
        "media_type": type_media,
    }
    group_calls = stream.get_active_call(chat_id, client.me.id)
    if not group_calls:
        try:
            streaming = await stream.run_stream(audio_original, type_media, quality="480p")
            await client.group_call.play(chat_id, streaming)
        except Exception as e:
            if "timed out" in str(e).lower() and type_media == "Video":
                try:
                    logger.info(f"⚠️ 480p timeout, trying 360p...")
                    streaming = await stream.run_stream(audio_original, type_media, quality="360p")
                    await client.group_call.play(chat_id, streaming)
                except Exception as e2:
                    if "timed out" in str(e2).lower():
                        logger.info(f"⚠️ 360p timeout, using audio-only...")
                        streaming = await stream.run_stream(audio_original, "Audio")
                        await client.group_call.play(chat_id, streaming)
                    else:
                        raise e2
            else:
                raise e
        stream.add_active_call(chat_id, client.me.id, client, message)
        stream.add_to_queue(chat_id, client.me.id, f_info)
        durations_to_min = dur
        status = (
            "5258077307985207053" if type_media == "Video" else "5258020476977946656"
        )
        try:
            await message.reply_photo(
                photo=thumb_media,
                caption=stream.play_text.format(
                    mode,
                    type_media,
                    status,
                    jadul,
                    uploade_r,
                    durations_to_min,
                    user_mention,
                ),
            )
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            await message.reply(
                stream.play_text.format(
                    mode,
                    type_media,
                    status,
                    jadul,
                    uploade_r,
                    durations_to_min,
                    user_mention,
                ),
                disable_web_page_preview=True,
            )
        return await pros.delete()
    else:
        stream.add_to_queue(chat_id, client.me.id, f_info)
        data = stream.get_queue(chat_id, client.me.id)
        return await pros.edit(
            f"{emo.sukses}<b>Added to queue #{len(data)}:</b> {jadul} | {type_media}",
            disable_web_page_preview=True,
        )


@CMD.UBOT("resume|cresume")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    cmd = message.command[0].lower()
    is_channel_mode = cmd.startswith("c")
    chat_id = (
        await dB.get_var(client.me.id, "CHANNEL")
        if is_channel_mode
        else message.chat.id
    )
    group_calls = stream.get_active_call(chat_id, client.me.id)
    if not group_calls:
        return await message.reply(f"{emo.gagal}<b>Is not playing the media. </b>")
    queue = stream.get_queue(chat_id, client.me.id)
    current_media = queue[0]
    current_song_name = current_media["song_name"]
    current_singer = current_media["singer"]
    current_dur = current_media["dur"]
    resumed = "<b>🎧 Continued playing</b>\n"
    resumed += f"🎵 Title: <code>{current_song_name}</code>\n"
    resumed += f"🎤 Singer: <code>{current_singer}</code>\n"
    resumed += f"⏲️ Duration: <code>{current_dur}</code></b>\n"
    try:
        await client.group_call.resume_stream(chat_id)
        return await message.reply(f"{resumed}")
    except Exception as e:
        return await message.reply(
            f"{emo.gagal}<b>Failed to continue the media:</b>\n<code>{str(e)}</code>"
        )


@CMD.UBOT("end|cend")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    cmd = message.command[0].lower()
    is_channel_mode = cmd.startswith("c")
    chat_id = (
        await dB.get_var(client.me.id, "CHANNEL")
        if is_channel_mode
        else message.chat.id
    )
    group_calls = stream.get_active_call(chat_id, client.me.id)
    if not group_calls:
        return await message.reply(f"{emo.gagal}<b>Is not playing the media.</b>")
    try:
        await client.group_call.leave_call(chat_id)
        stream.clear_queue(chat_id, client.me.id)
        stream.remove_active_call(chat_id, client.me.id)
        return await message.reply(
            f"{emo.sukses}<b>Successfully stopped the media.</b>"
        )
    except NotInCallError:
        return await message.reply(f"{emo.gagal}<b>Is not playing the media.</b>")
    except Exception as e:
        return await message.reply(
            f"{emo.gagal}<b>Failed to stop the media:\n<code>{str(e)}</code></b>"
        )


@CMD.UBOT("pause|cpause")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    cmd = message.command[0].lower()
    is_channel_mode = cmd.startswith("c")
    chat_id = (
        await dB.get_var(client.me.id, "CHANNEL")
        if is_channel_mode
        else message.chat.id
    )
    group_calls = stream.get_active_call(chat_id, client.me.id)
    if not group_calls:
        return await message.reply(f"{emo.gagal}<b>Is not playing the media.</b>")
    queue = stream.get_queue(chat_id, client.me.id)
    current_media = queue[0]
    current_song_name = current_media["song_name"]
    current_singer = current_media["singer"]
    current_dur = current_media["dur"]
    paused = "<b>🎧 Paused playing</b>\n"
    paused += f"🎵 Title: <code>{current_song_name}</code>\n"
    paused += f"🎤 Singer: <code>{current_singer}</code>\n"
    paused += f"⏲️ Duration: <code>{current_dur}</code></b>\n"
    try:
        await client.group_call.pause_stream(chat_id)
        return await message.reply(f"{paused}")
    except Exception as e:
        return await message.reply(f"Failed to break the media:</b>\n<code>{e}</code>")


@CMD.UBOT("skip|cskip")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    await Tools.get_logo()
    cmd = message.command[0].lower()
    is_channel_mode = cmd.startswith("c")
    chat_id = (
        await dB.get_var(client.me.id, "CHANNEL")
        if is_channel_mode
        else message.chat.id
    )
    group_calls = stream.get_active_call(chat_id, client.me.id)
    queue = stream.get_queue(chat_id, client.me.id)

    if not group_calls:
        return await message.reply(f"{emo.gagal}<b>While no media is played.</b>")

    if not queue or len(queue) <= 1:
        return await message.reply(f"{emo.gagal}<b>There is no next track.</b>")
    pros = await message.reply(
        f"{emo.proses}<b>The process of turning the next media...</b>"
    )
    c, m = group_calls

    next_song = stream.skip(chat_id, client.me.id)
    mode_ = next_song["mode"]
    type_ = next_song["media_type"]
    name_ = next_song["song_name"]
    singer_ = next_song["singer"]
    dur = next_song["dur"]
    media_link = next_song["url"]
    thumb_ = next_song["thumb"]
    file_path = next_song["file_name"]
    title_song = f'<a href="{media_link}">{name_}</a>'
    req_id = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
    status = "5258077307985207053" if type_ == "Video" else "5258020476977946656"

    try:
        streaming = await stream.run_stream(file_path, type_, quality="480p")
        await client.group_call.play(chat_id, streaming)
    except Exception as e:
        if "timed out" in str(e).lower() and type_ == "Video":
            try:
                logger.info(f"⚠️ 480p timeout, trying 360p...")
                streaming = await stream.run_stream(file_path, type_, quality="360p")
                await client.group_call.play(chat_id, streaming)
            except Exception as e2:
                if "timed out" in str(e2).lower():
                    try:
                        logger.info(f"⚠️ 360p timeout, using audio-only...")
                        streaming = await stream.run_stream(file_path, "Audio")
                        await client.group_call.play(chat_id, streaming)
                    except Exception as e3:
                        return await pros.edit(f"{emo.gagal}<b>Failed (tried 480p→360p→audio): {e3}</b>")
                else:
                    return await pros.edit(f"{emo.gagal}<b>Failed at 360p: {e2}</b>")
        else:
            return await pros.edit(f"{emo.gagal}<b>Failed: {str(e)}</b>")
    if thumb_:
        try:
            await message.reply_photo(
                photo=thumb_,
                caption=stream.play_text.format(
                    mode_, type_, status, title_song, singer_, dur, req_id
                ),
            )
        except Exception:
            await message.reply(
                stream.play_text.format(
                    mode_,
                    type_,
                    status,
                    title_song,
                    singer_,
                    dur,
                    req_id,
                    disable_web_page_preview=True,
                ),
            )
            await pros.delete()
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(thumb_):
                os.remove(thumb_)


@CMD.UBOT("playlist|cplaylist")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    logo = await Tools.get_logo()
    cmd = message.command[0].lower()
    is_channel_mode = cmd.startswith("c")
    chat_id = (
        await dB.get_var(client.me.id, "CHANNEL")
        if is_channel_mode
        else message.chat.id
    )
    group_calls = stream.get_active_call(chat_id, client.me.id)
    if not group_calls:
        return await message.reply(f"{emo.gagal}<b>While no media is played.</b>")

    pros = await message.reply(
        f"{emo.proses}<b>The process of taking a playlist...</b>"
    )

    current_media, next_media_list = stream.get_current_and_next_media(
        chat_id, client.me.id
    )
    if not current_media:
        return await pros.edit(f"{emo.gagal}<b>There is no media in the queue.</b>")

    current_song_name = current_media["song_name"]
    current_singer = current_media["singer"]
    current_dur = current_media["dur"]
    current_thumb = current_media.get("thumb", None)

    playlist = "<b>🎧 Currently playing</b>\n"
    playlist += f"🎵 Title: <code>{current_song_name}</code>\n"
    playlist += f"🎤 Singer: <code>{current_singer}</code>\n"
    playlist += f"⏲️ Duration: <code>{current_dur}</code>\n\n"

    if next_media_list:
        playlist += "<b>🎧 Playlist</b>\n"
        for count, track in enumerate(next_media_list, start=1):
            lagu = track["song_name"]
            if count == len(next_media_list):
                playlist += f"<code>{lagu}</code>\n"
            else:
                playlist += f"<code>{lagu}</code>\n"

    try:
        if current_thumb:
            await message.reply_photo(
                photo=current_thumb,
                caption=f"{playlist}",
            )
        else:
            await message.reply_photo(
                photo=logo,
                caption=f"{playlist}",
            )
        return await pros.delete()
    except Exception as e:
        return await pros.edit(f"{playlist}")


@CMD.UBOT("volume|cvolume")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    cmd = message.command[0].lower()
    is_channel_mode = cmd.startswith("c")
    chat_id = (
        await dB.get_var(client.me.id, "CHANNEL")
        if is_channel_mode
        else message.chat.id
    )
    nilai = client.get_text(message)
    if not nilai:
        return await message.reply(
            f"{emo.gagal}<b>Give numbers from 1 - 200 to change the volume of media.</b>"
        )
    group_calls = stream.get_active_call(chat_id, client.me.id)
    if not group_calls:
        return await message.reply(f"{emo.gagal}<b>Is not playing the media.</b>")
    try:
        await client.group_call.change_volume_call(chat_id, int(nilai))
        return await message.reply(
            f"{emo.sukses}<b>Succeeded in setting the volume of the media to be: <code>{nilai}%</code></b>"
        )
    except Exception as e:
        if "USER_VOLUME_INVALID" in str(e):
            return await message.reply(
                f"{emo.gagal}<b>Give numbers from 1 - 200 to change the volume of media.</b>"
            )
        return await message.reply(
            f"{emo.gagal}<b>Failed to use volume:\n<code>{str(e)}</code></b>"
        )


@CMD.UBOT("channelplay")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    pref = client.get_prefix(client.me.id)
    x = next(iter(pref))
    if len(message.command) not in [2, 3]:
        return await message.reply(
            f"{emo.warn}<b>You can play music on channels that are already connected to {message.chat.title or 'chat room'}.\n\nUse the following command if the channel is connected:\n<code>{x}channelplay linked</code></b>"
        )
    query = message.text.split(None, 2)[1].lower().strip()
    if str(query) == "disable":
        await dB.remove_var(client.me.id, "CHANNEL")
        return await message.reply(
            f"{emo.sukses}<b>Managed to stop and remove playback through the channel.</b>"
        )

    elif str(query) == "linked":
        try:
            chat = await client.get_chat(message.chat.id)
        except Exception as e:
            return await message.reply(
                f"{emo.gagal}<b>Error:\n<code>{str(e)}</code></b>"
            )

        if chat and chat.linked_chat:
            channel_id = chat.linked_chat.id
            try:
                members = await client.get_chat_member(channel_id, client.me.id)
                if not members.privileges.can_manage_video_chats:
                    return await message.reply(
                        f"{emo.gagal}<b>Make me an admin with permission to manage voting chat.</b>"
                    )
                await dB.set_var(client.me.id, "CHANNEL", channel_id)

                return await message.reply(
                    f"{emo.sukses}<b>Successfully set {chat.linked_chat.title} as a music playback channel.</b>"
                )
            except Exception as e:
                return await message.reply(
                    f"{emo.gagal}<b>There is an error:\n\n<code>{e}</code></b>"
                )
        else:
            if len(message.comand) < 3:
                return await message.reply(
                    f"{emo.gagal}**Please user command `{message.text.split()[0]} linked` @kynansupport"
                )
            chat_id = message.text.split()[3]
            try:
                if "/+" in str(chat_id):
                    gid = await client.get_chat(str(chat_id))
                    chat_id = int(gid.id)
                elif "t.me/" in str(chat_id) or "@" in str(chat_id):
                    chat_id = chat_id.replace("https://t.me/", "")
                    gid = await client.get_chat(str(chat_id))
                    chat_id = int(gid.id)
                else:
                    chat_id = int(chat_id)
                await dB.set_var(client.me.id, "CHANNEL", chat_id)
                return await message.reply(
                    f"{emo.sukses}<b>Successfully set {chat_id} as a music playback channel.</b>"
                )
            except Exception as err:
                return await message.reply(
                    f"{emo.gagal}<b>Cannot connect {chat_id}\nError: `{str(err)}`</b>"
                )

    elif str(query) == "status":
        mode = await dB.get_var(client.me.id, "CHANNEL")
        if not mode:
            return await message.reply(f"{emo.gagal}<b>No channel is linked.</b>")
        else:
            try:
                chat = await client.get_chat(int(mode))
                return await message.reply(
                    f"{emo.sukses}<b>Group {message.chat.title or 'this group'} is connected to:</b> {chat.title}"
                )
            except Exception as e:
                return await message.reply(
                    f"{emo.gagal}<b>There is an error:\n\n<code>{str(e)}</code></b>"
                )

    else:
        return await message.reply(f"{emo.gagal}<b>Invalid query!</b>")

import os
import re
import time
import traceback
from datetime import timedelta

import wget

from Zohun import bot
from Zohun.helpers import CMD, Emoji, YoutubeSearch, youtube
from Zohun.logger import logger

__MODULES__ = "Youtube"
__HELP__ = """<blockquote>Command Help **Youtube**</blockquote>

<blockquote>**Download the audio**</blockquote>
    **Download audio from youtube, you can use title or url**
        `{0}song` (url/title)
        
<blockquote>**Download the video**</blockquote>
    **Download video from youtube, you can use title or url**
        `{0}video` (url/title)
    
<b>   {1}</b>
"""


@CMD.UBOT("video|song")
async def _(client, message):
    try:
        emo = Emoji(client)
        await emo.get()
        pref = client.get_prefix(client.me.id)
        x = next(iter(pref))
        cmd = message.command[0].lower()
        now = time.time()
        proses_ = await emo.get_costum_text()
        if len(message.command) < 2 and not message.reply_to_message:
            return await message.reply_text(
                f"{emo.gagal}<b>Please give query or link:\n\nExample <code>{x}{cmd}</code> [title or link]</b>",
            )
        pros = await message.reply_text(f"{emo.proses}<b>{proses_[4]}</b>")
        kueri = client.get_text(message)
        if re.match(r"^https?://", kueri):
            link = kueri
        else:
            try:
                yt_search = YoutubeSearch(kueri, max_results=1)
                await yt_search.fetch_results()
                link = yt_search.get_link()
                logger.info(f"Link: {link}")
            except Exception as error:
                return await pros.edit(
                    f"{emo.gagal}<b>ERROR:</b><code>{str(error)}</code>"
                )
        as_video = message.command[0].lower().startswith("v")
        pros = await pros.edit(
            f"{emo.proses}<b>Try to downloading {'video' if as_video else 'audio'}...</b>"
        )

        try:
            (
                file_name,
                inpoh,
                title,
                duration,
                views,
                channel,
                url,
                _,
                thumb,
                data_ytp,
            ) = await youtube.download(link, as_video=as_video)

            if isinstance(duration, str):
                duration = duration.replace(".", "")
            duration = int(duration)

        except Exception as error:
            return await pros.edit(f"{emo.gagal}<b>ERROR:</b><code>{str(error)}</code>")

        thumbnail = wget.download(thumb)
        kapten = data_ytp.format(
            inpoh,
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            bot.me.mention,
        )

        if as_video:
            await client.send_video(
                message.chat.id,
                video=file_name,
                thumb=thumbnail,
                file_name=title,
                duration=duration,
                supports_streaming=True,
                caption=f"{kapten}",
                progress=youtube.progress,
                progress_args=(
                    pros,
                    now,
                    f"{emo.proses}<b>Trying to upload...</b>",
                    f"{file_name}",
                ),
                reply_to_message_id=message.id,
            )
        else:
            await client.send_audio(
                message.chat.id,
                audio=file_name,
                thumb=thumbnail,
                file_name=title,
                performer=channel,
                duration=duration,
                caption=f"{kapten}",
                progress=youtube.progress,
                progress_args=(
                    pros,
                    now,
                    f"{emo.proses}<b>Trying to upload...</b>",
                    f"{file_name}",
                ),
                reply_to_message_id=message.id,
            )
        await pros.delete()
        if os.path.exists(thumbnail):
            os.remove(thumbnail)
        if os.path.exists(file_name):
            os.remove(file_name)
    except Exception as er:
        logger.error(f"Error: {traceback.format_exc()}")

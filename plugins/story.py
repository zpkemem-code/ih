__MODULES__ = "Story"
__HELP__ = """<blockquote>Command Help **Story**</blockquote>

<blockquote>**Post story**</blockquote>
    **You can post media to telegram story** 
        `{0}story post` (reply media)
    
<blockquote>**Check story**</blockquote>
    **Get all stories on your account**
        `{0}story cek`

<blockquote>**Delete story**</blockquote>
    **You can delete story with this command**
        `{0}story del` (strory id)

<blockquote>**Get or steal story**</blockquote>
    **You can steal story from user**
        `{0}story get` (url)

<b>   {1}</b>
"""


import traceback

from Zohun.helpers import CMD, Emoji, Tools
from Zohun.logger import logger


@CMD.UBOT("story")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_[4]}**")
    args = ["cek", "del", "get", "post"]
    query = message.command[1]
    if len(message.command) < 2 and query not in args:
        return await proses.edit(
            f"{em.gagal}<b>Please give query [post, cek, get, or del]</b>"
        )
    prefix = client.get_prefix(client.me.id)
    if query == "cek":
        text = f"{em.owner}<b>Your stories:</b>\n\n"
        async for story in client.get_all_stories():
            if story.from_user.id == client.me.id:
                story_link = await client.export_story_link("me", story.id)
                text += f"{em.sukses}<b>• Story ID: `{story.id}` | Story Link: [Click Here]({story_link})</b>\n"
        await message.reply(text, disable_web_page_preview=True)
        return await proses.delete()

    elif query == "del":
        if len(message.command) < 3:
            return await proses.edit(
                f"<b>{em.gagal} That's not how it works!! Provide your story ID.\nExample: `{prefix[0]}story del` 5\n\nOr you can type `{prefix[0]}story cek` to see your story IDs!! </b>"
            )
        story_id = message.text.split()[2]
        if not story_id.isnumeric():
            return await proses.edit(
                f"{em.gagal}<b>ID should be a number, not letters or symbols.</b>"
            )
        await client.delete_stories(story_ids=int(story_id))
        return await proses.edit(
            f"{em.sukses}<b>Successfully deleted Story ID: `{story_id}`!!</b>"
        )

    elif query == "get":
        if len(message.command) < 3:
            return await proses.edit(f"{em.gagal}**Please give link story!**")
        link = message.text.split()[2]
        if "/s/" not in link:
            return await proses.edit(
                f"{em.gagal}<b>Please provide a valid Telegram stories link!!</b>"
            )
        user, story_id = Tools.extract_story_link(link)
        story = await client.get_stories(user, story_id)
        await Tools.download_media(story, client, proses, message, True)
        return await proses.delete()

    elif query == "post":
        reply = message.reply_to_message
        if not reply or reply and not reply.media:
            return await proses.edit(f"{em.gagal}**Please reply to photo or video**")
        kwargs = reply.photo.file_id or reply.video.file_id
        text = reply.caption or ""
        try:
            target = "me" if len(message.command) < 3 else message.text.split()[2]
            story = await client.send_story(
                target, kwargs, caption=text
            )
            this = await client.export_story_link("me", story.id)
            return await proses.edit(
                f"{em.sukses}<b>Succesfully upload to [Story]({this})!</b>",
                disable_web_page_preview=True,
            )
        except Exception as e:
            logger.error(f"Error: {traceback.format_exc()}")
            return await proses.edit(f"{em.gagal}**ERROR:** {str(e)}")
    else:
        return await proses.edit(
            f"{em.gagal}<b>Please give query [post, cek, get, or del]</b>"
        )

import asyncio

from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from Zohun.helpers import CMD, Emoji, task

from .admins import admin_check


@CMD.UBOT("all|tagall")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_[4]}**")
    botol = await admin_check(message, client.me.id)
    if not botol:
        return await proses.edit(f"{em.gagal}**You are not an admin in this group!**")

    task_id = task.start_task()
    replied = message.reply_to_message
    prefix = client.get_prefix(client.me.id)
    if len(message.command) < 2 and not replied:
        return await proses.edit(f"{em.gagal}**Please reply to text or give text!**")

    await proses.edit(
        f"{em.proses}<i>Task mention running #<code>{task_id}</code>. Type <code>{prefix[0]}cancel {task_id}</code> to cancel mention! Will timeout after 5 minutes.</i>"
    )

    async def tag_members():
        if replied:
            usernum = 0
            usertxt = ""
            try:
                async for m in client.get_chat_members(message.chat.id):
                    if not task.is_active(task_id):
                        return await proses.edit(
                            f"{em.gagal}**Task #{task_id} has been cancelled!**"
                        )

                    if m.user.is_deleted or m.user.is_bot:
                        continue
                    usernum += 1
                    usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                    if usernum == 7:
                        await replied.reply_text(
                            usertxt,
                            disable_web_page_preview=True,
                        )
                        await asyncio.sleep(1)
                        usernum = 0
                        usertxt = ""
                if usernum != 0:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                    )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            finally:
                task.end_task(task_id)
        else:
            try:
                usernum = 0
                usertxt = ""
                text = message.text.split(maxsplit=1)[1]
                async for m in client.get_chat_members(message.chat.id):
                    if m.user.is_deleted or m.user.is_bot:
                        continue
                    if not task.is_active(task_id):
                        await proses.edit(
                            f"{em.gagal}**Task #{task_id} has been cancelled!**"
                        )
                        return
                    usernum += 1
                    usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                    if usernum == 7:
                        await client.send_message(
                            message.chat.id,
                            f"{text}\n{usertxt}",
                            disable_web_page_preview=True,
                        )
                        await asyncio.sleep(2)
                        usernum = 0
                        usertxt = ""
                if usernum != 0:
                    await client.send_message(
                        message.chat.id,
                        f"<b>{text}</b>\n\n{usertxt}",
                        disable_web_page_preview=True,
                    )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            finally:
                task.end_task(task_id)

    try:
        await asyncio.wait_for(tag_members(), timeout=300)  # 300 seconds = 5 minutes
    except asyncio.TimeoutError:
        task.end_task(task_id)
        await proses.edit(f"{em.gagal}**Task #{task_id} timed out after 5 minutes!**")
        return

    return await proses.delete()


@CMD.UBOT_REGEX(r"^(@admins)")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_[4]}**")
    task_id = task.start_task()
    replied = message.reply_to_message
    prefix = client.get_prefix(client.me.id)
    if not replied and len(message.text.split()) == 1:
        return await proses.edit(f"{em.gagal}**Please reply to text or give text!**")
    await proses.edit(
        f"{em.proses}<i>Task mention running #<code>{task_id}</code>. Type <code>{prefix[0]}cancel {task_id}</code> to cancel mention!</i>"
    )
    if replied:
        usernum = 0
        usertxt = ""
        try:
            async for m in client.get_chat_members(
                message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if not task.is_active(task_id):
                    return await proses.edit(
                        f"{em.gagal}**Task #{task_id} has been cancelled!**"
                    )
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(1)
                    usernum = 0
                    usertxt = ""
            if usernum != 0:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        finally:
            task.end_task(task_id)
    else:
        usernum = 0
        usertxt = ""
        try:
            text = message.text.split(maxsplit=1)[1]
            async for m in client.get_chat_members(
                message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if not task.is_active(task_id):
                    return await proses.edit(
                        f"{em.gagal}**Task #{task_id} has been cancelled!**"
                    )
                if m.user.is_deleted or m.user.is_bot:
                    continue
                usernum += 1
                usertxt += f"[{m.user.first_name}](tg://user?id={m.user.id})  "
                if usernum == 7:
                    await client.send_message(
                        message.chat.id,
                        f"{text}\n{usertxt}",
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(2)
                    usernum = 0
                    usertxt = ""
            if usernum != 0:
                await client.send_message(
                    message.chat.id,
                    f"<b>{text}</b>\n\n{usertxt}",
                    disable_web_page_preview=True,
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        finally:
            task.end_task(task_id)
    return await proses.delete()


__MODULES__ = "Tagall"
__HELP__ = """<blockquote>Command Help **Tagall**</blockquote>

<blockquote>**Mention members**</blockquote>
    **Tag member from chat**
        `{0}tagall` (text/reply text)

<blockquote>**Mention admins**</blockquote>
    **Tag only admins from chat**
        `@admins` (text/reply text)

<blockquote>**Stop mention**</blockquote>
    **Stop task tag**
        `{0}cancel` (taskid)

<b>   {1}</b>
"""

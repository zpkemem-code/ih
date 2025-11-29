from Zohun.database import dB
from Zohun import bot
from Zohun.helpers import CMD, Emoji

__MODULES__ = "Autoread"
__HELP__ = """<blockquote>Command Help **AutoRead**</blockquote>

<blockquote>**Basic commands**</blockquote>
    **This command for autoread group messages**
        `{0}autoread group on`
        `{0}autoread group off`
    **This command for autoread private messages**
        `{0}autoread private on`
        `{0}autoread private off`
    **This command for autoread channel messages**
        `{0}autoread channel on`
        `{0}autoread channel off`
    **This command for autoread bot messages**
        `{0}autoread bot on`
        `{0}autoread bot off`
    **This command for autoread tagged messages**
        `{0}autoread tag on`
        `{0}autoread tag off`
    **This command for autoread all messages**
        `{0}autoread all on`
        `{0}autoread all off`
    **This command for settings autoread time**
        `{0}autoread time 3600`

<b>   {1}</b>
"""


@CMD.UBOT("autoread")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    mek = await message.reply(f"{em.proses}**{proses_[4]}**")
    if len(message.command) < 3:
        await mek.edit(f"{em.gagal}**Please type see help for module.**")
        return
    biji, peler, jembut = message.command[:3]
    if peler.lower() == "time":
        if jembut.isnumeric():
            lmt = int(jembut)
            await dB.set_var(client.me.id, "TIME_READ", lmt)
            await mek.edit(f"{em.sukses}Time autoread set to: `{lmt}`")
            return
        else:
            await mek.edit(f"{em.gagal}Please give me seconds time!!")
            return
    elif peler.lower() == "group":
        if jembut.lower() == "on":
            await dB.set_var(client.me.id, "READ_GC", True)
            await mek.edit(f"{em.sukses}**Successfully turned on group autoread.**")
            return
        else:
            await dB.remove_var(client.me.id, "READ_GC")
            await mek.edit(
                f"{em.sukses}**Autoread {peler} was successfully disabled.**"
            )
            return
    elif peler.lower() == "private":
        if jembut.lower() == "on":
            await dB.set_var(client.me.id, "READ_US", True)
            await mek.edit(f"{em.sukses}**Successfully turned on user autoread.**")
            return
        else:
            await dB.remove_var(client.me.id, "READ_US")
            await mek.edit(
                f"{em.sukses}**Autoread {peler} was successfully disabled.**"
            )
            return
    elif peler.lower() == "bot":
        if jembut.lower() == "on":
            await dB.set_var(client.me.id, "READ_BOT", True)
            await mek.edit(f"{em.sukses}**Successfully turned on autoread bot.**")
            return
        else:
            await dB.remove_var(client.me.id, "READ_BOT")
            await mek.edit(
                f"{em.sukses}**Autoread {peler} was successfully disabled.**"
            )
            return
    elif peler.lower() == "channel":
        if jembut.lower() == "on":
            await dB.set_var(client.me.id, "READ_CH", True)
            await mek.edit(f"{em.sukses}**Successfully turned on autoread channel.**")
            return
        else:
            await dB.remove_var(client.me.id, "READ_CH")
            await mek.edit(
                f"{em.sukses}**Autoread {peler} was successfully disabled.**"
            )
            return

    elif peler.lower() == "tag":
        if jembut.lower() == "on":
            await dB.set_var(client.me.id, "READ_MENTION", True)
            await mek.edit(f"{em.sukses}**Successfully turned on autoread mention.")
            return
        else:
            await dB.remove_var(client.me.id, "READ_MENTION")
            await mek.edit(
                f"{em.sukses}**Autoread {peler} was successfully disabled.**"
            )
            return
    elif peler.lower() == "all":
        if jembut.lower() == "on":
            await dB.set_var(client.me.id, "READ_ALL", True)
            await mek.edit(f"{em.sukses}**Successfully turned on autoread all.**")
            return
        else:
            await dB.remove_var(client.me.id, "READ_ALL")
            await mek.edit(
                f"{em.sukses}**Autoread {peler} was successfully disabled.**"
            )
            return
    else:
        await mek.edit(f"{em.gagal}**Please enter the query correctly!!**")
        return

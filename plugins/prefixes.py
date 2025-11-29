from Zohun.database import dB
from Zohun.helpers import CMD, Emoji

__MODULES__ = "Prefix"
__HELP__ = """<blockquote>Command Help **Prefix**</blockquote>

<blockquote>**Set handler userbot**</blockquote>
    **You can set handler or trigger to your userbot**
        `{0}setprefix` (trigger/symbol)

<b>   {1}</b>
"""


@CMD.UBOT("setprefix")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await emo.get_costum_text()
    pros = await message.reply(f"{emo.proses}**{proses_}**")
    if len(message.command) < 2:
        m = message.text.split()[0]
        return await pros.edit(
            f"{emo.gagal}<b>Please provide the Prefix/Handler you want to use.</b>\n\n"
            f"Example:\n<code>{m}setprefix , . ? : ;</code>\n\n"
            f"Or use <code>none</code> if you want to use commands without a Prefix/Handler."
        )
    ub_prefix = []
    for prefix in message.command[1:]:
        if prefix.lower() == "none":
            ub_prefix.append("")
        else:
            ub_prefix.append(prefix)
    try:
        client.set_prefix(client.me.id, ub_prefix)
        await dB.set_pref(client.me.id, ub_prefix)
        parsed_prefix = (
            " ".join(f"<code>{prefix}</code>" for prefix in ub_prefix if prefix)
            or "none"
        )
        return await pros.edit(
            f"{emo.sukses}<b>Successfully set the Prefix to: {parsed_prefix}</b>"
        )
    except Exception as error:
        return await pros.edit(f"{emo.gagal}<b>ERROR: <code>{error}</code></b>")

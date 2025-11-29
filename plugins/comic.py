__MODULES__ = "Comic"
__HELP__ = """<blockquote>Command Help **Comic**</blockquote>

<blockquote>**Basic commands**</blockquote>
    **Get news update Comic**
        `{0}comic`

<b>   {1}</b>
"""

from uuid import uuid4

import config
from Zohun import bot
from Zohun.database import state
from Zohun.helpers import CMD, ButtonUtils, Tools


@CMD.UBOT("comic")
async def _(_, message):
    try:
        url = f"https://api.maelyn.tech/api/infomatic/comic?apikey={config.API_MAELYN}"
        response = await Tools.fetch.get(url)
        if response.status_code == 200:
            data = response.json()["result"]["data"]
            uniq = f"{str(uuid4())}"
            state.set(uniq.split("-")[0], uniq.split("-")[0], data)
            try:
                inline = await ButtonUtils.send_inline_bot_result(
                    message,
                    message.chat.id,
                    bot.me.username,
                    f"inline_comic {uniq.split('-')[0]}",
                )
                if inline:
                    return await message.delete()
            except Exception as er:
                return await message.reply(f"**ERROR**: {str(er)}")
        else:
            return await message.reply(
                f"**Error with status `{response.status_code}`**"
            )
    except Exception as er:
        return await message.reply(f"**ERROR**: {str(er)}")

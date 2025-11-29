__MODULES__ = "G-news"
__HELP__ = """<blockquote>Command Help **G-News**</blockquote>

<blockquote>**Basic Commands**</blockquote>
    **You can get news from Google News**
        `{0}gnews`
        
<b>   {1}</b>
"""

from uuid import uuid4

import config
from Zohun import bot
from Zohun.database import state
from Zohun.helpers import CMD, ButtonUtils, Tools


@CMD.UBOT("gnews")
async def _(client, message):
    arg = client.get_text(message)
    if not arg:
        return await message.reply(
            f"<b>Please give word!!\nExample: `{message.text.split()[0]} Pendiri Telegram`</b>"
        )
    api_key = config.API_MAELYN
    headers = {"mg-apikey": api_key}
    params = {"q": arg}
    url = "https://api.maelyn.tech/api/gnews"
    response = await Tools.fetch.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()["result"]
        uniq = f"{str(uuid4())}"
        state.set(uniq.split("-")[0], uniq.split("-")[0], data)
        try:
            inline = await ButtonUtils.send_inline_bot_result(
                message,
                message.chat.id,
                bot.me.username,
                f"inline_gnews {uniq.split('-')[0]}",
            )
            if inline:
                return await message.delete()
        except Exception as er:
            return await message.reply(f"**ERROR**: {str(er)}")
    else:
        return await message.reply(f"**Error with status `{response.status_code}`**")

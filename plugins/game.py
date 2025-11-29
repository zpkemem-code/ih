import random

from Zohun.helpers import CMD, Emoji

__MODULES__ = "Games"
__HELP__ = """<blockquote>Command Help **Games**</blockquote>

<blockquote>**Send inline game**</blockquote>
    **You can send inline catur game to chat**
        `{0}catur`
    **For this command, you can send inline random games to this chat**
        `{0}game`
    
<b>   {1}</b>
"""


@CMD.UBOT("catur")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    try:
        x = await client.get_inline_bot_results("GameFactoryBot")
        msg = message.reply_to_message or message
        await client.send_inline_bot_result(
            message.chat.id,
            x.query_id,
            x.results[0].id,
            reply_to_message_id=msg.id,
        )
    except Exception as error:
        return await message.reply(f"{em.gagal}Error: {str(error)}")


@CMD.UBOT("game")
async def _(client, message):
    try:
        x = await client.get_inline_bot_results("gamee")
        msg = message.reply_to_message or message
        random_index = random.randint(0, len(x.results) - 1)
        await client.send_inline_bot_result(
            message.chat.id,
            x.query_id,
            x.results[random_index].id,
            reply_to_message_id=msg.id,
        )
    except Exception as error:
        await message.reply(error)

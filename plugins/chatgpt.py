from uuid import uuid4

from config import API_BOTCHAX
from Zohun import bot
from Zohun.database import state
from Zohun.helpers import CMD, ButtonUtils, Emoji, Message, Tools

__MODULES__ = "Chatgpt"
__HELP__ = """<blockquote>Command Help **ChatGpt**</blockquote>

<blockquote>**Chat with chatgpt**</blockquote>
    **You can chat to chatgpt**
        `{0}ask` (prompt)

<blockquote>**Audio with chatgpt**</blockquote>
    **You can chat to chatgpt asnwer with audio**
        `{0}ask` (prompt)

<blockquote>**Stop converstation**</blockquote>
    **Stop the converstation chatgpt**
        `{0}stop ask`

<b>   {1}</b>
"""


CONVERSATIONS = {}


@CMD.UBOT("ask|ai")
async def ai_chat(client, message):
    em = Emoji(client)
    await em.get()

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply(
            f"{em.gagal} **Please reply to message text or give message!**"
        )

    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id not in CONVERSATIONS:
        CONVERSATIONS[user_id] = [
            {
                "role": "system",
                "content": "Kamu adalah asisten paling canggih yang berbahasa Indonesia gaul, dan jangan gunakan bahasa inggris sebelum saya memulai duluan.",
            },
            {
                "role": "assistant",
                "content": "Kamu adalah asisten paling canggih yang berbahasa Indonesia gaul",
            },
        ]

    question = client.get_text(message)

    while True:
        proses_ = await em.get_costum_text()
        pros = await message.reply(f"{em.proses}**{proses_[4]}**")

        try:
            CONVERSATIONS[user_id].append({"role": "user", "content": question})

            url = "https://api.botcahx.eu.org/api/search/openai-custom"
            payload = {"message": CONVERSATIONS[user_id], "apikey": API_BOTCHAX}

            response = await Tools.fetch.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                output = data["result"]

                CONVERSATIONS[user_id].append({"role": "assistant", "content": output})

                if len(CONVERSATIONS[user_id]) > 20:
                    CONVERSATIONS[user_id] = (
                        CONVERSATIONS[user_id][:2] + CONVERSATIONS[user_id][-18:]
                    )

                await pros.delete()

                if len(output) > 4096:
                    result = await Tools.paste(output)
                    next_message = await client.ask(
                        chat_id=chat_id,
                        text=f"{em.sukses}<b>Message too long, upload to pastebin</b>\n<b>Question:\n<blockquote>{question}</blockquote>\n\nAnswer:\n</b><blockquote>{result}</blockquote>\n\n<b>Type <code>stop ask</code> to end the conversation.</b>",
                        disable_web_page_preview=True,
                        timeout=300,
                        reply_to_message_id=Message.ReplyCheck(message),
                    )
                else:
                    result = output
                    next_message = await client.ask(
                        chat_id=chat_id,
                        text=f"{em.sukses}<b>Question:\n<blockquote>{question}</blockquote>\n\nAnswer:\n</b><blockquote>{result}</blockquote>\n\n<b>Type <code>stop ask</code> to end the conversation.</b>",
                        timeout=300,
                        reply_to_message_id=Message.ReplyCheck(message),
                    )
                try:
                    if next_message.text.lower() == "stop ask":
                        del CONVERSATIONS[user_id]
                        await next_message.reply(
                            f"{em.sukses}**Conversation ended.**",
                            reply_to_message_id=Message.ReplyCheck(message),
                        )
                        break

                    question = next_message.text

                except TimeoutError:
                    del CONVERSATIONS[user_id]
                    await next_message.reply(
                        f"{em.gagal}**Conversation timed out after 5 minutes of inactivity.**",
                        reply_to_message_id=Message.ReplyCheck(message),
                    )
                    break
            else:
                await pros.edit(
                    f"{em.gagal}**API Error:** Status code {response.status_code}"
                )
                break

        except Exception as er:
            if user_id in CONVERSATIONS:
                del CONVERSATIONS[user_id]
            await pros.edit(f"{em.gagal}**ERROR:** {str(er)}")
            break


@CMD.UBOT("clearai")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    user_id = message.from_user.id
    if user_id in CONVERSATIONS:
        del CONVERSATIONS[user_id]
        await message.reply(f"{em.sukses}**AI conversation history cleared.**")
    else:
        await message.reply(f"{em.gagal}**No active AI conversation found.**")


@CMD.UBOT("aiaudio")
async def _(client, message):
    arg = client.get_text(message)
    if not arg:
        return await message.reply(
            f"<b>Please give question!!\nExample: `{message.text.split()[0]} Siapa kamu?`</b>"
        )
    uniq = f"{str(uuid4())}"
    data = {"prompt": arg, "idm": id(message)}
    state.set(uniq.split("-")[0], uniq.split("-")[0], data)
    proses = await message.reply("<b>Please wait a minute...</b>")
    try:
        inline = await ButtonUtils.send_inline_bot_result(
            message,
            message.chat.id,
            bot.me.username,
            f"inline_gptaudio {uniq.split('-')[0]}",
        )
        if inline:
            return await proses.delete()
    except Exception as er:
        return await proses.edit(f"**ERROR**: {str(er)}")

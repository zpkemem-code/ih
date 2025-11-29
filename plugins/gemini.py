import asyncio
import os

import google.generativeai as genai
from pyrogram.enums import ChatAction
from pyrogram.errors import ChatWriteForbidden

from config import API_GEMINI
from Zohun.helpers import CMD, Emoji

__MODULES__ = "Gemini"
__HELP__ = """<blockquote>Command Help **Gemini**</blockquote>

<blockquote>**Chat to gemini**</blockquote>
    **You can chat to gemini from this command**
        `{0}gemini` (prompt)

<b>   {1}</b>
"""


genai.configure(api_key=API_GEMINI)


def gemini(text):
    try:
        generation_config = {
            "temperature": 0.6,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH",
            },
        ]
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        respon = model.generate_content(text)
        if respon:
            return f"{respon.text}"
    except Exception as e:
        return f"Error generating text: {str(e)}"


async def mari_kirim(client, message, query):
    em = Emoji(client)
    await em.get()
    try:
        chat_id = message.chat.id
        respon = gemini(query)
        await message._client.send_chat_action(chat_id, ChatAction.TYPING)
        await asyncio.sleep(2)
        if len(respon) > 4096:
            with open("gemini.txt", "wb") as file:
                file.write(respon.encode("utf-8"))
            await message._client.send_chat_action(chat_id, ChatAction.UPLOAD_DOCUMENT)
            await asyncio.sleep(2)
            await message._client.send_document(
                chat_id, "gemini.txt", reply_to_message_id=message.id
            )
            os.remove("gemini.txt")
            return await message._client.send_chat_action(chat_id, ChatAction.CANCEL)
        else:
            await message.reply_text(
                f"{em.sukses}**{respon}**", reply_to_message_id=message.id
            )
        return await message._client.send_chat_action(chat_id, ChatAction.CANCEL)
    except ChatWriteForbidden:
        return


@CMD.UBOT("gemini")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply(
            f"{em.gagal} **Please reply to message text or give message!**"
        )
    reply_text = client.get_text(message)
    proses_ = await em.get_costum_text()
    pros = await message.reply(f"{em.proses}**{proses_[4]}**")
    await mari_kirim(client, message, reply_text)
    return await pros.delete()

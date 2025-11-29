import asyncio
import aiohttp
import random
from pyrogram import enums

import config
from Zohun import zohun
from Zohun.database import dB
from Zohun.helpers import CMD

__MODULES__ = "Autoreply"
__HELP__ = """<blockquote>Command Help **AutoReply**</blockquote>

<blockquote>**Basic commands**</blockquote>
    **Nyalain autoreply AI untuk balas semua pesan di group**
        `{0}autoreply` (on)
    **Matiin autoreply**
        `{0}autoreply` (off)
    **Cek status autoreply**
        `{0}autoreply` (status)

**Note:** Fitur ini akan otomatis membalas SEMUA pesan text di group dengan AI.

<b>   {1}</b>
"""

# Fallback responses (max 30 chars)
FALLBACK_RESPONSES = [
    "Oke bro!", "Sip!", "Mantap!", "Wkwk iya", "Boleh!",
    "Gas!", "Siap!", "Anjay", "Bet", "Gokil",
]

async def gen_autoreply_groq(text):
    """Generate autoreply response using Groq AI"""
    if not hasattr(config, 'GROQ_API_KEY') or not config.GROQ_API_KEY:
        return None
    
    if not config.GROQ_API_KEY.startswith('gsk_'):
        return None
    
    try:
        system_prompt = """Kamu asisten yang bales pesan SINGKAT banget, MAKSIMAL 30 KARAKTER.
Pake bahasa gaul anak jaksel: gue, lu, bro, anjay, bet, gokil, wkwk, sip, mantap.
Jawab singkat & to the point aja, ga usah panjang.
Kalo gambar, komen singkat tentang gambarnya."""

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(text)}
            ],
            "temperature": 0.9,
            "max_tokens": 50,
            "top_p": 1,
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    return None
                    
    except Exception as e:
        print(f"Autoreply Groq error: {e}")
        return None


@CMD.UBOT("autoreply")
@CMD.ONLY_GROUP
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(
            f"<b>🤖 Cara pake:</b>\n"
            f"• <code>{message.command[0]} on</code> - Nyalain autoreply AI (balas semua pesan)\n"
            f"• <code>{message.command[0]} off</code> - Matiin autoreply\n"
            f"• <code>{message.command[0]} status</code> - Cek status"
        )
    if message.command[1] == "on":
        current_chats = await dB.get_list_from_var(client.me.id, "AUTOREPLY_ALL") or []
        if message.chat.id in current_chats:
            return await message.reply("<b>🤖 Autoreply udah aktif!</b>")
        await dB.add_to_var(client.me.id, "AUTOREPLY_ALL", message.chat.id)
        return await message.reply("<b>🤖 Autoreply AI udah nyala!</b>")
    elif message.command[1] == "off":
        chat_id = message.chat.id
        chats = await dB.get_list_from_var(client.me.id, "AUTOREPLY_ALL") or []
        if chat_id not in chats:
            return await message.reply(f"**`{chat_id}` tidak ditemukan!**")
        await dB.remove_from_var(client.me.id, "AUTOREPLY_ALL", chat_id)
        name = (await client.get_chat(chat_id)).title
        return await message.reply(f"<b>🤖 Autoreply dimatiin buat group: {name}</b>")
    elif message.command[1] == "status":
        chats = await dB.get_list_from_var(client.me.id, "AUTOREPLY_ALL") or []
        if not chats:
            return await message.reply(
                "<b>❌ Ga ada grup yang aktifin autoreply</b>"
            )
        msg = "<b>🤖 Grup yang aktifin autoreply:</b>\n"
        for num, chat in enumerate(chats, 1):
            try:
                title = (await client.get_chat(chat)).title
                ids = (await client.get_chat(chat)).id
            except Exception:
                continue
            msg += f"{num}. {title} | <code>{ids}</code>\n"
        return await message.reply(msg)
    else:
        return await message.reply(
            f"<b>❌ Command ga valid. Pake:</b> <code>{message.command[0]} on|off|status</code>"
        )


# Message handler - NO COOLDOWN, reply to EVERYTHING
from pyrogram import filters

async def autoreply_handler(client, message):
    """Autoreply handler - responds to all non-userbot messages"""
    # Skip service/bot messages
    if not message.from_user or message.from_user.is_bot:
        return
    
    # Skip own messages  
    if message.from_user.id == client.me.id:
        return
    
    # Skip ALL userbot users
    all_userbot_ids = zohun._get_my_id if hasattr(zohun, '_get_my_id') else []
    if message.from_user.id in all_userbot_ids:
        return
    
    # Skip commands
    if message.text and message.text.startswith(('/', '.')):
        return
    
    # Check if THIS userbot enabled autoreply (not others)
    active_chats = await dB.get_list_from_var(client.me.id, "AUTOREPLY_ALL") or []
    if message.chat.id not in active_chats:
        return
    
    try:
        # Get content
        content = message.text or message.caption or "[media]"
        
        # Typing
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        
        # Generate
        response = await gen_autoreply_groq(content) or random.choice(FALLBACK_RESPONSES)
        
        # Truncate at sentence/word boundary (max 30 chars)
        if len(response) > 30:
            truncated = response[:30]
            sentence_end = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
            
            if sentence_end > 10:
                response = response[:sentence_end + 1]
            else:
                last_space = truncated.rfind(' ')
                if last_space > 15:
                    response = response[:last_space]
                else:
                    response = truncated
        
        # Reply
        await message.reply(response)
        await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
    except:
        pass

# Register
zohun.on_message(
    filters.text | filters.photo | filters.video | filters.sticker | filters.voice | filters.document,
    group=99
)(autoreply_handler)

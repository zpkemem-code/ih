import asyncio
import aiohttp
import random

from pyrogram import enums

import config
from Zohun import zohun
from Zohun.database import dB
from Zohun import bot
from Zohun.helpers import CMD, Tools

__MODULES__ = "Chatbot"
__HELP__ = """<blockquote>Command Help **Chatbot**</blockquote>

<blockquote>**Basic commands**</blockquote>
    **You can turned on autoreply in group chat**
        `{0}chatbot` (on)
    **You can turned off autoreply in group chat**
        `{0}chatbot` (off)
    **You can check status on database**
        `{0}chatbot` (status)

**Note:** This feature will work if someone replies to your message.        

<b>   {1}</b>
"""

# Simple responses if Groq fails
SIMPLE_RESPONSES = [
    "Gue lagi sibuk nih, bro!",
    "Waduh, gue lagi offline...",
    "Nanti gue balas ya, lagi ada urusan!",
    "Haha, oke deh!",
    "Mantap banget!",
    "Gue setuju banget!",
    "Yoi, gas terus!",
    "Sip, oke!",
    "Wkwkwk, lucu banget!",
    "Gue dukung!",
    "Keren abis!",
    "Boleh juga tuh!",
    "Gue ikut deh!",
    "Asik banget!",
    "Gue setuju!",
]

async def get_active_chats(client_id):
    """Get active chats from database for specific userbot"""
    try:
        chats = await dB.get_list_from_var(client_id, "CHATBOT") or []
        active_chats = set()
        for chat in chats:
            try:
                active_chats.add(int(chat))
            except (ValueError, TypeError):
                continue
        return active_chats
    except Exception as e:
        print(f"Error getting active chats: {e}")
        return set()

async def set_active_chats(client_id, chat_id, action="add"):
    """Manage active chats in database for specific userbot"""
    try:
        if action == "add":
            await dB.add_to_var(client_id, "CHATBOT", chat_id)
        else:
            await dB.remove_from_var(client_id, "CHATBOT", chat_id)
    except Exception as e:
        print(f"Error setting active chats: {e}")

async def gen_text_groq(text):
    """Generate response using Groq AI with bahasa gaul"""
    # Check if API key exists
    if not hasattr(config, 'GROQ_API_KEY') or not config.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not found in config")
        return None
    
    if not config.GROQ_API_KEY.startswith('gsk_'):
        print("❌ GROQ_API_KEY format invalid")
        return None
    
    try:
        # System prompt dengan karakter bahasa gaul
        system_prompt = """Kamu adalah cowo gaul Jakarta yang santai dan cool. 
Pake bahasa gaul sehari-hari kayak anak muda Jakarta.
Jangan pake bahasa formal, pake kata-kata kayak: gue, lu, bro, wkwk, mantap, oke, sip, yoi.
Jawab dengan singkat, maksimal 2-3 kalimat.
Jangan bertele-tele, langsung to the point.
Pake bahasa yang casual dan friendly."""

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(text)}
            ],
            "temperature": 0.8,
            "max_tokens": 150,
            "top_p": 1,
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {config.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        print(f"🔗 Sending to Groq AI: {text[:50]}...")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            ) as response:
                
                print(f"📨 Groq response status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    response_text = data["choices"][0]["message"]["content"]
                    print(f"💬 Groq response: {response_text}")
                    return response_text.strip()
                else:
                    error_text = await response.text()
                    print(f"❌ Groq API error {response.status}: {error_text}")
                    return None
                    
    except asyncio.TimeoutError:
        print("❌ Groq API timeout")
        return None
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return None

@CMD.UBOT("chatbot")
@CMD.ONLY_GROUP
async def _(client, message):
    """Handle chatbot commands"""
    if len(message.command) < 2:
        return await message.reply(
            f"<b>🤖 Cara pake:</b>\n"
            f"• <code>{message.command[0]} on</code> - Nyalain chatbot\n"
            f"• <code>{message.command[0]} off</code> - Matiin chatbot\n"
            f"• <code>{message.command[0]} status</code> - Cek status"
        )
    
    command = message.command[1].lower()
    
    if command == "on":
        await set_active_chats(client.me.id, message.chat.id, "add")
        return await message.reply("<b>🤖 Chatbot udah nyala! Reply pesan gue buat chat.</b>")
    
    elif command == "off":
        await set_active_chats(client.me.id, message.chat.id, "remove")
        try:
            name = (await client.get_chat(message.chat.id)).title
            return await message.reply(f"<b>🤖 Chatbot dimatiin buat group: {name}</b>")
        except:
            return await message.reply(f"<b>🤖 Chatbot dimatiin!</b>")
    
    elif command == "status":
        active_chats = await get_active_chats(client.me.id)
        if not active_chats:
            return await message.reply("<b>❌ Ga ada grup yang aktifin chatbot</b>")
        
        msg = "<b>🤖 Grup yang aktifin chatbot:</b>\n"
        for num, chat_id in enumerate(active_chats, 1):
            try:
                chat = await client.get_chat(chat_id)
                msg += f"{num}. {chat.title} | <code>{chat_id}</code>\n"
            except:
                msg += f"{num}. Unknown Chat | <code>{chat_id}</code>\n"
        
        return await message.reply(msg)
    
    else:
        return await message.reply(
            f"<b>❌ Command ga valid. Pake:</b> <code>{message.command[0]} on|off|status</code>"
        )

@CMD.NO_CMD("CHATBOT", zohun)
async def _(client, message):
    """Handle chatbot replies"""
    # Check if chatbot is active in this chat for this specific userbot
    active_chats = await get_active_chats(client.me.id)
    if message.chat.id not in active_chats:
        return
    
    # Check if replying to bot and has text
    if not message.text or not message.reply_to_message:
        return
        
    if message.reply_to_message.from_user.id != client.me.id:
        return
    
    # Skip if message is too long
    if len(message.text) > 500:
        return await message.reply("Wah, pesannya kepanjangan bro! Pendekin dikit.")
    
    print(f"🤖 Chatbot triggered in chat {message.chat.id}")
    
    # Typing action
    await client.send_chat_action(
        chat_id=message.chat.id, action=enums.ChatAction.TYPING
    )
    
    try:
        # Try Groq AI first
        response = await gen_text_groq(message.text)
        
        # If Groq fails, use simple random response
        if not response:
            response = random.choice(SIMPLE_RESPONSES)
            print(f"🔄 Using fallback response: {response}")
        
        # Send response
        await message.reply(response)
        
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        await message.reply("Waduh, error nih! Coba lagi ya bro.")
    
    finally:
        # Cancel typing action
        await client.send_chat_action(
            chat_id=message.chat.id, action=enums.ChatAction.CANCEL
        )
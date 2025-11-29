"""
Simple conversation handler to replace pyromod.ask()
This provides the .ask() method functionality without pyromod dependency
"""
import asyncio
from pyrogram import Client
from pyrogram.types import Message

# Store pending conversations: {user_id: {'event': asyncio.Event, 'response': Message}}
_conversations = {}


async def ask(
    client: Client,
    chat_id: int,
    text: str,
    timeout: int = 300,
    reply_markup=None,
    **kwargs
):
    """
    Ask a question and wait for the user's response
    
    Args:
        client: Pyrogram client
        chat_id: User/chat ID to send the question to
        text: Question text
        timeout: Timeout in seconds (default 300)
        reply_markup: Optional keyboard markup
        **kwargs: Additional arguments for send_message
    
    Returns:
        Message: User's response message
    
    Raises:
        asyncio.TimeoutError: If user doesn't respond within timeout
    """
    # Send the question
    await client.send_message(chat_id, text, reply_markup=reply_markup, **kwargs)
    
    # Create an event to wait for response
    event = asyncio.Event()
    _conversations[chat_id] = {
        'event': event,
        'response': None
    }
    
    try:
        # Wait for response with timeout
        await asyncio.wait_for(event.wait(), timeout=timeout)
        response = _conversations[chat_id]['response']
        return response
    finally:
        # Clean up
        if chat_id in _conversations:
            del _conversations[chat_id]


def handle_response(message: Message):
    """
    Handle incoming message as a response to a pending question
    
    Args:
        message: Incoming message
    
    Returns:
        bool: True if message was handled as a conversation response
    """
    user_id = message.from_user.id if message.from_user else message.chat.id
    
    if user_id in _conversations:
        conv = _conversations[user_id]
        conv['response'] = message
        conv['event'].set()
        return True
    
    return False


# Monkey-patch Client to add .ask() method
def patch_client():
    """Add .ask() method to Pyrogram Client"""
    if not hasattr(Client, 'ask'):
        Client.ask = ask


# Auto-patch on import
patch_client()

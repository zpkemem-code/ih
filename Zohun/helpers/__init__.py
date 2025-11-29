from .afk import AFK_
from .auto_referal import TokenReferal
from .autobc import (AutoBC, add_auto_text, get_auto_gcast_messages,
                     text_autogcast)
from .buttons import ButtonUtils, ikb, kb, paginate_modules
from .commands import CMD, FILTERS, PY, no_commands, no_trigger, trigger
from .emoji_logs import Emoji, emotikon
from .emo import EMO
from .fonts import Fonts, gens_font, query_fonts
from .loaders import (CheckSellerCount, CheckUsers, CleanAcces, ExpiredUser,
                      check_payment, installPeer, sending_user, stoped_ubot)
from .message import Message
from .misc import Sticker
from .quote import Quotly, QuotlyException
from .reads import ReadUser
from .spotify import Spotify
from .tasks import task
from .thumbnail import gen_qthumb
from .times import get_time, start_time
from .tools import get_arg, get_args, ApiImage, Tools
from .ytdlp import YoutubeSearch, cookies, stream, telegram, youtube


# Extract user helper
async def extract_user(message):
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id if message.reply_to_message.from_user else None
    elif len(message.command) > 1:
        try:
            user_id = int(message.command[1])
        except ValueError:
            try:
                user = await message._client.get_users(message.command[1])
                user_id = user.id
            except:
                user_id = None
    return user_id


# ===================================================================
# BTN and MSG Aliases - Fix for NameError
# ===================================================================

# BTN is an alias to ButtonUtils
BTN = ButtonUtils

# MSG is an alias to Message
MSG = Message


# ============================================================
# Helper function for extracting user and reason from message
# ============================================================

async def extract_user_and_reason(message, sender_chat=False):
    """Extract user_id and reason from message
    
    Supports:
    - Reply to message with optional reason
    - Direct mention/username with optional reason
    - Format: .command @user reason OR .command user_id reason
    
    Returns: (user_id, reason)
    """
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    
    # Case 1: Reply to message
    if message.reply_to_message:
        reply = message.reply_to_message
        
        if not reply.from_user:
            if (reply.sender_chat and 
                reply.sender_chat != message.chat.id and 
                sender_chat):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id
        
        # Extract reason from command text
        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        
        return id_, reason
    
    # Case 2: Username/ID in command (no reply)
    if len(args) == 2:
        # .command user_id
        user = text.split(None, 1)[1]
        user_id = await extract_userid(message, user)
        return user_id, None
    
    if len(args) > 2:
        # .command user_id reason
        user, reason = text.split(None, 2)[1:]
        user_id = await extract_userid(message, user)
        return user_id, reason
    
    return None, None


async def extract_userid(message, user):
    """Extract user ID from username or ID string"""
    # If it's already a number
    if user.isdigit():
        return int(user)
    
    # If it's a username
    if user.startswith("@"):
        try:
            user_obj = await message._client.get_users(user)
            return user_obj.id
        except:
            return None
    
    # Try as direct username
    try:
        user_obj = await message._client.get_users(user)
        return user_obj.id
    except:
        return None



# ============================================================
# Database Wrapper Functions
# These are standalone wrappers for database methods
# so they can be called without dB instance
# ============================================================

from Zohun.database import dB

# Expired date functions
async def set_expired_date(user_id, expire_date):
    """Set expiration date for a user"""
    return await dB.set_expired_date(user_id, expire_date)

async def get_expired_date(user_id):
    """Get expiration date for a user"""
    return await dB.get_expired_date(user_id)

async def rem_expired_date(user_id):
    """Remove expiration date for a user"""
    return await dB.rem_expired_date(user_id)

# Variable management functions (with 's' for compatibility)
async def add_to_vars(user_id, vars_name, value):
    """Add value to variable list (wrapper for add_to_var)"""
    return await dB.add_to_var(user_id, vars_name, value)

async def remove_from_vars(user_id, vars_name, value):
    """Remove value from variable list (wrapper for remove_from_var)"""
    return await dB.remove_from_var(user_id, vars_name, value)


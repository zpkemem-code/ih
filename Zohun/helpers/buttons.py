import re
from math import ceil
from typing import List, Optional, Tuple

from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            KeyboardButton, ReplyKeyboardMarkup, WebAppInfo)

from Zohun.database import state
from Zohun.logger import logger

COLUMN_SIZE = 4  # Controls the button number of height
NUM_COLUMNS = 2  # Controls the button number of width


def kb(rows=None, resize_keyboard=True, one_time_keyboard=False):
    """
    Create a ReplyKeyboardMarkup from a list of button rows.
    
    Args:
        rows: List of button rows, where each row is a list of button texts (strings).
        resize_keyboard: If True, the keyboard will be resized to fit the buttons.
        one_time_keyboard: If True, the keyboard will be hidden after one use.
        
    Returns:
        ReplyKeyboardMarkup object
        
    Examples:
        kb([["Button 1", "Button 2"]])
        kb([["Yes"], ["No"]], one_time_keyboard=True)
    """
    if rows is None:
        rows = []
    
    keyboard = []
    for row in rows:
        button_row = []
        for button in row:
            if isinstance(button, str):
                button_row.append(KeyboardButton(text=button))
            elif isinstance(button, tuple) and len(button) >= 1:
                button_row.append(KeyboardButton(text=button[0]))
            else:
                continue
        if button_row:
            keyboard.append(button_row)
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard
    )


def ikb(rows=None):
    """
    Create an InlineKeyboardMarkup from a list of button rows.
    
    Args:
        rows: List of button rows, where each row is a list of tuples.
              Each tuple can be (text, data) or (text, data, type).
              
    Returns:
        InlineKeyboardMarkup object
        
    Examples:
        ikb([[("Button 1", "data1"), ("Button 2", "data2")]])
        ikb([[("URL Button", "https://example.com", "url")]])
    """
    if rows is None:
        rows = []
    
    lines = []
    for row in rows:
        line = []
        for button in row:
            if len(button) == 2:
                text, data = button
                line.append(InlineKeyboardButton(text=text, callback_data=data))
            elif len(button) == 3:
                text, data, button_type = button
                if button_type == "url":
                    line.append(InlineKeyboardButton(text=text, url=data))
                elif button_type == "callback_data":
                    line.append(InlineKeyboardButton(text=text, callback_data=data))
                elif button_type == "user_id":
                    line.append(InlineKeyboardButton(text=text, user_id=int(data)))
                else:
                    line.append(InlineKeyboardButton(text=text, callback_data=data))
            else:
                continue
        if line:
            lines.append(line)
    
    return InlineKeyboardMarkup(inline_keyboard=lines)


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None):
    # Create a list of (module_name, module_object) tuples sorted by name
    module_items = sorted(
        [
            (getattr(x, "__MODULES__", None) or getattr(x, "__MODULE__", ""), x)
            for x in module_dict.values()
        ],
        key=lambda item: item[0]
    )
    
    if not chat:
        modules = [
            EqInlineKeyboardButton(
                module_name,
                # Use first 20 chars of module name to stay under 64-byte limit
                callback_data="{}_module({},{})".format(
                    prefix, module_name.lower()[:20], page_n
                ),
            )
            for module_name, _ in module_items
        ]
    else:
        modules = [
            EqInlineKeyboardButton(
                module_name,
                # Use first 15 chars of module name to accommodate chat ID
                callback_data="{}_module({},{},{})".format(
                    prefix, chat, module_name.lower()[:15], page_n
                ),
            )
            for module_name, _ in module_items
        ]
    
    pairs = [modules[i : i + NUM_COLUMNS] for i in range(0, len(modules), NUM_COLUMNS)]

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "《",
                    callback_data="{}_prev({})".format(
                        prefix,
                        modulo_page - 1 if modulo_page > 0 else max_num_pages - 1,
                    ),
                ),
                EqInlineKeyboardButton("✘", callback_data="close help"),
                EqInlineKeyboardButton(
                    "》",
                    callback_data="{}_next({})".format(prefix, modulo_page + 1),
                ),
            )
        ]
    else:
        pairs.append(
            [
                EqInlineKeyboardButton(
                    "⇱ Back",
                    callback_data="{}_back".format(prefix),  # Fixed: simplified callback
                ),
                # EqInlineKeyboardButton("x", callback_data="close help"),
            ]
        )

    return pairs


class ButtonUtils:
    # Compile regex patterns for better performance
    URL_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:[/?]\S+)?|tg://\S+"
    )
    BUTTON_PATTERN = re.compile(r"\[(.*?)\|(.*?)\]")
    FORMAT_TAGS = {
        "<b>": "**",
        "<i>": "__",
        "<strike>": "~~",
        "<spoiler>": "||",
        "<u>": "--",
    }

    @staticmethod
    def is_url(text: str) -> bool:
        """Check if text is a URL."""
        # return bool(ButtonUtils.URL_PATTERN.match(text))
        return bool(re.search(ButtonUtils.URL_PATTERN, text))

    @staticmethod
    def is_number(text: str) -> bool:
        """Check if text is a number."""
        return text.isdigit()

    @staticmethod
    def is_copy(text: str) -> bool:
        pattern = r"copy:"

        return bool(re.search(pattern, text))

    @staticmethod
    def is_web(text: str) -> bool:
        pattern = r"web:"

        return bool(re.search(pattern, text))

    @staticmethod
    def cek_tg(text):
        tg_pattern = r"https?:\/\/files\.catbox\.moe\/\S+"
        match = re.search(tg_pattern, text)

        if match:
            tg_link = match.group(0)
            non_tg_text = text.replace(tg_link, "").strip()
            return tg_link, non_tg_text
        else:
            return (None, text)

    @staticmethod
    def parse_msg_buttons(texts: str) -> Tuple[str, List[List]]:
        """Parse message text and extract button data."""
        btn = []
        for z in ButtonUtils.BUTTON_PATTERN.findall(texts):
            text, url = z
            urls = url.split("|")
            url = urls[0]
            if len(urls) > 1:
                btn[-1].append([text, url])
            else:
                btn.append([[text, url]])

        txt = texts
        for z in re.findall(r"\[.+?\|.+?\]", texts):
            txt = txt.replace(z, "")

        return txt.strip(), btn

    @staticmethod
    def create_button(
        text: str, data: str, with_suffix: str = ""
    ) -> InlineKeyboardButton:
        """Create an InlineKeyboardButton based on data type."""
        data = data.strip()
        if ButtonUtils.is_url(data):
            return InlineKeyboardButton(text=text, url=data)
        elif ButtonUtils.is_number(data):
            return InlineKeyboardButton(text=text, user_id=int(data))
        elif ButtonUtils.is_copy(data):
            # copy_text not supported in Pyrogram - using callback_data instead
            return InlineKeyboardButton(text=text, callback_data=data.replace("copy:", ""))
        elif ButtonUtils.is_web(data):
            url = data.replace("web:", "")
            logger.info(f"Type data:{url} ")
            return InlineKeyboardButton(text=text, web_app=WebAppInfo(url=url))
        return InlineKeyboardButton(
            text=text, callback_data=f"{data}_{with_suffix}" if with_suffix else data
        )

    @staticmethod
    def create_inline_keyboard(
        buttons: List[List], suffix: str = ""
    ) -> InlineKeyboardMarkup:
        """Create InlineKeyboardMarkup from button data."""
        keyboard = []
        for row in buttons:
            if len(row) > 1:
                keyboard.append(
                    [
                        ButtonUtils.create_button(text, data, suffix)
                        for text, data in row
                    ]
                )
            else:
                text, data = row[0]
                keyboard.append([ButtonUtils.create_button(text, data, suffix)])
        return InlineKeyboardMarkup(keyboard)

    """Pre-defined keyboard templates for Pyrogram."""

    @staticmethod
    def start_menu(is_admin: bool = False):
        """Generate start menu keyboard."""
        from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup
        
        common_buttons = [
            [KeyboardButton("✨ Mulai Buat Userbot")],
            [KeyboardButton("❓ Status Akun")],
            [KeyboardButton("🎟️ Referral"), KeyboardButton("🔑 Token")],
            [KeyboardButton("🔄 Reset Emoji"), KeyboardButton("🔄 Reset Prefix")],
            [KeyboardButton("🔄 Restart Userbot"), KeyboardButton("🔄 Reset Text")],
        ]

        if is_admin:
            common_buttons.extend(
                [
                    [KeyboardButton("🚀 Updates"), KeyboardButton("🛠️ Cek Fitur")],
                ]
            )
        else:
            common_buttons.extend([[KeyboardButton("🛠️ Cek Fitur")]])

        return ReplyKeyboardMarkup(common_buttons, resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def userbot(user_id, count):
        button = ikb(
            [
                [
                    (
                        "Delete User",
                        f"del_ubot {int(user_id)}",
                    ),
                    (
                        "Check Phone",
                        f"get_phone {int(count)}",
                    ),
                ],
                [
                    (
                        "Check Expired",
                        f"cek_masa_aktif {int(user_id)}",
                    )
                ],
                [
                    (
                        "Get Otp",
                        f"get_otp {int(count)}",
                    ),
                    (
                        "Get V2L",
                        f"get_faktor {int(count)}",
                    ),
                ],
                [
                    (
                        "Delete Account",
                        f"ub_deak {int(count)}",
                    )
                ],
                [
                    ("《", f"prev_ub {int(count)}"),
                    ("Close", f"close get_users"),
                    ("》", f"next_ub {int(count)}"),
                ],
            ]
        )
        return button

    @staticmethod
    def fake_userbot(user_id, count):
        button = ikb(
            [
                [
                    (
                        "Delete User",
                        f"del_ubot {int(user_id)}",
                    ),
                ],
                [
                    (
                        "Check Expired",
                        f"cek_masa_aktif {int(user_id)}",
                    )
                ],
                [
                    ("《", f"prev_ub {int(count)}"),
                    ("Close", f"close get_users"),
                    ("》", f"next_ub {int(count)}"),
                ],
            ]
        )
        return button

    @staticmethod
    def deak(user_id, count):
        button = ikb(
            [[("《", f"prev_ub {int(count)}"), ("Approve", f"deak_akun {int(count)}")]]
        )
        return button

    @staticmethod
    async def generate_inline_query(message, chat_id, bot_username, query):
        try:
            client = message._client
            results = await client.get_inline_bot_results(bot_username, query)
            if results and results.results:
                return {
                    "query_id": results.query_id,
                    "result_id": results.results[0].id,
                    "results": results.results,
                    "query": query,
                }
            return None
        except Exception as e:
            return None

    @staticmethod
    async def send_inline_bot_result(
        message,
        chat_id,
        bot_username,
        query,
        reply_to_message_id: Optional[int] = None,
    ) -> bool:
        """
        Send inline bot result to chat.

        Args:
            client: Pyrogram Client instance
            message: Original message to reply to
            bot_username: Username of the bot to query
            query: Query string to send to the bot
            reply_to_message_id: Optional message ID to reply to

        Returns:
            Boolean indicating success/failure
        """
        client = message._client
        try:
            query_results = await ButtonUtils.generate_inline_query(
                message, chat_id, bot_username, query
            )

            if not query_results:
                return False

            data = await client.send_inline_bot_result(
                chat_id,
                query_results["query_id"],
                query_results["result_id"],
                reply_to_message_id=reply_to_message_id,
            )
            # logger.warning(f"line 273 {data}")
            inline_id = {
                "chat": chat_id,
                "_id": data.updates[0].id,
                "me": client.me.id,
                "idm": id(message),
            }
            state.set(client.me.id, query, inline_id)
            return True

        except Exception as e:
            return False

    @staticmethod
    def plus_minus(query, amount):
        button = ikb(
            [
                [("⁻1 bulan", f"kurang {query}"), ("⁺1 bulan", f"tambah {query}")],
                [("Konfirmasi", f"confirm {amount} {query}")],
                [("Batal", "closed")],
            ]
        )
        return button

    @staticmethod
    def create_font_keyboard(font_list, get_id, current_batch):
        keyboard = []
        for font_dict in font_list:
            for key, value in font_dict.items():
                keyboard.append(
                    InlineKeyboardButton(
                        key, callback_data=f"get_font {get_id} {value}"
                    )
                )

        rows = [keyboard[i : i + 2] for i in range(0, len(keyboard), 2)]

        while len(rows) < 3:
            rows.append([])

        rows.append(
            [
                InlineKeyboardButton(
                    "《", callback_data=f"prev_font {get_id} {current_batch}"
                ),
                InlineKeyboardButton("✘", callback_data=f"close inline_font"),
                InlineKeyboardButton(
                    "》", callback_data=f"next_font {get_id} {current_batch}"
                ),
            ]
        )
        return rows

    @staticmethod
    def create_buttons_textpro(font_list, get_id, current_batch):
        keyboard = []
        for font_dict in font_list:
            for key, value in font_dict.items():
                keyboard.append(
                    InlineKeyboardButton(key, callback_data=f"genpro {get_id} {value}")
                )

        rows = [keyboard[i : i + 2] for i in range(0, len(keyboard), 2)]

        while len(rows) < 3:
            rows.append([])

        rows.append(
            [
                InlineKeyboardButton(
                    "《", callback_data=f"prev_textpro {get_id} {current_batch}"
                ),
                InlineKeyboardButton("✘", callback_data=f"close inline_textpro"),
                InlineKeyboardButton(
                    "》", callback_data=f"next_textpro {get_id} {current_batch}"
                ),
            ]
        )
        return rows

    @staticmethod
    def ALIVE(get_id):
        """Generate ALIVE inline keyboard buttons"""
        button = [
            [
                InlineKeyboardButton("📊 Stats", callback_data=f"alv_stats {get_id[1]} {get_id[2]}"),
                InlineKeyboardButton("✘", callback_data=f"alv_cls {get_id[1]} {get_id[2]}"),
            ]
        ]
        return button

    @staticmethod
    def BOT_HELP(message):
        """Generate BOT HELP keyboard buttons"""
        from config import OWNER_ID
        user_id = message.from_user.id if hasattr(message, 'from_user') else None
        button = [
            [
                InlineKeyboardButton("📋 Commands", callback_data="bot_commands"),
                InlineKeyboardButton("📊 Stats", callback_data="bot_stats"),
            ],
            [
                InlineKeyboardButton("🔄 Restart", callback_data="reboot"),
                InlineKeyboardButton("📥 Update", callback_data="update"),
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="balik"),
            ]
        ]
        return button

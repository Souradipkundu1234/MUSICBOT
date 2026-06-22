from pyrogram.types import InlineKeyboardButton

import config
from SONALI import app


def start_panel(_):
    bot_username = app.username or "your_bot_username"

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{bot_username}?startgroup=true"
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT
            ),
        ],
    ]

    return buttons


def private_panel(_):
    bot_username = app.username or "your_bot_username"

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{bot_username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"tg://openmessage?user_id={config.OWNER_ID}"
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                url=config.SUPPORT_CHAT
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                callback_data="settings_back_helper"
            )
        ],
    ]

    return buttons

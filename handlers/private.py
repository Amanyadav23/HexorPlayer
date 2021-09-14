from time import time
from datetime import datetime
from pyrogram import Client, filters
from helpers.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import sudo_users_only

from config import BOT_NAME as bn
from helpers.filters import other_filters2

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(other_filters2)
async def start(_, message: Message):
    
    await message.reply_text(
        f"""**
🌠𝚃𝚑𝚒𝚜 𝙸𝚜 𝙰𝚍𝚟𝚊𝚗𝚌𝚎 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝙼𝚞𝚜𝚒𝚌 𝙱𝚘𝚝 \n🌺𝚁𝚞𝚗 𝙾𝚗 𝚅𝙿𝚂 𝚂𝚎𝚛𝚟𝚎𝚛 \n🌼𝙵𝚎𝚎𝚕 𝙷𝚒𝚐𝚑 𝚀𝚞𝚊𝚕𝚒𝚝𝚢 𝙼𝚞𝚜𝚒𝚌 𝙸𝚗 𝚅𝙲\n😎𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚍 𝙱𝚢[𝙰𝙼𝙰𝙽](https://t.me/A_4_AMAN_official)**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❰𝙾𝚆𝙽𝙴𝚁❱", url="https://t.me/A_4_AMAN_official")
                  ],[
                    InlineKeyboardButton(
                        "❰𝚂𝚞𝚙𝚙𝚘𝚛𝚝❱", url="https://t.me/ACF_OP_BOLTE"
                    ),
                    InlineKeyboardButton(
                        "❰𝙶𝚛𝚘𝚞𝚙❱", url="https://t.me/ACF_OP_BOLTE"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "❰𝙼𝚘𝚛𝚎 𝙸𝚗𝚏𝚘❱", url="https://t.me/shivamdemon"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✅ **𝙰𝙼𝙰𝙽 𝚂𝙴𝚁𝚅𝙴𝚁 𝙸𝚂 𝚁𝚄𝙽𝙽𝙸𝙽𝙶**\n<b>💠 **𝚄𝙿𝚃𝙸𝙼𝙴:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨ 𝙶𝚁𝙾𝚄𝙿", url=f"https://t.me/ACF_OP_BOLTE"
                    ),
                    InlineKeyboardButton(
                        "📣 𝙲𝙷𝙰𝙽𝙽𝙴𝙻", url=f"https://t.me/ACF_OP_BOLTE"
                    )
                ]
            ]
        )
    )


@Client.on_message(filters.command("ping") & ~filters.private & ~filters.channel)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("ᴘɪɴɴɢ...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🌟`ᴘᴏɴɢ!!`\n"
        f"✨  `{delta_ping * 1000:.3f} ᴍꜱ`"
    )

@Client.on_message(filters.command("uptime") & ~filters.private & ~filters.channel)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🌳 ᴀᴍᴀɴ ꜱᴛᴀᴛᴜꜱ:\n"
        f"• **ᴜᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"• **ꜱᴛᴀʀᴛ ᴛɪᴍᴇ:** `{START_TIME_ISO}`"
    )

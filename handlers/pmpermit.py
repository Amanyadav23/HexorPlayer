from callsmusic.callsmusic import client as USER
from pyrogram import filters
from pyrogram.types import Chat, Message, User
from config import BOT_USERNAME

@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
  await USER.send_message(message.chat.id,"💕𝙷𝚎𝚛𝚎 𝙰𝚜𝚜𝚒𝚜𝚝𝚊𝚗𝚝 𝙾𝚏 @{AMAN_X_MUSICBOT}\n✨𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚍 𝙱𝚢 @A_4_AMAN_YADAV_0FFICIAL\n🌟𝙳𝚘𝚗𝚝 𝚂𝚙𝚊𝚖 𝙷𝚎𝚛𝚎")
  return                        

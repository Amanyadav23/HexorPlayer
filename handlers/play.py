import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("play") 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
async def play(_, message: Message):

    lel = await message.reply("🔄 **𝙻𝚘𝚊𝚍 𝙱𝚎𝚜𝚝 👌𝚀𝚞𝚊𝚕𝚒𝚝𝚢 ❤️ 𝚂𝚘𝚗𝚐 🎶🤟**")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "AMAN X MUSIC PLAYER"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>𝙰𝚍 𝙼𝚎 𝙰𝚜 𝙰𝚍𝚖𝚒𝚗 𝙾𝚏 𝚈𝚘𝚞𝚛 𝙶𝚛𝚘𝚞𝚙 𝙵𝚒𝚛𝚜𝚝 ❰ 𝙰𝙼𝙰𝙽 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 🚬 ❱</b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**𝙼𝚞𝚜𝚒𝚌 🎶 𝙰𝚜𝚜𝚒𝚜𝚝𝚊𝚗𝚝 😎 𝙹𝚘𝚒𝚗𝚎𝚍 𝚃𝚑𝚒𝚜 😉 𝙶𝚛𝚘𝚞𝚙 𝙵𝚘𝚛 𝙿𝚕𝚊𝚢 𝙼𝚞𝚜𝚒𝚌 ❤️🤟**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>❰𝙵𝚕𝚘𝚘𝚍 😒 𝚆𝚊𝚒𝚝 𝙴𝚛𝚛𝚘𝚛 😔❱</b>\n𝙷𝚎𝚢 𝙰𝚜𝚜𝚒𝚜𝚝𝚊𝚗𝚝 𝙾𝚏 𝙱𝚘𝚝 𝙲𝚘𝚞𝚕𝚍𝚗'𝚝 𝙹𝚘𝚒𝚗 𝚈𝚘𝚞𝚛 𝙶𝚛𝚘𝚞𝚙 𝙳𝚞𝚎 𝚃𝚘 𝙷𝚎𝚊𝚟𝚢 𝙹𝚘𝚒𝚗 𝚁𝚎𝚚𝚞𝚎𝚜𝚝 . 𝙼𝚊𝚔𝚎 𝚂𝚞𝚛𝚎 𝚄𝚜𝚎𝚛𝚋𝚘𝚝 𝙹𝚘𝚒𝚗𝚎𝚍  😔 𝙸𝚗 𝚃𝚑𝚒𝚜 𝙶𝚛𝚘𝚞𝚙 𝙰𝚗𝚍 𝚃𝚛𝚢  😎🤟𝙻𝚊𝚝𝚎𝚛 :) ")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>❰𝙰𝙼𝙰𝙽 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 🚬❱ 𝙰𝚜𝚜𝚒𝚜𝚝𝚊𝚗𝚝 𝙾𝚏 𝚄𝚜𝚎𝚛𝚋𝚘𝚝 𝙸𝚜 𝙽𝚘𝚝 𝙸𝚗 𝚃𝚑𝚒𝚜 𝙲𝚑𝚊𝚝' 𝙰𝚜𝚔 𝙰𝚍𝚖𝚒𝚗 𝚃𝚘 𝚂𝚎𝚗𝚍 𝙵𝚒𝚛𝚜𝚝 /𝚙𝚕𝚊𝚢 𝙲𝚘𝚖𝚖𝚊𝚗𝚍 𝙵𝚘𝚛 𝙰𝚍𝚍 𝙸𝚝  😎🤟</i>")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❰𝚅𝚒𝚍𝚎𝚘 🧿❱ 𝙻𝚘𝚗𝚐𝚎𝚛 𝚃𝚑𝚊𝚗 {DURATION_LIMIT} 𝙼𝚒𝚗𝚞𝚝𝚎𝚜 𝙰𝚛𝚎𝚗'𝚝 𝙰𝚕𝚕𝚘𝚠𝚎𝚍 ✨ 𝚃𝚘 𝙿𝚕𝚊𝚢 ❤️🤞"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/a67094fc4a99bca08114b.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="❰ 𝙶𝚛𝚘𝚞𝚙 😎❤️🤟 ❱",
                        url="https://t.me/A_4_AMAN_YADAV_0FFICIAL")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❰ 𝙶𝚛𝚘𝚞𝚙 😎❤️🤟 ❱",
                            url="https://t.me/A_4_AMAN_YADAV_0FFICIAL"),
                        

                    ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/a67094fc4a99bca08114b.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                            text="❰ 𝙶𝚛𝚘𝚞𝚙 😎❤️🤟 ❱",
                            url="https://t.me/A_4_AMAN_YADAV_0FFICIAL"),

                        ]
                    ]
                )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❰𝚅𝚒𝚍𝚎𝚘 🧿❱ 𝙻𝚘𝚗𝚐𝚎𝚛 𝚃𝚑𝚊𝚗 {DURATION_LIMIT} 𝙼𝚒𝚗𝚞𝚝𝚎𝚜 𝙰𝚛𝚎𝚗'𝚝 𝙰𝚕𝚕𝚘𝚠𝚎𝚍 ✨ 𝚃𝚘 𝙿𝚕𝚊𝚢 ❤️🤞")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("✌**𝚆𝚑𝚊𝚝'𝚂 ❤️ 𝚂𝚘𝚗𝚐 🎶 𝚈𝚘𝚞 😎 𝚆𝚊𝚗𝚝 𝚃𝚘 𝙿𝚕𝚊𝚢 🧿🤟**")
        await lel.edit("🔎 **𝙵𝚒𝚗𝚍𝚒𝚗𝚐  💫 𝚃𝚑𝚎 𝚂𝚘𝚗𝚐 ❤️ ❰𝙰𝙼𝙰𝙽 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 🚬❱...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🎵 **𝙿𝚛𝚘𝚌𝚎𝚜𝚜𝚒𝚗𝚐 𝚂𝚘𝚞𝚗𝚍 🔊**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "🌸 𝚂𝚘𝚗𝚐 𝙽𝚘𝚝 𝙵𝚘𝚞𝚗𝚍 ✌ 𝚂𝚙𝚎𝚕𝚕𝚒𝚗𝚐 𝙿𝚛𝚘𝚋𝚕𝚎𝚖 ."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                      
                        InlineKeyboardButton(
                            text="❰ 𝙶𝚛𝚘𝚞𝚙 😎❤️🤟 ❱",
                            url="https://t.me/A_4_AMAN_YADAV_0FFICIAL"),

                    ]
                ]
            )
        
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❰𝚅𝚒𝚍𝚎𝚘 🧿❱ 𝙻𝚘𝚗𝚐𝚎𝚛 𝚃𝚑𝚊𝚗 {DURATION_LIMIT} 𝙼𝚒𝚗𝚞𝚝𝚎𝚜 𝙰𝚛𝚎𝚗'𝚝 𝙰𝚕𝚕𝚘𝚠𝚎𝚍 ✨ 𝚃𝚘 𝙿𝚕𝚊𝚢 ❤️🤞")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption="**❰𝙰𝙼𝙰𝙽 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 🚬❱ 𝚂𝚘𝚗𝚐 ❤️ 𝙿𝚘𝚜𝚒𝚝𝚒𝚘𝚗 💫🤟** {}".format(
        position
        ),
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="**❰ 𝙰𝙼𝙰𝙽 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 🚬❱ Now 😄 𝙿𝚕𝚊𝚢𝚒𝚗𝚐 📀 𝙰𝚝🤟 `{}`...**".format(
        message.chat.title
        ), )
        os.remove("final.png")
        return await lel.delete()

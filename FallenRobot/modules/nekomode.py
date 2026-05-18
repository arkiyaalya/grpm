# <============================================== IMPORTS =========================================================>
import nekos
from pyrogram import filters
from pyrogram.types import Message

from Database.mongodb.toggle_mongo import is_nekomode_on, nekomode_off, nekomode_on
from FallenRobot import pbot
from FallenRobot.events import state  # Import the state function

# <=======================================================================================================>
url_sfw = "https://api.waifu.pics/sfw/"
allowed_commands = [
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "spank",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "wink",
    "poke",
    "dance",
    "cringe",
    "tickle",
]


# <================================================ FUNCTION =======================================================>
@pbot.on_message(filters.command("wallpaper"))
async def wallpaper(_, message: Message):
    chat_id = message.chat.id
    nekomode_status = await is_nekomode_on(chat_id)
    if nekomode_status:
        img_url = nekos.img("wallpaper")
        await message.reply_photo(photo=img_url)


@pbot.on_message(filters.command(["nekomode"]))
async def toggle_nekomode(_, message: Message):
    chat_id = message.chat.id
    args = message.text.split(None, 1)
    if len(args) < 2:
        await message.reply("Usage: /nekomode on | /nekomode off")
        return
    action = args[1].strip().lower()
    if action == "on":
        await nekomode_on(chat_id)
        await message.reply("Nekomode has been enabled.")
    elif action == "off":
        await nekomode_off(chat_id)
        await message.reply("Nekomode has been disabled.")
    else:
        await message.reply("Usage: /nekomode on | /nekomode off")


@pbot.on_message(filters.command(allowed_commands))
async def nekomode_commands(_, message: Message):
    chat_id = message.chat.id
    nekomode_status = await is_nekomode_on(chat_id)
    if nekomode_status:
        # Safely extract command from "/neko@bot" or "/neko arg"
        target = message.text.split()[0].split("@")[0][1:].lower()
        if target in allowed_commands:
            url = f"{url_sfw}{target}"
            response = await state.get(url)
            result = response.json()
            animation_url = result["url"]
            await message.reply_animation(animation=animation_url)


__help__ = """
*✨ Sends fun Gifs/Images*

➥ /nekomode on : Enables fun neko mode.
➥ /nekomode off : Disables fun neko mode

» /bully: sends random bully gifs.
» /neko: sends random neko gifs.
» /wallpaper: sends random wallpapers.
» /highfive: sends random highfive gifs.
» /tickle: sends random tickle GIFs.
» /wave: sends random wave GIFs.
» /smile: sends random smile GIFs.
» /feed: sends random feeding GIFs.
» /blush: sends random blush GIFs.
» /avatar: sends random avatar stickers.
» /waifu: sends random waifu stickers.
» /kiss: sends random kissing GIFs.
» /cuddle: sends random cuddle GIFs.
» /cry: sends random cry GIFs.
» /bonk: sends random cuddle GIFs.
» /smug: sends random smug GIFs.
» /slap: sends random slap GIFs.
» /hug: get hugged or hug a user.
» /pat: pats a user or get patted.
» /spank: sends a random spank gif.
» /dance: sends a random dance gif.
» /poke: sends a random poke gif.
» /wink: sends a random wink gif.
» /bite: sends random bite GIFs.
» /handhold: sends random handhold GIFs.
"""

__mod_name__ = "ɴᴇᴋᴏ"
# <================================================ END =======================================================>

from geopy.geocoders import Nominatim
from pyrogram import filters
from pyrogram.raw import functions as raw_functions
from pyrogram.raw import types as raw_types
from pyrogram.types import Message

from FallenRobot import pbot


@pbot.on_message(filters.command("gps"))
async def gps_handler(_, message: Message):
    args = message.text.split(None, 1)
    if len(args) < 2:
        await message.reply("Usage: /gps <location>")
        return

    location_query = args[1]
    try:
        geolocator = Nominatim(user_agent="FallenRobot")
        geoloc = geolocator.geocode(location_query)
        if not geoloc:
            await message.reply("I can't find that location.")
            return

        gm = f"https://www.google.com/maps/search/{geoloc.latitude},{geoloc.longitude}"

        # Send venue/location using Pyrogram
        await pbot.send_location(
            message.chat.id,
            latitude=float(geoloc.latitude),
            longitude=float(geoloc.longitude),
        )
        await message.reply(
            f"ᴏᴘᴇɴ ᴡɪᴛʜ : [🌏ɢᴏᴏɢʟᴇ ᴍᴀᴩs]({gm})",
            disable_web_page_preview=True,
        )
    except Exception:
        await message.reply("I can't find that")


__help__ = """
Sends you the gps location of the given query...

 ❍ /gps <location> *:* Get gps location.
"""

__mod_name__ = "Gᴘs"

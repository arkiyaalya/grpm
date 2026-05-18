import io

import aiohttp
from pyrogram import filters
from pyrogram.types import Message

from FallenRobot import pbot


@pbot.on_message(filters.command("weather"))
async def weather_handler(_, message: Message):
    args = message.text.split(None, 1)
    if len(args) < 2:
        await message.reply("Usage: /weather <city>")
        return

    input_str = args[1]
    sample_url = f"https://wttr.in/{input_str}.png"
    async with aiohttp.ClientSession() as session:
        async with session.get(sample_url) as response:
            data = await response.read()
            with io.BytesIO(data) as out_file:
                out_file.name = "weather.png"
                await message.reply_photo(photo=out_file)


__help__ = """
I can find weather of all cities

❍ /weather <city>*:* Advanced weather module
 ❍ /weather moon*:* Get the current status of moon
"""

__mod_name__ = "Wᴇᴀᴛʜᴇʀ"

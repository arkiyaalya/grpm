import io
import json as json_lib

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message

from FallenRobot import pbot


async def is_user_admin(chat_id: int, user_id: int) -> bool:
    async for member in pbot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == user_id:
            return True
    return False


@pbot.on_message(filters.command("json"))
async def json_handler(_, message: Message):
    if message.chat.type.value != "private":
        if not await is_user_admin(message.chat.id, message.from_user.id):
            await message.reply(
                "🥴 ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴩᴏᴡᴇʀ ᴛᴏ ᴜsᴇ ᴛʜɪs ɪɴ ɢʀᴏᴜᴩs﹐ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ɪᴛ ɪɴ ᴍʏ ᴩᴍ."
            )
            return

    target_message = message.reply_to_message if message.reply_to_message else message
    msg_dict = json_lib.loads(str(target_message))
    the_real_message = json_lib.dumps(msg_dict, indent=2, ensure_ascii=False)

    if len(the_real_message) > 4095:
        with io.BytesIO(the_real_message.encode()) as out_file:
            out_file.name = "json.txt"
            await message.reply_document(document=out_file)
    else:
        await message.reply(f"`{the_real_message}`")


__mod_name__ = "JSON"
__help__ = """
 ❍ /json*:* (reply to a message) Get raw JSON of that message.
"""

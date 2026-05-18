import time

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message

from FallenRobot import DRAGONS, pbot


async def user_is_admin(chat_id: int, user_id: int) -> bool:
    if user_id in DRAGONS:
        return True
    async for member in pbot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == user_id:
            return True
    return False


async def bot_can_delete(chat_id: int) -> bool:
    me = await pbot.get_me()
    async for member in pbot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == me.id:
            return member.privileges.can_delete_messages if member.privileges else False
    return False


@pbot.on_message(filters.command("purge") & filters.group)
async def purge_messages(_, message: Message):
    start = time.perf_counter()

    if not await user_is_admin(message.chat.id, message.from_user.id):
        await message.reply("Only Admins are allowed to use this command")
        return

    if not await bot_can_delete(message.chat.id):
        await message.reply("Can't seem to purge the message")
        return

    if not message.reply_to_message:
        await message.reply("Reply to a message to select where to start purging from.")
        return

    message_ids = []
    from_id = message.reply_to_message.id
    to_id = message.id
    for msg_id in range(from_id, to_id + 1):
        message_ids.append(msg_id)
        if len(message_ids) == 100:
            await pbot.delete_messages(message.chat.id, message_ids)
            message_ids = []
    if message_ids:
        await pbot.delete_messages(message.chat.id, message_ids)

    time_ = time.perf_counter() - start
    await pbot.send_message(message.chat.id, f"`Purged Successfully in {time_:0.2f} Seconds.`")


@pbot.on_message(filters.command("del") & filters.group)
async def delete_message(_, message: Message):
    if not await user_is_admin(message.chat.id, message.from_user.id):
        await message.reply("Only Admins are allowed to use this command")
        return

    if not await bot_can_delete(message.chat.id):
        await message.reply("Can't seem to delete this?")
        return

    if not message.reply_to_message:
        await message.reply("Whadya want to delete?")
        return

    await pbot.delete_messages(
        message.chat.id,
        [message.reply_to_message.id, message.id],
    )


__help__ = """
 ❍ /del*:* deletes the message you replied to
 ❍ /purge*:* deletes all messages between this and the replied to message.
"""

__mod_name__ = "Pᴜʀɢᴇ"

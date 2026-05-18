import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message

from FallenRobot import pbot

spam_chats = []


@pbot.on_message(filters.command(["tagall", "all"]) & filters.group)
async def mentionall(_, message: Message):
    chat_id = message.chat.id

    # Check if user is admin
    is_admin = False
    async for member in pbot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == message.from_user.id:
            is_admin = True
            break

    if not is_admin:
        return await message.reply("__Only admins can mention all!__")

    args = message.text.split(None, 1)
    if len(args) > 1 and message.reply_to_message:
        return await message.reply("__Give me one argument!__")
    elif len(args) > 1:
        mode = "text_on_cmd"
        msg_text = args[1]
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg_text = message.reply_to_message
    else:
        return await message.reply(
            "__Reply to a message or give me some text to mention others!__"
        )

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for member in pbot.get_chat_members(chat_id):
        if chat_id not in spam_chats:
            break
        user = member.user
        usrnum += 1
        usrtxt += f"[{user.first_name}](tg://user?id={user.id}), "
        if usrnum == 5:
            if mode == "text_on_cmd":
                await pbot.send_message(chat_id, f"{msg_text}\n{usrtxt}")
            elif mode == "text_on_reply":
                await msg_text.reply(usrtxt)
            await asyncio.sleep(3)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except Exception:
        pass


@pbot.on_message(filters.command("cancel") & filters.group)
async def cancel_spam(_, message: Message):
    chat_id = message.chat.id
    if chat_id not in spam_chats:
        return await message.reply("__There is no process on going...__")

    is_admin = False
    async for member in pbot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == message.from_user.id:
            is_admin = True
            break

    if not is_admin:
        return await message.reply("__Only admins can execute this command!__")

    try:
        spam_chats.remove(chat_id)
    except Exception:
        pass
    return await message.reply("__Stopped mention.__")


__mod_name__ = "Tᴀɢ Aʟʟ"
__help__ = """
*Only for admins*

❍ /tagall or @all '(reply to message or add another message) To mention all members in your group, without exception.'
"""

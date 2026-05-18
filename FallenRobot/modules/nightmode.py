from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.raw import functions as raw_functions
from pyrogram.raw import types as raw_types
from pyrogram.types import Message

from FallenRobot import BOT_NAME, pbot
from FallenRobot.modules.sql.night_mode_sql import (
    add_nightmode,
    get_all_chat_id,
    is_nightmode_indb,
    rmnightmode,
)

import logging
logger = logging.getLogger(__name__)


async def is_user_admin(chat_id: int, user_id: int) -> bool:
    async for member in pbot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == user_id:
            return True
    return False


@pbot.on_message(filters.command("nightmode") & filters.group)
async def close_ws(_, message: Message):
    if not await is_user_admin(message.chat.id, message.from_user.id):
        await message.reply("🤦🏻‍♂️You are not admin so you can't use this command...")
        return

    if is_nightmode_indb(str(message.chat.id)):
        await message.reply("This Chat Has Already Enabled Night Mode.")
        return

    add_nightmode(str(message.chat.id))
    await message.reply(
        f"Added Chat {message.chat.title} With Id {message.chat.id} To Database. "
        "**This Group Will Be Closed On 12Am(IST) And Will Opened On 06Am(IST)**"
    )


@pbot.on_message(filters.command("rmnight") & filters.group)
async def disable_ws(_, message: Message):
    if not await is_user_admin(message.chat.id, message.from_user.id):
        await message.reply("🤦🏻‍♂️You are not admin so you can't use this command...")
        return

    if not is_nightmode_indb(str(message.chat.id)):
        await message.reply("This Chat Has Not Enabled Night Mode.")
        return

    rmnightmode(str(message.chat.id))
    await message.reply(
        f"Removed Chat {message.chat.title} With Id {message.chat.id} From Database."
    )


async def job_close():
    ws_chats = get_all_chat_id()
    if not ws_chats:
        return
    for warner in ws_chats:
        try:
            chat_id = int(warner.chat_id)
            await pbot.send_message(
                chat_id,
                f"**Night Mode Started**\n\n`Group Is Closing Till 6 Am, Only admins can messages in this chat.`\n\n__Powered By {BOT_NAME}__",
            )
            # Lock chat using raw API
            peer = await pbot.resolve_peer(chat_id)
            await pbot.invoke(
                raw_functions.messages.EditChatDefaultBannedRights(
                    peer=peer,
                    banned_rights=raw_types.ChatBannedRights(
                        until_date=None,
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_inline=True,
                        send_polls=True,
                        invite_users=True,
                        pin_messages=True,
                        change_info=True,
                    ),
                )
            )
        except Exception as e:
            logger.info(f"Unable To Close Group {warner} - {e}")


async def job_open():
    ws_chats = get_all_chat_id()
    if not ws_chats:
        return
    for warner in ws_chats:
        try:
            chat_id = int(warner.chat_id)
            await pbot.send_message(
                chat_id,
                f"**Night Mode Ended**\n\n`Group is opening again now everyone can send messages in this chat.`\n__Powered By {BOT_NAME}__",
            )
            # Unlock chat using raw API
            peer = await pbot.resolve_peer(chat_id)
            await pbot.invoke(
                raw_functions.messages.EditChatDefaultBannedRights(
                    peer=peer,
                    banned_rights=raw_types.ChatBannedRights(
                        until_date=None,
                        send_messages=False,
                        send_media=False,
                        send_stickers=False,
                        send_gifs=False,
                        send_games=False,
                        send_inline=False,
                        send_polls=False,
                        invite_users=True,
                        pin_messages=True,
                        change_info=True,
                    ),
                )
            )
        except Exception as e:
            logger.info(f"Unable To Open Group {warner.chat_id} - {e}")


# Run everyday at 12am IST
scheduler_close = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler_close.add_job(job_close, trigger="cron", hour=23, minute=59)
scheduler_close.start()

# Run everyday at 06am IST
scheduler_open = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler_open.add_job(job_open, trigger="cron", hour=6, minute=1)
scheduler_open.start()

__help__ = """
*Admins Only*

❍ /nightmode*:* Adds Group to NightMode Chats
 ❍ /rmnight*:* Removes Group From NightMode Chats

*Note:* Night Mode chats get Automatically closed at 12 am(IST) and Automatically openned at 6 am(IST) to Prevent Night Spams.
"""

__mod_name__ = "Nɪɢʜᴛ"

import os
import time
import zipfile

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message

from FallenRobot import TEMP_DOWNLOAD_DIRECTORY, pbot


async def is_user_admin(chat_id: int, user_id: int) -> bool:
    async for member in pbot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.id == user_id:
            return True
    return False


extracted = TEMP_DOWNLOAD_DIRECTORY + "extracted/"
thumb_image_path = TEMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
if not os.path.isdir(extracted):
    os.makedirs(extracted)


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


@pbot.on_message(filters.command("zip"))
async def zip_handler(_, message: Message):
    if not message.reply_to_message:
        await message.reply("Reply to a file to compress it.")
        return

    if message.chat.type.value != "private":
        if not await is_user_admin(message.chat.id, message.from_user.id):
            await message.reply(
                "Hey, you are not admin. You can't use this command, But you can use in my PM 🙂"
            )
            return

    mone = await message.reply("⏳️ Please wait...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    try:
        downloaded_file_name = await message.reply_to_message.download(
            file_name=TEMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await mone.edit(str(e))
        return

    zip_path = downloaded_file_name + ".zip"
    zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED).write(downloaded_file_name)

    await message.reply_document(
        document=zip_path,
        reply_to_message_id=message.id,
    )
    os.remove(downloaded_file_name)
    os.remove(zip_path)
    await mone.delete()


@pbot.on_message(filters.command("unzip"))
async def unzip_handler(_, message: Message):
    if not message.reply_to_message:
        await message.reply("Reply to a zip file.")
        return

    if message.chat.type.value != "private":
        if not await is_user_admin(message.chat.id, message.from_user.id):
            await message.reply(
                "Hey, You are not admin. You can't use this command, But you can use in my PM 🙂"
            )
            return

    mone = await message.reply("Processing...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    try:
        downloaded_file_name = await message.reply_to_message.download(
            file_name=TEMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await mone.edit(str(e))
        return

    with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
        zip_ref.extractall(extracted)

    filename = sorted(get_lst_of_files(extracted, []))
    await message.reply("Unzipping now 😌")

    for single_file in filename:
        if os.path.exists(single_file):
            caption_rts = os.path.basename(single_file)
            try:
                await message.reply_document(
                    document=single_file,
                    reply_to_message_id=message.id,
                )
            except Exception as e:
                await pbot.send_message(
                    message.chat.id,
                    f"{caption_rts} caused `{e}`",
                    reply_to_message_id=message.id,
                )
            os.remove(single_file)

    os.remove(downloaded_file_name)
    await mone.delete()


__help__ = """
Hey I can convert files here.

 ❍ /zip*:* reply to a telegram file to compress it in .zip format
 ❍ /unzip*:* reply to a telegram file to decompress it from the .zip format
"""

__mod_name__ = "Zɪᴘᴘᴇʀ"

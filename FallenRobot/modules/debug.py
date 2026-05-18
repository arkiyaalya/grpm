import datetime
import os

from pyrogram import filters
from pyrogram.types import Message
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from FallenRobot import dispatcher, pbot
from FallenRobot.modules.helper_funcs.chat_status import dev_plus

DEBUG_MODE = False


@dev_plus
def debug(update: Update, context: CallbackContext):
    global DEBUG_MODE
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message
    print(DEBUG_MODE)
    if len(args) > 1:
        if args[1] in ("yes", "on"):
            DEBUG_MODE = True
            message.reply_text("Debug mode is now on.")
        elif args[1] in ("no", "off"):
            DEBUG_MODE = False
            message.reply_text("Debug mode is now off.")
    else:
        if DEBUG_MODE:
            message.reply_text("Debug mode is currently on.")
        else:
            message.reply_text("Debug mode is currently off.")


@pbot.on_message(filters.regex(r"^[/!]"))
async def i_do_nothing_yes(_, message: Message):
    global DEBUG_MODE
    if DEBUG_MODE:
        text = message.text or ""
        from_id = message.from_user.id if message.from_user else "Unknown"
        chat_id = message.chat.id
        print(f"-{from_id} ({chat_id}) : {text}")
        if os.path.exists("updates.txt"):
            with open("updates.txt", "r") as f:
                existing = f.read()
            with open("updates.txt", "w+") as f:
                f.write(existing + f"\n-{from_id} ({chat_id}) : {text}")
        else:
            with open("updates.txt", "w+") as f:
                f.write(
                    f"- {from_id} ({chat_id}) : {text} | {datetime.datetime.now()}"
                )


@dev_plus
def logs(update: Update, context: CallbackContext):
    user = update.effective_user
    with open("log.txt", "rb") as f:
        context.bot.send_document(document=f, filename=f.name, chat_id=user.id)


LOG_HANDLER = CommandHandler("logs", logs, run_async=True)
DEBUG_HANDLER = CommandHandler("debug", debug, run_async=True)

dispatcher.add_handler(LOG_HANDLER)
dispatcher.add_handler(DEBUG_HANDLER)

__mod_name__ = "Debug"
__command_list__ = ["debug"]
__handlers__ = [DEBUG_HANDLER]

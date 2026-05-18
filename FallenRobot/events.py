import inspect
import re
import traceback
from functools import wraps
from pathlib import Path

from httpx import AsyncClient, Timeout
from pymongo import MongoClient
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden

from FallenRobot import MONGO_DB_URI, SUPPORT_CHAT

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["Anonymous"]
gbanned = db.gban


state = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)


def get_urls_from_text(text: str) -> list:
    # This regex will match most URLs in a given text.
    regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))"""

    # Use re.findall to find all occurrences that match the regex
    return [x[0] for x in re.findall(regex, text)]


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await app.leave_chat(message.chat.id)
            return
        except Exception as err:
            errors = traceback.format_exc()
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await app.send_message(SUPPORT_CHAT, x)
            raise err

    return capture


def register(**args):
    """No-op decorator: modules have been migrated to Pyrofork."""
    def decorator(func):
        return func
    return decorator


def chataction(**args):
    """No-op decorator: modules have been migrated to Pyrofork."""
    def decorator(func):
        return func
    return decorator


def userupdate(**args):
    """No-op decorator: modules have been migrated to Pyrofork."""
    def decorator(func):
        return func
    return decorator


def inlinequery(**args):
    """No-op decorator: modules have been migrated to Pyrofork."""
    def decorator(func):
        return func
    return decorator


def callbackquery(**args):
    """No-op decorator: modules have been migrated to Pyrofork."""
    def decorator(func):
        return func
    return decorator


def bot(**args):
    """No-op decorator: modules have been migrated to Pyrofork."""
    def decorator(func):
        return func
    return decorator


def fallenrobot(**args):
    pattern = args.get("pattern", None)
    args.get("disable_edited", False)
    ignore_unsafe = args.get("ignore_unsafe", False)
    unsafe_pattern = r"^[^/!#@\$A-Za-z]"
    args.get("group_only", False)
    args.get("disable_errors", False)
    args.get("insecure", False)
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    if "ignore_unsafe" in args:
        del args["ignore_unsafe"]

    if "group_only" in args:
        del args["group_only"]

    if "disable_errors" in args:
        del args["disable_errors"]

    if "insecure" in args:
        del args["insecure"]

    if pattern:
        if not ignore_unsafe:
            args["pattern"] = args["pattern"].replace("^.", unsafe_pattern, 1)

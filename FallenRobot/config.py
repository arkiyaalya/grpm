class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    API_ID = 10130264
    API_HASH = "aa0734d88e68fa88b19504fc1124af9b"

    CASH_API_KEY = "U556QDQ2OR78JKRS"  # Get this value for currency converter from https://www.alphavantage.co/support/#api-key
    # new
    DATABASE_URL = "postgresql://postgres:Pr%40040503rP%40@db.hkdyxmtftngpgftqwexf.supabase.co:5432/postgres"
    # old
    # DATABASE_URL = "postgresql://neondb_owner:npg_rSisxCA0Gk7H@ep-spring-sun-a43z382i-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

    EVENT_LOGS = ()  # Event logs channel to note down important bot level events

    MONGO_DB_URI = "mongodb+srv://JeffyBackUp:JeffyBackUp@cluster0.hgbjdhr.mongodb.net/?retryWrites=true&w=majority"

    # Telegraph link of the image which will be shown at start command.
    START_IMG = "http://master.koyeb.app/view/O8Eu5i1e"

    SUPPORT_CHAT = "Emitingstars_botz"  # Your Telegram support group chat username where your users will go and bother you https://t.me/EmitingStars_Botz

    TOKEN = "8575153893:AAEDg4br1PrmGibmkHX_aYlMFHLqUlBST38"  # Get bot token from @BotFather on Telegram

    TIME_API_KEY = "PAVA0FXIC2Z2"  # Get this value from https://timezonedb.com/api

    OWNER_ID = 7089676783  # User id of your telegram account (Must be integer)

    # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True

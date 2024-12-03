from telegram_handle.config import TelegramBot
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
group_chat_id = os.getenv("GROUP_CHAT_ID")

# create instance
tg_bot = TelegramBot(bot_token, group_chat_id)

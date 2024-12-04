from src.database.setup import db

from telegram import Bot
from telegram import InputFile, Update
from telegram.ext import Application, CommandHandler, CallbackContext
from collections import defaultdict
import time
import os
import logging
import asyncio
import requests
import httpx

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the level to INFO to capture log messages at the INFO level and above
    format="%(asctime)s - %(levelname)s - %(message)s",  # Optional: format the log output
)


class TelegramBot:
    def __init__(self, bot_token: str, group_chat_id: str) -> None:
        self.bot_token = bot_token
        self.group_chat_id = group_chat_id

        self.app = None

    def initialize(self):
        # initialize the bot when creating a new instance
        self.app = Application.builder().token(self.bot_token).build()
        self._register_handlers()

    def run(self) -> None:
        """Run the bot in polling mode."""
        if not self.app:
            raise RuntimeError("Bot is not initialized. Call `initialize` first.")
        print(f"Application instance: {self.app}")
        print("Bot is running...")
        try:
            asyncio.run(self.app.run_polling(drop_pending_updates=True))
        except Exception as e:
            print(f"Error running bot: {e}")
        finally:
            asyncio.run(self.app.shutdown())

    def shutdown(self):
        self.app.shutdown()

    def _register_handlers(self) -> None:
        # handler for /start command
        self.app.add_handler(CommandHandler("start", self.start))

        # handler for /request_file command
        self.app.add_handler(CommandHandler("request_file", self.send_file_to_group))

    def start(self, update: Update, context: CallbackContext) -> None:
        """Handle /start command"""
        update.message.reply_text(
            """ Hello! You can request files by using the command "/request_file <filename>". """
        )

    async def send_file_to_group(
        self, update: Update, context: CallbackContext
    ) -> None:

        FILE_DIR = os.path.join(os.path.dirname(__file__), "../data")
        request_filename = " ".join(context.args)
        logging.info(request_filename)
        print(FILE_DIR, request_filename)

        # if request file is shinkansen
        # run query then save csv and push to telegram
        if request_filename in "shinkansen":
            # make a request to FastAPI server to get data and save as csv
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/shinkansen")

            if response.status_code == 200:
                with open(os.path.join(FILE_DIR, "shinkansen.csv"), "rb") as file:
                    await update.message.reply_document(
                        document=InputFile(file),
                        caption=f"Requested file: {request_filename}.csv",
                    )
                logging.info(f"Sent {request_filename} to Telegram group.")
            else:
                await update.message.reply_text(f"Error generating {request_filename} ")
        else:
            await update.message.reply_text(f"File {request_filename} not found.")

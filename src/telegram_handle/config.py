from src.database.setup import db

from telegram import Bot
from telegram import InputFile, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    ContextTypes,
    CallbackQueryHandler,
)
from src.telegram_handle.business_logic import check_sending_request_context
from src.utils.data_utils import tg_keywords
from dotenv import load_dotenv
import os
import logging
import asyncio


load_dotenv()
# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the level to INFO to capture log messages at the INFO level and above
    format="%(asctime)s - %(levelname)s - %(message)s",  # Optional: format the log output
)


class TelegramBot:
    def __init__(self, bot_token: str, group_chat_id: str) -> None:
        self.bot_token = bot_token
        self.group_chat_id = group_chat_id
        self.tg_keywords = tg_keywords()
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
        # handler for button click
        self.app.add_handler(CallbackQueryHandler(self.handle_menu_click))

        # handler for /request_file command
        self.app.add_handler(CommandHandler("request_file", self.handle_request_file))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if str(update.message.chat_id) != str(os.getenv("GROUP_CHAT_ID")):
            logging.info("Cannot handle the request, Unauthorized group")
            await update.message.reply_text(
                "you are not allowed to send the request message"
            )
            return

        """Handle /start command"""
        keyboard = [
            [InlineKeyboardButton("Shinkansen", callback_data="Shinkansen")],
            [InlineKeyboardButton("Tokyo", callback_data="Tokyo")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

    async def handle_menu_click(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if str(update.callback_query.message.chat.id) != str(
            os.getenv("GROUP_CHAT_ID")
        ):
            logging.info("Cannot handle the request, Unauthorized group")
            await update.callback_query.message.reply_text(
                "you are not allowed to send the request message"
            )
            return
        query = update.callback_query
        await query.answer()
        if query.data.lower() in self.tg_keywords:
            context.args = [query.data]
            await query.edit_message_text(
                f"{query.data} clicked, Processing request..."
            )
            await self.send_file_to_group(query.message, context)
        else:
            await query.edit_message_text("Invalid option")

    async def handle_request_file(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Handle /request_file command"""
        if str(update.message.chat_id) != str(os.getenv("GROUP_CHAT_ID")):
            logging.info("Cannot handle the request, Unauthorized group")
            await update.message.reply_text(
                "you are not allowed to send the request message"
            )
            return

        request_filename = " ".join(context.args) if context.args else None
        if not request_filename:
            await update.message.reply_text("Please specify the file name.")
            return

        # Ensure `update.message` is passed as the message parameter
        await self.send_file_to_group(update.message, context)

    async def send_file_to_group(self, message, context: CallbackContext) -> None:
        request_filename = context.args[0]
        output_filepath = await check_sending_request_context(
            request_filename, self.tg_keywords
        )

        if not output_filepath:
            await message.reply_text(
                f"Error generating {request_filename} , check the filename and output filepath. "
            )
            return

        with open(output_filepath, "rb") as file:
            await message.reply_document(
                document=InputFile(file),
                caption=f"Requested file: {request_filename}",
            )
        logging.info(f"Sent {request_filename} to Telegram group.")

from telegram import Bot
from telegram import InputFile, Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
import logging
import httpx


async def check_sending_request_context(request_filename, tg_keywords):

    FILE_DIR = os.path.join(os.path.dirname(__file__), "../data")
    request_filename = request_filename.lower()
    # if request file is shinkansen
    # run query then save csv and push to telegram
    if request_filename in tg_keywords:
        # make a request to FastAPI server to get data and save as csv
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                f"http://localhost:8000/data/?filename={request_filename}"
            )

            if response.status_code != 200:
                logging.info("HTTP Response: {}".format(response.status_code))
                return False

            file_path = os.path.join(FILE_DIR, f"{request_filename}.csv")

            if os.path.exists(file_path):
                return file_path

from src.database.setup import db
from src.telegram_handle.setup import tg_bot
from src.api.routes import app
import threading
import uvicorn


def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def start_telegram_bot():
    tg_bot.initialize()
    tg_bot.run()


if __name__ == "__main__":
    # start FastAPI server in a separate thread
    thread_fastapi = threading.Thread(target=start_fastapi)
    thread_fastapi.start()

    # main thread
    start_telegram_bot()

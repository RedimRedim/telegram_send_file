from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

from src.api.logic import ApiLogicInstance

app = FastAPI()


@app.get("/")
def testing():
    return {"message": "Hello, World!"}


@app.get("/shinkansen")
def get_file():
    ApiLogicInstance.get_shinkansen_data()
    # run query + save the file + find the file
    file = os.path.join(os.path.dirname(__file__), "../data/shinkansen.csv")

    return FileResponse(file, media_type="text/csv", filename="shinkansen.csv")

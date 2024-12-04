from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

from src.api.logic import ApiLogicInstance

app = FastAPI()


@app.get("/")
def testing():
    return {"message": "Hello, World!"}


@app.get("/data")
async def get_file(filename: str):
    filename = filename.lower()

    if not filename:
        return {"error": "Filename is required."}

    if filename not in ["shinkansen", "tokyo"]:
        raise HTTPException(status_code=400, detail="Invalid filename")

    if filename == "shinkansen":
        # run query + save the file + find the file
        ApiLogicInstance.get_shinkansen_data()
    elif filename == "tokyo":
        ApiLogicInstance.get_tokyo_data()

    file = os.path.join(os.path.dirname(__file__), f"../data/{filename}.csv")
    return FileResponse(file, media_type="text/csv", filename=f"{filename}.csv")

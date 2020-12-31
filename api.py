import os
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

# to run server, uvicorn api:app --reload
app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    with open("tmp/input.jpg", "wb") as ff:
        ff.write(contents)

    os.system(
        "python neural_style/neural_style.py eval --content-image tmp/input.jpg --model saved-models/mosaic.pth --output-image tmp/output.jpg  --cuda 0"
    )
    ##processing

    return FileResponse("tmp/output.jpg")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
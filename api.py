import os
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
#from app.api.routes import router as api_router

# to run server, uvicorn api:app --reload
def get_application():
    app = FastAPI(title="Phresh", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    #app.include_router(api_router, prefix="/api")
    return app
app = get_application()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...), style: Optional[str] = "mosaic"
):
    # resolve style
    if style + ".pth" not in os.listdir("saved-models"):
        style = "mosaic"

    contents = await file.read()
    with open("tmp/input.jpg", "wb") as ff:
        ff.write(contents)

    os.system(
        "python neural_style/neural_style.py eval --content-image tmp/input.jpg --model saved-models/"
        + style
        + ".pth --output-image tmp/output.jpg  --cuda 0"
    )
    ##processing

    return {"style": style, "img": FileResponse("tmp/output.jpg")}


@app.get("/style_image/{style}")
async def stylize_image(style: str, file: UploadFile = File(...)):
    contents = await file.read()
    with open("tmp/input.jpg", "wb") as ff:
        ff.write(contents)

    os.system(
        "python neural_style/neural_style.py eval --content-image tmp/input.jpg --model saved-models/mosaic.pth --output-image tmp/output.jpg  --cuda 0"
    )
    ##processing

    return {"style": style, "img": FileResponse("tmp/output.jpg")}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
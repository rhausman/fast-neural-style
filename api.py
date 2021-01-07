import os
import base64
from skimage import io, transform
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# from app.api.routes import router as api_router

# to run server, uvicorn api:app --reload
def get_application():
    app = FastAPI(title="Phresh", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # *
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.include_router(api_router, prefix="/api")
    return app


app = get_application()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.post("/style_image/{style}")
async def style_the_image(
    file: UploadFile = File(...), style: Optional[str] = "mosaic"
):
    print("STYLE: ", style)
    # resolve style
    if style + ".pth" not in os.listdir("saved-models"):
        style = "mosaic"

    contents = await file.read()
    with open("tmp/input.jpg", "wb") as ff:
        ff.write(contents)
    # open the image, resize, and save
    # desired width = 300px
    img = io.imread("tmp/input.jpg")
    scale_factor = 300 / img.shape[1]
    height, width = (img.shape[0] * scale_factor, img.shape[1] * scale_factor)
    img = transform.resize(img, (height, width, 3))
    print("SHAPE: ", img.shape)
    io.imsave("tmp/input.jpg", img)

    os.system(
        "python neural_style/neural_style.py eval --content-image tmp/input.jpg --model saved-models/"
        + style
        + ".pth --output-image tmp/output.jpg  --cuda 0"
    )
    ##processing
    with open("tmp/output.jpg", "rb") as ff:
        encoded = base64.b64encode(ff.read())
    return {
        "name": style,
        "img": encoded,
    }


# get the example style images
# @app.get
"""
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

"""


@app.get("/get_available_styles")
def read_test():
    return [pth.split(".")[0] for pth in os.listdir("saved-models")]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: str):
    # , file: Optional[UploadFile] = File(...)):
    print("ID:::", item_id)
    return {"Hello": item_id}  # , "image": file}


@app.post("/items/{item_id}")
def read_item(item_id: str, file: Optional[UploadFile] = File(...)):
    print("ID:::", item_id, "incoming", file)
    return FileResponse(
        "tmp/output.jpg"
    )  # {"name": item_id, "img": FileResponse("tmp/output.jpg")}  # , "image": file}


@app.post("/filetest/{item_id}")
def read_item(item_id: str, file: Optional[UploadFile] = File(...)):
    print("TEST: ", item_id)
    with open("tmp/output.jpg", "rb") as ff:
        encoded = base64.b64encode(ff.read())
    print(encoded)
    return {
        "name": item_id,
        "img": encoded,
    }  # FileResponse("tmp/output.jpg")}  # , "image": file}


"""
@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    print(item_id)
    return {"item_name": item.name, "item_id": item_id}
"""
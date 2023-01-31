from fastapi import FastAPI, UploadFile, File, Response
from fastapi.param_functions import Depends
from typing import List, Union, Optional, Dict, Any

from app.model import SDAFNet_Tryon, get_model, get_avatar, predict_from_image_byte

app = FastAPI()

@app.get("/")
def hello_world():
    return {"hello": "world"}

# @app.get("/order", description="주문 리스트를 가져옵니다")
# async def get_orders() -> List[Order]:
#     return orders

@app.post("/order", description="결과를 요청합니다")
async def make_order(files: List[UploadFile] = File(...),
                     model: SDAFNet_Tryon = Depends(get_model),
                     result: Dict[str, Any] = Depends(get_avatar)):
    for file in files:
        image_bytes = await file.read()
        inference_result = predict_from_image_byte(model=model, image_bytes=image_bytes, result=result)
        print('OK !!!!!')

    headers = {'Content-Disposition': 'inline; filename="test.jpeg"'}
    
    return Response(inference_result, headers=headers, media_type='image/jpeg')
# とりあえずデータ送信がうまくいってるか確認する用のスクリプト．

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return {"message": 'Hello World!'}


if __name__=="__main__":
    uvicorn.run("run:app",port=3001, reload=True)
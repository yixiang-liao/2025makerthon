from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import admin
from app.services.websocket_manager import manager
from app.services.scheduler import start_scheduler
from app.services.crawler import crawl

import json, os


IMG_DB_PATH = "data/image_db.json"
TITLE_PATH = "data/title.json"

def load_json(path):
    return json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else {}

app = FastAPI()

app = FastAPI(root_path="/2025skill/api")

# ✅ CORS 跨域設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 上線可改指定網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("✅ 有 WebSocket 連線")
    try:
        while True:
            try:
                data = await websocket.receive_json()
                action = data.get("action")

                if action == "get_all":
                    images_db = load_json(IMG_DB_PATH)
                    images = [{ "id": k, "url": f"/admin/image/{k}" } for k in images_db]
                    title_data = load_json(TITLE_PATH)
                    crawled = await crawl()

                    await websocket.send_json({
                        "type": "full_data",
                        "data": {
                            "images": images,
                            "title": title_data.get("title", ""),
                            "equipment_data": crawled.get("equipment_data", []),
                            "tool_data": crawled.get("tool_data", "")
                        }
                    })

                else:
                    await websocket.send_json({ "type": "error", "message": "未知操作" })

            except json.JSONDecodeError:
                await websocket.receive_text()

    except WebSocketDisconnect:
        print("❌ WebSocket 中斷")
        await manager.disconnect(websocket)

# API & 靜態目錄
app.include_router(admin.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

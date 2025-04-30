# ✅ app/api/admin.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import uuid, os, json

router = APIRouter()

# 路徑設定
IMAGE_DIR = "static/images"
IMG_DB_PATH = "data/image_db.json"
TITLE_PATH = "data/title.json"

# 輔助函式 - 讀寫 JSON
def load_json(path):
    return json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------------- 圖片 API ----------------

@router.post("/admin/upload_image")
async def upload_image(file: UploadFile = File(...)):
    db = load_json(IMG_DB_PATH)
    image_id = f"img_{uuid.uuid4().hex[:8]}"
    ext = file.filename.split(".")[-1]
    filename = f"{image_id}.{ext}"
    path = os.path.join(IMAGE_DIR, filename)

    with open(path, "wb") as buffer:
        buffer.write(await file.read())

    db[image_id] = filename
    save_json(IMG_DB_PATH, db)

    # 廣播圖片更新
    from app.services.websocket_manager import manager
    images = [{ "id": k, "url": f"/admin/image/{k}" } for k in db]
    await manager.broadcast({ "type": "images", "data": images })

    return {"image_id": image_id, "filename": filename}

@router.get("/admin/images")
def list_images():
    db = load_json(IMG_DB_PATH)
    return [
        { "id": image_id, "url": f"/admin/image/{image_id}" }
        for image_id in db
    ]

@router.get("/admin/image/{image_id}")
def get_image(image_id: str):
    db = load_json(IMG_DB_PATH)
    if image_id not in db:
        raise HTTPException(status_code=404, detail="圖片不存在")
    return FileResponse(os.path.join(IMAGE_DIR, db[image_id]))

@router.delete("/admin/image/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(image_id: str):
    db = load_json(IMG_DB_PATH)
    if image_id not in db:
        raise HTTPException(status_code=404, detail="找不到圖片")

    filename = db[image_id]
    filepath = os.path.join(IMAGE_DIR, filename)

    # 刪除圖片檔案
    if os.path.exists(filepath):
        os.remove(filepath)

    # 刪除資料庫中的記錄
    del db[image_id]
    save_json(IMG_DB_PATH, db)

    # 廣播圖片更新
    from app.services.websocket_manager import manager
    images = [{ "id": k, "url": f"/admin/image/{k}" } for k in db]
    await manager.broadcast({ "type": "images", "data": images })

    return

# ---------------- 標題 API ----------------

@router.get("/admin/title")
def get_title():
    return load_json(TITLE_PATH)

@router.put("/admin/title")
async def update_title(new_title: str = Form(...)):
    save_json(TITLE_PATH, {"title": new_title})

    # 廣播標題更新
    from app.services.websocket_manager import manager
    await manager.broadcast({ "type": "title", "data": { "title": new_title } })

    return { "msg": "標題已更新", "title": new_title }



# @router.websocket("/ws/admin")
# async def websocket_admin(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_json()
#             action = data.get("action")

#             if action == "get_images":
#                 db = load_json(IMG_DB_PATH)
#                 images = [
#                     { "id": k, "url": f"/admin/image/{k}" }
#                     for k in db
#                 ]
#                 await websocket.send_json({ "type": "images", "data": images })

#             elif action == "get_title":
#                 title_data = load_json(TITLE_PATH)
#                 await websocket.send_json({ "type": "title", "data": title_data })

#             else:
#                 await websocket.send_json({ "type": "error", "message": "未知操作" })

#     except WebSocketDisconnect:
#         print("❌ 管理 WebSocket 中斷")
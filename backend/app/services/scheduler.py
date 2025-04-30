from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .crawler import crawl
from .websocket_manager import manager
from app.api.admin import load_json, IMG_DB_PATH, TITLE_PATH

import asyncio

scheduler = AsyncIOScheduler()

async def run_crawler_and_broadcast():
    try:
        images_db = load_json(IMG_DB_PATH)
        images = [{ "id": k, "url": f"/admin/image/{k}" } for k in images_db]
        title_data = load_json(TITLE_PATH)
        crawled = await crawl()

        await manager.broadcast({
            "type": "full_data",
            "data": {
                "images": images,
                "title": title_data.get("title", ""),
                "equipment_data": crawled.get("equipment_data", []),
                "tool_data": crawled.get("tool_data", "")
            }
        })

    except Exception as e:
        print(f"[排程錯誤] {e}")

def start_scheduler():
    scheduler.add_job(run_crawler_and_broadcast, "interval", minutes=1)
    scheduler.start()

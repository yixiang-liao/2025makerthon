from fastapi import WebSocket
from typing import List

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("🔌 新連線，目前連線數：", len(self.active_connections))

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print("❌ 連線中斷，目前連線數：", len(self.active_connections))

    async def broadcast(self, message: dict):
        print(f"📢 廣播訊息給 {len(self.active_connections)} 個連線")
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                await self.disconnect(connection)


manager = WebSocketManager()

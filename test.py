import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("✅ 已連線到 WebSocket")

        # 發送 get_all 請求
        await websocket.send(json.dumps({ "action": "get_all" }))
        print("📤 發送 get_all 請求")

        try:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                print(data)

                if data.get("type") == "full_data":
                    d = data["data"]

                    print("\n📷 圖片：")
                    for img in d["images"]:
                        print(f"  ➤ {img['id']} → {img['url']}")

                    print("\n📝 標題：", d["title"])

                    print("\n🛠 設備資料：")
                    for item in d["equipment_data"]:
                        print(f"  {item['類別']}: 正取={item['正取']}、備取={item['備取']}")

                    print("\n🧰 工具資料：", d["tool_data"])

                else:
                    print("📦 其他資料：", data)

        except websockets.exceptions.ConnectionClosed:
            print("❌ WebSocket 關閉")

if __name__ == "__main__":
    asyncio.run(test_websocket())

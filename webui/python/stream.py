import asyncio
import websockets
import cv2

async def send_stream(websocket, path):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # 在这里进行任何 openCV 处理

        # 将处理后的帧转换为字符串
        print(111)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_str = buffer.tobytes()
        # 发送帧数据到HTML页面
        await websocket.send(frame_str)

async def main():
    start_server = await websockets.serve(send_stream, 'localhost', 8088)
    await start_server.wait_closed()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
loop.run_forever()
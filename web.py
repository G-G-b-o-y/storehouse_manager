from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket
from fastapi.testclient import TestClient
import webbrowser
import uvicorn
from modules.camera import usecamera

html_raw = []
page_list = ["model.html", "signItem.html"]
for fileName in page_list:
    with open(f'htmlpages/{fileName}', 'r', encoding='utf-8') as f:
        data = f.read()   #读取文本
    
    html_raw.append(data)



webapp = FastAPI()

@webapp.get("/", response_class=HTMLResponse)
async def home():
    # 模板页
    return html_raw[0]

# websocket
@webapp.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket.accept()
    # 需要异步的连接，否则会造成阻塞
    while True:
        data = await websocket.receive_text()
        if data == "1004":
            await websocket.send_json({"html" : html_raw[1], "code" : data})
        if data == "scand": 
            await websocket.send_json({"msg" : "please show qrcode", "code" : "203"})  # 提示窗口
            codeData = usecamera()
            await websocket.send_json({"msg" : codeData, "res":"success", "code" : "200"})  # 发送到前端

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8000')
    # 运行fastapi程序
    uvicorn.run(app="web:webapp", host="127.0.0.1", port=8000, reload=True)

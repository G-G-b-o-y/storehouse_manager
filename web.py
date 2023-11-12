from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket
from fastapi.testclient import TestClient
from enum import Enum
import webbrowser
import uvicorn
from modules.camera import usecamera

html_raw = {}
page_list = ["model.html", "signItem.html", "itemInto.html", "outItem.html", "reportTable.html"]
for fileName in page_list:
    with open(f'htmlpages/{fileName}', 'r', encoding='utf-8') as f:
        data = f.read()   #读取文本 
    
    html_raw[fileName[0:-5]] = data

# 枚举
class pages(str, Enum):
    signItem = "signItem"
    itemInto = "itemInto"
    outItem = "outItem"
    reportTable = "reportTable"
    


webapp = FastAPI()

@webapp.get("/{page}", response_class=HTMLResponse)
async def home(page:pages, opened=None):
    if opened:
        return html_raw[page]
    # 模板页
    htmlInsert = html_raw['model'].split("<!-- 内容主体区域 -->", 1)
    # 初次打开 传送整个页面
    return htmlInsert[0]+html_raw[page]+htmlInsert[1]



# websocket
@webapp.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket.accept()
    # 需要异步的连接，否则会造成阻塞
    while True:
        data = await websocket.receive_text()
        if data == "scand": 
            await websocket.send_json({"msg" : "please show qrcode", "code" : "203"})  # 提示窗口
            codeData = usecamera()
            await websocket.send_json({"msg" : codeData, "res":"success", "code" : "200"})  # 发送到前端

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8000/signItem')
    # 运行fastapi程序
    uvicorn.run(app="web:webapp", host="127.0.0.1", port=8000, reload=True)

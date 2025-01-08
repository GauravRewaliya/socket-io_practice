import socketio
from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp
from fastapi.responses import HTMLResponse

app = FastAPI()

sio = AsyncServer(cors_allowed_origins="*", async_mode="asgi")
sio_app = ASGIApp(sio)
app.mount("/socket.io", sio_app)

# app = socketio.ASGIApp(sio, app)
# sio = socketio.ASGIApp(sio)

@app.get("/")
def read_root():
    # return {"Hello": "World"}
    with open("Home.html") as f:
        return HTMLResponse(content=f.read())

@sio.on("connect")
async def connect(sid, environ):
    print("-->>>>  New Client Connected to This id :"+" "+str(sid))
    await sio.emit("send_msg", "Hello from Server")
    
@sio.on("disconnect")
async def disconnect(sid):
    print("--<<<< Client Disconnected from This id :"+" "+str(sid))
    # @sio.on("message")

# @sio.on("message")
# async def message(sid, data):
#     print(data)
#     await sio.emit("message", data, room=sid)
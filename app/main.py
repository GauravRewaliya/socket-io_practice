from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp
from fastapi.responses import HTMLResponse

app = FastAPI()

sio = AsyncServer(cors_allowed_origins="*", async_mode="asgi")
sio_app = ASGIApp(sio)
app.mount("/socket.io", sio_app)

@app.get("/")
def read_root():
    with open("ui/home.html") as f:
        return HTMLResponse(content=f.read())

ROOM_MESSAGES = {}
@app.get("/room/{room_id}")
def read_room(room_id: str):
    with open("ui/room.html") as f:
        return HTMLResponse(content=f.read())

@sio.on("connect", namespace="/room")
async def connect(sid, environ):
    room_id = environ["QUERY_STRING"].split("=")[-1]
    print(f"-->>>>  New Client Connected to This id {sid}::{room_id}")
    await sio.emit("message", {"msg": f"Welcome to Room {room_id}"}, to=sid, namespace=f"/room/{room_id}")

@sio.on("disconnect", namespace="/room")
async def disconnect(sid):
    print(f"<<<---- Client Disconnected from This id :{sid}")

@sio.on("message", namespace="/room")
async def handle_message(sid, data):
    room_id = data.get("room_id")
    message = data.get("message")
    
    if room_id not in ROOM_MESSAGES:
        ROOM_MESSAGES[room_id] = []
    ROOM_MESSAGES[room_id].append(message)
    print(f"Room {room_id} - New message: {message}")
    # await sio.emit("message", {"room_id": room_id, "messages": ROOM_MESSAGES[room_id]}, room=sid, namespace=f"/room/{room_id}")
    await sio.emit("message", {"room_id": room_id, "messages": ROOM_MESSAGES[room_id]}, namespace=f"/room/{room_id}")
    await sio.emit("message", {"room_id": room_id, "messages": ROOM_MESSAGES[room_id]}, namespace=f"/room")
    await sio.emit("message", "hiiii")

@sio.on("delete_message", namespace="/room")
async def delete_message(sid, data):
    message_id = data.get("message_index")
    await sio.emit("delete_message",{message_id: message_id},namespace="/room")
                   
@sio.on("connect")
async def connect(sid, environ):
    print("-->>>>  New Client Connected to This id :"+" "+str(sid))
    await sio.emit("send_msg", "Hello from Server")
    
@sio.on("disconnect")
async def disconnect(sid):
    print("--<<<< Client Disconnected from This id :"+" "+str(sid))
    # @sio.on("message")

@sio.on("message") ## recive data from client
async def message(sid, data):
    print(f"--{sid}->>>>>"+data)
    await sio.emit("message", data, room=sid) ## send to all user's
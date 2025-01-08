from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp
from fastapi.responses import HTMLResponse
from app.room import sio
app = FastAPI()

app.mount("/socket.io", ASGIApp(sio))

@app.get("/")
def read_root():
    with open("ui/home.html") as f:
        return HTMLResponse(content=f.read())

ROOM_MESSAGES = {}
@app.get("/room/{room_id}")
def read_room(room_id: str):
    with open("ui/room.html") as f:
        return HTMLResponse(content=f.read())
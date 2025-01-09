from fastapi import FastAPI
from socketio import AsyncServer
from socketio.asgi import ASGIApp
from fastapi.responses import HTMLResponse
from app.socket_logics import sio
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

@app.get("/socket_docs/api")
async def get_socket_actions():
    # todo: add this dynamically if possible , or seprated doc logic
    return [
        {
            "namespace": "/room",
            "actions": [
            {
                "name": "connect",
                "description": "Connect to the server",
                "params": [],
                "responses": []
            },
            {
                "name": "disconnect",
                "description": "Disconnect from the server",
                "params": [],
                "responses": []
            },
            {
                "name": "join_room",
                "description": "Join a specific room",
                "params": [
                { "name": "room_id", "type": "string", "example": "1234" }
                ],
                "responses": [
                {
                    "namespace": "/room",
                    "room": "1234",
                    "action": "join_room",
                    "data": { "status": "success", "message": "Joined room 1234" }
                }
                ]
            },
            {
                "name": "message",
                "description": "Send a message to a room",
                "params": [
                { "name": "room_id", "type": "string", "example": "1234" },
                { "name": "message", "type": "string", "example": "Hello, world!" }
                ],
                "responses": [
                {
                    "namespace": "/room",
                    "room": "1234",
                    "action": "message",
                    "data": { "status": "success", "message": "Message sent to room 1234" }
                }
                ]
            },
            {
                "name": "delete_message",
                "description": "Delete a message from a room",
                "params": [
                { "name": "room_id", "type": "string", "example": "1234" },
                { "name": "message_id", "type": "string", "example": "5678" }
                ],
                "responses": [
                # {
                #     "namespace": "/room",
                #     "room": "1234",
                #     "action": "delete_message",
                #     "data": { "status": "success", "message": "Message deleted from room 1234" }
                # }
                {
                    "namespace": "/room",
                    "room": "1234",
                    "action": "message",
                    "data": { "room_id": "1234", "messages": ["all messages accept deletedd"] }
                }
                ]
            }
            ]
        },
        {
            "namespace": "/notification",
            "actions": [
                {
                    "name": "connect",
                    "description": "Connect to the server",
                    "params": [],
                    "responses": [
                        {
                            "namespace": "/notification",
                            "room": None,
                            "skip_sid": "self_id",
                            "action": "notification",
                            "data": {"message": "User: sid is connected"}
                        }
                    ]
                },
                {
                    "name": "register",
                    "description": "Register for notifications",
                    "params": [
                    { "name": "user_id", "type": "string", "example": "5678" }
                    ],
                    "responses": [
                    {
                        "namespace": "/notification",
                        "action": "register",
                        "data": { "status": "success", "message": "Registered for notifications" }
                    }
                    ]
                },
                {
                    "name": "disconnect",
                    "description": "Disconnect from the server",
                    "params": [],
                    "responses": []
                }
            ]
        }
    ]
@app.get("/socket_docs")
def socket_docs():
    with open("ui/socket_docs.html") as f:
        return HTMLResponse(content=f.read())
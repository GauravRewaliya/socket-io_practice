from socketio import AsyncServer
from .room import RoomNamespace
from .notification import NotificationNamespace

sio = AsyncServer(cors_allowed_origins="*", async_mode="asgi")
# Register the class-based namespace
sio.register_namespace(RoomNamespace("/room"))
sio.register_namespace(NotificationNamespace("/notification"))

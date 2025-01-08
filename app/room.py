from socketio import AsyncServer, AsyncNamespace

class RoomNamespace(AsyncNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.room_messages = {}

    async def on_connect(self, sid, environ):
        print(f"-->>>> Client connected: {sid}")

    async def on_join_room(self, sid, data):
        room_id = data.get("room_id")
        if not room_id:
            return
        
        await self.enter_room(sid, room_id)
        print(f"-->>>> {sid} joined room {room_id}")

        # Initialize room messages if not already present
        if room_id not in self.room_messages:
            self.room_messages[room_id] = []

        # Send welcome message and existing messages to the client
        await self.emit("message", {
            "msg": f"Welcome to Room {room_id}",
            "messages": self.room_messages[room_id]
        }, to=sid)

    async def on_message(self, sid, data):
        room_id = data.get("room_id")
        message = data.get("message")

        if not room_id or not message:
            return

        # Append the message to the room's message list
        if room_id not in self.room_messages:
            self.room_messages[room_id] = []

        self.room_messages[room_id].append(message)
        print(f"Room {room_id} - New message: {message}")

        # Broadcast updated messages to all clients in the room
        await self.emit("message", {
            "room_id": room_id,
            "messages": self.room_messages[room_id]
        }, room=room_id)

    async def on_delete_message(self, sid, data):
        room_id = data.get("room_id")
        message_index = data.get("message_index")

        if room_id in self.room_messages and 0 <= message_index < len(self.room_messages[room_id]):
            del self.room_messages[room_id][message_index]
            print(f"Room {room_id} - Message {message_index} deleted")

            # Broadcast updated messages to all clients in the room
            await self.emit("message", {
                "room_id": room_id,
                "messages": self.room_messages[room_id]
            }, room=room_id)

    async def on_disconnect(self, sid):
        print(f"--<<<< Client disconnected: {sid}")

# Create the Socket.IO server
sio = AsyncServer(cors_allowed_origins="*", async_mode="asgi")

# Register the class-based namespace
sio.register_namespace(RoomNamespace("/room"))

from socketio import AsyncServer, AsyncNamespace

class NotificationNamespace(AsyncNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.users = {}

    async def on_connect(self, sid, environ):
        await self.emit("notification", {"message": f"User: {sid} is connected"},skip_sid=sid)
        print(f"Notification client connected: {sid}")

    async def on_register(self, sid, data):
        user_id = data.get("user_id")
        if user_id:
            self.users[user_id] = sid
            print(f"User {user_id} registered for notifications")

    async def on_disconnect(self, sid):
        print(f"Notification client disconnected: {sid}")
        self.users = {user: user_sid for user, user_sid in self.users.items() if user_sid != sid}

# Register the namespace
sio.register_namespace(NotificationNamespace("/notification"))

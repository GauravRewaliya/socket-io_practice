
from socketio import AsyncNamespace

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
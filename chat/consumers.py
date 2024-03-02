import base64
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .views import rooms


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.token = self.scope["url_route"]["kwargs"]["token"]
        self.room_name, self.person_name = (
            base64.b64decode(self.token).decode("utf-8").split("<><>")
        )
        self.room_group_name = "chat_%s" % self.room_name

        if self.room_name not in rooms.keys():
            rooms.update(
                {
                    self.room_name: [
                        self.person_name,
                    ]
                }
            )
        else:
            rooms.get(self.room_name).append(self.person_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group

        if self.room_name in rooms.keys():
            rooms.get(self.room_name).remove(self.person_name)

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

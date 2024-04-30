from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.location = self.scope["url_route"]["kwargs"]["location"]
        self.room_group_name = f"{self.location}_group"

        # join the location group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def notification(self, event):
        """
        send the notification to the client side to tell that there is a earthquake now
        """
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

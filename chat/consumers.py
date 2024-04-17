from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, Message
import json
# store the connections => use redis maybe
user_connections = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called when the WebSocket connection is established
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        print("this is the text: ", message)


import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OutageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'outages'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (we won't use this for now)
    async def receive(self, text_data):
        pass

    # Receive message from room group
    async def outage_notification(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


from channels.generic.websocket import AsyncWebsocketConsumer
from json import loads, dumps

class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print(f'disconnected with code: {close_code}')

    async def receive(self, text_data):
        text_json_data = loads(text_data)

        message = text_json_data.get('message')
        sender = text_json_data.get('sender')

        data = dumps({
            'message': message,
            'sender': sender,
        })

        await self.send(data)


class DashboardUsersConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print(f'disconnected with code: {close_code}')

    async def receive(self, text_data):
        text_json_data = loads(text_data)

        message = text_json_data.get('message')
        sender = text_json_data.get('sender')

        data = dumps({
            'message': message,
            'sender': sender,
        })

        await self.send(data)


class DashboardUserConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_pk = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'user-{self.user_pk}'

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print(f'disconnected with code: {close_code}')

        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name,
        )

    async def receive(self, text_data):
        text_json_data = loads(text_data)
        message = text_json_data.get('message')
        sender = text_json_data.get('sender')

        data = {
            'type': 'dashboard_user',
            'message': message,
            'sender': sender,
        }

        await self.channel_layer.group_send(self.room_group_name, data)

    async def dashboard_user(self, event):
        data = dumps({
            'message': event.get('message'),
            'sender': event.get('sender'),
        })

        await self.send(text_data=data)
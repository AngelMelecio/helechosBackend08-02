from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PedidosConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pedido_id']
        self.room_group_name = f'pedido_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f'Se creo el grupo: {self.room_group_name}')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f'Se cerró la conexión para el grupo: {self.room_group_name}')

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # sender = text_data_json['sender']

        # print(message, sender)

        await self.send(text_data=json.dumps({
            'message':message,
            #'sender':sender
        }))
    
    async def pedido_message(self, event):
        message = event['text']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'consumerMessage': message
        })) 
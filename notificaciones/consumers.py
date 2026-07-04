from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("Cliente conectado")

        await self.accept()

        await self.send_json({
            "mensaje": "Hola desde Django Channels 🚀"
        })

    async def disconnect(self, close_code):
        print("Cliente desconectado")

    async def receive_json(self, content):
        print("Mensaje recibido:", content)

        await self.send_json({
            "echo": content
        })
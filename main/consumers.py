import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Driver, DriverLocationHistory

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.token = self.scope['url_route']['kwargs'].get('token')
        
        if self.token == 'admin':
            self.driver = None
            self.admin_group = "admins"
            await self.channel_layer.group_add(self.admin_group, self.channel_name)
            await self.accept()
            return

        self.driver = await self.get_driver(self.token)
        if self.driver:
            self.group_name = f"driver_{self.driver.id}"
            self.admin_group = "admins"

            # Join groups
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.channel_layer.group_add(self.admin_group, self.channel_name)

            await self.accept()

            # Update database and notify admins
            await self.set_driver_online_status(True)
            await self.channel_layer.group_send(
                self.admin_group,
                {
                    'type': 'connection_status',
                    'driver_id': self.driver.id,
                    'is_online': True
                }
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            await self.channel_layer.group_discard(self.admin_group, self.channel_name)

            # Update database and notify admins
            if self.driver:
                await self.set_driver_online_status(False)
                await self.channel_layer.group_send(
                    self.admin_group,
                    {
                        'type': 'connection_status',
                        'driver_id': self.driver.id,
                        'is_online': False
                    }
                )

    async def connection_status(self, event):
        await self.send(text_data=json.dumps(event))

    async def receive(self, text_data):
        if not self.driver:
            return

        data = json.loads(text_data)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude and longitude:
            # Update database
            await self.update_driver_location(latitude, longitude)

            # Notify admins
            await self.channel_layer.group_send(
                self.admin_group,
                {
                    'type': 'location_update',
                    'driver_id': self.driver.id,
                    'driver_name': self.driver.name,
                    'latitude': latitude,
                    'longitude': longitude
                }
            )

    async def location_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_driver(self, token):
        try:
            return Driver.objects.get(token=token)
        except Driver.DoesNotExist:
            return None

    @database_sync_to_async
    def set_driver_online_status(self, online):
        Driver.objects.filter(id=self.driver.id).update(is_online=online)

    @database_sync_to_async
    def update_driver_location(self, lat, lon):
        Driver.objects.filter(id=self.driver.id).update(latitude=lat, longitude=lon, is_online=True)
        DriverLocationHistory.objects.create(driver_id=self.driver.id, latitude=lat, longitude=lon)

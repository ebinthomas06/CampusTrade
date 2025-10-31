# In api/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
# --- DO NOT IMPORT MODELS HERE ---

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the "room name" from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_body = data['message']
        sender_username = data['sender']
        item_id = data['item']

        # Save the message to the database
        message = await self.save_message(sender_username, item_id, message_body)

        # Broadcast the message to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', 
                'message': message_body,
                'sender': sender_username,
                'created_at': message.created_at.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def save_message(self, sender_username, item_id, message_body):
        # --- IMPORTS MOVED HERE ---
        from django.contrib.auth.models import User
        from .models import Message, Item
        
        sender = User.objects.get(username=sender_username)
        item = Item.objects.get(id=item_id)
        receiver = item.seller

        if sender == receiver:
            # Logic to find the other person in the chat
            try:
                first_message = Message.objects.filter(item=item).order_by('created_at').first()
                if first_message and first_message.sender != sender:
                    receiver = first_message.sender
                else:
                    return # Can't determine receiver, don't save
            except Message.DoesNotExist:
                 return # No messages yet, and sender is seller, so don't save

        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            item=item,
            body=message_body
        )
        return message
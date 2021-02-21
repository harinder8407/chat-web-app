import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.auth import login


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
    
        # Join room 
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name 
            
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        
        # Sends an event to a group.
        # An event has a special 'type' key corresponding to the name of the method that should be invoked on consumers that receive the event.
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {   
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive event from room group 
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        # Send message to WebSocket of user who recieved the event
        self.send(text_data=json.dumps({
            'message': message,
            'username':username
        }))
    
    # if we are sending message to group it we will be echoed back to us
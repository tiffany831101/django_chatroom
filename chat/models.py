from django.db import models

class User(models.Model):
    class Meta:
        app_label = 'chat'
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    

class Chatroom(models.Model):
    class Meta:
      app_label = 'chat'

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')    
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chatroom between {self.sender.username} and {self.receiver.username}"
    
class Message(models.Model):
    class Meta:
      app_label = 'chat'

    chatroom = models.ForeignKey(Chatroom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chatroom}"
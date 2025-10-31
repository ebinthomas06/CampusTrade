from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2,help_text="Enter price in indian rupees")
    seller=models.ForeignKey(User, on_delete=models.CASCADE)
    trade_for=models.CharField(max_length=200, blank=True, null=True, help_text="What would you trade this for?")
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Message(models.Model):
    item=models.ForeignKey(Item,related_name="messages",on_delete=models.CASCADE)
    sender=models.ForeignKey(User,related_name="sent_messages",on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,related_name="received_messages",on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['sender', 'receiver', 'item']),
            models.Index(fields=['-created_at']),
        ]
    
    
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} re: {self.item.title}"
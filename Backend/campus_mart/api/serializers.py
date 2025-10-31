from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Item
from .models import Message

class UserSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),message="A user with this email already exists")]
    )
    class Meta:
        model=User
        fields=('id','username','password','email')
        extra_kwargs={'password':{'write_only' : True}}
        
    def validate_email(self,value):
        email=value.lower()
        if not email.endswith("@iiitkottayam.ac.in"):
            raise serializers.ValidationError("Onl college email id is allowed!")
        return email
        
    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
            
            
class ItemSerializer(serializers.ModelSerializer):
    seller=serializers.ReadOnlyField(source="seller.username")
    seller_id = serializers.ReadOnlyField(source='seller.id')
    class Meta :
        model=Item
        fields=['id','title','description','price','seller','seller_id','trade_for','created_at']
        
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')
    item_title= serializers.ReadOnlyField(source='item.title')
    
    class Meta:
        model=Message
        fields=['id','item','item_title','sender','receiver','body','created_at']
        read_only_fields=['item','sender','receiver']
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # This function runs when creating the token payload
        token = super().get_token(user)

        # Add custom claims MANUALLY
        token['username'] = user.username
        # You can add other fields here too if needed
        # token['email'] = user.email 

        return token
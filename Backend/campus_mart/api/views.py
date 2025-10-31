from django.shortcuts import render

from rest_framework.filters import SearchFilter, OrderingFilter

from django.contrib.auth.models import User
from rest_framework import generics,viewsets,permissions
from .serializers import UserSerializer,ItemSerializer,MessageSerializer
from django.db.models import Q

from django.shortcuts import get_object_or_404

from .permissions import IsOwnerOrReadOnly
from .models import Item,Message

from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer 

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 100 
    
    
class RegisterView(generics.CreateAPIView):
        queryset=User.objects.all()
        serializer_class=UserSerializer
        
class ItemViewSet(viewsets.ModelViewSet):
    queryset=Item.objects.all().order_by('-created_at')
    serializer_class=ItemSerializer
    pagination_class = StandardResultsSetPagination
    
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'trade_for'] # Fields to search
    ordering_fields = ['created_at', 'price']
    
    def get_permissions(self):
     
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else: 
            permission_classes = [IsOwnerOrReadOnly] 
        return [permission() for permission in permission_classes]
    
    def perform_create(self,serializer):
        serializer.save(seller=self.request.user)
        
   
class InboxView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-created_at')
    
class CreateMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError, APIException
        from django.contrib.auth.models import User 

        try:
            item_id = self.request.data.get('item_id')
            item = Item.objects.get(pk=item_id)
            sender = self.request.user
            seller = item.seller
            receiver = None

            if sender == seller:
                other_participant_id = Message.objects.filter(item=item).exclude(sender=seller).values_list('sender_id', flat=True).first()

                if other_participant_id:
                    try:
                        receiver = User.objects.get(pk=other_participant_id)
                    except User.DoesNotExist:
                        raise ValidationError('Original sender not found.')
                else:
                    raise ValidationError('Cannot determine recipient for seller message.')
            else:
                receiver = seller

            if receiver is None:
                 raise ValidationError('Could not determine the message recipient.')
            if sender == receiver: 
                 raise ValidationError('You cannot send a message to yourself.')

            serializer.save(sender=sender, receiver=receiver, item=item)

        except Item.DoesNotExist:
             raise ValidationError('Item not found.')
        except Exception as e:
             print(f"Unexpected error in perform_create: {type(e).__name__} - {e}")
             raise APIException("An error occurred while sending the message.")

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class ChatThreadView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        item_id = self.kwargs.get('item_id')
        other_user_username = self.kwargs.get('other_user_username')
        
        current_user = self.request.user
        
        # Find the other user object
        other_user = get_object_or_404(User, username=other_user_username)
        
        # Filter messages involving both users for the specific item
        queryset = Message.objects.filter(
            item_id=item_id
        ).filter(
            # Message is from current_user to other_user OR from other_user to current_user
            (Q(sender=current_user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=current_user))
        ).order_by('created_at') # Order oldest first for chat display
        
        return queryset

class MyItemsView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated] 
    pagination_class = None 

    def get_queryset(self):
        return Item.objects.filter(seller=self.request.user).order_by('-created_at')
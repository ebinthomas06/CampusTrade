from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView, ItemViewSet, InboxView, CreateMessageView,
    MyTokenObtainPairView, ChatThreadView ,MyItemsView
)


router=DefaultRouter()
router.register (r'items',ItemViewSet,basename='item')

urlpatterns=[
    path('register/',RegisterView.as_view(),name="register"),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    
    path("inbox/",InboxView.as_view(),name='inbox'),
    path('messages/create/', CreateMessageView.as_view(), name='create_message'),
    
    path('my-items/', MyItemsView.as_view(), name='my_items'),
    
    path('chat/<int:item_id>/<str:other_user_username>/', ChatThreadView.as_view(), name='chat_thread'),
    
    path("",include(router.urls)),
]
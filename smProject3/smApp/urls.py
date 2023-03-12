from django.urls import include, path
from . import views
from . import consumers
# from . import api

urlpatterns = [
    path('', views.index, name='index'),
    # path('api/image/', api.ImageDetail.as_view(),name="image_api"),
    # path('api/images/', api.ImageList.as_view(),name="image_api"),
    # path('chat/<str:room_name>', views.chat, name='room'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('sign-in', views.sign_in, name='sign_in'),
    path('log-out', views.log_out, name='log_out'),
    path('settings', views.settings, name='settings'),
    path('post', views.post, name='post'),
    path('upload', views.upload, name='upload'),
    path('like_post', views.like_post, name='like_post'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('followers', views.followers, name='followers'),
    path('search', views.search, name='search'),
    # chat
    path('chat', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('chat_with_a_friend', views.chat_with_a_friend, name='chat_with_a_friend'),
    path('chat/private_chat/<str:room_id>/', views.private_chat, name='private_chat'),
    # api
    path('api/profiles/', views.profileList.as_view()),
]
from django.contrib import admin
from django.urls import path
from tools import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('instagram-reel-download/', views.instagram_reel_download, name='instagram_reel_download'),
    path('instagram-hashtag-generator/', views.instagram_hashtag_generator, name='instagram_hashtag_generator'),
    path('instagram-story-download/', views.instagram_story_download, name='instagram_story_download'),
    path('instagram-to-mp3/', views.instagram_to_mp3, name='instagram_to_mp3'),
    path('instagram-photo-download/', views.instagram_photo_download, name='instagram_photo_download'),
    path('facebook-reel-download/', views.facebook_reel_download, name='facebook_reel_download'),
    path('youtube-reel-download/', views.youtube_reel_download, name='youtube_reel_download'),
    path('dailymotion-download/', views.dailymotion_download, name='dailymotion_download'),
    path('shutterstock-download/', views.shutterstock_download, name='shutterstock_download'),
    path('ai-image-generator/', views.ai_image_generator, name='ai_image_generator'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

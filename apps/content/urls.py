from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.content_home, name='home'),
    path('news/', views.news_list, name='news_list'),
    path('articles/', views.articles_list, name='articles_list'),
    path('memes/', views.memes_list, name='memes_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
]
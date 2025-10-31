from django.urls import path
from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.dictionary_home, name='home'),
    path('search/', views.word_search, name='search'),
    path('word/<int:word_id>/', views.word_detail, name='word_detail'),
    path('hsk/<int:level>/', views.words_by_hsk, name='words_by_hsk'),
]
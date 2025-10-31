from django.shortcuts import render, get_object_or_404
from .models import Article

def content_home(request):
    return render(request, 'content/home.html')

def news_list(request):
    news = Article.objects.filter(content_type='news') if Article.objects.exists() else []
    return render(request, 'content/news_list.html', {'news': news})

def articles_list(request):
    articles = Article.objects.filter(content_type='article') if Article.objects.exists() else []
    return render(request, 'content/articles_list.html', {'articles': articles})

def memes_list(request):
    memes = Article.objects.filter(content_type='meme') if Article.objects.exists() else []
    return render(request, 'content/memes_list.html', {'memes': memes})

def article_detail(request, article_id):
    return render(request, 'content/article_detail.html', {'article': None})
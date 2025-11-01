from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Article, Category, Comment


def home(request):
    """Главная страница контента - показывает последние материалы"""
    # Получаем последние статьи, мемы и новости
    latest_articles = Article.objects.filter(
        content_type='article',
        is_published=True
    ).order_by('-created_at')[:3]

    latest_memes = Article.objects.filter(
        content_type='meme',
        is_published=True
    ).order_by('-created_at')[:3]

    latest_news = Article.objects.filter(
        content_type='news',
        is_published=True
    ).order_by('-created_at')[:3]

    return render(request, 'content/home.html', {
        'latest_articles': latest_articles,
        'latest_memes': latest_memes,
        'latest_news': latest_news
    })



def articles_list(request):
    articles = Article.objects.filter(
        content_type='article',
        is_published=True
    ).order_by('-created_at')

    categories = Category.objects.all()

    return render(request, 'content/articles_list.html', {
        'articles': articles,
        'categories': categories
    })


def memes_list(request):
    memes = Article.objects.filter(
        content_type='meme',
        is_published=True
    ).order_by('-created_at')

    return render(request, 'content/memes_list.html', {
        'memes': memes
    })


def news_list(request):
    news = Article.objects.filter(
        content_type='news',
        is_published=True
    ).order_by('-created_at')

    return render(request, 'content/news_list.html', {
        'news': news
    })


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, is_published=True)

    # Увеличиваем счетчик просмотров
    article.views += 1
    article.save()

    # Получаем комментарии к статье
    comments = article.comments.filter(is_active=True).order_by('-created_at')

    return render(request, 'content/article_detail.html', {
        'article': article,
        'comments': comments
    })


@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.create(
                article=article,
                author=request.user,
                text=text,
                created_at=timezone.now()
            )

    return redirect('content:article_detail', article_id=article_id)
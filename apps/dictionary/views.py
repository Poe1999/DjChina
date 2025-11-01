from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Word


def dictionary_home(request):
    featured_words = Word.objects.all()[:8]

    # Статистика
    total_words = Word.objects.count()
    words_by_hsk = {
        'HSK 1': Word.objects.filter(hsk_level=1).count(),
        'HSK 2': Word.objects.filter(hsk_level=2).count(),
        'HSK 3': Word.objects.filter(hsk_level=3).count(),
        'HSK 4': Word.objects.filter(hsk_level=4).count(),
        'HSK 5': Word.objects.filter(hsk_level=5).count(),
        'HSK 6': Word.objects.filter(hsk_level=6).count(),
    }

    return render(request, 'dictionary/home.html', {
        'featured_words': featured_words,
        'total_words': total_words,
        'words_by_hsk': words_by_hsk,
    })


def word_search(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'ru-zh')

    results = []
    if query:
        if search_type == 'ru-zh':
            results = Word.objects.filter(
                Q(russian__icontains=query) |
                Q(russian__istartswith=query)
            )
        elif search_type == 'zh-ru':
            results = Word.objects.filter(
                Q(chinese_simplified__icontains=query) |
                Q(pinyin__icontains=query)
            )

    return render(request, 'dictionary/search_result.html', {
        'results': results,
        'query': query,
        'search_type': search_type,
        'results_count': len(results)
    })


def word_detail(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    examples = word.examples.all()

    similar_words = Word.objects.filter(
        part_of_speech=word.part_of_speech
    ).exclude(id=word.id)[:5]

    return render(request, 'dictionary/word_detail.html', {
        'word': word,
        'examples': examples,
        'similar_words': similar_words,
    })


def words_by_hsk(request, level):
    words = Word.objects.filter(hsk_level=level).order_by('russian')
    return render(request, 'dictionary/words_by_hsk.html', {
        'words': words,
        'hsk_level': level
    })
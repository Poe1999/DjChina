from django.db import models


class Word(models.Model):
    PART_OF_SPEECH_CHOICES = [
        ('noun', 'Существительное'),
        ('verb', 'Глагол'),
        ('adjective', 'Прилагательное'),
        ('adverb', 'Наречие'),
        ('pronoun', 'Местоимение'),
        ('numeral', 'Числительное'),
        ('preposition', 'Предлог'),
        ('conjunction', 'Союз'),
        ('interjection', 'Междометие'),
        ('measure word', ' Счетное слово')
    ]

    russian = models.CharField(max_length=200, verbose_name="Русское слово")
    chinese_simplified = models.CharField(max_length=100, verbose_name="Китайский (упрощенный)")
    pinyin = models.CharField(max_length=200, verbose_name="Пиньинь")
    part_of_speech = models.CharField(max_length=20, choices=PART_OF_SPEECH_CHOICES, default='noun')
    hsk_level = models.IntegerField(verbose_name="Уровень HSK", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"
        ordering = ['russian']
        indexes = [
            models.Index(fields=['russian']),
            models.Index(fields=['chinese_simplified']),
            models.Index(fields=['pinyin']),
        ]

    def __str__(self):
        return f"{self.russian} - {self.chinese_simplified}"


class WordExample(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='examples')
    example_ru = models.TextField(verbose_name="Пример на русском")
    example_zh = models.TextField(verbose_name="Пример на китайском")
    example_pinyin = models.TextField(verbose_name="Пиньинь примера")

    class Meta:
        verbose_name = "Пример использования"
        verbose_name_plural = "Примеры использования"

    def __str__(self):
        return f"Пример для {self.word.russian}"


class WordCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория слов"
        verbose_name_plural = "Категории слов"

    def __str__(self):
        return self.name
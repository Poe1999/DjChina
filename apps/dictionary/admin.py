from django.contrib import admin
from .models import Word, WordExample, WordCategory

class WordExampleInline(admin.TabularInline):
    model = WordExample
    extra = 1
    fields = ['example_ru', 'example_zh', 'example_pinyin']

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['russian', 'chinese_simplified', 'pinyin', 'part_of_speech', 'hsk_level']
    list_filter = ['part_of_speech', 'hsk_level']
    search_fields = ['russian', 'chinese_simplified', 'pinyin']
    inlines = [WordExampleInline]
    ordering = ['russian']

@admin.register(WordExample)
class WordExampleAdmin(admin.ModelAdmin):
    list_display = ['word', 'example_ru']
    search_fields = ['example_ru', 'example_zh']
    list_filter = ['word__part_of_speech']

@admin.register(WordCategory)
class WordCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
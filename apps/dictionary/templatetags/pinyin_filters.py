# apps/dictionary/templatetags/pinyin_tags.py
from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

# Цвета для тонов
TONE_COLORS = {
    1: '#FFA500',  # желтый - первый тон
    2: '#008000',  # зеленый - второй тон
    3: '#4169E1',  # синий - третий тон
    4: '#8B0000',  # красный - четвертый тон
    0: '#A9A9A9',  # Серый - нейтральный тон
}


def split_pinyin_syllables(pinyin_text):
    """
    Правильно разделяет пиньинь на слоги, даже если они написаны слитно
    """
    if not pinyin_text:
        return []

    # Приводим к нижнему регистру
    pinyin_text = pinyin_text.lower().strip()

    # Паттерн для поиска слогов пиньиня
    pattern = r'([bcdfghjklmnpqrstwxyz]*[aeiouüāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+[ng]*)'

    syllables = re.findall(pattern, pinyin_text)

    # Фильтруем пустые строки
    syllables = [syl for syl in syllables if syl]

    return syllables


def detect_tone(syllable):
    """
    Определяет тон слога пиньиня
    """
    tone_mapping = {
        'ā': 1, 'á': 2, 'ǎ': 3, 'à': 4,
        'ē': 1, 'é': 2, 'ě': 3, 'è': 4,
        'ī': 1, 'í': 2, 'ǐ': 3, 'ì': 4,
        'ō': 1, 'ó': 2, 'ǒ': 3, 'ò': 4,
        'ū': 1, 'ú': 2, 'ǔ': 3, 'ù': 4,
        'ǖ': 1, 'ǘ': 2, 'ǚ': 3, 'ǜ': 4
    }

    for char in syllable:
        if char in tone_mapping:
            return tone_mapping[char]

    return 0  # нейтральный тон


def get_base_syllable(syllable):
    """
    Возвращает базовую форму слога без тоновых знаков
    """
    tone_replacements = [
        ('āáǎà', 'a'), ('ēéěè', 'e'), ('īíǐì', 'i'),
        ('ōóǒò', 'o'), ('ūúǔù', 'u'), ('ǖǘǚǜ', 'ü')
    ]

    base_syllable = syllable
    for marks, replacement in tone_replacements:
        for mark in marks:
            base_syllable = base_syllable.replace(mark, replacement)

    return base_syllable


@register.filter
def colorize_pinyin(pinyin_text):
    """
    Фильтр для раскрашивания пиньиня по тонам
    """
    if not pinyin_text:
        return ""

    # Разделяем на слоги
    syllables_list = split_pinyin_syllables(pinyin_text)

    if not syllables_list:
        return mark_safe(f'<span style="color: #95a5a6;">{pinyin_text}</span>')

    html_parts = []

    for syllable in syllables_list:
        tone = detect_tone(syllable)
        color = TONE_COLORS.get(tone, TONE_COLORS[0])

        html_parts.append(
            f'<span class="pinyin-syllable" style="color: {color}; margin: 0 3px; display: inline-block; text-align: center; vertical-align: top;">'
            f'<span class="pinyin-text" style="font-size: 1.1em; display: block;">{syllable}</span>'
            f'<span class="tone-indicator" style="font-size: 0.8em; font-weight: bold; display: block;">{tone if tone > 0 else "⁰"}</span>'
            f'</span>'
        )

    return mark_safe(''.join(html_parts))


@register.filter
def colorize_characters(chinese_text, pinyin_text):
    """
    Фильтр для раскрашивания иероглифов по тонам пиньиня
    """
    if not chinese_text or not pinyin_text:
        return mark_safe(f'<span style="font-size: 1.5em; font-weight: bold;">{chinese_text or ""}</span>')

    # Разделяем пиньинь на слоги
    pinyin_syllables = split_pinyin_syllables(pinyin_text)
    characters = list(chinese_text.strip())

    # Если количество иероглифов совпадает с количеством слогов
    if len(characters) == len(pinyin_syllables):
        html_parts = []
        for char, pinyin_syllable in zip(characters, pinyin_syllables):
            tone = detect_tone(pinyin_syllable)
            color = TONE_COLORS.get(tone, TONE_COLORS[0])

            html_parts.append(
                f'<span class="chinese-char" style="color: {color}; font-size: 1.5em; font-weight: bold; margin: 0 5px; display: inline-block;">{char}</span>'
            )
        return mark_safe(''.join(html_parts))
    else:
        # Если не совпадает, пытаемся сопоставить посимвольно для коротких слов
        if len(characters) <= 4 and pinyin_syllables:
            html_parts = []
            # Распределяем цвета между иероглифами
            for i, char in enumerate(characters):
                tone_index = i % len(pinyin_syllables)
                tone = detect_tone(pinyin_syllables[tone_index])
                color = TONE_COLORS.get(tone, TONE_COLORS[0])

                html_parts.append(
                    f'<span class="chinese-char" style="color: {color}; font-size: 1.5em; font-weight: bold; margin: 0 5px; display: inline-block;">{char}</span>'
                )
            return mark_safe(''.join(html_parts))
        else:
            # Если не совпадает, показываем исходный текст
            return mark_safe(f'<span style="font-size: 1.5em; font-weight: bold;">{chinese_text}</span>')


@register.filter
def pinyin_with_tones(pinyin_text):
    """
    Фильтр для отображения пиньиня с цифрами тонов
    Пример: "xiǎomāo" -> "xiao3 mao1"
    """
    if not pinyin_text:
        return ""

    syllables_list = split_pinyin_syllables(pinyin_text)
    result_syllables = []

    for syllable in syllables_list:
        tone = detect_tone(syllable)
        base_syllable = get_base_syllable(syllable)
        if tone > 0:
            result_syllables.append(f"{base_syllable}{tone}")
        else:
            result_syllables.append(base_syllable)

    return ' '.join(result_syllables)


@register.simple_tag
def display_word_with_pinyin(chinese_text, pinyin_text):
    """
    Комбинированный тег для отображения иероглифов и пиньиня вместе
    """
    colored_chars = colorize_characters(chinese_text, pinyin_text)
    colored_pinyin = colorize_pinyin(pinyin_text)

    return mark_safe(f'''
    <div style="text-align: center; margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <div style="margin-bottom: 10px;">{colored_chars}</div>
        <div>{colored_pinyin}</div>
    </div>
    ''')
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_remove_word_frequency_alter_word_part_of_speech'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE dictionary_word_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                russian VARCHAR(200) NOT NULL,
                chinese_simplified VARCHAR(100) NOT NULL,
                pinyin VARCHAR(200) NOT NULL,
                part_of_speech VARCHAR(20) NOT NULL,
                hsk_level INTEGER NOT NULL DEFAULT 1,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            );
            """,
            reverse_sql="""
            CREATE TABLE dictionary_word_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                russian VARCHAR(200) NOT NULL,
                chinese_simplified VARCHAR(100) NOT NULL,
                chinese_traditional VARCHAR(100) NOT NULL,
                pinyin VARCHAR(200) NOT NULL,
                part_of_speech VARCHAR(20) NOT NULL,
                hsk_level INTEGER NOT NULL DEFAULT 1,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL
            );
            """
        ),
        migrations.RunSQL(
            """
            INSERT INTO dictionary_word_new (id, russian, chinese_simplified, pinyin, part_of_speech, hsk_level, created_at, updated_at)
            SELECT id, russian, chinese_simplified, pinyin, part_of_speech, hsk_level, created_at, updated_at
            FROM dictionary_word;
            """,
            reverse_sql="""
            INSERT INTO dictionary_word_new (id, russian, chinese_simplified, chinese_traditional, pinyin, part_of_speech, hsk_level, created_at, updated_at)
            SELECT id, russian, chinese_simplified, chinese_simplified, pinyin, part_of_speech, hsk_level, created_at, updated_at
            FROM dictionary_word;
            """
        ),
        migrations.RunSQL(
            """
            DROP TABLE dictionary_word;
            """,
            reverse_sql="""
            DROP TABLE dictionary_word_new;
            """
        ),
        migrations.RunSQL(
            """
            ALTER TABLE dictionary_word_new RENAME TO dictionary_word;
            """,
            reverse_sql="""
            ALTER TABLE dictionary_word RENAME TO dictionary_word_old;
            """
        )
    ]
import json
from arabic_reshaper import ArabicReshaper # Used to make Arabic text display properly
from bidi.algorithm import get_display # Used to make Arabic text display properly

configuration = {
    'delete_harakat': False,
    'shift_harakat_position': True
    
}

reshaper = ArabicReshaper(configuration=configuration)

# Text source:
# https://github.com/amrayn/quran-text/blob/main/quran-min-tashkeel.json
with open("quran-min-tashkeel.json", "r", encoding="utf-8") as file:
        book = json.load(file)

def get_chapter_by_id(book, chapter_id):
    for chapter in book:
        if chapter['id'] == chapter_id:
            return chapter

    return None

def get_verse_count(book, chapter_id):
    chapter = get_chapter_by_id(book, chapter_id)

    if chapter is None:
        return None

    return chapter['total_verses']

def get_verse(chapter_id, verse_id):
    chapter = get_chapter_by_id(book, chapter_id)
    
    for verse in chapter['verses']:
            if verse['id'] == verse_id:
                return verse
    
    return None

def get_verse_text(chapter_id, verse_id):
    verse = get_verse(chapter_id, verse_id)
    reshaped_verse = reshaper.reshape(verse['text'])

    return get_display(reshaped_verse)
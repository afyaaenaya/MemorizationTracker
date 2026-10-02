import json
from pathlib import Path
from arabic_reshaper import ArabicReshaper # Used to make Arabic text display properly
from bidi.algorithm import get_display # Used to make Arabic text display properly

## Loading and querying JSON file

configuration = {
    'delete_harakat': False,
    'shift_harakat_position': True
    
}

reshaper = ArabicReshaper(configuration=configuration)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Text source:
# https://github.com/amrayn/quran-text/blob/main/quran-min-tashkeel.json
with open(DATA_DIR / "quran-min-tashkeel.json", "r", encoding="utf-8") as file:
        book = json.load(file)


def get_chapters():
    return [f"{chapter['id']}: {get_display(reshaper.reshape(chapter['name']))}" for chapter in book] 


def get_chapter_by_id(chapter_id):
    for chapter in book:
        if chapter['id'] == chapter_id:
            return chapter

    return None



def get_verse_count(chapter_id):
    chapter = get_chapter_by_id(chapter_id)

    if chapter is None:
        return None

    return chapter['total_verses']



def get_verse(chapter_id, verse_id):
    chapter = get_chapter_by_id(chapter_id)

    if chapter is None:
            return None
    
    for verse in chapter['verses']:
            if verse['id'] == verse_id:
                return verse
    
    return None



def get_next_5_verses(chapter_id, verse_id):
    text = []

    current_chapter_id = chapter_id
    current_verse_id = verse_id + 1

    while len(text) < 5:
        chapter = get_chapter_by_id(current_chapter_id)

        if chapter is None:
            break
        
        verses = chapter['verses']
        
        for verse in verses:
            if verse['id'] >= current_verse_id:
                text.append(verse)
                
                if len(text) == 5:
                    return text
                
        current_chapter_id += 1
        current_verse_id = 1
    
    return text



def get_verse_text(chapter_id, verse_id):
    verse = get_verse(chapter_id, verse_id)

    if verse is None:
        return None

    reshaped_verse = reshaper.reshape(verse['text'])

    return get_display(reshaped_verse)



def get_next_5_verses_text(chapter_id, verse_id):
    verses = get_next_5_verses(chapter_id, verse_id)
    if not verses:
        return []

    results = []
    
    for verse in verses:
        reshaped_verse = reshaper.reshape(verse['text'])
        results.append(get_display(reshaped_verse))
    
    
    return results
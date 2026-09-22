import random
from book import get_verse_count, get_verse_text, get_verse
from tracker import load_progress, save_progress

def start_quiz():
    
    mode = input("Select mode: 1 - random   2 - weakest: ")

    while mode not in ("1", "2"):
        mode = input("Select mode: 1 - random   2 - weakest: ")
    
    if mode == 1:
        
        start_chapter = int(input("Start chapter: "))
        end_chapter = int(input("End chapter: "))
        
        quiz_random_verse(start_chapter, end_chapter)
        
    elif mode == 2:
        
        qrange = input('Select range: 1 - all saved cards   2 - chapter range: ')
        
        while qrange not in ("1", "2"):
            qrange = input('Select range: 1 - all saved cards   2 - chapter range: ')
        
        if qrange == '1':
            quiz_weakest_verse()
            
        elif qrange == '2':
            start_chapter = int(input("Start chapter: "))
            end_chapter = int(input("End chapter: "))

            quiz_weakest_verse(start_chapter, end_chapter)
   


def quiz_random_verse(start_chapter, end_chapter):
    chapter_id = random.randint(start_chapter, end_chapter)

    verse_count = get_verse_count(chapter_id)
    verse_id = random.randint(1, verse_count)

    print(get_verse_text(chapter_id, verse_id))


    
def quiz_weakest_verse(start_chapter = None, end_chapter = None):
    cards = load_progress()
    
    if start_chapter is None and end_chapter is None:
            eligible_cards = cards
            
    else:
        eligible_cards = [card for card in cards if start_chapter <= card['chapter_id'] <= end_chapter]
        
    weakest = min(eligible_cards, key = lambda card: card["score"])

    chapter_id = weakest["chapter_id"]
    verse_id = weakest["verse_id"]

    print(get_verse_text(chapter_id, verse_id))
            



def record_answer(chapter_id, verse_id, correct: bool):
    cards = load_progress()

    for card in cards:
        if (card["chapter_id"] == chapter_id and card["verse_id"] == verse_id):
            if correct:
                card["score"] += 1
            else:
                card["score"] -= 1

            save_progress(cards)
            return
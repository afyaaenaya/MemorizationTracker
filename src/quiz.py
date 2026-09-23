import random
from book import get_verse_count, get_verse_text, get_next_5_verses_text
from tracker import get_weak_verses, update_score



def start_quiz():
    mode, start, end = mode_selector()

    if mode == 1:
        quiz_random_verse(start, end)
    elif mode == 2:
        quiz_weakest_verse(start, end)
    else:
        print("Quiz could not be started.")
    

            


def mode_selector():
    mode = input("Select mode: 1 - random   2 - weakest: ")

    while mode not in ("1", "2"):
        mode = input("Select mode: 1 - random   2 - weakest: ")
    
    if mode == '1':
        start_chapter, end_chapter = chapter_selector()
        
        return 1, start_chapter, end_chapter
        
    elif mode == '2':
        
        qrange = input('Select range: 1 - all saved cards   2 - chapter range: ')
        
        while qrange not in ("1", "2"):
            qrange = input('Select range: 1 - all saved cards   2 - chapter range: ')
        
        if qrange == '1':
            return 2, None, None
            
        elif qrange == '2':
            start_chapter, end_chapter = chapter_selector()

            return 2, start_chapter, end_chapter
        
    return None



def chapter_selector():
    while True:
        try:
            start_chapter = int(input("Start chapter: "))
            end_chapter = int(input("End chapter: "))
        except ValueError:
            print("Please enter whole numbers.")
            continue

        if 1 <= start_chapter <= end_chapter <= 114:
            return start_chapter, end_chapter

        print("Enter chapters from 1 to 114, with start <= end.")
   


def quiz_random_verse(start_chapter, end_chapter):
    chapter_id = random.randint(start_chapter, end_chapter)

    verse_count = get_verse_count(chapter_id)
    verse_id = random.randint(1, verse_count)

    quiz_card(chapter_id, verse_id)


    
def quiz_weakest_verse(start_chapter = None, end_chapter = None):
    cards = get_weak_verses()
    
    if start_chapter is None and end_chapter is None:
            eligible_cards = cards
            
    else:
        eligible_cards = [card for card in cards if start_chapter <= card['chapter_id'] <= end_chapter]
    
    if eligible_cards:
        weakest = eligible_cards[0]
    else:
        print('No verses found')
        return

    chapter_id = weakest["chapter_id"]
    verse_id = weakest["verse_id"]

    quiz_card(chapter_id, verse_id)


def quiz_card(chapter_id, verse_id):
    print(get_verse_text(chapter_id, verse_id))
    
    next_verses = get_next_5_verses_text(chapter_id, verse_id)
    if not next_verses:
        print('End of text.')
    
    input("Press Enter to reveal next verses.")

    for verse in next_verses:
        print(verse)
        
    answer = input("Did you recite them correctly? (y/n): ").strip().lower()
    while answer not in ("y", "n"):
        answer = input("Please enter y or n: ").strip().lower()
    
    update_score(chapter_id, verse_id, correct=(answer == "y"))
    print("Progress saved.")
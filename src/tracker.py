import json
from datetime import datetime


def calculate_score(card):
    if card["attempts"] == 0:
        return 0.0
    return 100 * card["correct_count"] / card["attempts"]

def get_score(chapter_id, verse_id):
    for card in load_progress():
        if card["chapter_id"] == chapter_id and card["verse_id"] == verse_id:
            return calculate_score(card)
        
    return None
    
def update_score(chapter_id, verse_id, correct: bool):
    cards = load_progress()
    
    tested_card = None

    for card in cards:
        if (card["chapter_id"] == chapter_id and card["verse_id"] == verse_id):
            tested_card = card
            
    if tested_card is None:
        tested_card = {
            'chapter_id': chapter_id,
            'verse_id': verse_id,
            'correct_count': 0,
            'attempts': 0,
            'last_reviewed': datetime.min.isoformat()
        }
        cards.append(tested_card)
        
    tested_card.setdefault('attempts', 0)
    tested_card.setdefault('correct_count', 0)

    tested_card['attempts'] += 1
    tested_card['correct_count'] += int(correct)
    tested_card['last_reviewed'] = datetime.now().isoformat()
        
    save_progress(cards)
    



def get_low_scores():
    return sorted(load_progress(), key=lambda card: card["score"])

def load_progress():
    with open('data/score.json', 'r') as file:
            scores = json.load(file)
    return scores

def save_progress(scores):
    with open("data/score.json", "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)

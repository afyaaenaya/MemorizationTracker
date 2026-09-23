import json

def get_score(chapter_id, verse_id):
    for card in load_progress():
        if card["chapter_id"] == chapter_id and card["verse_id"] == verse_id:
            return card["score"]
    return 0
    
def update_score(chapter_id, verse_id, correct: bool):
    scores = load_progress()

    for score in scores:
        if (score["chapter_id"] == chapter_id and score["verse_id"] == verse_id):
            if correct:
                score["score"] += 1
            else:
                score["score"] -= 1

            save_progress(scores)
            return
        
    new_score = {
        "chapter_id": chapter_id,
        "verse_id": verse_id,
        "score": 1 if correct else -1
    }

    scores.append(new_score)
    save_progress(scores)
    



def get_weak_verses():
    return sorted(load_progress(), key=lambda card: card["score"])

def load_progress():
    with open('data/score.json', 'r') as file:
            scores = json.load(file)
    return scores

def save_progress(scores):
    with open("data/score.json", "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)
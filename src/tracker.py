import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SCORE_HALF_LIFE_DAYS = 30


class ProgressFileError(ValueError):
    """Progress cannot be loaded safely."""


def calculate_score(card):
    attempts = card.get("attempts", 0)
    if attempts == 0 or not card.get("last_reviewed"):
        return 0.0

    last_reviewed = datetime.fromisoformat(card["last_reviewed"])
    now = datetime.now(last_reviewed.tzinfo)
    days_since_review = max(0.0, (now - last_reviewed).total_seconds() / 86400)
    time_factor = 0.5 ** (days_since_review / SCORE_HALF_LIFE_DAYS)
    accuracy = 100 * card.get("correct_count", 0) / attempts
    return accuracy * time_factor



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
    return sorted(load_progress(), key=calculate_score)

def load_progress():
    progress_path = DATA_DIR / "score.json"
    try:
        with open(progress_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ProgressFileError(
            f"Cannot read progress from {progress_path}: invalid JSON or encoding. "
            "The file has been left unchanged. Repair it before trying again."
        ) from error

def save_progress(scores):
    temporary_path = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=DATA_DIR,
            prefix="score-", suffix=".tmp", delete=False
        ) as file:
            temporary_path = Path(file.name)
            json.dump(scores, file, indent=4)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, DATA_DIR / "score.json")
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

# MemorizationTracker

A command-line Quran memorization practice tool. It shows a starting verse, lets you recite the next five verses from memory, and records your self-assessed result. Arabic text is reshaped and reordered for terminal display.

## Setup

Use Python 3.8 or later and a terminal with an Arabic-capable font. From the project directory, run these commands in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install arabic-reshaper==3.0.1 python-bidi==0.6.11
.\.venv\Scripts\python.exe src/main.py
```

The dependency versions above match the project's existing development environment. There is currently no `requirements.txt`.

On macOS or Linux, use `.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.

## Practicing

1. Select a mode:
   - **Random:** Select an inclusive chapter range, then practice random starting verses within it.
   - **Weakest:** Practice the saved card with the lowest current score, across all saved cards or within a chapter range. 
   Start with random mode if you have no saved cards.
2. Read the starting verse and try to recite the next five verses from memory.
3. Press Enter to reveal the verses.
4. Enter `y` for a correct recitation, `n` for an incorrect one, or `0` to cancel the current question without recording a result.

Both modes continue asking questions. Cancelling a question moves on to the next question; press **Ctrl+C** to stop the session (The current program will display a `KeyboardInterrupt` traceback when stopped this way).

Chapter ranges restrict the **starting verse** for now. The next five verses can cross into another chapter, including one outside the selected range. Near the end of the Quran, fewer than five verses may be available. If none remain, the question is skipped without saving a result.

## Scoring

Each card is identified by its starting chapter and verse. Its result represents the recitation of the following verses, rather than a separate score for each verse recited.

```text
accuracy = 100 × correct_count / attempts
score = accuracy × 0.5 ** (days_since_last_review / 30)
```

For example, a card with 80% accuracy has a score of approximately 80 immediately after practice, 40 after 30 days, and 20 after 60 days without further practice. Cards with no attempts or no review timestamp score zero.

Change `SCORE_HALF_LIFE_DAYS` in `src/tracker.py` to adjust how quickly scores decrease. Weakest mode recalculates scores before each question and selects the lowest one; it can select the same card again.

## Saved progress

Progress is stored locally in `data/score.json`:

```json
[
    {
        "chapter_id": 39,
        "verse_id": 54,
        "correct_count": 1,
        "attempts": 1,
        "last_reviewed": "2026-10-01T12:00:00"
    }
]
```

The file contains practice history; scores are calculated when needed. A missing progress file is treated as empty history and created on the next saved result. Invalid JSON or encoding produces an error and stops the session without overwriting the file. Saves write to a temporary file in the data directory before replacing the original.

Valid JSON with incorrectly structured cards is not currently validated and can still cause errors.

## Project layout

```text
MemorizationTracker/
├── src/
│   ├── main.py                 # Application entry point and progress-error reporting
│   ├── quiz.py                 # Menus, question loops, and answer handling
│   ├── book.py                 # Quran lookups and Arabic text formatting
│   └── tracker.py              # Practice history, scoring, and file storage
└── data/
    ├── quran-min-tashkeel.json  # Quran text dataset
    └── score.json              # Saved practice history
```

Data paths are resolved relative to the source files, so they do not depend on the terminal's working directory.

## Next steps

- Validate saved cards, including chapter and verse IDs, counters, timestamps, and duplicate entries.
- Move cards from JSON file to SQL database.
- Fix issue with multiline Arabic text where line order is inverted.
- Add a proper session exit option that is not **Ctrl + C**.
- Handle file-access and save failures with clear messages.
- Exclude questions that go out of the selected chapter range.
- Add a `requirements.txt` to make dependency installation easier.
- Show practice statistics, such as accuracy, attempts, and time since the last review.
- (Potentially) adding a graphical user interface.

## Text source

The Quran dataset is sourced from [amrayn/quran-text](https://github.com/amrayn/quran-text/blob/main/quran-min-tashkeel.json).
from typing import List, Dict


def normalize_emotion_data(raw_logs: List[Dict]) -> Dict[str, int]:
    """
    Converts raw mood logs into a frequency map.
    Each log is expected to have an 'emotion' field (case-insensitive).
    Missing or blank emotions default to 'neutral'.
    """
    emotion_count = {}
    for log in raw_logs:
        emotion = str(log.get("emotion", "neutral")).strip().lower() or "neutral"
        emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
    return emotion_count


def extract_journal_keywords(entries: List[str], debug: bool = False) -> List[str]:
    """
    Extracts emotion-related labels from journal entries.
    - Uses static trigger → label map for now (NLP-ready structure).
    - Optional debug mode for investor demo tracing.
    """
    KEYWORDS_MAP = {
        "stress": "stress",
        "grateful": "gratitude",
        "anxious": "anxiety",
        "happy": "happiness",
        "tired": "fatigue",
        "lonely": "loneliness",
        "angry": "anger",
    }

    found_labels = set()

    for entry in entries:
        entry_lower = str(entry).lower()
        for trigger, label in KEYWORDS_MAP.items():
            if trigger in entry_lower:
                found_labels.add(label)

    if debug:
        print(f"[DEBUG] Extracted journal emotion labels: {list(found_labels)}")

    return list(found_labels)


# Placeholder for future GPT/NLP journal analysis
def analyze_journals_nlp(entries: List[str]) -> Dict:
    """
    Future extension: run GPT or spaCy to extract sentiment, themes, emotion vectors, etc.
    Currently returns a static placeholder.
    """
    return {
        "themes": [],
        "sentiment_score": 0.0,
        "insights": "NLP analysis not yet implemented."
    }
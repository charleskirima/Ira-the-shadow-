import pytest
from src.engines.emotional_engine import process_mood
from src.engines.physical_engine import recommend_hydration

def test_process_mood_sad():
    """Should suggest journaling or emotional processing when mood is sad."""
    response = process_mood("sad")
    assert isinstance(response, str), "Expected response to be a string"
    assert any(word in response.lower() for word in ["journal", "write"]), \
        f"Expected journaling-related advice, got: {response}"

def test_process_mood_happy():
    """Should reflect positive or gratitude-related advice when mood is happy."""
    response = process_mood("happy")
    assert isinstance(response, str), "Expected response to be a string"
    assert any(word in response.lower() for word in ["gratitude", "reflect", "journal"]), \
        f"Expected gratitude or reflection advice, got: {response}"

def test_recommend_hydration_low():
    """Should prompt hydration when intake is low."""
    recommendation = recommend_hydration(0.5)
    assert isinstance(recommendation, str), "Expected recommendation to be a string"
    assert "drink" in recommendation.lower(), \
        f"Expected prompt to hydrate, got: {recommendation}"

def test_recommend_hydration_high():
    """Should affirm hydration when intake is sufficient."""
    recommendation = recommend_hydration(2.5)
    assert isinstance(recommendation, str), "Expected recommendation to be a string"
    assert any(word in recommendation.lower() for word in ["hydrated", "good", "nice"]), \
        f"Expected hydration affirmation, got: {recommendation}"
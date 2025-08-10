from typing import List, Dict, Union

def format_summary_card(title: str, content_lines: List[str]) -> Dict[str, str]:
    """
    Formats a report card dictionary with a title and multiline content.

    Args:
        title: The card title.
        content_lines: A list of content strings.

    Returns:
        A dictionary with 'title' and newline-joined 'content'.
    """
    return {
        "title": title,
        "content": "\n".join(content_lines)
    }

def score_daily_alignment(sleep: float, water: float, goals_done: Union[List[Dict], int]) -> int:
    """
    Computes a daily alignment score out of 100 based on:
        - ≥ 7 hours of sleep
        - ≥ 2.0 liters of water
        - ≥ 1 goal completed

    Args:
        sleep: Hours of sleep.
        water: Water intake in liters.
        goals_done: List of completed goal dicts or a count.

    Returns:
        Integer score between 0 and 100.
    """
    score = 0

    if isinstance(sleep, (int, float)) and sleep >= 7:
        score += 1
    if isinstance(water, (int, float)) and water >= 2.0:
        score += 1
    if (isinstance(goals_done, list) and len(goals_done) > 0) or \
       (isinstance(goals_done, int) and goals_done > 0):
        score += 1

    return round((score / 3) * 100)
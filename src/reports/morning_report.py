from typing import List, Dict, Any
from datetime import datetime, timedelta
from src.utils.text_utils import summarize_list
from src.business_logic.report_utils import format_summary_card

def generate_morning_report(logs_today: Dict[str, Any], logs_past_week: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Builds the morning report with today’s logs and a weekly reflection memory.

    Args:
        logs_today: Dict with today's mood, sleep, water, etc.
        logs_past_week: List of logs for last 7 days.

    Returns:
        Dict with message, actions, memory_summary, and GPT_context.
    """
    # === DAILY REPORT ===
    mood = logs_today.get("mood", "neutral").capitalize()
    sleep = logs_today.get("sleep", 0)
    water = logs_today.get("water", 0.0)
    goals = logs_today.get("goals_completed", [])

    message = (
        f"🌅 Morning Check-in:\n"
        f"• Mood: {mood}\n"
        f"• Sleep: {sleep} hrs\n"
        f"• Water: {water}L\n"
        f"• Goals Completed: {len(goals)}"
    )

    # === ACTION SUGGESTIONS ===
    actions = []
    if sleep < 6:
        actions.append("😴 You slept less than usual. Try to rest early today.")
    if water < 1.5:
        actions.append("💧 Start hydrating early.")
    if len(goals) == 0:
        actions.append("🎯 Pick one small goal to focus on this morning.")

    # === WEEKLY MEMORY SUMMARY ===
    mood_trend = summarize_list([log.get("mood", "neutral") for log in logs_past_week])
    avg_sleep = round(sum([log.get("sleep", 0) for log in logs_past_week]) / 7, 1)
    total_journals = sum(1 for log in logs_past_week if log.get("journaled", False))
    water_trend = summarize_list([log.get("water", 0) for log in logs_past_week], mode="numeric")

    memory_summary = (
        f"🧠 Weekly Reflection:\n"
        f"• Avg Sleep: {avg_sleep} hrs\n"
        f"• Water trend: {water_trend}\n"
        f"• Mood trend: {mood_trend}\n"
        f"• Journaling: {total_journals} times"
    )

    # === GPT CONTEXT ===
    gpt_context = {
        "sleep": sleep,
        "water": water,
        "mood": mood.lower(),
        "weekly_sleep_avg": avg_sleep,
        "weekly_water_trend": water_trend,
        "weekly_mood_trend": mood_trend,
        "journals_this_week": total_journals
    }

    return {
        "title": "Morning Report",
        "message": message,
        "actions": actions,
        "memory_summary": memory_summary,
        "gpt_context": gpt_context
    }
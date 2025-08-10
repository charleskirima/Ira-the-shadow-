from typing import Dict, Any, List, Optional

def map_log_entry_to_gpt_format(log: Dict[str, Any]) -> str:
    """
    Converts a raw log entry into a concise GPT-readable summary.
    """
    log_type = log.get("type")
    data = log.get("data", {})
    timestamp = log.get("created_at", "")

    if log_type == "spiritual":
        action = data.get("activity", "Unknown")
        mood = data.get("mood", "")
        return f"[{timestamp}] Spiritual: Did '{action}' — Mood: {mood}"

    elif log_type == "emotional":
        feeling = data.get("feeling", "Unknown")
        trigger = data.get("trigger", "")
        return f"[{timestamp}] Emotional: Felt '{feeling}' — Trigger: {trigger}"

    elif log_type == "physical":
        action = data.get("activity", "Unknown")
        water = data.get("water", "")
        sleep = data.get("sleep", "")
        return f"[{timestamp}] Physical: {action} — Water: {water}L — Sleep: {sleep}h"

    elif log_type == "mental":
        note = data.get("note", "")
        return f"[{timestamp}] Mental: Journaled '{note[:50]}...'" if note else f"[{timestamp}] Mental: Journaled."

    elif log_type == "work":
        summary = data.get("summary", "")
        tasks = data.get("tasks_completed", [])
        task_text = ", ".join(tasks) if tasks else "No tasks listed"
        return f"[{timestamp}] Work: {summary} — Tasks: {task_text}"

    elif log_type == "financial":
        budget = data.get("budget_used", "")
        gain = data.get("income", "")
        return f"[{timestamp}] Financial: Budgeted {budget} — Income {gain}"

    else:
        return f"[{timestamp}] Unknown log type: {log_type}"
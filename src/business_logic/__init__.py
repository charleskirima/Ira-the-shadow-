# src/business_logic/__init__.py

"""
Initializer for the shared business logic module.
Exposes core logic components for scheduling, recommendations, chat, and data processing.
"""

from .calculations import calculate_summary_stats
from .planner import DailyPlanner
from .recommender import EventRecommender
from .chat_context import ChatContextManager
from .data_processor import DataProcessor
from .chat_engine import ChatEngine

__all__ = [
    "calculate_summary_stats",
    "DailyPlanner",
    "EventRecommender",
    "ChatContextManager",
    "DataProcessor",
    "ChatEngine",
]
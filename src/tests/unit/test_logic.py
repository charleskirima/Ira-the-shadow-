from src.business_logic.planner import generate_daily_plan

def test_daily_plan_with_goals():
    goals = [{"title": "Read", "duration": 30}]
    plan = generate_daily_plan(goals, sleep_hours=7, mood="neutral")
    
    assert isinstance(plan, list)
    assert any("Read" in step for step in plan)

def test_plan_adds_nap_if_low_sleep():
    goals = []
    plan = generate_daily_plan(goals, sleep_hours=4, mood="neutral")
    assert "Take a 15-minute power nap." in plan

def test_plan_adds_breathing_if_stressed():
    goals = []
    plan = generate_daily_plan(goals, sleep_hours=8, mood="stressed")
    assert "Do a 5-minute breathing exercise." in plan
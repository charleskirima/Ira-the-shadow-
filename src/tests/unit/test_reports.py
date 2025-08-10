from src.reports import morning_report

def test_morning_report_suggestions():
    logs = {
        "sleep_hours": 5,
        "mood": "low",
        "water_intake": 0.6
    }
    report = morning_report.generate_morning_report(logs)

    assert isinstance(report, dict), "Report should be a dictionary"
    suggestions = report.get("suggestions", [])
    
    assert "Try to sleep earlier tonight." in suggestions, "Missing sleep suggestion"
    assert "Start your day with a glass of water." in suggestions, "Missing hydration suggestion"
    assert any("gratitude" in s.lower() or "breathing" in s.lower() for s in suggestions), \
        "Missing mood-related suggestion (gratitude or breathing)"

def test_morning_report_with_missing_data():
    logs = {}  # All fields missing
    report = morning_report.generate_morning_report(logs)

    assert isinstance(report, dict), "Report should be a dictionary even if input is empty"
    assert "Sleep: unknown" in report["summary"], "Summary should indicate unknown sleep"
    assert isinstance(report.get("suggestions"), list), "Suggestions should default to a list"
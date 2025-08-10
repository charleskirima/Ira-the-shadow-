from typing import Dict, Union

def evaluate_budget(income: float, expenses: float) -> Dict[str, Union[float, str]]:
    """
    Evaluates the user's budget status based on income and expenses.

    Args:
        income (float): Total user income.
        expenses (float): Total user expenses.

    Returns:
        Dict[str, Union[float, str]]: Dictionary with calculated balance and budget status.
    """
    try:
        balance = round(income - expenses, 2)
        if balance > 0:
            status = "surplus"
        elif balance < 0:
            status = "deficit"
        else:
            status = "break-even"
        return {"balance": balance, "status": status}
    except Exception as e:
        return {"balance": 0.0, "status": f"error: {str(e)}"}

def suggest_financial_tip(goal: str) -> str:
    """
    Returns a financial tip based on the user's selected goal.

    Args:
        goal (str): One of "save", "invest", or "earn".

    Returns:
        str: Contextual financial advice.
    """
    tips = {
        "save": "Set aside 10% of your income weekly.",
        "invest": "Consider starting with diversified, low-risk ETFs.",
        "earn": "Leverage your skills through freelance or side hustles."
    }
    return tips.get(goal.lower(), "Track your spending and set clear goals.")
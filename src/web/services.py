def get_random_quote():
    return "You are allowed to rest. Growth doesn’t always look loud."

def get_job_suggestions():
    return ["Remote copywriting", "Junior frontend dev", "Sell digital journals"]

def fetch_reflection_prompt(belief):
    prompts = {
        "Christian": "How did you see grace today?",
        "Muslim": "What lesson did you take from your prayer today?",
        "Buddhist": "What truth was revealed today?",
        "Atheist": "What principle guided your actions today?"
    }
    return prompts.get(belief, "What gave you peace today?")
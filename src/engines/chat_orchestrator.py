import openai
from src.business_logic.chat_engine import interpret_intent, fallback_response
from src.engines.prompt_builder import build_system_prompt
from src.config.settings import OPENAI_API_KEY  # Assumes a central config file

# Configure OpenAI API key securely
openai.api_key = OPENAI_API_KEY

def orchestrate_response(user_message, context_data, use_gpt=True):
    if not use_gpt:
        intent = interpret_intent(user_message)
        print(f"[🔁] Intent identified: {intent}")

        if intent == "sleep_advice":
            return "Try sleeping at the same time every night and avoid screens an hour before bed."
        elif intent == "emotional_support":
            return "Want to talk about what’s making you feel this way? I'm here."
        elif intent == "daily_planner":
            return "Let’s map your goals for today. What would you like to focus on first?"
        else:
            return fallback_response()

    # Use GPT for open-ended responses
    try:
        system_prompt = build_system_prompt(context_data)

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=800
        )

        return response.choices[0].message["content"]

    except Exception as e:
        print(f"[❌] OpenAI API error: {e}")
        return "Hmm… I ran into a problem. Please try again later."
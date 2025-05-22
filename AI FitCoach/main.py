import os
from flask import Flask, request, jsonify
import google.generativeai as genai

# Configure Gemini with API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in environment variables.")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Start Flask app
app = Flask(__name__)

# Start conversation thread (for compatibility)
@app.route('/start', methods=['GET'])
def start_conversation():
    return jsonify({"thread_id": "fitness-session"})

# Generate response
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')

    if not thread_id:
        return jsonify({"error": "Missing thread_id"}), 400

    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    # Role-based messages with fitness assistant instruction
    messages = [
        {
            "role": "system",
            "content": """
You are an AI fitness assistant designed to help users plan their diet and workouts based on their personal information and fitness goals.

Ask for and use the following information:
- Name
- Age
- Sex
- Current weight
- Meal preference (veg, non-veg, or both)
- Goal (e.g., weight loss, weight gain, muscle gain, or fat loss)

Based on this input, generate:
- A 7-day meal plan:
    • Day 1 to Day 6: structured meals for breakfast, lunch, dinner, and snacks.
    • Day 7: rest or cheat meal suggestions aligned with the goal.
- A 7-day workout plan:
    • Day 1 to Day 6: daily workouts including warm-up, main exercises, and cool-down.
    • Day 7: rest day or light walking/stretching.

Guidelines:
- Keep responses simple, motivational, and tailored to the user's goal.
- Do not mention brands or supplements unless asked.
- Avoid medical claims or prescribing treatments.
- If the user asks anything unrelated to fitness, nutrition, or exercise, respond politely that you’re only a fitness assistant.

Example message style:
“Hey! Based on your info, here’s your Day 1 meal and workout plan 💪 Let’s crush your goals together!”
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # Convert to plain text prompt
    prompt = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in messages])

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
    except Exception as e:
        result = f"Error generating response: {str(e)}"

    return jsonify({"response": result})


# Run the Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

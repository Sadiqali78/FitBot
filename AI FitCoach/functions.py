import os
import json
import google.generativeai as genai

# Load Gemini API Key from environment variable (set your env variable as GOOGLE_API_KEY)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  
genai.configure(api_key=GOOGLE_API_KEY)

# Create a Gemini model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def get_completion_from_messages(messages, temperature=0.2, max_tokens=500):
    prompt = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in messages])

    response = model.generate_content(prompt,
                                      generation_config={
                                          "temperature": temperature,
                                          "max_output_tokens": max_tokens
                                      })

    return response.text

def create_assistant():
    assistant_file_path = 'assistant.json'
    
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            print("Loaded existing assistant settings.")
            return assistant_data
    else:
        # Load context from a document file (e.g., fitness_guide.txt)
        with open("FitCoach AI.docx", "r") as doc_file:
            document_content = doc_file.read()

        assistant_info = {
            "instructions": f"""
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

                Additional Reference (Fitness Guide Document):
                {document_content}

                Guidelines:
                    - Keep responses simple, motivational, and tailored to the user's goal.
                    - Do not mention brands or supplements unless asked.
                    - Avoid medical claims or prescribing treatments.
                    - If the user asks anything unrelated to fitness, nutrition, or exercise, respond politely that you’re only a fitness assistant.

                Example message style:
                “Hey! Based on your info, here’s your Day 1 meal and workout plan 💪 Let’s crush your goals together!”
            """,
            "model": "gemini-1.5-pro-latest"
        }

        with open(assistant_file_path, 'w') as file:
            json.dump(assistant_info, file)
            print("Created new assistant settings.")
        return assistant_info

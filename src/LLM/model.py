import requests
import json
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

TITLES_LIST = os.getenv("TITLES_LIST")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "samantha-mistral"



system_prompt = '''
You are a fiction book advisor.
Read the following list of book titles.
Analyze their style, genre, and tone.
Then recommend 5–10 original book titles that would appeal to someone who enjoyed these books.

Rules:
- Provide only the book titles.
- No explanations, introductions, or commentary.
- Make them sound realistic and engaging.
'''

user_prompt = "\n".join(TITLES_LIST)

def query_llm(prompt: str, system_prompt: str) -> str:
    full_prompt = f"### System:\n{system_prompt}\n### Input Titles:\n{prompt}\n### Recommendations:"
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": full_prompt},
            stream=True,
            timeout=300,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error querying LLM:", e)
        return ""

    text = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                if "response" in data:
                    text += data["response"]
            except json.JSONDecodeError:
                continue

    return text.strip()

if __name__ == "__main__":
    print("Querying...")
    reply = query_llm(user_prompt, system_prompt)
    
    print(reply)

    with open("LLM_recommendations.txt", "w", encoding="utf-8") as f:
        f.write(reply)

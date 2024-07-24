from openai import OpenAI

from app.core.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_gpt_response(prompt, repo_path):
    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=150,
    n=1,
    stop=None,
    temperature=0.7)
    return response.choices[0].message.content.strip()

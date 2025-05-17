from openai import OpenAI

client = OpenAI(api_key="")  # Вставь свой OpenAI API ключ

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Ты ассистент."},
        {"role": "user", "content": "Привет!"},
    ]
)
print(response.choices[0].message.content) 

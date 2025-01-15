from openai import OpenAI

client = OpenAI(
    api_key="sk-79GgdKZzhyOK8rvnpciFogWX3yA61T5W",
    base_url="https://api.proxyapi.ru/openai/v1",
)

a = 0.1
b = 0.2
print(a + b)


chat_completion = client.chat.completions.create(
    model="gpt-4o",
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Посчитай сумму чисел 0.1 и 0.2. в ответе запиши только число."},
            ],
        }
    ],
    max_tokens=1000
)
print('Генеративное сложение чисел 0.1 и 0.2:', chat_completion.choices[0].message.content)


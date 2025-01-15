from openai import OpenAI

client = OpenAI(
    api_key="sk-79GgdKZzhyOK8rvnpciFogWX3yA61T5W",
    base_url="https://api.proxyapi.ru/openai/v1",
)

#image = 'https://contest.yandex.ru/testsys/statement-image?imageId=48800fd8917ebc83276a787929b703b521347909b82d790cc17b82aef6aa800f'
image = 'http://sasgus.ru/uploads/new.png'

first = input()
second = input()
chat_completion = client.chat.completions.create(
    model="gpt-4o",
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Первое слово: '" + first + "', второе слово: " + second + ". На картинке слова указывают друг на друга стрелками. Например, слово 'Ром' указывает на слово 'Пират'. Найди на картинке эти слова, и внимательно проверь: если наше первое слово указывает стрелкой на картинке на второе, ответь: 'первый', если второе слово стрелкой на картинке указывает на первое, ответь 'второй', если же первое и второе слова совпадают, ответь 'ничья'. ответ дай в формате JSON: первый элемент - объяснение, второй элемент - ответ одним словом"},
                {"type": "image_url", "image_url": {"url": image,},},
            ],
        }
    ],
    max_tokens=1000
)

print(chat_completion.choices[0].message.content)
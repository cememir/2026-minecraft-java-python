import openai

client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="google/gemma-4-e4b", # Burası fark etmez, sunucu hangi modeli yüklediyse o çalışır
  messages=[
    {"role": "user", "content": "Python ile bir Fibonacci fonksiyonu yaz."}
  ]
)

print(completion.choices[0].message.content)

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5-mini",
    input="Reply only with: AI connection works"
)

print(response.output_text)
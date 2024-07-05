from openai import OpenAI
from API_KEY import OPEN_API_KEY

KEY = OPEN_API_KEY

client = OpenAI(api_key=KEY)

# calling openai_api
def ask_gpt(inputs, model="gpt-3.5-turbo-0613"): # you csn call any model you want to use
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are . Answer the following in Japanese. You are given a value from 0 to 100, which shows the degree of intimacy of two people.  \
                Please give me your opinion for improving the intimacy. It is much better to say your opinion with great deal of subjectiveness. You are not allowed to say your opinion in more than 200 words."},
            {"role": "user", "content": inputs}
        ],
        max_tokens=2000,
        temperature=0.8, # 0.7 is default
    )
    return response.choices[0].message.content.strip() # picking up the closest one
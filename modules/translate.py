import aiohttp

OPENAI_API_KEY = "Put your OpenAI API key here"

async def translate(string):
    if not OPENAI_API_KEY:
        return
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You will only output the exact translation of a singular line. You are not to change the order or organization of each line. You will respect each new line and line break and will make sure not to touch how the lines are positioned. If you cannot translate the text, you will output the original text."},
            {"role": "user", "content": string}
        ]
    }
    print('Translating...')
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data, timeout=10) as response:
                response.raise_for_status()
                content = (await response.json()).get('choices', [{}])[0].get('message', {}).get('content', None)
                if content:
                    return content
                else:
                    return f"Empty response from the API"
        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print("An unexpected error occurred: {e}")

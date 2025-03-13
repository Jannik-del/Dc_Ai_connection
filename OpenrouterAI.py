import nextcord
from nextcord.ext import commands
import requests
import time
import json
from config import OPENROUTER_API_KEY, OPENROUTER_CHANNEL_ID  # API-Key & Channel-ID aus config.py laden


# OpenRouter API-Funktion mit Fehler- und Rate-Limit-Handling
def query_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    for _ in range(3):  # Maximal 3 Versuche bei Rate-Limit
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            try:
                return response.json()["choices"][0]["message"]["content"]
            except (KeyError, IndexError, json.JSONDecodeError):
                return "Fehler beim Verarbeiten der Antwort."

        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            time.sleep(retry_after)  # Wartezeit basierend auf Header oder 5 Sekunden
        else:
            return f"API-Fehler: {response.status_code} - {response.text}"

    return "Fehlgeschlagen: Rate-Limit erreicht oder keine Antwort."


# Funktion zum Senden langer Nachrichten in Discord
async def send_long_message(channel, text):
    for i in range(0, len(text), 2000):
        await channel.send(text[i:i + 2000])


# Discord Cog für OpenRouter AI
class OpenRouterAI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id != OPENROUTER_CHANNEL_ID:
            return

        async with message.channel.typing():
            response = query_openrouter(message.content)
            await send_long_message(message.channel, response)


def setup(client):
    client.add_cog(OpenRouterAI(client))

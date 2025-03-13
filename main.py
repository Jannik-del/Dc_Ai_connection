import config
import nextcord
from nextcord.ext import commands
import os

# Bot-Intents festlegen
intents = nextcord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Erforderlich für Befehle

# Bot initialisieren
client = commands.Bot(command_prefix="!", intents=intents)
guild = client.get_guild(config.GUILD_ID)

#extensions
client.load_extension("reload")
client.load_extension("commands")
client.load_extension("OpenrouterAI")


@client.event
async def on_ready():
    print(f'Bot is active as {client.user}')

    activity = nextcord.Activity(
        type=nextcord.ActivityType.competing,
        name="Ai connection",
        state="Providing Ai to Discord"
        " using OpenAi´s api",
        details="trying to stay alive",
        assets={"large_image": "", "large_text": "Providing"}
    )
    await client.change_presence(activity=activity)

client.run(config.BOT_TOKEN)
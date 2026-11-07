import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Ladataan ympäristömuuttujat .env-tiedostosta (tai Square Cloudin muuttujista)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Määritetään botin esiintymä ja tavallinen viestiprefiksi (tässä '::')
intents = discord.Intents.default()
intents.message_content = True  # Vaaditaan tekstiviestien lukemiseen

bot = commands.Bot(command_prefix="::", intents=intents)

@bot.event
async def on_ready():
    print(f"Botti kirjautuneena sisään: {bot.user} (ID: {bot.user.id})")
    
    # Synkronoidaan Slash-komennot Discordiin
    try:
        synced = await bot.tree.sync()
        print(f"Synkronoitu {len(synced)} slash-komentoa.")
    except Exception as e:
        print(f"Virhe slash-komentojen synkronoinnissa: {e}")

    print("Lunar on valmis toimintaan!")

# Funktio, joka lataa automaattisesti kaikki cogs-kansion python-tiedostot
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(extension_name)
                print(f"Ladattu cog: {extension_name}")
            except Exception as e:
                print(f"Virhe ladattaessa cogia {extension_name}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Käynnistetään botti
if __name__ == "__main__":
    asyncio.run(main())

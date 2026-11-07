import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Ladataan ympäristömuuttujat (mikäli käytetään .env-tiedostoa paikallisesti)
load_dotenv()

# Haetaan token joko TOKEN- tai DISCORD_TOKEN-muuttujasta
TOKEN = os.getenv("TOKEN") or os.getenv("DISCORD_TOKEN")

# Määritetään botin esiintymä ja tarvittavat oikeudet (Intents)
intents = discord.Intents.default()
intents.message_content = True  # Vaaditaan tekstiviestien lukemiseen ja perinteisiin komentoihin

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
    if not os.path.exists("./cogs"):
        print("Varoitus: 'cogs'-kansiota ei löytynyt!")
        return

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(extension_name)
                print(f"Ladattu cog: {extension_name}")
            except Exception as e:
                print(f"Virhe ladattaessa cogia {extension_name}: {e}")

async def main():
    if not TOKEN:
        print("VIRHE: Discord-tokenia ei löytynyt! Tarkista Bot-Hosting.netin ympäristömuuttujat.")
        return

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Käynnistetään botti
if __name__ == "__main__":
    asyncio.run(main())

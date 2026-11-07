import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Asetetaan etuliikkeeksi nuolimerkki '>'
bot = commands.Bot(command_prefix=">", intents=intents)


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user} (ID: {bot.user.id})")

  # Synkronoidaan slash-komennot Discordiin, jotta ne näkyvät kun kirjoitat '/'
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} slash command(s).")
  except Exception as e:
    print(f"Failed to sync slash commands: {e}")

  print("Bot is ready and online!")


# Ladataan automaattisesti kaikki cogs-kansion tiedostot
async def load_extensions():
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      await bot.load_extension(f"cogs.{filename[:-3]}")
      print(f"Loaded cog: {filename}")


async def main():
  async with bot:
    await load_extensions()
    await bot.start(os.getenv("DISCORD_TOKEN"))


asyncio.run(main())

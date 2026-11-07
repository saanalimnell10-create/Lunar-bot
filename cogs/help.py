import discord
from discord.ext import commands
from discord import app_commands

# 1. Luodaan Dropdown-valikko (Select UI)
class HelpDropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="General", 
                description="Basic and info commands", 
                emoji="ℹ️"
            ),
            discord.SelectOption(
                label="Moderation", 
                description="Server management commands", 
                emoji="🛡️"
            ),
            discord.SelectOption(
                label="Fun", 
                description="Entertainment and minigame commands", 
                emoji="🎮"
            ),
        ]
        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Vaihdetaan Embedin sisältö valinnan mukaan
        if self.values[0] == "General":
            embed = discord.Embed(
                title="ℹ️ General Commands",
                description="`::ping` - Check bot latency\n`::info` - Information about the bot",
                color=discord.Color.blue()
            )
        elif self.values[0] == "Moderation":
            embed = discord.Embed(
                title="🛡️ Moderation Commands",
                description="`::clear [amount]` - Delete messages\n`::kick [member]` - Kick a member",
                color=discord.Color.red()
            )
        elif self.values[0] == "Fun":
            embed = discord.Embed(
                title="🎮 Fun Commands",
                description="`::8ball [question]` - Ask the oracle\n`::roll` - Roll a dice",
                color=discord.Color.green()
            )

        await interaction.response.edit_message(embed=embed)

# 2. Luodaan View, joka sisältää dropdown-valikon
class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.add_item(HelpDropdown(bot))

# 3. Varsinainen Cog, joka sisältää sekä perinteisen että slash-komennon
class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Poistetaan Discordin oletus-help, jotta ::help toimii
        self.bot.remove_command('help')

    # Perinteinen komento: ::help (ja alias ::apu)
    @commands.command(name="help", aliases=["apu"])
    async def custom_help(self, ctx):
        embed = discord.Embed(
            title="🌙 Lunar Bot - Help Menu",
            description="Select a category from the dropdown menu below to view commands!",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

        view = HelpView(self.bot)
        await ctx.send(embed=embed, view=view)

    # Slash-komento: /help
    @app_commands.command(name="help", description="Show Lunar's help menu with a dropdown menu")
    async def slash_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌙 Lunar Bot - Help Menu",
            description="Select a category from the dropdown menu below to view commands!",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Requested by: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)

        view = HelpView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

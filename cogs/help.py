import discord
from discord.ext import commands

# 1. Create the Dropdown Menu (Select UI)
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
        # Change the Embed content based on the selection
        if self.values[0] == "General":
            embed = discord.Embed(
                title="ℹ️ General Commands",
                description="`!ping` - Check bot latency\n`!info` - Information about the bot",
                color=discord.Color.blue()
            )
        elif self.values[0] == "Moderation":
            embed = discord.Embed(
                title="🛡️ Moderation Commands",
                description="`!clear [amount]` - Delete messages\n`!kick [member]` - Kick a member",
                color=discord.Color.red()
            )
        elif self.values[0] == "Fun":
            embed = discord.Embed(
                title="🎮 Fun Commands",
                description="`!8ball [question]` - Ask the oracle\n`!roll` - Roll a dice",
                color=discord.Color.green()
            )

        await interaction.response.edit_message(embed=embed)

# 2. Create the View containing the dropdown menu
class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)  # The menu times out after 60 seconds
        self.add_item(HelpDropdown(bot))

# 3. Create the actual Cog
class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Remove Discord's default help command so this one works
        self.bot.remove_command('help')

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

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

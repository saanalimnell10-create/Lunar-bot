import discord
from discord.ext import commands
from discord import app_commands

# Soft Pastel / Cotton Candy Pink color
PASTEL_PINK = discord.Color.from_rgb(255, 183, 197)

# 1. Dropdown Select Menu
class HelpSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="Overview", 
                description="View a quick summary of all categories", 
                emoji="🌙", 
                value="overview"
            ),
            discord.SelectOption(
                label="Moderation", 
                description="View moderation commands (clear, kick, ban)", 
                emoji="🛡️", 
                value="moderation"
            ),
            discord.SelectOption(
                label="Utility", 
                description="View utility commands (help)", 
                emoji="⚙️", 
                value="utility"
            )
        ]
        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "overview":
            embed = discord.Embed(
                title="🌙 Lunar Bot - Command Menu",
                description="Select a category from the dropdown menu below to see details!",
                color=PASTEL_PINK
            )
            embed.add_field(name="🛡️ Moderation", value="`/clear`, `/kick`, `/ban`", inline=False)
            embed.add_field(name="⚙️ Utility", value="`/help`", inline=False)

        elif selected == "moderation":
            embed = discord.Embed(
                title="🛡️ Moderation Commands",
                description="All available moderation commands (supports both `::` and `/`):",
                color=PASTEL_PINK
            )
            embed.add_field(
                name="clear", 
                value="**`::clear [amount]`** / **`/clear [amount]`**\nDeletes messages from the channel (default: 5).", 
                inline=False
            )
            embed.add_field(
                name="kick", 
                value="**`::kick @user [reason]`** / **`/kick @user [reason]`**\nKicks a member from the server.", 
                inline=False
            )
            embed.add_field(
                name="ban", 
                value="**`::ban @user [reason]`** / **`/ban @user [reason]`**\nBans a member from the server.", 
                inline=False
            )

        elif selected == "utility":
            embed = discord.Embed(
                title="⚙️ Utility Commands",
                description="General utility commands:",
                color=PASTEL_PINK
            )
            embed.add_field(
                name="help", 
                value="**`::help`** / **`/help`**\nOpens this interactive help menu.", 
                inline=False
            )

        embed.set_footer(text="Lunar Bot • Cotton Candy Theme")
        await interaction.response.edit_message(embed=embed, view=self.view)


# 2. View Container
class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)  # Dropdown expires after 60 seconds
        self.add_item(HelpSelect(bot))


# 3. Cog Definition
class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = None

    @commands.command(name="help", aliases=["info"])
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🌙 Lunar Bot - Command Menu",
            description="Select a category from the dropdown menu below to see details!",
            color=PASTEL_PINK
        )
        view = HelpView(self.bot)
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="help", description="Show Lunar bot dropdown menu")
    async def slash_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌙 Lunar Bot - Command Menu",
            description="Select a category from the dropdown menu below to see details!",
            color=PASTEL_PINK
        )
        view = HelpView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

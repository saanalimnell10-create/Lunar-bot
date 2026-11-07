import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Poistetaan Discordin oletus-help, jotta tämä oma toimii
        self.bot.help_command = None

    # Prefix-komento: ::help
    @commands.command(name="help", aliases=["apu", "ohje"])
    async def help_command(self, ctx):
        """Displays the help menu."""
        embed = self.build_help_embed()
        await ctx.send(embed=embed)

    # Slash-komento: /help
    @app_commands.command(name="help", description="Show active Lunar bot commands")
    async def slash_help(self, interaction: discord.Interaction):
        embed = self.build_help_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    def build_help_embed(self):
        embed = discord.Embed(
            title="🌙 Lunar Bot - Command Menu",
            description="Lunar supports both prefix (`::`) and Slash (`/`) commands!",
            color=discord.Color.blue()
        )
        if self.bot.user and self.bot.user.display_avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        # Active Moderation Commands
        mod_commands = (
            "**`::clear [amount]`** | **`/clear [amount]`**\n"
            "↳ Delete messages from the channel (default: 5).\n\n"
            "**`::kick @user [reason]`** | **`/kick @user [reason]`**\n"
            "↳ Kick a member from the server.\n\n"
            "**`::ban @user [reason]`** | **`/ban @user [reason]`**\n"
            "↳ Ban a member from the server."
        )
        embed.add_field(name="🛡️ Moderation", value=mod_commands, inline=False)

        # Utility Commands
        general_commands = (
            "**`::help`** | **`/help`**\n"
            "↳ Show this active help menu."
        )
        embed.add_field(name="⚙️ Utility", value=general_commands, inline=False)

        embed.set_footer(text="Lunar Bot • Moderation Module")
        return embed

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

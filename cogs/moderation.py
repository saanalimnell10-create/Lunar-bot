import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- CLEAR / PURGE ---
    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Deletes messages from the channel."""
        if amount <= 0:
            await ctx.send("Please provide a number greater than 0!", delete_after=5)
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Purged {len(deleted) - 1} messages!", delete_after=5)

    @app_commands.command(name="clear", description="Delete messages from this channel")
    @app_commands.describe(amount="Number of messages to delete (default 5)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def slash_clear(self, interaction: discord.Interaction, amount: int = 5):
        if amount <= 0:
            await interaction.response.send_message("Please provide a number greater than 0!", ephemeral=True)
            return

        await interaction.response.defer(thinking=True, ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🧹 Purged {len(deleted)} messages!", ephemeral=True)

    # --- KICK ---
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """Kicks a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f"👢 **{member.name}** has been kicked. Reason: {reason}")

    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.describe(member="The member to kick", reason="Reason for the kick")
    @app_commands.checks.has_permissions(kick_members=True)
    async def slash_kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 **{member.name}** has been kicked. Reason: {reason}")

    # --- BAN ---
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """Bans a member from the server."""
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.name}** has been banned. Reason: {reason}")

    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.describe(member="The member to ban", reason="Reason for the ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def slash_ban(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 **{member.name}** has been banned. Reason: {reason}")

    # --- ERROR HANDLING ---
    @clear.error
    @kick.error
    @ban.error
    async def mod_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Missing arguments. Check command usage!", delete_after=5)

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))

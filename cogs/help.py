import discord
from discord.ext import commands
from discord import app_commands

# 1. Luodaan Dropdown-valikko (Select-komponentti)
class HelpSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="Yleiskatsaus", 
                description="Katso kaikkien komentojen tiivistelmä", 
                emoji="🌙", 
                value="overview"
            ),
            discord.SelectOption(
                label="Moderointi", 
                description="Katso moderoinnin komennot (clear, kick, ban)", 
                emoji="🛡️", 
                value="moderation"
            ),
            discord.SelectOption(
                label="Työkalut", 
                description="Katso hyötykomennot (help)", 
                emoji="⚙️", 
                value="utility"
            )
        ]
        super().__init__(placeholder="Valitse kategoria...", min_values=1, max_values=1, options=options)

    # Tämä funktio suoritetaan, kun käyttäjä valitsee jotain valikosta
    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "overview":
            embed = discord.Embed(
                title="🌙 Lunar Bot - Command Menu",
                description="Valitse dropdown-valikosta kategoria nähdäksesi lisätietoja!",
                color=discord.Color.blue()
            )
            embed.add_field(name="🛡️ Moderation", value="`/clear`, `/kick`, `/ban`", inline=False)
            embed.add_field(name="⚙️ Utility", value="`/help`", inline=False)

        elif selected == "moderation":
            embed = discord.Embed(
                title="🛡️ Moderointikomennot",
                description="Kaikki moderoinnin peruskommennot (tukee sekä `::` että `/`):",
                color=discord.Color.red()
            )
            embed.add_field(name="clear", value="**`::clear [määrä]`** / **`/clear [määrä]`**\nPoistaa viestejä kanavalta (oletus: 5).", inline=False)
            embed.add_field(name="kick", value="**`::kick @user [syy]`** / **`/kick @user [syy]`**\nPotkaisee käyttäjän palvelimelta.", inline=False)
            embed.add_field(name="ban", value="**`::ban @user [syy]`** / **`/ban @user [syy]`**\nPorttikieltää käyttäjän palvelimelta.", inline=False)

        elif selected == "utility":
            embed = discord.Embed(
                title="⚙️ Työkalukomennot",
                description="Yleiset hyötykomennot:",
                color=discord.Color.green()
            )
            embed.add_field(name="help", value="**`::help`** / **`/help`**\nAvaa tämän ohjevalikon.", inline=False)

        embed.set_footer(text="Lunar Bot • Dropdown Help")
        await interaction.response.edit_message(embed=embed, view=self.view)


# 2. Luodaan View, joka sisältää dropdown-valikon
class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60) # Valikko vanhenee 60 sekunnissa
        self.add_item(HelpSelect(bot))


# 3. Cog itse
class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = None

    @commands.command(name="help", aliases=["apu", "ohje"])
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🌙 Lunar Bot - Command Menu",
            description="Valitse dropdown-valikosta kategoria nähdäksesi lisätietoja!",
            color=discord.Color.blue()
        )
        view = HelpView(self.bot)
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="help", description="Show Lunar bot dropdown menu")
    async def slash_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🌙 Lunar Bot - Command Menu",
            description="Valitse dropdown-valikosta kategoria nähdäksesi lisätietoja!",
            color=discord.Color.blue()
        )
        view = HelpView(self.bot)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))

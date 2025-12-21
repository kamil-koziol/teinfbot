import discord
from discord.ext import commands
from discord import app_commands
from bot.utils.time_parser import TimeParser

from bot import Bot
from db import TimeEntryRepository
import bot.utils.discord as dc

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Czas(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @app_commands.command(
        name="czas", description="Wyświetla czas spędzony na serwerze"
    )
    @app_commands.describe(user="Użytkownik")
    async def czas(self, interaction: discord.Interaction, user: discord.Member = None):
        try:
            user = user or interaction.user

            time_spent = TimeEntryRepository().get_user_time_entry_count(user.id)

            em = discord.Embed(
                title="Czas spędzony na serwerze",
                description=f"{user.name} spędził {str(TimeParser(time_spent * 60))} na serwerze",
                color=discord.Colour.green(),
            )
            await interaction.response.send_message(embed=em)
        except Exception as e:
            print(e)

    @app_commands.command(
        name="czas_top",
        description="Wyświetla top użytkowników pod względem czasu spędzonego",
    )
    @app_commands.describe(number="Liczba użytkowników do wyświetlenia (1-20)")
    async def czas_top(self, interaction: discord.Interaction, number: int):
        if number < 1 or number > 20:
            await interaction.response.send_message(
                "Liczba musi być między 1 a 20!", ephemeral=True
            )
            return

        top_user_ids = TimeEntryRepository().get_top_users_by_time_entry_count(number)

        description = ""
        for i, top_user in enumerate(top_user_ids, 1):
            description += f"{i}. {dc.mention_user(top_user['user_id'])} - {TimeParser(top_user['total'] * 60)}\n"

        em = discord.Embed(
            title=f"Top {number} użytkowników pod względem spędzonego czasu",
            description=description or "Brak danych.",
            color=discord.Colour.green(),
        )
        await interaction.response.send_message(embed=em)

    async def cog_load(self):
        # Register both commands with a specific guild
        self.bot.tree.add_command(self.czas, guild=self.bot.guild)
        self.bot.tree.add_command(self.czas_top, guild=self.bot.guild)


async def setup(bot: Bot):
    await bot.add_cog(Czas(bot))

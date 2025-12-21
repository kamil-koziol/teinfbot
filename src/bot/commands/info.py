import discord
from discord.ext import commands
from discord import app_commands

from bot import Bot
from bot.utils.discord import mention_user
from bot.utils.time_parser import TimeParser
from db import TimeEntryRepository

import logging

logger = logging.getLogger(__name__)


class Info(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @app_commands.command(name="info", description="Wyświetla informacje o użytkowniku")
    @app_commands.describe(user="Użytkownik")
    async def info(self, interaction: discord.Interaction, user: discord.Member = None):
        try:
            member = user or interaction.user
            time_spent = TimeEntryRepository().get_user_time_entry_count(member.id)

            informacje = {
                "#": mention_user(member.id),
                "Nick": member.name,
                "Spędzony czas": str(TimeParser(time_spent * 60)),
                "ID": member.id,
                "Status": member.status,
                "Najwyższa rola": member.top_role.name,
                "Dołączył/a": member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
                if member.joined_at
                else "Nieznane",
                "Avatar": member.avatar.url if member.avatar else "Brak",
                "Serwer": member.guild.name,
            }

            wiadomosc = "\n".join(
                f"{key} : {value}" for key, value in informacje.items()
            )

            em = discord.Embed(
                title=f"Informacje o {informacje['Nick']}",
                description=wiadomosc,
                colour=discord.Colour.green(),
            )
            await interaction.response.send_message(embed=em)
        except Exception as e:
            logger.error(f"{self.czas_top.__name__} failed with {e}")

    async def cog_load(self):
        # Directly add the command to the bot's set guild
        self.bot.tree.add_command(self.info, guild=self.bot.guild)


async def setup(bot: Bot):
    await bot.add_cog(Info(bot))

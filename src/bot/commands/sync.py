from discord.ext import commands
from discord import app_commands
from bot import Bot
import discord
from db import User, UserRepository


class Sync(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @app_commands.command(
        name="sync",
        description="Synchronizuje wszystkich członków serwera z bazą danych",
    )
    async def sync(self, interaction: discord.Interaction):
        # Check if user is an administrator
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Tylko administratorzy mogą używać tej komendy.", ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)

        try:
            guild = interaction.guild
            members = [member async for member in guild.fetch_members(limit=None)]
            users_by_id = {user.id: user for user in UserRepository().list_users()}

            created_count = 0
            for member in members:
                # Skip bots
                if member.bot:
                    continue

                if member.id in users_by_id:
                    continue

                UserRepository().create(User(id=member.id))
                created_count += 1

            await interaction.followup.send(
                f"Synchronizacja zakończona. Utworzono {created_count} nowych użytkowników."
            )
        except Exception as e:
            await interaction.followup.send(
                f"Wystąpił błąd podczas synchronizacji: {e}"
            )

    async def cog_load(self):
        self.bot.tree.add_command(self.sync, guild=self.bot.guild)


async def setup(bot: Bot):
    await bot.add_cog(Sync(bot))

from discord.ext import tasks, commands

from bot import Bot
from db import TimeEntryRepository, TimeEntry, TimeEntryType
import datetime

import logging

logger = logging.getLogger(__name__)

class TimeCounter(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.time_counter.start()

    def cog_unload(self):
        self.time_counter.cancel()

    @tasks.loop(minutes=1)
    async def time_counter(self):
        await self.bot.wait_until_ready()
        online_members = await self.bot.get_members_in_voice_channels()
        ids = [m.id for m in online_members]
        logger.info(f"time update for {ids}")

        time_entry_repo = TimeEntryRepository()
        for _id in ids:
            time_entry_repo.create(TimeEntry(user_id=_id))

        afk_members = await self.bot.get_members_in_afk_channel()
        ids = [m.id for m in afk_members]
        logger.info(f"AFK time update for {ids}")

        time_entry_repo = TimeEntryRepository()
        for _id in ids:
            time_entry_repo.create(TimeEntry(user_id=_id, type=TimeEntryType.AFK))

    @time_counter.before_loop
    async def before_time_counter(self):
        await self.bot.wait_until_ready()


async def setup(bot: Bot):
    await bot.add_cog(TimeCounter(bot))

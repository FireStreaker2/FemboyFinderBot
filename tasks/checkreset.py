import util.config
from discord.ext import tasks
from datetime import datetime
from database.redis import r


@tasks.loop(minutes=1)
async def check_reset():
    if datetime.now().day == 1 and util.config.RESET_STATUS != True:
        await r.set("femboys", 0)
        util.config.RESET_STATUS = True

        print("Femboy count has been reset!")

    elif datetime.now().day == 2 and util.config.RESET_STATUS:
        util.config.RESET_STATUS = False

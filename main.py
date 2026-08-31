# packages
import util.config
import database.redis
import discord
from discord.ext import commands
from os import listdir
from asyncio import sleep
from tasks.checkreset import check_reset

bot = commands.AutoShardedBot(intents=util.config.INTENTS)
for filename in listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        bot.load_extension(f"cogs.{filename[:-3]}")


# events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print(f"Shards: {bot.shard_count}")

    await database.redis.initialize_redis()
    await util.emojis.emojis.load(bot)

    if util.config.MONTHLY_RESET == True:
        check_reset.start()

    if util.config.FEMBOYS:
        await database.redis.r.set("femboys", util.config.FEMBOYS)
        print(f"Femboy count set to {util.config.FEMBOYS}\n")

    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=util.config.STATUS
        ),
    )


@bot.event
async def on_guild_join(guild):
    await sleep(5)

    try:
        channel = guild.system_channel
        embed = (
            discord.Embed(
                title="Hello!",
                description="Yahoo! My name is Astolfo! Rider Class! And, and...umm, nice to meet you!",
            )
            .add_field(
                name="Help",
                value=f"If you need help, you can run the ``/help`` command!",
                inline=False,
            )
            .add_field(
                name="Have fun!", value="I hope you have fun using me!", inline=False
            )
            .add_field(
                name="Notice",
                value="Please note that I may occasionally send NSFW content.",
            )
            .set_thumbnail(
                url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg"
            )
            .set_footer(
                text="FemboyFinderBot ❤️",
                icon_url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg",
            )
        )

        await channel.send(embed=embed)
    except Exception as error:
        print(f"Unable to send welcome message: {error}")


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond(
            "Hm? Is it tough not having any common sense? Well, I guess so. But you know, there are things that only I can understand because I lack common sense. (you forgot to add all the arguments)"
        )
    elif isinstance(error, commands.CommandNotFound):
        await ctx.respond("master, i couldnt find that command")
    else:
        await ctx.respond(f"An error occurred: {error}")


bot.run(util.config.TOKEN)

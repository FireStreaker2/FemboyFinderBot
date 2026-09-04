# packages
import util.config
import database.redis
import discord
from discord.ext import commands
from os import listdir
from asyncio import sleep
from tasks.checkreset import check_reset
from util.embeds import base_embed, error_embed

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
            base_embed(
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
        )

        await channel.send(embed=embed)
    except Exception as error:
        print(f"Unable to send welcome message: {error}")


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = error_embed(
            title="Missing Arguments",
            description=(
                "Hm? Is it tough not having any common sense? "
                "Well, I guess so. But you know, there are things "
                "that only I can understand because I lack common sense."
            ),
        ).add_field(
            name="What happened?",
            value="You forgot to add all the required arguments.",
            inline=False,
        )

        await ctx.respond(embed=embed)

    elif isinstance(error, commands.CommandNotFound):
        embed = error_embed(
            title="Command Not Found",
            description="Master, I couldn't find that command!",
        )

        await ctx.respond(embed=embed)

    else:
        print(f"Error in {ctx.command}: {error}")

        embed = error_embed(
            title="Something Went Wrong",
            description=(
                "Something unexpected happened while running this command. "
                "Please try again later."
                "If this happens again, please make a support ticket in the [support server](https://discord.gg/bruQhB8Eg5)."
            ),
        )

        await ctx.respond(embed=embed)


bot.run(util.config.TOKEN)

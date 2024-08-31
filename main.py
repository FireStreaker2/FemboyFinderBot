# packages
import discord
from discord.ext import commands, tasks
from asyncio import sleep
from aiohttp import ClientSession
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

# environment variables
load_dotenv()

config = {
    "token": getenv("TOKEN"),
    "status": getenv("STATUS", "Femboys"),
    "femboys": int(getenv("FEMBOY_COUNT", 0)),
    "monthlyReset": bool(getenv("MONTHLY_RESET", False)),
    "resetStatus": False,
    "api": getenv("API", "https://femboyfinder.firestreaker2.gq/api"),
    "intents": discord.Intents.default(),
}

bot = commands.Bot(intents=config["intents"])


async def fetch(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()


# events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")

    copy = config.copy()
    copy["token"] = f"{copy['token'].split(".")[0]}.*******"
    print(f"Using config:\n{copy}")

    if config["monthlyReset"] == True:
        check_reset.start()

    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=config["status"]
        ),
    )


@bot.event
async def on_guild_join(guild):
    await sleep(5)

    pfp = discord.File("./images/gura.png", filename="gura.png")
    logo = discord.File("./images/astolfo.jpg", filename="astolfo.jpg")

    try:
        channel = guild.system_channel
        embed = discord.Embed(
            title="Hello!",
            description="Yahoo! My name is Astolfo! Rider Class! And, and...umm, nice to meet you!",
        )
        embed.add_field(
            name="Help",
            value=f"If you need help, you can run the ``/help`` command!",
            inline=False,
        )
        embed.add_field(
            name="Have fun!", value="I hope you have fun using me!", inline=False
        )
        embed.add_field(
            name="Notice",
            value="Please note that I may occasionally send NSFW content.",
        )
        embed.set_thumbnail(url="attachment://astolfo.jpg")
        embed.set_footer(
            text="Made by FireStreaker2",
            icon_url="attachment://gura.png",
        )

        await channel.send(embed=embed, files=[pfp, logo])
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


@tasks.loop(minutes=1)
async def check_reset():
    if datetime.now().day == 1 and config["resetStatus"] != True:
        config["femboys"] = 0
        config["ResetStatus"] = True

        print("Femboy count has been reset!")

    elif datetime.now().day == 2 and config["ResetStatus"]:
        config["ResetStatus"] = False


# commands
@bot.slash_command(
    integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },
    description="Find a femboy near you!",
)
async def find(ctx, query):
    await ctx.defer()

    pfp = discord.File("./images/gura.png", filename="gura.png")
    logo = discord.File("./images/astolfo.jpg", filename="astolfo.jpg")

    if isinstance(ctx.channel, discord.DMChannel) or (
        isinstance(ctx.channel, discord.TextChannel) and ctx.channel.is_nsfw()
    ):
        try:
            data = await fetch(f"{config['api']}/{query}")

        except:
            embed = discord.Embed(
                title="An Error Occurred",
                description="Hey, hey, Master! Something's up, let's go check it out!",
            )
            embed.add_field(name="Internal Server Error", value="404: No femboys found")
            embed.set_thumbnail(url="attachment://astolfo.jpg")
            embed.set_footer(
                text="Made by FireStreaker2",
                icon_url="attachment://gura.png",
            )

            await ctx.respond(embed=embed, files=[pfp, logo])
            return

        image = data.get("url")
        tags = data.get("tags")
        source = data.get("source")

        embed = discord.Embed(title="Femboy Found!", url=source)
        embed.add_field(name="Query", value=query, inline=False)
        embed.add_field(name="Tags", value=tags, inline=False)
        embed.set_image(url=image)
        embed.set_footer(
            text="Made by FireStreaker2",
            icon_url="attachment://gura.png",
        )

        await ctx.respond(embed=embed, file=pfp)
        config["femboys"] += 1

    else:
        embed = discord.Embed(
            title="Error",
            description="This channel is not marked as NSFW. In order to succesfully run this command, please mark this channel as NSFW and rerun this command.",
        )
        embed.set_thumbnail(url="attachment://astolfo.jpg")
        embed.set_footer(
            text="Made by FireStreaker2",
            icon_url="attachment://gura.png",
        )

        await ctx.respond(embed=embed, files=[pfp, logo])
        return


@bot.slash_command(
    integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },
    description="About FemboyFinderBot",
)
async def about(ctx):
    await ctx.defer()

    pfp = discord.File("./images/gura.png", filename="gura.png")
    logo = discord.File("./images/astolfo.jpg", filename="astolfo.jpg")

    embed = discord.Embed(
        title="About",
        description="FemboyFinderBot is a bot developed by firestreaker2, using Pycord. It works by querying the FemboyFinder API for images given the value provided by the end user, and randomly selects one.",
    )
    embed.add_field(
        name="Support Server",
        value="You may join our support server [here](https://discord.gg/bruQhB8Eg5).",
    )
    embed.add_field(
        name="More Resources",
        value="For more info, you may refer to the [GitHub Page](https://github.com/FireStreaker2/FemboyFinderBot) or the [FemboyFinder API](https://github.com/FireStreaker2/FemboyFinder).",
        inline=False,
    )
    embed.set_thumbnail(url="attachment://astolfo.jpg")
    embed.set_footer(
        text="Made by FireStreaker2",
        icon_url="attachment://gura.png",
    )

    await ctx.respond(embed=embed, files=[pfp, logo])


@bot.slash_command(
    integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },
    description="Bot Statistics",
)
async def stats(ctx):
    await ctx.defer()

    pfp = discord.File("./images/gura.png", filename="gura.png")
    logo = discord.File("./images/astolfo.jpg", filename="astolfo.jpg")

    embed = discord.Embed(title="Stats")
    embed.add_field(
        name="Guilds",
        value=f"I am currently in {len(bot.guilds)} servers.",
        inline=False,
    )
    embed.add_field(
        name="Femboys",
        value=f"I have found {config['femboys']} femboys {'this month' if config['monthlyReset'] else 'so far'}.",
        inline=False,
    )
    embed.set_thumbnail(url="attachment://astolfo.jpg")
    embed.set_footer(
        text="Made by FireStreaker2",
        icon_url="attachment://gura.png",
    )

    await ctx.respond(embed=embed, files=[pfp, logo])


## custom help message
bot.remove_command("help")


@bot.slash_command(
    integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },
    description="Send a help message",
)
async def help(ctx):
    await ctx.defer()

    pfp = discord.File("./images/gura.png", filename="gura.png")
    logo = discord.File("./images/astolfo.jpg", filename="astolfo.jpg")

    embed = discord.Embed(title="Help", description="Help for FemboyFinderBot")
    embed.add_field(name="Prefix", value="``/``", inline=False)
    embed.add_field(
        name="/find [query]",
        value="Find a femboy!\nExample: ``/find astolfo``\n\n> Note that if you are trying to search with a term that has more than one word, use a ``_`` instead of a space. If you are searching for multiple tags, then use a space between them.\n> Example: ``/find felix_argyle``\n> Example 2: ``/find astolfo stockings``",
        inline=False,
    )
    embed.add_field(
        name="/about",
        value="Sends the about message.\nExample: ``/about``",
        inline=False,
    )
    embed.add_field(
        name="/stats", value="Sends bot statistics.\nExample: ``/stats``", inline=False
    )
    embed.add_field(
        name="/help", value="Sends this message!\nExample: ``/help``", inline=False
    )
    embed.add_field(
        name="Support Server",
        value="You may join our support server [here](https://discord.gg/bruQhB8Eg5).",
    )
    embed.set_thumbnail(url="attachment://astolfo.jpg")
    embed.set_footer(
        text="Made by FireStreaker2",
        icon_url="attachment://gura.png",
    )

    await ctx.respond(embed=embed, files=[pfp, logo])


bot.run(config["token"])

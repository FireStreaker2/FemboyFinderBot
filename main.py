# packages
import discord
from discord.ext import commands, tasks
import asyncio
from dotenv import load_dotenv
import os
import requests
import json
import datetime

# environment variables
load_dotenv()
femboys = int(os.getenv("FEMBOY_COUNT", 0))

config = {
    "TOKEN": os.getenv("TOKEN"),
    "Status": os.getenv("STATUS", "Femboys"),
    "MonthlyReset": os.getenv("MONTHLY_RESET", False),
    "API": os.getenv("API", "https://femboyfinder.firestreaker2.gq/api"),
    "Intents": discord.Intents.default(),
}

bot = commands.Bot(intents=config["Intents"])


# events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=config["Status"]
        ),
    )


@bot.event
async def on_guild_join(guild):
    await asyncio.sleep(5)

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
async def on_command_error(ctx, error):
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
    if config["MonthlyReset"] == True:
        now = datetime.datetime.now()
        if now.day == 1 and now.hour == 0 and now.minute == 0:
            global femboys
            femboys = 0


# commands
@bot.slash_command(description="Find a femboy near you!")
async def find(ctx, query):
    await ctx.defer()

    pfp = discord.File("./images/gura.png", filename="gura.png")
    logo = discord.File("./images/astolfo.jpg", filename="astolfo.jpg")

    if isinstance(ctx.channel, discord.DMChannel) or (
        isinstance(ctx.channel, discord.TextChannel) and ctx.channel.is_nsfw()
    ):
        response = requests.get(f"{config['API']}/{query}")
        data = response.json()
        status = data.get("Status")

        # error handling
        if response.status_code != 200 or status != 200:
            embed = discord.Embed(
                title="An Error Occurred",
                description="Hey, hey, Master! Something's up, let's go check it out!",
            )
            embed.add_field(name="Internal Server Error", value="500: No femboys found")
            embed.set_thumbnail(url="attachment://astolfo.jpg")
            embed.set_footer(
                text="Made by FireStreaker2",
                icon_url="attachment://gura.png",
            )

            await ctx.respond(embed=embed, files=[pfp, logo])
            return

        image = data.get("URL")
        dimensions = data.get("Dimensions")

        if dimensions == None:
            embed = discord.Embed(
                title="An Error Occurred",
                description="Hey, hey, Master! Something's up, let's go check it out!",
            )
            embed.add_field(name="Internal Server Error", value="500: No femboys found")
            embed.set_thumbnail(url="attachment://astolfo.jpg")
            embed.set_footer(
                text="Made by FireStreaker2",
                icon_url="attachment://gura.png",
            )

            await ctx.respond(embed=embed, files=[pfp, logo])
            return

        embed = discord.Embed(title="Femboy Found!")
        embed.add_field(name="Query", value=query, inline=False)
        embed.add_field(name="Dimensions", value=dimensions, inline=False)
        embed.set_image(url=image)
        embed.set_footer(
            text="Made by FireStreaker2",
            icon_url="attachment://gura.png",
        )

        await ctx.respond(embed=embed, file=pfp)
        global femboys
        femboys += 1

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


@bot.slash_command(description="About FemboyFinderBot")
async def about(ctx):
    await ctx.defer()

    pfp = discord.File("./images/gura.png", filename="gura.png")
    logo = discord.File("./images/astolfo.jpg", filename="astolfo.jpg")

    embed = discord.Embed(
        title="About",
        description="FemboyFinderBot is a bot developed by firestreaker2, using Pycord. It works by querying the Danbooru API for images given the value provided by the end user, and randomly selects one.",
    )
    embed.add_field(
        name="Support Server",
        value="You may join our support server [here](https://discord.gg/bruQhB8Eg5).",
    )
    embed.add_field(
        name="More Resources",
        value="For more info, you may refer to the [GitHub Page](https://github.com/FireStreaker2/FemboyFinderBot).",
        inline=False,
    )
    embed.set_thumbnail(url="attachment://astolfo.jpg")
    embed.set_footer(
        text="Made by FireStreaker2",
        icon_url="attachment://gura.png",
    )

    await ctx.respond(embed=embed, files=[pfp, logo])


@bot.slash_command(description="Bot Statistics")
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
        value=f"I have found {femboys} femboys this month.",
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


@bot.slash_command(description="Send a help message")
async def help(ctx):
    await ctx.defer()

    pfp = discord.File("./images/gura.png", filename="gura.png")
    logo = discord.File("./images/astolfo.jpg", filename="astolfo.jpg")

    embed = discord.Embed(title="Help", description="Help for FemboyFinderBot")
    embed.add_field(name="Prefix", value="``/``", inline=False)
    embed.add_field(
        name="/find [query]",
        value="Find a femboy!\nExample: ``/find astolfo``\n\n> Note that if you are trying to search with a term that has more than one word, use a ``_`` instead of a space.\n> Example: ``/find felix_argyle``",
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
        name="/help", value="Sends this message!\nExamle: ``/help``", inline=False
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


bot.run(config["TOKEN"])

import util.config
import discord
from discord.ext import commands
from database.redis import r


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="stats",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        description="Bot Statistics",
    )
    async def stats(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        embed = (
            discord.Embed(title="Stats")
            .add_field(
                name="Guilds",
                value=f"I am currently in {len(self.bot.guilds)} servers.",
                inline=False,
            )
            .add_field(
                name="Femboys",
                value=f"I have found {int((await r.get('femboys')) or 0)} femboys {'this month' if util.config.MONTHLY_RESET else 'so far'}.",
                inline=False,
            )
            .add_field(
                name="Shard",
                value=f"Shard: {(ctx.guild.shard_id + 1) if ctx.guild else '0'}/{self.bot.shard_count}\nPing: {round(self.bot.latency * 1000)}ms",
                inline=False,
            )
            .set_thumbnail(
                url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg"
            )
            .set_footer(
                text="FemboyFinderBot ❤️",
                icon_url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg",
            )
        )

        await ctx.respond(embed=embed)

    @discord.slash_command(
        name="about",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        description="About FemboyFinderBot",
    )
    async def about(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        embed = (
            discord.Embed(
                title="About",
                description="FemboyFinderBot is a bot developed by firestreaker2, using Pycord. It works by querying the FemboyFinder API for images given the value provided by the end user, and randomly selects one.",
            )
            .add_field(
                name="Support Server",
                value="You may join our support server [here](https://discord.gg/bruQhB8Eg5).",
            )
            .add_field(
                name="More Resources",
                value="For more info, you may refer to the [GitHub Page](https://github.com/FireStreaker2/FemboyFinderBot) or the [FemboyFinder API](https://github.com/FireStreaker2/FemboyFinder).",
                inline=False,
            )
            .set_thumbnail(
                url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg"
            )
            .set_footer(
                text="FemboyFinderBot ❤️",
                icon_url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg",
            )
        )

        await ctx.respond(embed=embed)

    @discord.slash_command(
        name="help",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        description="Send a help message",
    )
    async def help(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        embed = (
            discord.Embed(title="Help", description="Help for FemboyFinderBot")
            .add_field(name="Prefix", value="``/``", inline=False)
            .add_field(
                name="/find [query]",
                value="Find a femboy!\nExample: ``/find *astolfo*``\n\n> If you are trying to search with a term that has more than one word, use a ``_`` instead of a space. If you are searching for multiple tags, then use a space between them. Some tags may be more specific than expected; if so, add a wild card symbol `*` around the term.\n\n> Example: ``/find felix_argyle``\n> Example 2: ``/find *astolfo* stockings``\n\nYou may use all the syntax supported by common image booru sites. For a list, please refer to the [cheatsheet](https://yande.re/help/cheatsheet) or the [list of all tags](https://yande.re/tag)",
                inline=False,
            )
            .add_field(
                name="/about",
                value="Sends the about message.\nExample: ``/about``",
                inline=False,
            )
            .add_field(
                name="/stats",
                value="Sends bot statistics.\nExample: ``/stats``",
                inline=False,
            )
            .add_field(
                name="/help",
                value="Sends this message!\nExample: ``/help``",
                inline=False,
            )
            .add_field(
                name="Support Server",
                value="You may join our support server [here](https://discord.gg/bruQhB8Eg5).",
            )
            .set_thumbnail(
                url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg"
            )
            .set_footer(
                text="FemboyFinderBot ❤️",
                icon_url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg",
            )
        )

        await ctx.respond(embed=embed)

    @discord.slash_command(
        name="ping",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        description="Check the bot's latency",
    )
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"{round(self.bot.latency * 1000)}ms")


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))

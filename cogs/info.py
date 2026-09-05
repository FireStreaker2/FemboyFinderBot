import util.config
import discord
from discord.ext import commands
from util.helpers import add_commands
from util.embeds import base_embed
from util.emojis import emojis
from views.support import SupportView
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
            base_embed(title="Stats")
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
            base_embed(
                title="About",
                description="FemboyFinderBot is a bot developed by firestreaker2, using Pycord. It works by querying the FemboyFinder API for images given the value provided by the end user, and randomly selects one.",
            )
            .add_field(
                name="Support Server",
                value="You may join our support server [here](https://discord.gg/bruQhB8Eg5).",
            )
            .add_field(
                name="More Resources",
                value=f"For more info, you may refer to the [GitHub Page](https://github.com/FireStreaker2/FemboyFinderBot) or the [FemboyFinder API](https://github.com/FireStreaker2/FemboyFinder). Please consider leaving a star to support me! {emojis.get('astolfo_love')}",
                inline=False,
            )
        )

        await ctx.respond(embed=embed, view=SupportView())

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

        embed = base_embed(
            title="Help",
            description="Help for FemboyFinderBot",
        ).add_field(
            name="Prefix",
            value="``/``",
            inline=False,
        )

        add_commands(embed, self.bot.application_commands)

        embed.add_field(
            name="Ratings",
            value=(
                "You may use either the ``rating:`` tag or the rating option "
                "to filter results by rating. The available ratings are:\n"
                "- ``general`` - G-rated content.\n"
                "- ``sensitive`` - Suggestive or mildly erotic content.\n"
                "- ``questionable`` - Softcore erotica.\n"
                "- ``explicit`` - Explicit sexual content.\n\n"
                "Sourced from the [Gelbooru Wiki]"
                "(https://gelbooru.com/index.php?page=wiki&s=view&id=2535)"
            ),
            inline=False,
        ).add_field(
            name="Support Server",
            value=(
                "You may join our support server "
                "[here](https://discord.gg/bruQhB8Eg5)."
            ),
        )

        await ctx.respond(
            embed=embed,
            view=SupportView(),
        )


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))

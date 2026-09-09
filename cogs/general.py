import util.config
import util.helpers
import discord
from discord.ext import commands
from util.autocomplete import booru_autocomplete
from util.embeds import error_embed
from database.redis import r


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="find",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        description="Find a femboy near you!",
    )
    @discord.option(
        "query",
        description="Tags to search for!",
        required=True,
        autocomplete=booru_autocomplete,
    )
    @discord.option(
        "rating",
        description="The rating to search for!",
        required=False,
        choices=[
            discord.OptionChoice(name="General", value="general"),
            discord.OptionChoice(name="Sensitive", value="sensitive"),
            discord.OptionChoice(name="Questionable", value="questionable"),
            discord.OptionChoice(name="Explicit", value="explicit"),
        ],
    )
    async def find(self, ctx: discord.ApplicationContext, query: str, rating=None):
        await ctx.defer()

        if not (
            isinstance(ctx.channel, discord.DMChannel)
            or (isinstance(ctx.channel, discord.TextChannel) and ctx.channel.is_nsfw())
        ):
            embed = error_embed(
                title="Error",
                description=(
                    "This channel is not marked as NSFW. In order to successfully run this command, please mark this channel as NSFW and rerun  this command."
                ),
            )

            await ctx.respond(embed=embed)
            return

        if rating:
            query = f"{query} rating:{rating}"

        try:
            data = await util.helpers.fetch(
                f"{util.config.API}/{query}?provider=danbooru"
            )

        except Exception as error:
            print(f"Error fetching data from API: {error}")

            embed = error_embed(
                title="An Error Occurred",
                description=(
                    "Hey, hey, Master! Something's up, let's go check it out!"
                ),
            ).add_field(
                name="Internal Server Error",
                value="404: No femboys found",
            )

            await ctx.respond(embed=embed)
            return

        image = data["url"]["danbooru"]
        source = data["source"]
        tags = util.helpers.truncate(
            data.get("tags").replace("_", r"\_"),
            1024,
        )

        embed = (
            discord.Embed(
                title="Femboy Found!",
                url=source,
            )
            .add_field(
                name="Query",
                value=query,
                inline=False,
            )
            .add_field(
                name="Tags",
                value=tags,
                inline=False,
            )
            .set_image(url=image)
        )

        view = (
            discord.ui.View()
            .add_item(
                discord.ui.Button(label="Open in Gelbooru", url=data["url"]["gelbooru"])
            )
            .add_item(discord.ui.Button(label="Source", url=source))
        )

        await ctx.respond(embed=embed, view=view)

        if image.lower().endswith((".mp4", ".webm", ".mov", ".avi", ".gif")):
            await ctx.respond(image)

        await r.incr("femboys")


def setup(bot: commands.Bot):
    bot.add_cog(General(bot))

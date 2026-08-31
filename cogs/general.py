import util.config
import util.helpers
import discord
from discord.ext import commands
from io import BytesIO
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
    )
    async def find(self, ctx: discord.ApplicationContext, query: str):
        await ctx.defer()

        if isinstance(ctx.channel, discord.DMChannel) or (
            isinstance(ctx.channel, discord.TextChannel) and ctx.channel.is_nsfw()
        ):
            try:
                data = await util.helpers.fetch(f"{util.config.API}/{query}")

            except:
                embed = (
                    discord.Embed(
                        title="An Error Occurred",
                        description="Hey, hey, Master! Something's up, let's go check it out!",
                    )
                    .add_field(
                        name="Internal Server Error", value="404: No femboys found"
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
                return

            image = data.get("url")
            file = None
            tags = util.helpers.truncate(data.get("tags").replace("_", r"\_"), 1024)
            source = data.get("source")

            if not image.lower().endswith((".mp4", ".webm", ".mov", ".avi")):
                file = discord.File(
                    BytesIO(await util.helpers.fetch(image)), filename="image.jpg"
                )

            embed = (
                discord.Embed(title="Femboy Found!", url=source)
                .add_field(name="Query", value=query, inline=False)
                .add_field(name="Tags", value=tags, inline=False)
                .set_image(url="attachment://image.jpg")
                .set_footer(
                    text="FemboyFinderBot ❤️",
                    icon_url="https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg",
                )
            )

            await ctx.respond(embed=embed, file=file)
            if image.lower().endswith((".mp4", ".webm", ".mov", ".avi")):
                await ctx.respond(image)

            await r.incr("femboys")

        else:
            embed = (
                discord.Embed(
                    title="Error",
                    description="This channel is not marked as NSFW. In order to successfully run this command, please mark this channel as NSFW and rerun this command.",
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
            return


def setup(bot: commands.Bot):
    bot.add_cog(General(bot))

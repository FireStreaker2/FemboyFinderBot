import util.helpers
import discord
from discord.ext import commands
from util.embeds import raw_embed, error_embed
from util.emojis import emojis
from views import HugView, KissView


class Fun(commands.Cog):
    fun = discord.SlashCommandGroup("fun", "Fun roleplay commands for FemboyFinderBot")

    def __init__(self, bot):
        self.bot = bot

    @fun.command(
        name="hug",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        description="Hug a friend!",
    )
    @discord.option(
        "user",
        description="The user to hug!",
        required=True,
    )
    async def hug(self, ctx, user: discord.Member):
        if user == ctx.author:
            embed = error_embed(
                title="Error",
                description=f"You cannot hug yourself! Please hug someone else... {emojis.get('astolfo_shy')}",
            )

            await ctx.respond(embed=embed)
            return

        query = "hug astolfo_(fate) rating:general"
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

        embed = raw_embed(
            title="Hug",
            description=f"{ctx.author.mention} hugs {user.mention}! {emojis.get('astolfo_shy')}",
        ).set_image(url=data["url"]["danbooru"])

        view = HugView(
            author=ctx.author,
            target=user,
            image=data["url"]["danbooru"],
        )

        await ctx.respond(
            embed=embed,
            view=view,
        )

    @fun.command(
        name="kiss",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
        description="Kiss a friend!",
    )
    @discord.option(
        "user",
        description="The user to kiss!",
        required=True,
    )
    async def kiss(self, ctx, user: discord.Member):
        if user == ctx.author:
            embed = error_embed(
                title="Error",
                description=f"You cannot kiss yourself! Please kiss someone else... {emojis.get('astolfo_shy')}",
            )

            await ctx.respond(embed=embed)
            return

        query = "kiss astolfo_(fate) rating:general"
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

        embed = raw_embed(
            title="Kiss",
            description=f"{ctx.author.mention} kisses {user.mention}! {emojis.get('astolfo_shy')}",
        ).set_image(url=data["url"]["danbooru"])

        view = KissView(
            author=ctx.author,
            target=user,
            image=data["url"]["danbooru"],
        )

        await ctx.respond(
            embed=embed,
            view=view,
        )


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))

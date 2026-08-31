import discord
from discord.ext import commands
from util.emojis import emojis


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="hug", description="Hug a friend!")
    async def hug(self, ctx, user: discord.Member):
        if user == ctx.author:
            await ctx.respond("You can't hug yourself!")
            return

        await ctx.respond(
            f"{ctx.author.mention} hugs {user.mention}! {emojis.get('astolfo_shy')}"
        )


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))

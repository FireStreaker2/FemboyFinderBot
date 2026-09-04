import discord
from util.embeds import raw_embed
from util.emojis import emojis


class HugView(discord.ui.View):
    def __init__(self, author: discord.Member, target: discord.Member, image: str):
        super().__init__(timeout=300)
        self.author = author
        self.target = target
        self.image = image

        self.hug_back.emoji = emojis.get("astolfo_shy")

    @discord.ui.button(
        label="Hug Back",
        style=discord.ButtonStyle.primary,
    )
    async def hug_back(
        self,
        button: discord.ui.Button,
        interaction: discord.Interaction,
    ):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message(
                "This button isn't for you!",
                ephemeral=True,
            )
            return

        embed = raw_embed(
            title="Hug",
            description=f"{interaction.user.mention} hugs {self.author.mention} back! {emojis.get('astolfo_shy')}",
        ).set_image(url=self.image)

        await interaction.response.edit_message(
            embed=embed,
            view=None,
        )

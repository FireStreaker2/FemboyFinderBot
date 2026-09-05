import discord
from util.embeds import raw_embed
from util.emojis import emojis


class TemplateView(discord.ui.View):
    def __init__(
        self,
        author: discord.Member,
        target: discord.Member,
        title: str,
        image: str | None,
        button_label: str,
        button_emoji: str,
        action_description: str,
        response_description: str,
    ):
        super().__init__(timeout=300)

        self.author = author
        self.target = target
        self.title = title
        self.image = image
        self.action_description = action_description
        self.response_description = response_description

        self.action_button.label = button_label
        self.action_button.emoji = emojis.get(button_emoji)

    @discord.ui.button(
        label="Action",
        style=discord.ButtonStyle.primary,
    )
    async def action_button(
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
            title=self.title,
            description=self.response_description.format(
                author=self.author.mention,
                target=interaction.user.mention,
            ),
        )

        if self.image:
            embed.set_image(url=self.image)

        await interaction.response.edit_message(
            embed=embed,
            view=None,
        )

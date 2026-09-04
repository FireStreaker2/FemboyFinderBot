import discord
from util.emojis import emojis


class SupportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.Button(
                label="Join Discord",
                emoji=emojis.get("felix_peek"),
                style=discord.ButtonStyle.link,
                url="https://discord.gg/bruQhB8Eg5",
            )
        )

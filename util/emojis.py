import discord


class EmojiManager:
    def __init__(self):
        self.emojis: dict[str, discord.Emoji] = {}

    async def load(self, bot: discord.Bot):
        app_emojis = await bot.fetch_emojis()

        self.emojis = {
            emoji.name: emoji for emoji in app_emojis if emoji.name is not None
        }

        print(f"Loaded {len(self.emojis)} application emojis.")

    def get(self, name: str) -> discord.Emoji:
        try:
            return self.emojis[name]
        except KeyError:
            raise KeyError(f"Application emoji '{name}' was not found.")

    def __getitem__(self, name: str) -> discord.Emoji:
        return self.get(name)

    def __contains__(self, name: str) -> bool:
        return name in self.emojis


emojis = EmojiManager()

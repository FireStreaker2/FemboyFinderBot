from discord import Embed, Color

THUMBNAIL_URL = "https://raw.githubusercontent.com/FireStreaker2/FemboyFinderBot/refs/heads/main/images/astolfo.jpg"
FOOTER_TEXT = "FemboyFinderBot ❤️"


def base_embed(**kwargs):
    embed = Embed(**kwargs)

    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_footer(
        text=FOOTER_TEXT,
        icon_url=THUMBNAIL_URL,
    )

    return embed


def error_embed(**kwargs):
    return base_embed(
        color=Color.red(),
        **kwargs,
    )

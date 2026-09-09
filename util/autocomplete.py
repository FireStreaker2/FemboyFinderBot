import discord
from urllib.parse import urlencode
from util.helpers import fetch


async def booru_autocomplete(ctx: discord.AutocompleteContext) -> list[str]:
    query = ctx.value
    current_tag = query.rsplit(" ", 1)[-1]

    if len(current_tag) < 2:
        return []

    url = "https://danbooru.donmai.us/autocomplete.json?" + urlencode(
        {
            "search[query]": current_tag,
            "search[type]": "tag_query",
            "version": "3",
            "limit": 20,
        }
    )

    try:
        data = await fetch(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "FemboyFinderBot/1.0",
            },
        )

        if not isinstance(data, list):
            return []

        prefix = query[: query.rfind(" ") + 1] if " " in query else ""
        suggestions = []

        for tag in data:
            value = tag.get("label") or tag.get("value")

            if not value:
                continue

            value = value.replace(" ", "_")
            suggestions.append(prefix + value)

        return suggestions[:25]

    except Exception:
        return []

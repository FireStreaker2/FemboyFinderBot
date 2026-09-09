import discord
import aiohttp


async def booru_autocomplete(ctx: discord.AutocompleteContext) -> list[str]:
    query = ctx.value
    current_tag = query.rsplit(" ", 1)[-1]

    if len(current_tag) < 2:
        return []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://danbooru.donmai.us/autocomplete.json",
                params={
                    "search[query]": current_tag,
                    "search[type]": "tag_query",
                    "version": "3",
                    "limit": 20,
                },
                headers={
                    "Accept": "application/json",
                    "User-Agent": "FemboyFinderBot/1.0",
                },
                timeout=aiohttp.ClientTimeout(total=2),
            ) as response:

                if response.status != 200:
                    return []

                data = await response.json(content_type=None)

        prefix = query[: query.rfind(" ") + 1] if " " in query else ""
        suggestions = []

        for tag in data:
            value = tag.get("label") or tag.get("value")

            if not value:
                continue

            value = value.replace(" ", "_")
            suggestions.append(prefix + value)

        return suggestions[:25]

    except (aiohttp.ClientError, TimeoutError):
        return []

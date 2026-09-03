from aiohttp import ClientSession


async def fetch(url: str):
    async with ClientSession() as session:
        headers = {
            "Referer": "https://gelbooru.com/",
        }

        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                content = response.headers.get("Content-Type", "")
                if "application/json" in content:
                    return await response.json()

                elif content.startswith("image/"):
                    return await response.read()

                else:
                    return await response.text()
            else:
                print(response.status)
                response.raise_for_status()


def truncate(text: str, max_length: int):
    if len(text) <= max_length:
        return text

    truncated = text[: max_length - 3]
    last = truncated.rfind(" ")

    if last == -1:
        return truncated + "..."

    return truncated[:last] + "..."

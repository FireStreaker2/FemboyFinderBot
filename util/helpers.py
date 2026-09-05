import discord
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


def add_commands(embed: discord.Embed, commands: list, prefix: str = ""):
    descriptions = {
        "find": (
            "Find a femboy!\n\n"
            "> If you are trying to search with a term that has more than one "
            "word, use a ``_`` instead of a space. If you are searching for "
            "multiple tags, then use a space between them. Some tags may be "
            "more specific than expected; if so, add a wild card symbol `*` "
            "around the term.\n\n"
            "> Example: ``/find felix_argyle``\n"
            "> Example 2: ``/find *astolfo* stockings``\n\n"
            "You may use all the syntax supported by common image booru "
            "sites. For a list, please refer to the "
            "[cheatsheet](https://gelbooru.com/index.php?page=help&topic=cheatsheet) or the "
            "[list of all tags](https://gelbooru.com/index.php?page=tags&s=list)"
        ),
    }

    for command in sorted(commands, key=lambda command: command.name):
        name = f"{prefix}{command.name}"

        if isinstance(command, discord.SlashCommandGroup):
            add_commands(
                embed,
                command.subcommands,
                prefix=f"{name} ",
            )
            continue

        command_id = command.parent.id if command.parent else command.id
        parameters = []
        for option in command.options:
            if option.required:
                parameters.append(f"<{option.name}>")

            else:
                parameters.append(f"[{option.name}]")

        command_name = f"</{name}:{command_id}>"
        if parameters:
            command_name += " " + " ".join(parameters)

        embed.add_field(
            name=command_name,
            value=descriptions.get(
                command.name,
                command.description or "No description provided.",
            ),
            inline=False,
        )

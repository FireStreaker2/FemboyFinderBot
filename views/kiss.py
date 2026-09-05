from discord import Member
from util.emojis import emojis
from views.template import TemplateView


class KissView(TemplateView):
    def __init__(
        self,
        author: Member,
        target: Member,
        image: str | None = None,
    ):
        super().__init__(
            author=author,
            target=target,
            title="Kiss",
            image=image,
            button_label="Kiss Back",
            button_emoji="astolfo_shy",
            action_description="kisses",
            response_description=(
                "{target} kisses {author} back! " f"{emojis.get('astolfo_shy')}"
            ),
        )

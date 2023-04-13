import solara
from solara.alias import rv
import re
from ...components.story_card import StoryCard


@solara.component
def Page():
    with rv.ItemGroup() as main:
        with rv.Container():
            with rv.Row():

                for i in range(3):
                    with rv.Col(md=4):
                        with rv.Item():
                            StoryCard()

    return main
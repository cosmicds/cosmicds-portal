import re

import solara
from solara.alias import rv
from solara_enterprise import auth

from ...components.class_text_field import ClassTextField
from ...components.story_card import StoryCard


@solara.component
def Page():
    if not auth.user.value:
        solara.Markdown("Please login before creating a class.")
    else:
        rv.Html(tag="div", children=["Create Class"], class_="display-1")

        data, set_data = solara.use_state([])

        ClassTextField(data, set_data)

        rv.DataTable(
            items=data,
            headers=[
                {
                    "text": "Name",
                    "align": "start",
                    "sortable": True,
                    "value": "name",
                },
                {"text": "Code", "value": "code"},
                {"text": "Actions", "value": "actions", "align": "end"},
            ],
            v_slots=[
                {
                    "name": "item.actions",
                    "variable": "x",
                    "children": solara.Button(
                        small=True,
                        icon_name="delete",
                        icon=True,
                        on_click=lambda *args: print(args),
                        # v_on="x.item",
                        # v_bind="x.item",

                    ),
                }
            ],
        )

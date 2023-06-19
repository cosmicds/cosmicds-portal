from pathlib import Path

import shortuuid
import solara
from solara.alias import rv


@solara.component
def ClassTextField(state, state_callback):
    text, set_text = solara.use_state("")

    text_field = rv.TextField(
        label="Class name",
        outlined=True,
        required=True,
        append_outer_icon="add",
        v_model=text,
        on_v_model=set_text
    )
    rv.use_event(
        text_field,
        "click:append-outer",
        lambda *args: state_callback(
            state
            + [
                {
                    "name": f"{text}",
                    "code": f"{shortuuid.uuid()}",
                }
            ]
        ),
    )

    return text_field

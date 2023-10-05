import solara
from solara.alias import rv

from ... import state
from ...database import get_student_classes, add_student_to_class


@solara.component
def JoinTextField(code, set_code, callback):
    text_field = rv.TextField(label="Class Code", v_model=code,
                              on_v_model=set_code,
                              outlined=True, append_outer_icon="add", )
    rv.use_event(
        text_field,
        "click:append-outer",
        callback,
    )


@solara.component
def ClassStoryCard(title, text, date):
    with rv.Card(max_width=400, class_="mx-auto") as story_card:
        with rv.Img(class_="white--text align-end", height="150px",
                    src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"):
            rv.CardTitle(children=[f"{title}"])

        with rv.CardTitle():
            solara.Text(f"{text}")

        with rv.CardSubtitle():
            solara.Text(f"{date}")

        # with rv.CardText():
        #     solara.Text(f"{text}")

        with rv.CardActions():
            solara.Button("Leave", color="error", text=True)
            rv.Spacer()
            solara.Button("Open", elevation=0)

    return story_card


@solara.component
def Page():
    solara.Text("Join Class", classes=["display-1"])

    code, set_code = solara.use_state("")
    classes, set_classes = solara.use_state([])

    def _update_classes():
        student_classes = get_student_classes(state.user_info['username'])

        if student_classes is not None:
            set_classes(student_classes)

    _update_classes()

    def _add_button_clicked(*args):
        add_student_to_class(state.user_info['username'], code)
        _update_classes()

    JoinTextField(code, set_code, _add_button_clicked)

    with solara.ColumnsResponsive([3]):
        for cls in classes:
            ClassStoryCard(cls['name'], cls['stories'], cls['date'])

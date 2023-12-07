import solara
from solara.alias import rv
import httpx
from ...utils import CDS_API_URL

from ..state import GLOBAL_STATE


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

        rv.Divider()
        with rv.CardActions():
            rv.Spacer()
            solara.Button("Leave", color="error", text=True)
            solara.Button("Open", elevation=0)

    return story_card


@solara.component
def Page():
    router = solara.use_router()

    if not GLOBAL_STATE.user.exists():
        router.push(f"/")
        return

    solara.Text("Join Class", classes=["display-1"])

    code, set_code = solara.use_state("")
    classes, set_classes = solara.use_state([])

    def _update_classes():
        r = httpx.get(
            f"{CDS_API_URL}/students/{GLOBAL_STATE.user.username.value}/classes")

        if r.json() is not None:
            set_classes(r.json())

    _update_classes()

    def _add_button_clicked(*args):
        r = httpx.post(
            f"${CDS_API_URL}/classes/join",
            params={'username': GLOBAL_STATE.user.username.value,
                    'class_code': code})

        _update_classes()

    JoinTextField(code, set_code, _add_button_clicked)

    with solara.ColumnsResponsive([3]):
        for cls in classes:
            ClassStoryCard(cls['name'], cls['stories'], cls['date'])

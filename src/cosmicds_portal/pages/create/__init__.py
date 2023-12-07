from datetime import date

import shortuuid
import solara
from solara.alias import rv
import httpx
from ...utils import CDS_API_URL

from ..state import GLOBAL_STATE


@solara.component
def AddClassDialog(callback, **btn_kwargs):
    active, set_active = solara.use_state(False)  #
    text, set_text = solara.use_state("")
    stories, set_stories = solara.use_state([])

    with rv.Dialog(
            v_model=active,
            on_v_model=set_active,
            v_slots=[{"name": "activator", "variable": "x",
                      "children": rv.Btn(v_on="x.on", v_bind="x.attrs",
                                         children=["Add"], elevation=0,
                                         **btn_kwargs)}],
            max_width=600,
    ) as dialog:
        with rv.Card(outlined=True):
            with rv.CardTitle():
                rv.Html(tag="text-h5", children=["Add Class"])

            with rv.CardText():
                rv.TextField(
                    label="Class name",
                    outlined=True,
                    required=True,
                    v_model=text,
                    on_v_model=set_text
                )

                rv.Select(v_model=stories,
                          outlined=True,
                          on_v_model=set_stories,
                          label="Data Stories",
                          items=["Hubble"],
                          multiple=True
                          )

            rv.Divider()

            with rv.CardActions():
                def _add_button_clicked(*args):
                    callback({
                        "name": f"{text}",
                        "date": f"{date.today()}",
                        "stories": f"{', '.join(stories)}",
                        "code": f"{shortuuid.uuid()}",
                    })
                    set_active(False)

                rv.Spacer()

                solara.Button("Cancel",
                              on_click=lambda *args: set_active(False),
                              elevation=0)
                solara.Button("Add", color="success",
                              on_click=_add_button_clicked, elevation=0)

    return dialog


@solara.component
def Page():
    router = solara.use_router()

    if not GLOBAL_STATE.user.exists():
        router.push(f"/")
        return

    solara.Text("Create Class", classes=["display-1"])

    data, set_data = solara.use_state([])
    selected_rows, set_selected_rows = solara.use_state([])

    def _update_data():
        r = httpx.get(
            f"{CDS_API_URL}/educators/{GLOBAL_STATE.user.username.value}/classes")

        set_data(r.json())

    _update_data()

    def _delete_button_clicked(*args):
        for row in selected_rows:
            r = httpx.delete(
                f"{CDS_API_URL}/classes/{row['code']}")

        _update_data()

    def _create_class_callback(item):
        r = httpx.post(
            f"{CDS_API_URL}/classes/create",
            json=item,
            params={'username': GLOBAL_STATE.user.username.value})

        _update_data()

    rv.DataTable(
        items=data,
        single_select=False,
        show_select=True,
        v_model=selected_rows,
        on_v_model=set_selected_rows,
        headers=[
            {
                "text": "Name",
                "align": "start",
                "sortable": True,
                "value": "name",
            },
            {"text": "Date", "value": "date"},
            {"text": "Stories", "value": "stories"},
            {"text": "Code", "value": "code"},
            # {"text": "Actions", "value": "actions", "align": "end"},
        ],
        v_slots=[
            {
                "name": "body.append",
                "variable": "x",
                "children": [
                    rv.Row(style_="min-width: 200px", class_="ma-2",
                           children=[AddClassDialog(_create_class_callback),
                                     solara.Button("Delete", elevation=0,
                                                   on_click=_delete_button_clicked,
                                                   color="error",
                                                   classes=["mx-2"])])
                ],
            }
        ],
    )

import solara
from solara.alias import rv
# from ..server import manager


@solara.component
def Login(**btn_kwargs):
    active, set_active = solara.use_state(False)

    with rv.Dialog(
            v_model=active,
            on_v_model=set_active,
            v_slots=[{"name": "activator", "variable": "x",
                      "children": rv.Btn(v_on="x.on", v_bind="x.attrs",
                                         children=["Login"], **btn_kwargs)}],
            max_width=600,
    ) as login:
        with rv.Card():
            # user = await manager.get_current_user(
            #     token=request.cookies.get('token'))
            # rv.Html(tag='div', children=[f"{user}"])

            with rv.CardTitle():
                rv.Html(tag="text-h5", children=["Login"])

            with rv.CardText():
                with rv.Container():
                    rv.Html(tag='div', children=[f"Is active? {active}"])
                    with rv.Row():
                        with rv.Col(cols=12):
                            rv.TextField(label="Username")
                        with rv.Col(cols=12):
                            rv.TextField(label="Password")

            with rv.CardActions():
                rv.Spacer()

                close_btn = rv.Btn(children=["Close"], text=True)
                rv.use_event(close_btn, 'click',
                             lambda *args: set_active(False))

                save_btn = rv.Btn(children=["Save"], text=True)
                rv.use_event(save_btn, 'click', lambda *args: set_active(True))

    return login

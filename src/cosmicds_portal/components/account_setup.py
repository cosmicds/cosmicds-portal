import solara
from solara.alias import rv
from .educator_request_form import EducatorRequestForm


# from ..server import manager


@solara.component
def AccountSetup(**btn_kwargs):
    active, set_active = solara.use_state(False)
    step, set_step = solara.use_state(1)

    with rv.Dialog(
            v_model=active,
            on_v_model=set_active,
            v_slots=[{"name": "activator", "variable": "x",
                      "children": rv.Btn(v_on="x.on", v_bind="x.attrs",
                                         children=["Setup"], **btn_kwargs)}],
            max_width=800,
    ) as setup:
        with rv.Card():
            # user = await manager.get_current_user(
            #     token=request.cookies.get('token'))
            # rv.Html(tag='div', children=[f"{user}"])

            with rv.Stepper(v_model=step, on_v_model=set_step):
                with rv.StepperStep(step=1):
                    solara.Text("Level")

                with rv.StepperContent(step=1):
                    with rv.Card(style="flex: 1", to="https://google.com"):
                        with rv.CardTitle():
                            solara.Text("Educator!")

                        solara.Text("I am an educator")
                    with solara.Card(title="Student", style="flex: 1"):
                        solara.Text("I am a student")

                    solara.Button(label="Cancel", text=True)
                    solara.Button(label="Continue",
                                  on_click=lambda: set_step(step + 1))

                with rv.StepperStep(step=2):
                    solara.Text("Request")

                with rv.StepperContent(step=2):
                    EducatorRequestForm()

    return setup

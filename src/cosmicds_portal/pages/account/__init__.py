import re

import solara
from solara.alias import rv
from solara_enterprise import auth
from ...database import check_user_type_defined
from ... import state
from ...components.account_setup import AccountSetup
from ...components.educator_request_form import EducatorRequestForm


@solara.component
def Page():
    step, set_step = solara.use_state(1)
    level = solara.reactive(0)  # 0 - undefined, 1 - educator, 2 - student
    request_submitted = solara.reactive(False)
    user_info = auth.user.value["userinfo"]

    if not check_user_type_defined(user_info['name']):
        solara.Text("Account Setup",
                    classes=["display-1", "pb-4"])

        with rv.Stepper(v_model=step, on_v_model=set_step, flat=True,
                        elevation=0, outlined=True, non_linear=True,
                        class_="elevation-0 border-1 ma-0 pa-0"):
            with rv.StepperHeader(class_="elevation-0"):
                with rv.StepperStep(step=1, complete=step > 1):
                    solara.Text("Level")

                rv.Divider()

                with rv.StepperStep(step=2, complete=step > 2):
                    solara.Text("Request")

                rv.Divider()

                with rv.StepperStep(step=3, complete=step > 3):
                    solara.Text("Finalize")

            with rv.StepperContent(step=1):
                with solara.ColumnsResponsive([1, 1]):
                    with rv.Card(style_="flex: 1",
                                 flat=True,
                                 outlined=True):
                        with rv.CardTitle():
                            solara.Text("Educator")

                        with rv.CardText():
                            solara.Text("I am an educator")

                        with rv.CardActions():
                            def _click_educator():
                                set_step(step + 1)
                                level = 1

                            solara.Button(label="Cancel", text=True)
                            solara.Button(label="Continue", elevation=0,
                                          color="success",
                                          on_click=_click_educator)
                    with rv.Card(style_="flex: 1",
                                 flat=True,
                                 outlined=True):
                        with rv.CardTitle():
                            solara.Text("Student")

                        with rv.CardText():
                            solara.Text("I am a student")

                        with rv.CardActions():
                            def _click_student():
                                set_step(step + 2)
                                level = 2

                            solara.Button(label="Cancel", text=True)
                            solara.Button(label="Continue", elevation=0,
                                          color="primary",
                                          on_click=_click_student)

            with rv.StepperContent(step=2):
                with solara.Card(title="Account request form", style="flex: 1",
                                 elevation=0):
                    EducatorRequestForm()

                    rv.Divider()

                    with solara.CardActions():
                        solara.Button(label="Back", text=True,
                                      on_click=lambda: set_step(step - 1))
                        solara.Button(label="Continue", elevation=0,
                                      disabled=not request_submitted.value,
                                      on_click=lambda: set_step(
                                          step + 1))

            with rv.StepperContent(step=3):
                with solara.Card(title="Finalize", style="flex: 1",
                                 elevation=0):
                    rv.Divider()

                    with solara.CardActions():
                        solara.Button(label="Back", text=True,
                                      on_click=lambda: set_step(step - 1))
                        solara.Button(label="Continue", elevation=0)
    else:
        solara.Markdown("DEFINED!?")

    # with solara.GridLayout():
    # for k, v in user_info.items():
    #     solara.Text(f"{k}")
    #     solara.Text(f"{v}")

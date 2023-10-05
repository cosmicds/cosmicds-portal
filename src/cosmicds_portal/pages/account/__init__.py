import solara
from solara.alias import rv
from solara_enterprise import auth

from ... import state
from ...components.educator_request_form import EducatorRequestForm
from ...database import create_educator, create_student


@solara.component
def Page():
    step, set_step = solara.use_state(1)
    level, set_level = solara.use_state(
        0)  # 0 - undefined, 1 - educator, 2 - student
    user_info = auth.user.value["userinfo"]

    stu_form_data, set_stu_form_data = solara.use_state({
        "username": ""
    })

    set_stu_form_data({'username': user_info['name']})

    edu_form_data, set_edu_form_data = solara.use_state({
        "valid": False,
        "verified": False,
        "username": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "confirm_email": "",
        "school_name": "",
        "school_zip": "",
        "grade_levels": [],
        "classes_taught": "",
    })

    set_edu_form_data({**edu_form_data, 'username': user_info['name']})

    if state.user_info is None:
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
                with solara.Card(title="Access level", style="flex: 1",
                                 elevation=0):
                    with solara.ColumnsResponsive([1, 1]):
                        with rv.Card(style_="flex: 1",
                                     flat=True,
                                     outlined=True):
                            with rv.CardTitle():
                                solara.Checkbox(
                                    value=level == 1,
                                    on_value=lambda e: set_level(
                                        1 if e else 0))
                                solara.Text("Educator")

                            with rv.CardText():
                                solara.Text("I am an educator")
                        with rv.Card(style_="flex: 1",
                                     flat=True,
                                     outlined=True):
                            with rv.CardTitle():
                                solara.Checkbox(
                                    value=level == 2,
                                    on_value=lambda e: set_level(
                                        2 if e else 0))
                                solara.Text("Student")

                            with rv.CardText():
                                solara.Text("I am a student")

                    # rv.Divider()

                    with solara.CardActions():
                        solara.Button(label="Continue", elevation=0,
                                      disabled=level == 0,
                                      on_click=lambda: set_step(
                                          step + level))

            with rv.StepperContent(step=2):
                with solara.Card(title="Account request form", style="flex: 1",
                                 elevation=0):
                    EducatorRequestForm(edu_form_data, set_edu_form_data)

                    # rv.Divider()

                    with solara.CardActions():
                        solara.Button(label="Back", text=True,
                                      on_click=lambda: set_step(step - 1))
                        solara.Button(label="Continue", elevation=0,
                                      disabled=not edu_form_data['valid'],
                                      on_click=lambda: set_step(
                                          step + 1))

            with rv.StepperContent(step=3):
                with solara.Card(title="Finalize", style="flex: 1",
                                 elevation=0):
                    rv.Alert(color="warning", border="left", outlined=True,
                             children=[
                                 f"You have selected a{' STUDENT' if level == 2 else 'n EDUCATOR'} account."])

                    def _submit_form():
                        if level == 1:
                            result = create_educator(
                                {**edu_form_data})
                        elif level == 2:
                            result = create_student({**stu_form_data})

                        print(result)

                        if result['ok']:
                            rv.Alert(color="success",
                                     children=[
                                         "Account setup successfully completed"])
                        else:
                            rv.Alert(color="error",
                                     children=[result['error']])

                    with solara.CardActions():
                        solara.Button(label="Back", text=True,
                                      on_click=lambda: set_step(step - level))
                        solara.Button(label="Submit", elevation=0,
                                      on_click=_submit_form)
    else:
        solara.Text("Account", classes=["display-1"])

        solara.Text(f"{state.user_info}")

        with solara.GridLayout():
            for k, v in state.user_info.items():
                solara.Text("HERE")
                # print(k, v)
                # solara.Text(f"{k}")
                # solara.Text(f"{v}")

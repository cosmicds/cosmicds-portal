import solara
from solara.alias import rv
import httpx
from typing import Callable
import solara.lab
import time

from ...utils import CDS_API_URL

from ..state import GLOBAL_STATE
from ...components.educator_request_form import EducatorRequestForm


def use_interval(f: Callable, interval: float = 10.0, enabled=True):
    def run():
        if enabled:
            time_start = time.time()
            next_tick = time_start + interval

            while True:
                f()
                time.sleep(max(0, next_tick - time.time()))
                next_tick += interval

    return solara.use_thread(run, dependencies=[interval, enabled])


@solara.component
def Page():
    router = solara.use_router()

    if not GLOBAL_STATE.user.exists():
        router.push(f"/")
        return
    elif GLOBAL_STATE.user.setup_completed.value:
        router.push(f"/account")
        return

    count = solara.use_reactive(3)
    confirmed = solara.use_reactive(False)

    step, set_step = solara.use_state(1)

    # 0 - undefined, 1 - educator, 2 - student
    level, set_level = solara.use_state(0)

    stu_form_data, set_stu_form_data = solara.use_state({
        "username": ""
    })

    set_stu_form_data({'username': GLOBAL_STATE.user.username.value})

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

    set_edu_form_data(
        {**edu_form_data, 'username': GLOBAL_STATE.user.username.value})

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
                        payload = {**edu_form_data}
                        payload['grade_levels'] = ','.join(
                            payload['grade_levels'])
                        del payload['valid']
                        del payload['confirm_email']

                        r = httpx.post(
                            f"{CDS_API_URL}/educators/create",
                            json=payload)
                    elif level == 2:
                        payload = {**stu_form_data}

                        r = httpx.post(
                            f"{CDS_API_URL}/students/create",
                            json=payload)

                    if r.status_code == 200:
                        confirmed.set(True)

                with solara.CardActions():
                    solara.Button(label="Back", text=True,
                                  on_click=lambda: set_step(step - level))
                    solara.Button(label="Submit", elevation=0,
                                  on_click=lambda: _submit_form())

    def _count_down():
        if count.value > 0:
            count.value -= 1
        else:
            router.push(f"/")

    use_interval(_count_down, interval=1, enabled=confirmed.value)

    with solara.v.Dialog(
            v_model=confirmed.value,
            on_v_model=confirmed.set,
            persistent=True,
            max_width=500,
    ) as confirm_dialog:

        with solara.v.Card():
            with solara.v.Alert(text=True, color="info", class_="ma-0"):
                with solara.v.Row(align="center", no_gutters=True):
                    with solara.v.Col(class_="grow"):
                        solara.Text(
                            "Setup completed successfully, redirecting...")
                    # solara.v.Spacer()
                    with solara.v.Col(class_="shrink"):
                        solara.v.ProgressCircular(indeterminate=True)

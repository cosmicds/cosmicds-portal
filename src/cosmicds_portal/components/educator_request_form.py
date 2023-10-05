import solara
from solara.alias import rv


@solara.component
def EducatorRequestForm(form_data, set_form_data):
    submitted, set_submitted = solara.use_state(False)

    if submitted:
        rv.Alert(children=[
            f"Form submitted successfully. You will receive a notification at "
            f"{form_data['email']} when your account has been verified."],
            type="success")

    def _update_form_data(new_data):
        set_form_data({**new_data, 'valid': all(
            [x is True for y in rules.values() for x in y])})

    rules = {
        "first_name": [
            len(form_data[
                    "first_name"]) > 3 or "Must be more than 2 characters"
        ],
        "last_name": [
            len(form_data[
                    "first_name"]) > 3 or "Must be more than 2 characters"
        ],
        "email": [
            len(form_data['email']) > 0 or "Must enter an email"
        ],
        "confirm_email": [
            form_data['email'] == form_data[
                'confirm_email'] or "Emails must match"
        ],
        "school_name": [
            len(form_data['school_name']) > 0 or "Must enter an school name"
        ],
        "school_zip": [
            len(form_data['school_zip']) > 0 or "Must enter an school zip"
        ],
        "grade_levels": [
            len(form_data['grade_levels']) > 0 or "Must select grade levels"
        ],
        "classes_taught": [
            len(form_data[
                    'classes_taught']) > 0 or "Must enter an classes taught"
        ],
    }
    with rv.Card(outlined=True, disabled=submitted):
        with rv.CardText():
            with solara.Row():
                rv.TextField(
                    v_model=form_data["first_name"],
                    on_v_model=lambda x: _update_form_data(
                        {**form_data, 'first_name': x}),
                    label="First name",
                    rules=rules.get('first_name'),
                    filled=True,
                    required=True)
                rv.TextField(v_model=form_data['last_name'],
                             on_v_model=lambda x: _update_form_data(
                                 {**form_data, 'last_name': x}),
                             label="Last name",
                             rules=rules.get('last_name'),
                             filled=True,
                             required=True)
            rv.TextField(v_model=form_data['email'],
                         on_v_model=lambda x: _update_form_data(
                             {**form_data, 'email': x}),
                         label="Email",
                         rules=rules.get('email'),
                         filled=True,
                         required=True)
            rv.TextField(v_model=form_data['confirm_email'],
                         on_v_model=lambda x: _update_form_data(
                             {**form_data, 'confirm_email': x}),
                         label="Confirm email",
                         rules=rules.get('confirm_email'),
                         filled=True,
                         required=True)
            rv.TextField(v_model=form_data['school_name'],
                         on_v_model=lambda x: _update_form_data(
                             {**form_data, 'school_name': x}),
                         label="School name",
                         rules=rules.get('school_name'),
                         filled=True,
                         required=True)
            rv.TextField(v_model=form_data['school_zip'],
                         on_v_model=lambda x: _update_form_data(
                             {**form_data, 'school_zip': x}),
                         label="School zip code",
                         rules=rules.get('school_zip'),
                         filled=True,
                         required=True)
            rv.Select(v_model=form_data["grade_levels"],
                      on_v_model=lambda x: _update_form_data(
                          {**form_data, 'grade_levels': x}),
                      label="Grade levels taught",
                      items=["Elementary", "Middle School", "High School",
                             "Undergraduate", "Graduate"],
                      rules=rules.get('grade_levels'),
                      filled=True,
                      multiple=True
                      )
            rv.TextField(v_model=form_data['classes_taught'],
                         on_v_model=lambda x: _update_form_data(
                             {**form_data, 'classes_taught': x}),
                         label="Classes taught",
                         rules=rules.get('classes_taught'),
                         filled=True,
                         required=True)

    solara.Markdown(f"{form_data}")

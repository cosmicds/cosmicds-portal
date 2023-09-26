import re

import solara
from solara.alias import rv
from solara_enterprise import auth


@solara.component
def EducatorRequestForm():
    valid, set_valid = solara.use_state({
        "valid": False,
        "first_name": "",
        "last_name": "",
        "email": "",
        "confirm_email": "",
        "school_name": "",
        "school_zip": None,
        "grade_levels": [],
        "classes": [],
    })

    with rv.Form(v_model=valid["valid"], on_v_model=lambda x: set_valid(
            {**valid, 'valid': x})) as main:
        with rv.Card(outlined=True):
            with rv.CardText():
                with solara.Row():
                    rv.TextField(v_model=valid["first_name"],
                                 on_v_model=lambda x: set_valid(
                                     {**valid, 'first_name': x}),
                                 label="First name",
                                 required=True)
                    rv.TextField(v_model=valid['last_name'],
                                 on_v_model=lambda x: set_valid(
                                     {**valid, 'last_name': x}),
                                 label="Last name",
                                 required=True)
                rv.TextField(v_model=valid['email'],
                             on_v_model=lambda x: set_valid(
                                 {**valid, 'email': x}),
                             label="Email",
                             required=True)
                rv.TextField(v_model=valid['confirm_email'],
                             on_v_model=lambda x: set_valid(
                                 {**valid, 'confirm_email': x}),
                             label="Confirm email",
                             required=True)
                rv.TextField(v_model=valid['school_name'],
                             on_v_model=lambda x: set_valid(
                                 {**valid, 'school_name': x}),
                             label="School name",
                             required=True)
                rv.TextField(v_model=valid['school_zip'],
                             on_v_model=lambda x: set_valid(
                                 {**valid, 'school_zip': x}),
                             label="School zip code",
                             required=True)
                rv.Select(v_model=valid["grade_levels"],
                          on_v_model=lambda x: set_valid(
                              {**valid, 'grade_levels': x}),
                          label="Grade levels taught",
                          items=["Elementary", "Middle School", "High School",
                                 "Undergraduate", "Graduate"],
                          multiple=True
                          )
                rv.TextField(v_model=valid['classes'],
                             on_v_model=lambda x: set_valid(
                                 {**valid, 'classes': x}),
                             label="Classes taught",
                             required=True)

            rv.Divider()
            with rv.CardActions():
                rv.Spacer()
                solara.Button("Clear", text=True)
                solara.Button("Submit", elevation=0, color="success")

        solara.Markdown(f"{valid}")

    return main

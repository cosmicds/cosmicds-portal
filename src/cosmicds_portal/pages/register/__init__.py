import re

import solara
from solara.alias import rv
from solara_enterprise import auth


@solara.component
def Page():
    if not auth.user.value:
        solara.Button("DO IT", icon_name="mdi-logon", href=auth.get_login_url())
    else:
        user_info = auth.user.value["userinfo"]
        
        if "name" in user_info:
            solara.Markdown(f"### Welcome {user_info['name']}")
        solara.Button("Logout", icon_name="mdi-logout", href=auth.get_logout_url())
    # valid, set_valid = solara.use_state({
    #   "valid": False,
    #   "firstname": "",
    #   "lastname": "",
    #   "nameRules": [
    #     lambda v: v or 'Name is required',
    #     lambda v: len(v) <= 10 or 'Name must be less than 10 characters',
    #   ],
    #   "email": "",
    #   "emailRules": [
    #     lambda v: v or 'E-mail is required',
    #     lambda v: re.match("/.+@.+/", v) or 'E-mail must be valid',
    #   ],
    # })

    # with rv.Form() as main:
    #     rv.Html(tag='div', children=['Create an Account'], class_="display-1")

    #     with rv.Container():
    #         with rv.Row():
    #             with rv.Col(cols=12):
    #                 rv.TextField(v_model=valid['firstname'],
    #                              #rules=valid['nameRules'],
    #                              counter="10",
    #                              label="First name",
    #                              required=True)

    # return main

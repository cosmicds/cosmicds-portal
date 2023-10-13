from pathlib import Path

import ipyvuetify as v
import solara
from solara.alias import rv
from solara_enterprise import auth
import httpx

from .state import user

v.theme.dark = True

IMG_PATH = Path("static") / "public" / "images"


@solara.component
def Hero():
    with rv.Parallax(src=str(IMG_PATH / "opo0006a.jpg")) as hero:
        with rv.Container():
            with rv.Row():
                with rv.Col(cols=6):
                    # with rv.Container():
                    rv.Html(tag="div", children=["Cosmic Data Stories"],
                            class_="display-4")
                    rv.Html(tag="div", children=[
                        "Interactive data stories designed by NASA "
                        "astronomers to inspire learners of all ages "
                        "to explore the universe."], class_="display-1")

    return hero


@solara.component
def Page():
    with solara.Row(classes=['fill-height']) as main:
        with solara.Columns([8, 4]):
            with solara.Column():
                solara.Text("Our Mission", classes=["display-1"])
                solara.Markdown(
                    """
    The world is fast-becoming a place driven by data.  To address dire shortages 
    of data-competency in the workforce, industry leaders are calling for 
    educational pathways that teach people how to interact with data.  The Cosmic 
    Data Stories (CosmicDS) project promotes public understanding of data science 
    through engaging, interactive data stories.
    
    The project facilitates connections between astronomers who want to tell the 
    story of a discovery and learners who can interrogate the data behind the 
    story on their own, using easy-to-use but powerful data science and 
    visualization techniques."""
                )

            with solara.Column():
                with rv.Card(flat=True, outlined=True):
                    with rv.CardTitle():
                        solara.Text("Getting Started")

                    with rv.CardText():
                        with solara.Column():
                            with solara.Link(solara.resolve_path("/register")):
                                solara.Button(label="Educator", outlined=True,
                                              style="width: 100%")

                            solara.Button(label="Student", outlined=True)

                    with rv.ExpansionPanels(flat=True):
                        with rv.ExpansionPanel():
                            with rv.ExpansionPanelHeader():
                                solara.Text("Why create an account?")

                            with rv.ExpansionPanelContent():
                                solara.Markdown("""
In Cosmic Data Stories, students collect and analyze their own astronomy data. 
Students’ measurements are stored anonymously in the CosmicDS database. Creating an account will:

- Associate student data with their class cohort.
- Allow students to view their results within the context of their class’s dataset and the full participant dataset.
- Keep track of students’ place within the data story if they aren’t able to finish the story within one class period
""")
                        with rv.ExpansionPanel():
                            with rv.ExpansionPanelHeader():
                                solara.Text("How do accounts work?")

                            with rv.ExpansionPanelContent():
                                solara.Markdown("""
Educators complete a brief form to receive a CosmicDS educator key by email.

Educators and Students access the CosmicDS portal and Data Story app by logging 
on through the OAuth authentication service. You can use credentials from 
common services like gmail or microsoft.

Educators enter their educator key to create classroom keys that associates 
students’ accounts with you and their classmates.

""")
                        with rv.ExpansionPanel():
                            with rv.ExpansionPanelHeader():
                                solara.Text("Privacy Policy")

                            with rv.ExpansionPanelContent():
                                solara.Markdown("""
Educator contact information is stored according to 
<link to Harvard privacy policy>. Used for …

Student contact information is anonymized by …
""")

    return main


@solara.component
def Layout(children=[]):
    location_context = solara.use_context(solara.routing._location_context)
    snackbar, set_snackbar = solara.use_state(True)

    # def _update_user_info(new, old):
    #     print("UPDATING-----")
    #     user_data.set({**user_data.value, **new.get('userinfo')})
    #
    # auth.user.subscribe_change(_update_user_info)

    with rv.App(dark=True) as main:
        solara.Title("Cosmic Data Stories")

        with rv.AppBar(elevate_on_scroll=True, app=True):
            with solara.Link(solara.resolve_path("/")):
                rv.Avatar(class_="me-10 ms-4", color="#cccccc", size="32")

            # with rv.ToolbarItems():
            with solara.Link(solara.resolve_path("/data_stories")):
                solara.Button("Data Stories", text=True)

            rv.Btn(text=True, children=["Mini Stories"])

            rv.Spacer()

            if not auth.user.value:
                solara.Button(
                    "Login",
                    icon_name="mdi-login",
                    href=auth.get_login_url(),
                    depressed=True,
                )
            else:
                if not user.value:
                    r = httpx.get(
                        f"http://127.0.0.1:8000/api/users/{auth.user.value['userinfo']['name']}")

                    if r.status_code == 200:
                        if r.json() is None:
                            print("USER NOT FOUND IN DATABASE")
                            user.set(
                                {'username': auth.user.value['userinfo'][
                                    'name'],
                                 'setup_completed': False})
                        else:
                            print("USER FOUND IN DATABASE")
                            user.set({**r.json(), 'setup_completed': True})

                        location_context.pathname = '/'

                elif user.value and not user.value['setup_completed']:
                    rv.Snackbar(v_model=snackbar, on_v_model=set_snackbar,
                                timeout=-1,
                                children=["Your account has not been setup.",
                                          solara.Button("Setup")])

                if user.value and user.value['setup_completed']:
                    if user.value.get('type') == 'educator':
                        with solara.Link(solara.resolve_path("/create")):
                            solara.Button("Create Class", elevation=0)
                    elif user.value.get('type') == 'student':
                        with solara.Link(solara.resolve_path("/join")):
                            solara.Button("Join Class", elevation=0)

                with solara.Link(solara.resolve_path("/account")):
                    rv.Btn(
                        children=[rv.Icon(children=["mdi-account"])],
                        # icon=True,
                        elevation=0,
                        color="green",
                    )

                def _logout_button_clicked(*args):
                    user.set(None)
                    location_context.pathname = '/'

                solara.Button(
                    "Logout",
                    icon_name="mdi-logout",
                    href=auth.get_logout_url(),
                    on_click=_logout_button_clicked,
                    depressed=True,
                )

        with rv.Content():
            route_current, routes = solara.use_route()

            if route_current.path == '/':
                Hero()

            with rv.Container(children=children, class_="pt-8"):
                pass

        with rv.Footer(app=False, padless=True):
            with rv.Container():
                with rv.Row():
                    with rv.Col(class_="d-flex justify-center"):
                        rv.Btn(children=["About"], text=True)
                        rv.Btn(children=["Team"], text=True)
                        rv.Btn(children=["Contact"], text=True)
                        rv.Btn(children=["Privacy"], text=True)
                        rv.Btn(children=["Digital Accessibility"], text=True)

                rv.Divider()

                with rv.Row():
                    with rv.Col(class_="d-flex justify-center"):
                        rv.Html(
                            tag="p",
                            children=[
                                "Copyright © 2023 The President and Fellows of Harvard College"
                            ],
                        )

    return main

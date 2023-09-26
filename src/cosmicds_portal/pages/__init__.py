import ipyvuetify as v
import solara
from solara.alias import rv
from solara_enterprise import auth

from ..components.hero import Hero
from ..components.login import Login

# # required if you don't use the default test account
# SOLARA_SESSION_SECRET_KEY="SECRETTESTKEY"
# # found in the Auth0 dashboard Applications->Applications->Client ID
# SOLARA_OAUTH_CLIENT_ID="ohpOLLdBibfGp2YUVwkmokTw18CXiD0B"
# # found in the Auth0 dashboard Applications->Applications->Client secret
# SOLARA_OAUTH_CLIENT_SECRET="DRmKDfn4ikzkdkSHXvCQPg6p0vQe46aCqmUND4YVQ9yzxZPrjdqp9qdMkGBl23MC"
# # found in the Auth0 dashboard Applications->Applications->Domain
# SOLARA_OAUTH_API_BASE_URL="dev-tbr72rd5whnwlyrg.us.auth0.com"
# SOLARA_OAUTH_SCOPE="openid profile email"

# # For testing locally
# SOLARA_SESSION_HTTPS_ONLY= "false"


v.theme.dark = True


@solara.component
def Page():
    with solara.Row(classes=['fill-height']) as main:
        with solara.Columns([8, 4]):
            with solara.Column():
                # solara.HTML(tag="div", children="Our Mission", class_="display-1")
                solara.Text("Our Mission", classes=["display-1"])
                # with rv.Html(tag="p", class_="subtitle-1"):
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
    with rv.App(dark=True) as main:
        solara.Title("Testing")

        with rv.AppBar(elevate_on_scroll=True, app=True):
            # with rv.Container(class_="fill-height d-flex align-center"):
            with solara.Link(solara.resolve_path("/")):
                rv.Avatar(class_="me-10 ms-4", color="#cccccc", size="32")

            with solara.Link(solara.resolve_path("/data_stories")):
                level = solara.use_route_level()
                rv.Btn(text=True, children=["Data Stories"])

            rv.Btn(text=True, children=["Mini Stories"])

            rv.Spacer()

            # Login(text=True)

            # with solara.Link(solara.resolve_path("/register")):
            #     rv.Btn(children=["Register"], depressed=True)

            if not auth.user.value:
                solara.Button(
                    "Login",
                    icon_name="mdi-logon",
                    href=auth.get_login_url(),
                    depressed=True,
                )
            else:
                user_info = auth.user.value["userinfo"]

                if "name" in user_info:
                    solara.Markdown(f"{user_info['name']}")

                with solara.Link(solara.resolve_path("/account")):
                    rv.Btn(
                        children=[rv.Icon(children=["mdi-account"])],
                        # icon=True,
                        elevation=0,
                        color="green",
                    )
                solara.Button(
                    "Logout",
                    icon_name="mdi-logout",
                    href=auth.get_logout_url(),
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
                                "Copyright © 2021 The President and Fellows of Harvard College"
                            ],
                        )

    return main

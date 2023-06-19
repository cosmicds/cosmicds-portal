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
    with rv.Row() as main:
        with rv.Col(cols=6):
            rv.Html(tag="div", children="Our Mission", class_="display-1")
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

        with rv.Col(cols=6):
            rv.Sheet(
                rounded="lg", color="#cccccc", class_="fill-height", min_height="20vh"
            )

    return main


@solara.component
def Layout(children=[]):
    router = solara.use_context(solara.routing.router_context)
    level = solara.use_route_level()

    with rv.App(dark=True) as main:
        solara.Title("Testing")

        with rv.AppBar(elevate_on_scroll=True, app=True):
            with rv.Container(class_="fill-height d-flex align-center"):
                with solara.Link(solara.resolve_path("/")):
                    rv.Avatar(class_="me-10 ms-4", color="#cccccc", size="32")

                with solara.Link(solara.resolve_path("/data_stories")):
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

                    with solara.Link(solara.resolve_path("/create_class")):
                        rv.Btn(
                            children=["Create Class"],
                            outlined=True,
                            color="green",
                        )
                    solara.Button(
                        "Logout",
                        icon_name="mdi-logout",
                        href=auth.get_logout_url(),
                        depressed=True,
                    )

        with rv.Content():
            if level == 0:
                Hero()

            with rv.Container(children=children):
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

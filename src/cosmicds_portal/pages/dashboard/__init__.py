import solara
from solara.alias import rv
from educator_dashboard.pages import Page as EducatorDashboard


@solara.component
def Page():
    EducatorDashboard()
    # solara.Text("Data Stories", classes=["display-1"])

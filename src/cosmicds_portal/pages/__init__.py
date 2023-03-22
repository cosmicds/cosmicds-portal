import solara
from solara.alias import rv


@solara.component
def Layout(children=[]):
    router = solara.use_context(solara.routing.router_context)
    with solara.VBox() as navigation:
        with rv.List(dense=True):
            with rv.ListItemGroup(v_model=router.path):
                with solara.Link(solara.resolve_path("/")):
                    with solara.ListItem("Home", icon_name="mdi-home",
                                         value="/"):
                        pass
                with solara.ListItem("tabular data", icon_name="mdi-database"):
                    for name in ['one', 'two', 'three']:
                        pathname = f"/tabular/{name}"
                        # with solara.Link(solara.resolve_path(pathname)):
                        solara.ListItem(name, value=pathname)
                with solara.ListItem("Articles", icon_name="mdi-book-open"):
                    for name in ['a', 'b', 'c']:
                        pathname = f"/article/{name}"
                        # with solara.Link(solara.resolve_path(pathname)):
                        solara.ListItem(name, value=pathname)

    with solara.AppLayout(navigation=navigation, title="Solara demo",
                          children=children) as main:
        pass

    return main

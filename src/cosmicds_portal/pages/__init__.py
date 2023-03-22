import solara
from solara.alias import rv


@solara.component
def Page():
    with solara.VBox() as main:
        solara.Title("Solara demo » Home")

        with solara.ColumnsResponsive(12):
            with solara.Card("Other"):
                with solara.ColumnsResponsive(6):
                    with solara.Card("Quick links"):
                        with solara.Column():
                            for name in ['one', 'two', 'three']:
                                solara.Button(f"Scatter for {name}", text=True)
                                # with solara.Link(f"/viz/scatter/{name}"):
                                solara.Button(f"Scatter for {name}", text=True)
                                # with solara.Link(f"/viz/histogram/{name}"):
                                solara.Button(f"Histogram for {name}", text=True)

    return main

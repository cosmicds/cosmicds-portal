import solara
from solara.alias import rv
from pathlib import Path


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

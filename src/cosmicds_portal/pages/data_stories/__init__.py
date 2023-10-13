import solara
from solara.alias import rv


@solara.component
def StoryCard():
    with rv.Card(max_width=400, class_="mx-auto") as story_card:
        rv.Img(class_="white--text align-end", height="200px",
               src="https://cdn.vuetifyjs.com/images/cards/docks.jpg")

        with rv.CardTitle():
            solara.Text("Hubble")

        with rv.CardSubtitle():
            solara.Text("Data Story")

        with rv.CardText():
            solara.Markdown(
                "The Hubble Data Story (HubbleDS) is the first prototype "
                "story under development by the CosmicDS team. In the "
                "HubbleDS, learners will use real astronomical data to "
                "answer questions like, “Has the universe always existed? "
                "If not, how long ago did it form?”")

        with rv.CardActions():
            solara.Button("View", elevation=0, color="primary")
            # rv.Btn(children=["Details"], color="orange")
            # rv.Spacer()
            # solara.HTML("div",
            #             unsafe_innerHTML="<a href='https://cosmicds.2i2c.cloud/hub/user-redirect/hubble/'>Create</a>")

    return story_card


@solara.component
def Page():
    with rv.ItemGroup() as main:
        solara.Text("Data Stories", classes=["display-1"])

        with solara.ColumnsResponsive([4]):
            for i in range(3):
                StoryCard()

    return main

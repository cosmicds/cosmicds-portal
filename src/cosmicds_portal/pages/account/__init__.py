import solara

from ..state import GLOBAL_STATE


@solara.component
def Page():
    router = solara.use_router()

    if not GLOBAL_STATE.user.exists():
        router.push(f"/")
        return
    elif not GLOBAL_STATE.user.setup_completed.value:
        router.push(f"/account_setup")
        return

    solara.Text("Account", classes=["display-1"])

    solara.Text(f"{GLOBAL_STATE.user.username}")
    solara.Text(f"{GLOBAL_STATE.user.type}")
    solara.Text(f"{GLOBAL_STATE.user.setup_completed}")

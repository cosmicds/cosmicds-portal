import solara
import dataclasses
from typing import Optional, cast, Dict
from solara_enterprise import auth


@dataclasses.dataclass
class UserInfo:
    username: str
    setup_completed: bool = False


user = solara.reactive(cast(Optional[UserInfo], None))

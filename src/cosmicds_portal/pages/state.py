import solara
import dataclasses
from typing import Optional, cast, Dict, Union
from solara.lab import Reactive
import httpx
from solara_enterprise import auth


@dataclasses.dataclass
class UserInfo:
    username: Reactive[cast(Optional[str], None)] = dataclasses.field(
        default=Reactive(cast(Optional[str], None)))
    setup_completed: Reactive[bool] = dataclasses.field(
        default=Reactive(False))
    type: Reactive[cast(Optional[str], None)] = dataclasses.field(
        default=Reactive(cast(Optional[str], None)))

    def exists(self):
        return self.username.value is not None

    def exists_and_setup(self):
        return self.exists() and self.setup_completed.value

    def logout(self):
        self.username.set(None)
        self.setup_completed.set(False)

    def is_student(self):
        return self.type.value == 'student'

    def is_educator(self):
        return self.type.value == 'educator'

    def check_database(self):
        r = httpx.get(
            f"http://127.0.0.1:8000/api/users/{auth.user.value['userinfo']['name']}")

        if r.status_code == 200:
            if r.json() is None:
                self.username.set(auth.user.value['userinfo']['name'])
            else:
                self.username.set(r.json().get('username'))
                self.setup_completed.set(True)
                self.type.set(r.json().get('type'))

    def authorized(self):
        return auth.user.value is not None


@dataclasses.dataclass
class GlobalState:
    user: Reactive[UserInfo] = dataclasses.field(default=UserInfo())


GLOBAL_STATE = GlobalState()

from typing import Any

from code.domain.state import DialogueState
from code.task.action.base import Action, ActionResult


class ActionListen(Action):
    name="action_listen"
    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:
        pass
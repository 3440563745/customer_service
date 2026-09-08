from typing import Any

from code.domain.state import DialogueState
from code.task.action.base import Action, ActionResult


class CustomAction(Action):
    name = "custom"
    async def run(self, state: DialogueState, action_kwargs: dict[str, Any]) -> ActionResult:
        print("custom_action")
        return ActionResult()



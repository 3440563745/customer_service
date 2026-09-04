# ctr h
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict

from code.task.flow.links import FlowStepLink, StaticLink, ConditionalLink, FallbackLink


class FlowStepType(Enum):
    START="start"
    COLLECT="collect"
    ACTION="action"
    END="end"
# x=FlowStepType(value="start")
# print(x)
@dataclass(slots=True)
class ResponseDefinition:
    mode:str="static"
    text:str|None=None
    prompt:str|None=None
@dataclass(slots=True)
class SlotValidation:
    condition:str|None=None
    failure_response:ResponseDefinition|None=None

@dataclass(slots=True)
class FlowStep:
    id:str
    type:FlowStepType
    description:str
    next:list[FlowStepLink]=field(default_factory=list)

    @classmethod
    def from_dict(cls, step:dict)->"FlowStep":
        step_type=step["type"]
        clz=STEP_TYPE_TO_CLASS[step_type]
        return clz.from_dict(step)

    @staticmethod
    def get_next(step_next: list|str) -> list[FlowStepLink]:
        step_next_list:list[FlowStepLink]=[]
        if isinstance(step_next,str):
            step_next_list.append(
                StaticLink(
                    target=step_next
                )
            )
            return step_next_list
        elif isinstance(step_next,list):
            for data in step_next:
                if "if" in data:
                    step_next_list.append(ConditionalLink(
                        condition=data["if"],
                        target=data["then"]
                    ))
                else:
                    step_next_list.append(FallbackLink(
                        target=data["else"]
                    ))
        return step_next_list
    @staticmethod
    def transfer_step(step:dict[str,Any])->dict[str,Any]:
        return {
            "id":step["id"],
            "type":FlowStepType(step["type"]),
            "description":step.get("description",""),
            "next":FlowStep.get_next(step["next"])
        }


@dataclass(slots=True)
class ActionFlowStep(FlowStep):
    args:Dict[str,Any]=field(default_factory=dict)
    action:str=""
    @classmethod
    def from_dict(cls,step:dict)->"ActionFlowStep":
        return cls(
            **FlowStep.transfer_step(step),
            action=step["action"],
            args=step.get("args",{})
        )
@dataclass(slots=True)
class CollectSlotStep(FlowStep):
    slot_name:str=""
    response:ResponseDefinition=field(default_factory=ResponseDefinition)
    validation:SlotValidation|None=None
    @classmethod
    def from_dict(cls, step:dict)->"CollectSlotStep":
        return cls(
            **FlowStep.transfer_step(step),
            slot_name=step["slot_name"],
            response=ResponseDefinition(**step["response"]),
            validation=SlotValidation(
                condition=step["validation"]["condition"],
                failure_response=ResponseDefinition(**step["validation"]["failure_response"])
            ) if "validation" in step else None
                               )

@dataclass(slots=True)
class StartFlowStep(FlowStep):
    @classmethod
    def from_dict(cls,step:dict)->"StartFlowStep":
        return cls(
            **FlowStep.transfer_step(step)
        )
@dataclass(slots=True)
class EndFlowStep(FlowStep):
    @classmethod
    def from_dict(cls,step:dict)->"EndFlowStep":
        return cls(
            **FlowStep.transfer_step(step)
        )
STEP_TYPE_TO_CLASS={
    "start":StartFlowStep,
    "collect":CollectSlotStep,
    "action":ActionFlowStep,
    "end":EndFlowStep,
}
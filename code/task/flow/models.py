from dataclasses import dataclass, field
from typing import Dict,List

from code.task.flow.steps import FlowStep


@dataclass(slots=True)
class FlowSlot:
    name:str
    type:str="any"
    label:str=""
    description:str=""
@dataclass(slots=True)
class Flow:
    id:str
    description:str=""
    steps:List[FlowStep]=field(default_factory=list)
    slots:List[FlowSlot]=field(default_factory=list)
    name:str|None=None

    @classmethod
    def from_dict(cls, flows_name:str,flows_data:dict)->"Flow":
        return cls(
            id=flows_name,
            name=flows_data["name"],
            description=flows_data["description"],
            steps=[FlowStep.from_dict(step) for step in flows_data["steps"]]
        )


@dataclass(slots=True)
class FlowsList:
    flows:List[Flow]=field(default_factory=list)
    slots:Dict[str,FlowSlot]=field(default_factory=dict)
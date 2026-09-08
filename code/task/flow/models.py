from dataclasses import dataclass, field
from typing import Dict,List

from code.task.flow.steps import FlowStep, FlowStepType


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
    def find_start_step(self)->FlowStep|None:
        for step in self.steps:
            if step.type==FlowStepType.START:
                return step
        return None
    # def get_flow_by_id(self,id)->FlowStep|None:
    #     for step in self.steps:
    #         if step.id==id:
    #             return step
    #     return None
    def get_step_by_id(self, step_id)->FlowStep|None:
        for flowstep in self.steps:
            if flowstep.id==step_id:
                return flowstep
        return None


@dataclass(slots=True)
class FlowsList:
    flows:List[Flow]=field(default_factory=list)
    slots:Dict[str,FlowSlot]=field(default_factory=dict)

    def find_flow(self, flow_id)->Flow|None:
        for flow in self.flows:
            if flow_id==flow.id:
                return flow
        return None

    def get_flow_by_id(self, flow_id)->Flow|None:
        for flow in self.flows:
            if flow_id==flow.id:
                return flow
        return None

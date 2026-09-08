import dataclasses
from dataclasses import dataclass,field,asdict
from typing import Any
from code.domain.messages import ProcessedMessage


@dataclass
class TaskContext:
    flow_id:str
    step_id:str|None=None
    slots:dict=field(default_factory=dict)
    @classmethod
    def from_dict(cls,data:dict[str,Any])->"TaskContext":
        return cls(
            flow_id=data["flow_id"],
            step_id=data["step_id"],
            slots=data["slots"]
        )
    def to_dict(self)->dict[str,Any]:
        return {
            "flow_id":self.flow_id,
            "step_id":self.step_id,
            "slots":self.slots
        }
@dataclass
class SystemContext:
    flow_id:str
    step_id:str|None=None
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SystemContext":
        clz=FLOW_ID_TO_CONTEXT_CLASS[data["flow_id"]]
        return clz(**data)
#active_task:TaskContext|None=None
    #当前面的active_task为taskcontext的子类，那么调用to_dict的时候，也是调用的之类的对应这个方法，
    #但是子类里面没有这个方法，全调用的父类的方法，然后父类里面的return asdict(self)就是会return
    #对应的子类对象
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
@dataclass
class StartedSystemContext(SystemContext):
    started_flow_id:str=""
    started_flow_name:str=""

@dataclass
class InterruptedSystemContext(SystemContext):
    interrupted_flow_id:str=""
    interrupted_flow_name:str=""
    started_flow_id:str=""
    started_flow_name:str=""
@dataclass
class ResumedSystemContext(SystemContext):
    resumed_flow_id:str=""
    resumed_flow_name:str=""
@dataclass
class CanceledSystemContext(SystemContext):
    canceled_flow_id:str=""
    canceled_flow_name:str=""
@dataclass
class CollectSystemContext(SystemContext):
    response:dict[str,Any]=field(default_factory=dict)
    slot_name:str=""
FLOW_ID_TO_CONTEXT_CLASS={
    "system_task_started":StartedSystemContext,
    "system_task_interrupted":InterruptedSystemContext,
    "system_task_canceled":CanceledSystemContext,
    "system_task_resumed":ResumedSystemContext,
    "system_collect_information":CollectSystemContext,
}

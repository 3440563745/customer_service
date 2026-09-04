from typing import Any

import yaml

from code.task.flow.models import FlowsList, FlowSlot, Flow
from pathlib  import Path

from code.task.flow.steps import FlowStep, CollectSlotStep


class FlowLoader:
    def load_many(self,paths=list[Path])->FlowsList:
        flows:list[Flow]=[]
        slots:dict[str,FlowSlot]={}
        for path in paths:
            flow_list=self.load(path)
            flows.extend(flow_list.flows)
            slots.update(flow_list.slots)
        return FlowsList(flows=flows,slots=slots)



    def load(self,path:Path)->FlowsList:
        with open(path,"r",encoding="utf-8") as f:
            data=yaml.safe_load(f)
            slots=self._load_slots(data.get("slots",{}))
            # print(slots)
            flows=self._load_flows(data.get("flows",{}),slots)
            return FlowsList(flows=flows,slots=slots)
    def _load_slots(self,data:dict[str,dict])->dict[str,FlowSlot]:
            slots={}
            for slot_name,slot_data in data.items():
                slots[slot_name]=FlowSlot(**slot_data,name=slot_name)
            return slots

    def _load_flows(self, flows_data:dict[str,dict], slots:dict[str,FlowSlot])->list[Flow]:
        flows:list[Flow]=[]
        for flows_name,flows_data in flows_data.items():
            steps:list[FlowStep]=[FlowStep.from_dict(data) for data in flows_data["steps"]]
            slots_flow:list[FlowSlot]=[]
            for step in steps:
                if isinstance(step,CollectSlotStep):
                    slots_flow.append(slots[step.slot_name])

            flow=Flow(
                id=flows_name,
                name=flows_data["name"],
                description=flows_data["description"],
                steps=steps,
                slots=slots_flow
            )
            flows.append(flow)
        return flows


if __name__ == "__main__":
    loader = FlowLoader()
    base_path=Path(__file__).parent.parent.parent.parent
    user_flow_path=base_path/"flow_config"/"user_flows.yml"
    system_flow_path=base_path/"flow_config"/"system_flows.yml"
    flows_list=loader.load_many([user_flow_path,system_flow_path])
    print(flows_list)

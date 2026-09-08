from dataclasses import asdict

from code.domain.contexts import CollectSystemContext
from code.domain.messages import ProcessedMessage
from code.domain.state import DialogueState
from code.task.action.base import ActionResult
from code.task.action.runner import ActionRunner, ActionCall
from code.task.flow.links import FlowStepLink, StaticLink, ConditionalLink, FallbackLink
from code.task.flow.models import FlowsList, Flow
from code.task.flow.steps import StartFlowStep, EndFlowStep, CollectSlotStep, ActionFlowStep, FlowStep


class FlowExecutor:

    async def run_task(self,state:DialogueState,flows:FlowsList,action_runner:ActionRunner)->list[ProcessedMessage]:
        messages:list[ProcessedMessage]=[]
        while True:
            action_call:ActionCall=self.advance_until_action(state,flows)
            if action_call.action_name=="action_listen":
                break
            else:
                action_result:ActionResult=await action_runner.run(action_call,state)
                messages.extend(action_result.messages)
                state.set_slots(action_result.slot_updates)
        return messages



    def advance_until_action(self,state:DialogueState,flows:FlowsList)->ActionCall:
        while True:
            current_task=state.get_current_context()
            if current_task is None:
                return ActionCall(action_name="action_listen")
            flow:Flow=flows.get_flow_by_id(current_task.flow_id)
            step:FlowStep=flow.get_step_by_id(current_task.step_id)
            result:ActionCall|None=self._run_step(state,step,flows)
            if result is not None:
                return result

    def _run_step(self, state:DialogueState, step:FlowStep,flows:FlowsList)->ActionCall|None:
        if isinstance(step,StartFlowStep):
            return self.run_start_step(step,state)
        if isinstance(step,EndFlowStep):
            return self.run_end_step(step,state)
        if isinstance(step,CollectSlotStep):
            return self.run_collect_slot_step(step,state,flows)
        if isinstance(step,ActionFlowStep):
            return self.run_action_step(step,state)

    def run_start_step(self, step:FlowStep, state:DialogueState)->ActionCall|None:
        self._advance_to_next_step(step,state)
        return None
    def run_end_step(self, step:FlowStep, state:DialogueState)->ActionCall|None:
        pass

    def run_collect_slot_step(self, step:CollectSlotStep, state:DialogueState,flows:FlowsList)->ActionCall|None:
        self.try_to_fill_slot_from_focused_object(step,state)
        if state.active_task.slots[step.slot_name] is not None:
            if step.validation:
                pass
            else:
                #无需校验
                self._advance_to_next_step(step,state)
                return None
        else:
            state.create_system_task(
                CollectSystemContext(
                    flow_id="system_collect_information",
                    step_id=flows.get_flow_by_id("system_collect_information").find_start_step().id,
                    slot_name=step.slot_name,
                    response=asdict(step.response)
                )
            )
            return None
    def run_action_step(self, step:ActionFlowStep, state:DialogueState)->ActionCall|None:
        #推进到下一个step
        self._advance_to_next_step(step,state)
        #get ActionCall
        action_call:ActionCall=self._build_action_call(step,state)
        return action_call
    def _get_next_step_id(self,step:FlowStep,state:DialogueState)->str:
        next:list[FlowStepLink]=step.next
        for link in next:
            if isinstance(link,StaticLink):
                return link.target
            if isinstance(link,ConditionalLink):
                func=link.condition
                context=state.get_current_context()
                data={
                    "context":asdict(context),
                    "slots":state.active_task.slots
                }
                if bool(eval(func,{},data)):
                    return link.target
            if isinstance(link,FallbackLink):
                return link.target
    def _advance_to_next_step(self,step:FlowStep,state:DialogueState):
        next_step_id=self._get_next_step_id(step,state)
        context=state.get_current_context()
        context.step_id=next_step_id

    def _build_action_call(self, step:ActionFlowStep, state:DialogueState)->ActionCall:
        name=step.action
        args=step.args
        if isinstance(args,str):
            args=asdict(state.get_current_context())[args.split(".")[1]]
        return ActionCall(
            action_name=name,
            action_kwargs=args
        )

    def try_to_fill_slot_from_focused_object(self, step:CollectSlotStep, state:DialogueState):
        slot_name=step.slot_name
        if state.focused_object is None:
            return
        if slot_name=="order_number" and state.focused_object.type=="order":
            state.set_slots({slot_name:state.focused_object.id})
        if slot_name=="product_id" and state.focused_object.type=="product":
            state.set_slots({slot_name:state.focused_object.id})



if __name__=="__main__":
    f="a>b"
    print(eval(f,{},{"a":1,"b":2}))


from code.domain.contexts import TaskContext, SystemContext, StartedSystemContext, InterruptedSystemContext, \
    CanceledSystemContext, ResumedSystemContext
from code.domain.state import DialogueState
from code.task.command.models import Command, StartFlowCommand, SetSlotsCommand, CancelFlowCommand, ResumeFlowCommand
from code.task.flow.models import FlowsList


class CommandProcessor:
    def run(self,
            commands:list[Command],
            state:DialogueState,
            flows:FlowsList
            )->None:
        for command in commands:
            self._apply(command,state,flows)
    def _apply(self,
               command:Command,
               state:DialogueState,
               flows:FlowsList)->None:
        if isinstance(command,StartFlowCommand):
            self._handle_start_flow(command,state,flows)
        elif isinstance(command,SetSlotsCommand):
            self._handle_set_slots(command,state)
        elif isinstance(command,CancelFlowCommand):
            self._handle_cancel_flow(state,flows)
        elif isinstance(command,ResumeFlowCommand):
            self._handle_resume_task(command,state,flows)

    def _handle_start_flow(self, command:StartFlowCommand, state:DialogueState, flows:FlowsList):
        state.remove_system_task()
        active_task=state.active_task
        flow = flows.find_flow(command.flow)
        if state.active_task:
            #有运行任务，那么需要挂起
            state.interrupt_active_task()
            #将任务添加到active_task中
            #先找flow

            #构建active_task
            state.create_active_task(TaskContext(
                flow_id=flow.id,
                step_id=flow.find_start_step().id
            ))
            #构建系统任务
            system_flow=flows.find_flow("system_task_interrupted")
            state.create_system_task(
                InterruptedSystemContext(
                    flow_id=system_flow.id,
                    step_id=system_flow.find_start_step().id,
                    interrupted_flow_id=active_task.flow_id,
                    interrupted_flow_name=flows.get_flow_by_id(active_task.flow_id).name,
                    started_flow_id=flow.id,
                    started_flow_name=flow.name
                )
            )
        else:
            state.create_active_task(
                TaskContext(
                    flow_id=command.flow,
                    step_id=flow.find_start_step().id
                )
            )
            state.create_system_task(
                StartedSystemContext(
                    flow_id="system_task_started",
                    step_id=flows.get_flow_by_id("system_task_started").find_start_step().id,
                    started_flow_id=command.flow,
                    started_flow_name=flow.name
                )
            )



    def _handle_set_slots(self, command:SetSlotsCommand, state:DialogueState):
        if state.active_task:
            state.set_slots(command.slots)

    def _handle_cancel_flow(self, state:DialogueState, flows:FlowsList):
        active_task=state.active_task
        target_flow=flows.get_flow_by_id(active_task.flow_id)
        state.cancel_task()
        #将systemcontext里面加入cancelcontext，告诉系统是打断的哪一个
        state.create_system_task(
                 CanceledSystemContext(
                     flow_id="system_task_canceled",
                     step_id=flows.get_flow_by_id("system_task_canceled").find_start_step().id,
                     canceled_flow_id=active_task.flow_id,
                     canceled_flow_name=target_flow.name,
                 )
        )

    def _handle_resume_task(self, command:ResumeFlowCommand, state:DialogueState, flows:FlowsList):
        flow=flows.get_flow_by_id(command.flow)
        active_task=state.active_task
        if active_task:
            #先暂停task
            state.cancel_task()
            #再将查pausedtask里面的放入
            state.resume_task(flow.id)
            #将打断任务加入系统任务中
            state.create_system_task(
                InterruptedSystemContext(
                    step_id=flows.get_flow_by_id("system_task_interrupted").find_start_step().id,
                    flow_id="system_task_interrupted",
                    interrupted_flow_id=active_task.flow_id,
                    interrupted_flow_name=flows.get_flow_by_id(active_task.flow_id).name,
                    started_flow_id=flow.id,
                    started_flow_name=flow.name
                )
            )
        else:
            state.resume_task(flow.id)
            state.create_system_task(
                ResumedSystemContext(
                    flow_id="system_task_resumed",
                    step_id=flows.get_flow_by_id("system_task_resumed").find_start_step().id,
                    resumed_flow_id=command.flow,
                    resumed_flow_name=flow.name
                )

            )


    
    

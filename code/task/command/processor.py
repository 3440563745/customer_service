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

    def _handle_start_flow(self, command, state, flows):
        pass

    def _handle_set_slots(self, command, state):
        pass

    def _handle_cancel_flow(self, state, flows):
        pass

    def _handle_resume_task(self, command, state, flows):
        pass
    
    

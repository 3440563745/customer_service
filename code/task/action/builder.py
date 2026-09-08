import importlib
import inspect
import pkgutil

from code.task.action.base import Action
from code.task.action.builtin.action_listen import ActionListen
from code.task.action.builtin.action_response import ActionResponse
from code.task.action.registry import ActionRegistry
from code.task.action.runner import ActionRunner


def register_builtin_actions(action_runner:ActionRunner):
    action_runner.registry.registry(ActionResponse())
    action_runner.registry.registry(ActionListen())


def register_custom_action(action_runner:ActionRunner):
    package=importlib.import_module("code.task.action.custom")
    for _,module_name,is_pkg in pkgutil.iter_modules(package.__path__,prefix=f"{package.__name__}."):
        if is_pkg:
            continue
        module=importlib.import_module(module_name)
        for _,obj in inspect.getmembers(module,inspect.isclass):
            if not issubclass(obj,Action) or obj is Action:
                continue
            if obj.__module__ !=module.__name__:
                continue
            action_runner.registry.registry(obj())




def build_action_runner(registry:ActionRegistry)->ActionRunner:
    action_runner=ActionRunner(registry=registry)
    register_builtin_actions(action_runner)
    register_custom_action(action_runner)
    return action_runner

if __name__=="__main__":
    action_runner=build_action_runner(ActionRegistry())
    print(action_runner)
    print(action_runner.registry._actions)
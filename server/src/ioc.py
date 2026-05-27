from typing import Any, Callable

from server.src.exceptions import ArgumentException

def raise_(ex):
    raise ex

class Ioc:
    _strategy: Any = lambda dependency, *args: UpdateIocResolveDependencyStrategyCommand(args[0])  \
        if ("Update Ioc Resolve Dependency Strategy" == dependency) \
        else raise_(ArgumentException(msg = "dependency is not found"))

    @staticmethod
    def resolve(dependency: str, *args) -> Any:
        return Ioc._strategy(dependency, *args)

    @staticmethod
    def reset_strategy():
        return lambda dependency, *args: UpdateIocResolveDependencyStrategyCommand(args[0]) \
            if ("Update Ioc Resolve Dependency Strategy" == dependency) \
            else raise_(ArgumentException(msg="dependency is not found"))


class UpdateIocResolveDependencyStrategyCommand:
    def __init__(self, updater: Callable):
        self._update_ioc_strategy: Callable = updater

    def execute(self):
        Ioc._strategy = self._update_ioc_strategy(Ioc._strategy)   # pylint: disable=W0212

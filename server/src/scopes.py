import threading
from typing import Dict, Callable

from server.src.exceptions import NoParentException
from server.src.ioc import Ioc


class DependencyResolver:
    def __init__(self, scope: Dict[str, Callable]):
        self.dependencies = scope

    def resolve(self, dependency: str, *args):
        dependencies = self.dependencies
        while True:
            dependency_resolver_strategy = dependencies.get(dependency)
            if dependency_resolver_strategy:
                return dependency_resolver_strategy(*args)
            dependencies = dependencies.get("IoC.Scope.Parent")(*args)


class RegisterDependencyCommand:
    def __init__(self, dependency: str, dependency_resolver_strategy: Callable):
        self.dependency: str = dependency
        self.dependency_resolver_strategy: Callable = dependency_resolver_strategy

    def execute(self):
        current_scope: Dict[str, Callable] = Ioc.resolve("IoC.Scope.Current")
        current_scope.update({self.dependency: self.dependency_resolver_strategy})


class SetCurrentScopeCommand:
    def __init__(self, scope: Dict[str, Callable]):
        self.scope = scope

    def execute(self):
        InitCommand.current_scopes.value = self.scope


class InitCommand:
    root_scope: Dict[str, Callable] = {}
    current_scopes = threading.local()

    @classmethod
    def resolve(cls, _foo: Callable) -> Callable:
        def func(dependency: str, *args):
            try:
                scope = cls.current_scopes.value if cls.current_scopes.value else cls.root_scope
            except AttributeError:
                scope = cls.root_scope
            return DependencyResolver(scope).resolve(dependency, *args)
        return func

    @classmethod
    def scope_cur(cls, *args) -> Dict[str, Callable]:    # pylint: disable=W0613
        try:
            return cls.current_scopes.value
        except AttributeError:
            return cls.root_scope

    def scope_cur_set(self, *args):
        return SetCurrentScopeCommand(args[0])

    def scope_parent(self, *args):
        raise NoParentException()

    def scope_create(self, *args) -> Dict[str, Callable]:
        creating_scope: Dict[str, Callable] = {}
        if len(args) > 0:
            parent_scope = args[0]
        else:
            parent_scope = Ioc.resolve("IoC.Scope.Current")
        creating_scope.update({"IoC.Scope.Parent": lambda *args: parent_scope})
        return creating_scope

    def register(self, *args):
        return RegisterDependencyCommand(args[0], args[1])

    def execute(self):
        lock = threading.Lock()
        with lock:
            self.root_scope.update({"IoC.Scope.Current.Set": self.scope_cur_set})
            self.root_scope.update({"IoC.Scope.Current": self.scope_cur})
            self.root_scope.update({"IoC.Scope.Parent": self.scope_parent})
            self.root_scope.update({"IoC.Scope.Create": self.scope_create})
            self.root_scope.update({"IoC.Register": self.register})
            Ioc.resolve("Update Ioc Resolve Dependency Strategy", self.resolve).execute()

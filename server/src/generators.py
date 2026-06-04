from typing import Any, Callable, Dict

from server.src.ioc import Ioc


class AdapterGenerator:
    @staticmethod
    def _generate_constructor() -> Callable:
        def __init__(self, obj):
            self._obj = obj
        return __init__

    @staticmethod
    def _generate_method(method_name: str, class_name: str) -> Callable:
        def adapter_method_name(*args):
            if "get" in method_name:
                return Ioc.resolve(f"Spaceship.Operations.{class_name}.{method_name}")
            return Ioc.resolve(f"Spaceship.Operations.{class_name}.{method_name}", *args).execute()
        adapter_method_name.__name__ = method_name
        return adapter_method_name

    @staticmethod
    def _generate_methods(interface_class: type) -> Dict[str, Callable]:
        methods = {}
        for method_name, method in interface_class.__dict__.items():
            if callable(method) and not method_name.startswith('__'):
                methods[method_name] = AdapterGenerator._generate_method(
                    method_name=method_name,
                    class_name=interface_class.__name__
                )
        return methods

    @staticmethod
    def generate_adapter(interface_class: type, obj: Any) -> type:
        class_name = f"{interface_class.__name__}Adapter"
        adapter_class = type(
            class_name,
            (interface_class,),
            {
                '_obj': obj,
                '__init__': AdapterGenerator._generate_constructor(),
                **AdapterGenerator._generate_methods(interface_class=interface_class)
            }
        )
        return adapter_class(obj)

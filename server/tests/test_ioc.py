from typing import Any

import pytest

from server.src.exceptions import ArgumentException
from server.src.ioc import Ioc

def test_ioc_update_resolve_dependency_strategy():
    was_called: bool = False
    def strategy(func: Any):
        nonlocal was_called
        was_called = True
        return func
    Ioc.resolve("Update Ioc Resolve Dependency Strategy", strategy).execute()
    assert was_called


def test_ioc_not_exists_strategy():
    with pytest.raises(ArgumentException):
        def strategy(func: Any):
            return func
        Ioc.resolve("Wrong Strategy", strategy).execute()

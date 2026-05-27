import pytest

from server.src.exceptions import ArgumentException, NoParentException
from server.src.ioc import Ioc
from server.src.scopes import InitCommand


def init() -> None:
    InitCommand().execute()
    ioc_scope = Ioc.resolve("IoC.Scope.Create")
    Ioc.resolve("IoC.Scope.Current.Set", ioc_scope).execute()


def test_register_no_parent():
    InitCommand().execute()
    with pytest.raises(NoParentException):
        Ioc.resolve("IoC.Scope.Parent")


def test_register():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    Ioc.resolve("IoC.Register", "someDependency", lambda : 1).execute()
    assert Ioc.resolve("someDependency") == 1


def test_register_exception():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    with pytest.raises(ArgumentException):
        Ioc.resolve("someDependency")


def test_parent_scope():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    Ioc.resolve("IoC.Register", "someDependency", lambda: 1).execute()
    _parent_scope = Ioc.resolve("IoC.Scope.Current")
    new_scope = Ioc.resolve("IoC.Scope.Create")
    Ioc.resolve("IoC.Scope.Current.Set", new_scope).execute()
    assert Ioc.resolve("someDependency") == 1
    assert Ioc.resolve("IoC.Scope.Current") == new_scope


def test_scope_in_scope():
    Ioc._strategy = Ioc.reset_strategy()  # pylint: disable=W0212
    init()
    scope1 = Ioc.resolve("IoC.Scope.Create")
    scope2 = Ioc.resolve("IoC.Scope.Create", scope1)
    Ioc.resolve("IoC.Scope.Current.Set", scope1).execute()
    Ioc.resolve("IoC.Register", "someDependency", lambda: 1).execute()
    Ioc.resolve("IoC.Scope.Current.Set", scope2).execute()
    assert Ioc.resolve("someDependency") == 1

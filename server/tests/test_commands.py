import pathlib
from unittest.mock import patch, mock_open

import pytest

from server.src.commands import WriteToLog, RetryOnce, RetryTwice
from server.tests.conftest import TestException


def test_write_to_log(fs):
    file_path = f"{pathlib.Path().resolve()}.log"
    fs.create_file(file_path)
    cmd = WriteToLog(exc=TestException(msg="test message"))
    cmd.execute()
    f = fs.get_object(file_path)
    assert f.contents == "test message"


def test_write_to_log_exception():
    open_mock = mock_open()
    open_mock.side_effect=TestException(msg='error')
    with patch('builtins.open', open_mock):
        with pytest.raises(TestException):
            cmd = WriteToLog(exc=TestException(msg="test message"))
            cmd.execute()


def test_retry_once(fs):
    file_path = f"{pathlib.Path().resolve()}.log"
    fs.create_file(file_path)
    log_cmd = WriteToLog(exc=TestException(msg="test message"))
    cmd = RetryOnce(cmd=log_cmd)
    cmd.execute()
    f = fs.get_object(file_path)
    assert f.contents == "test message"


def test_retry_once_exception():
    open_mock = mock_open()
    open_mock.side_effect=TestException(msg='error')
    with patch('builtins.open', open_mock):
        with pytest.raises(TestException):
            log_cmd = WriteToLog(exc=TestException(msg="test message"))
            repeater_cmd = RetryOnce(cmd=log_cmd)
            repeater_cmd.execute()


def test_retry_twice(fs):
    file_path = f"{pathlib.Path().resolve()}.log"
    fs.create_file(file_path)
    log_cmd = WriteToLog(exc=TestException(msg="test message"))
    cmd = RetryOnce(cmd=log_cmd)
    cmd.execute()
    f = fs.get_object(file_path)
    assert f.contents == "test message"


def test_retry_twice_exception():
    open_mock = mock_open()
    open_mock.side_effect=TestException(msg='error')
    with patch('builtins.open', open_mock):
        with pytest.raises(TestException):
            log_cmd = WriteToLog(exc=TestException(msg="test message"))
            repeater_cmd = RetryTwice(cmd=log_cmd)
            repeater_cmd.execute()

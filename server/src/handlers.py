from server.src.commands import WriteToLog, RetryOnce, RetryTwice
from server.src.interfaces import ICommand


class PutInQueueWriteToLogHandler:
    def __init__(self):
        pass

    def handle(self, exc: Exception, cmd: ICommand = None) -> ICommand:  # pylint: disable=W0613
        return WriteToLog(exc=exc)


class PutInQueueRetryOnceHandler:
    def __init__(self):
        pass

    def handle(self, cmd: ICommand, exc: Exception = None) -> ICommand:  # pylint: disable=W0613
        return RetryOnce(cmd=cmd)


class RetryOnceThenLogHandler:
    def __init__(self):
        pass

    def handle(self, cmd: ICommand, exc: Exception) -> ICommand:
        if isinstance(cmd, RetryOnce):
            return PutInQueueWriteToLogHandler().handle(exc=exc, cmd=cmd)
        return PutInQueueRetryOnceHandler().handle(exc=exc, cmd=cmd)


class RetryTwiceThenLogHandler:
    def __init__(self):
        self.store = {
            RetryTwice: {Exception: lambda cmd, exc: PutInQueueRetryOnceHandler().handle(cmd=cmd, exc=exc)},
            RetryOnce:  {Exception: lambda cmd, exc: PutInQueueWriteToLogHandler().handle(cmd=cmd, exc=exc)},
        }

    def handle(self, cmd: ICommand, exc: Exception) -> ICommand:
        cmd_type = type(cmd)
        exc_type = type(exc)
        if Exception in exc_type.__mro__:
            exc_type = Exception
        try:
            func = self.store[cmd_type][exc_type]
        except KeyError:
            func = RetryTwice
        return func(cmd=cmd, exc=exc)

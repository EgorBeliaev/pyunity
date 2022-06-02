# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Event", "EventLoopManager", "WaitForSeconds", "WaitForEventLoop",
           "WaitForUpdate", "WaitForFixedUpdate"]

from . import Logger, config
from .errors import PyUnityException, PyUnityExit
from .core import Component, GameObject
from .values import SavableStruct, StructEntry, Clock
from functools import update_wrapper
import threading
import asyncio
import inspect
# import signal
import time

@SavableStruct(
    component=StructEntry(Component, required=True),
    name=StructEntry(str, required=True),
    args=StructEntry(tuple, required=True))
class Event:
    def __init__(self, func, args=(), kwargs={}):
        if not hasattr(func, "__self__"):
            raise PyUnityException(
                "Cannot create event from callback that is not attached to a Component")
        if not isinstance(func.__self__, Component):
            raise PyUnityException(
                "Cannot create event from callback that is not attached to a Component")
        if not isinstance(func.__self__.gameObject, GameObject):
            raise PyUnityException(
                "Provided callback component does not belong to a GameObject")

        update_wrapper(self, func)

        self.component = func.__self__
        self.name = func.__name__

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.isAsync = inspect.iscoroutinefunction(func)

    async def asyncTrigger(self):
        await self.func(*self.args, **self.kwargs)

    def trigger(self):
        self.func(*self.args, **self.kwargs)

    def callSoon(self):
        if self.isAsync:
            loop = asyncio.get_running_loop()
            loop.call_soon(self.trigger)
        else:
            if EventLoopManager.current is None:
                raise PyUnityException("No EventLoopManager running")
            EventLoopManager.current.pending.append(self)

    def _fromDict(self, factory, attrs, instanceCheck=None):
        def wrapper(component, method, args=(), kwargs={}):
            func = getattr(component, method)
            return factory(func, args, kwargs)
        return SavableStruct.fromDict(self, wrapper, attrs, instanceCheck)

class EventLoopManager:
    current = None
    exceptions = []

    def __init__(self):
        self.threads = []
        self.loops = []
        self.waiting = {}
        self.pending = []
        self.updates = []
        self.running = False

    def schedule(self, *funcs, main=False, ups=None, waitFor=None):
        if main:
            self.updates.extend(funcs)
        else:
            if ups is None:
                raise PyUnityException("ups argument is required if main is False")

            self.waiting[waitFor] = []

            loop = EventLoop()
            self.loops.append(loop)
            def inner():
                clock = Clock()
                clock.Start(ups)
                while self.running:
                    for waiter in self.waiting[waitFor]:
                        waiter.loop.call_soon_threadsafe(waiter.event.set)

                    for func in funcs:
                        try:
                            func(loop)
                        except Exception as e:
                            EventLoopManager.exception = e
                            break
                        loop.call_soon(loop.stop)
                        loop.run_forever()
                    clock.Maintain()

            t = threading.Thread(target=inner, daemon=True)
            self.threads.append(t)

    def set(self):
        if EventLoopManager.current is not None:
            raise PyUnityException("Only one EventLoopManager can be running")
        EventLoopManager.current = self

    def start(self):
        self.running = True
        for thread in self.threads:
            thread.start()

        while True:
            if len(EventLoopManager.exceptions):
                from . import SceneManager
                if config.exitOnError:
                    Logger.LogLine(Logger.ERROR,
                                f"Exception in Scene: {SceneManager.CurrentScene().name!r}")
                    Logger.LogException(EventLoopManager.exceptions[0])
                    raise PyUnityExit
                else:
                    for exception in EventLoopManager.exceptions:
                        Logger.LogLine(Logger.ERROR,
                                    f"Exception ignored in Scene: {SceneManager.CurrentScene().name!r}")
                        Logger.LogException(exception)
                    EventLoopManager.exceptions.clear()

            for func in self.updates:
                func()

            for event in self.pending:
                event.trigger()
            self.pending.clear()

    def quit(self):
        self.running = False
        for thread in self.threads:
            thread.join() # Will wait until this iteration has finished
        self.threads.clear()
        EventLoopManager.current = None

class EventLoop(asyncio.SelectorEventLoop):
    def __init__(self, selector=None):
        super(EventLoop, self).__init__(selector)
        self.set_exception_handler(EventLoop.handleException)

        # signals = (signal.SIGTERM, signal.SIGINT)
        # for s in signals:
        #     self.add_signal_handler(
        #         s, lambda sig=s: asyncio.create_task(self.shutdown(sig)))

    async def shutdown(self, signal=None):
        if signal is not None:
            Logger.LogLine(Logger.INFO, f"Received exit signal {signal.name}")
        tasks = [t for t in asyncio.all_tasks(self) if t is not
                 asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        self.stop()

    def handleException(self, context):
        if "exception" in context:
            EventLoopManager.exceptions.append(context["exception"])

class WaitForSeconds:
    def __init__(self, length):
        self.length = length

    def __await__(self):
        start = time.perf_counter()
        sleep = asyncio.sleep(self.length)
        yield from sleep.__await__()
        return time.perf_counter() - start

class WaitForEventLoop:
    def __init__(self):
        self.event = asyncio.Event()
        self.loop = asyncio.get_running_loop()
        EventLoopManager.current.waiting[type(self)].append(self)

    def __await__(self):
        start = time.perf_counter()
        yield from self.event.wait().__await__()
        EventLoopManager.current.waiting[type(self)].remove(self)
        return time.perf_counter() - start

class WaitForUpdate(WaitForEventLoop):
    pass

class WaitForFixedUpdate(WaitForEventLoop):
    pass

"""
Utility functions to log output of PyUnity.

This will be imported as ``pyunity.Logger``.

"""

from typing import Callable, Tuple, IO

def get_tmp() -> str: ...

folder: str = ...
stream: IO[str] = ...
timestamp: str = ...
start: float = ...

class Level:
    abbr: str
    name: str
    def __init__(self, abbr: str, name: str) -> None: ...

OUTPUT: Level = ...
INFO: Level = ...
DEBUG: Level = ...
ERROR: Level = ...
WARN: Level = ...

class Special:
    func: Callable[[None], str]
    def __init__(self, func: Callable[[None], str]) -> None: ...

RUNNING_TIME: Special = ...

def Log(*mesage: str) -> None: ...
def LogLine(level: Level, *message: str, silent: bool=...) -> Tuple[float, str]: ...
def LogException(e: Exception) -> None: ...
def LogSpecial(level: Level, type: Special) -> None: ...
def Save() -> None: ...
def SetStream(s: IO[str]) -> None: ...
def ResetStream() -> None: ...

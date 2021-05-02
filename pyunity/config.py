import os
from . import logger as Logger
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
if "PYUNITY_DEBUG_MODE" not in os.environ:
    os.environ["PYUNITY_DEBUG_MODE"] = "1"
if "PYUNITY_INTERACTIVE" not in os.environ:
    os.environ["PYUNITY_INTERACTIVE"] = "1"

size = (800, 500)
fps = 60
faceCulling = True
audio = True

Logger.LogLine(Logger.DEBUG, "Loaded config")

if os.environ["PYUNITY_INTERACTIVE"] == "1":
    from . import window
    windowProvider = window.GetWindowProvider()
    del window

del os

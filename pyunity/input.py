from enum import IntEnum, auto
from .scenes import SceneManager

class KeyState(IntEnum):
    UP = auto()
    DOWN = auto()
    PRESS = auto()
    NONE = auto()

class KeyCode(IntEnum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()
    Space = auto()
    Alpha0 = auto()
    Alpha1 = auto()
    Alpha2 = auto()
    Alpha3 = auto()
    Alpha4 = auto()
    Alpha5 = auto()
    Alpha6 = auto()
    Alpha7 = auto()
    Alpha8 = auto()
    Alpha9 = auto()
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    Keypad0 = auto()
    Keypad1 = auto()
    Keypad2 = auto()
    Keypad3 = auto()
    Keypad4 = auto()
    Keypad5 = auto()
    Keypad6 = auto()
    Keypad7 = auto()
    Keypad8 = auto()
    Keypad9 = auto()
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

class MouseCode(IntEnum):
    Left = auto()
    Middle = auto()
    Right = auto()

def GetKey(keycode):
    """
    Check if key is pressed at moment of function call

    Parameters
    ----------
    keycode : KeyCode
        Key to query

    Returns
    -------
    boolean
        If the key is pressed

    """
    return SceneManager.windowObject.get_key(keycode, KeyState.PRESS)

def GetKeyUp(keycode):
    """
    Check if key was released this frame.

    Parameters
    ----------
    keycode : KeyCode
        Key to query

    Returns
    -------
    boolean
        If the key was released

    """
    return SceneManager.windowObject.get_key(keycode, KeyState.UP)

def GetKeyDown(keycode):
    """
    Check if key was pressed down this frame.

    Parameters
    ----------
    keycode : KeyCode
        Key to query

    Returns
    -------
    boolean
        If the key was pressed down

    """
    return SceneManager.windowObject.get_key(keycode, KeyState.DOWN)

def GetMouse(mousecode):
    """
    Check if mouse button is pressed at moment of function call

    Parameters
    ----------
    mousecode : MouseCode
        Mouse button to query

    Returns
    -------
    boolean
        If the mouse button is pressed

    """
    return SceneManager.windowObject.get_mouse(mousecode, KeyState.PRESS)

def GetMouseUp(mousecode):
    """
    Check if mouse button was released this frame.

    Parameters
    ----------
    mousecode : MouseCode
        Mouse button to query

    Returns
    -------
    boolean
        If the mouse button was released

    """
    return SceneManager.windowObject.get_mouse(mousecode, KeyState.UP)

def GetMouseDown(mousecode):
    """
    Check if mouse button was pressed down this frame.

    Parameters
    ----------
    mousecode : MouseCode
        Mouse button to query

    Returns
    -------
    boolean
        If the mouse button was pressed down

    """
    return SceneManager.windowObject.get_mouse(mousecode, KeyState.DOWN)

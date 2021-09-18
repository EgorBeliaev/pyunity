__all__ = ["Canvas", "RectData", "RectAnchors",
           "RectOffset", "RectTransform", "Image2D", "Gui",
           "Text", "FontLoader"]

from pyunity.errors import PyUnityException
from .values import Vector2, Color, RGB
from .core import Component, GameObject, ShowInInspector
from .files import Texture2D
from .input import Input, MouseCode, KeyState
from types import FunctionType
import os
import sys
from PIL import Image, ImageDraw, ImageFont

class Canvas(Component):
    def Update(self, updated):
        for descendant in self.transform.GetDescendants():
            if descendant in updated:
                continue
            updated.append(descendant)
            button = descendant.GetComponent(Button)
            if button is not None:
                button.pressed = Input.GetMouse(button.mouseButton)
                rectTransform = descendant.GetComponent(RectTransform)
                rect = rectTransform.GetRect() + rectTransform.offset
                pos = Vector2(Input.mousePosition)
                if rect.min < pos < rect.max:
                    button.pressed = True
                    if Input.GetMouseState(button.mouseButton, button.state):
                        button.callback()
                else:
                    button.pressed = False

class RectData:
    def __init__(self, min_or_both=None, max=None):
        if min_or_both is None:
            self.min = Vector2.zero()
            self.max = Vector2.zero()
        elif max is None:
            if isinstance(min_or_both, RectData):
                self.min = min_or_both.min.copy()
                self.max = min_or_both.max.copy()
            else:
                self.min = min_or_both.copy()
                self.min = min_or_both.copy()
        else:
            self.min = min_or_both.copy()
            self.max = max.copy()

    def __repr__(self):
        return "<{} min={} max={}>".format(self.__class__.__name__, self.min, self.max)
    
    def __add__(self, other):
        if isinstance(other, RectData):
            return RectData(self.min + other.min, self.max + other.max)
        else:
            return RectData(self.min + other, self.max + other)
    
    def __sub__(self, other):
        if isinstance(other, RectData):
            return RectData(self.min - other.min, self.max - other.max)
        else:
            return RectData(self.min - other, self.max - other)
    
    def __mul__(self, other):
        if isinstance(other, RectData):
            return RectData(self.min * other.min, self.max * other.max)
        else:
            return RectData(self.min * other, self.max * other)

class RectAnchors(RectData):
    def SetPoint(self, p):
        self.min = p.copy()
        self.max = p.copy()

    def RelativeTo(self, other):
        parentSize = other.max - other.min
        absAnchorMin = other.min + (self.min * parentSize)
        absAnchorMax = other.min + (self.max * parentSize)
        return RectData(absAnchorMin, absAnchorMax)

class RectOffset(RectData):
    @staticmethod
    def Square(size, center=Vector2.zero()):
        return RectOffset(center - size / 2, center + size / 2)

    def Move(self, pos):
        self.min += pos
        self.max += pos

    def SetCenter(self, pos):
        size = self.max - self.min
        self.min = pos - size / 2
        self.max = pos + size / 2

class RectTransform(Component):
    anchors = ShowInInspector(RectAnchors)
    offset = ShowInInspector(RectOffset)
    pivot = ShowInInspector(Vector2)
    rotation = ShowInInspector(float, 0)
    def __init__(self, transform):
        super(RectTransform, self).__init__(transform)
        self.anchors = RectAnchors()
        self.offset = RectOffset()
        self.pivot = Vector2(0.5, 0.5)

        if self.transform.parent is None:
            self.parent = None
        else:
            self.parent = self.transform.parent.GetComponent(RectTransform)

    def GetRect(self):
        from .render import Screen
        if self.parent is None:
            return self.anchors * Screen.size
        else:
            parentRect = self.parent.GetRect() + self.parent.offset
            rect = self.anchors.RelativeTo(parentRect)
            return rect

class Image2D(Component):
    texture = ShowInInspector(Texture2D)
    def __init__(self, transform):
        super(Image2D, self).__init__(transform)
        self.rectTransform = self.GetComponent(RectTransform)

class Button(Component):
    callback = ShowInInspector(FunctionType, lambda: None)
    state = ShowInInspector(KeyState, KeyState.UP)
    mouseButton = ShowInInspector(MouseCode, MouseCode.Left)
    pressed = ShowInInspector(bool, False)

buttonDefault = Texture2D(os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "shaders", "gui", "button.png"))

class Gui:
    @classmethod
    def MakeButton(cls, name, scene, texture2d=None):
        if texture2d is None:
            texture2d = buttonDefault
        
        button = GameObject(name)
        transform = button.AddComponent(RectTransform)

        texture = GameObject("Button", button)
        transform2 = texture.AddComponent(RectTransform)
        transform2.anchors = RectAnchors(Vector2.zero(), Vector2.one())
        img = texture.AddComponent(Image2D)
        img.texture = texture2d
        buttonComponent = button.AddComponent(Button)

        scene.Add(button)
        scene.Add(texture)
        return transform, buttonComponent

class _FontLoader:
    fonts = {}

    @classmethod
    def LoadFont(cls, name, size):
        if name in cls.fonts:
            if size in cls.fonts[name]:
                return cls.fonts[name][size]
        else:
            cls.fonts[name] = {}
        file = cls.LoadFile(name)
        font = ImageFont.truetype(file, size)
        cls.fonts[name][size] = font
        return Font(name, font)

    @classmethod
    def LoadFile(cls, name):
        raise NotImplemented

class WinFontLoader(_FontLoader):
    @classmethod
    def LoadFile(cls, name):
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts\\")
        try:
            file = winreg.QueryValueEx(key, name + " (TrueType)")
        except WindowsError:
            file = None
        if file is None:
            raise PyUnityException("Cannot find font called " + repr(name))
        return file[0]

class UnixFontLoader(_FontLoader):
    pass

if sys.platform.startswith("linux") or sys.platform == "darwin":
    FontLoader = UnixFontLoader
else:
    FontLoader = WinFontLoader

class Font:
    def __init__(self, name, imagefont):
        if not isinstance(imagefont, ImageFont.FreeTypeFont):
            raise PyUnityException("Please specify a FreeType font" + \
                "created from ImageFont.freetype")
        
        self._font = imagefont
        self.name = name

class Text(Component):
    font = ShowInInspector(Font, FontLoader.LoadFont("Arial", 16))
    text = ShowInInspector(str, "Text")
    color = ShowInInspector(Color)
    def __init__(self, transform):
        super(Text, self).__init__(transform)
        self.rect = None
        self.color = RGB(255, 255, 255)
    
    def GetTexture(self):
        if self.rect is None:
            self.rect = self.GetComponent(RectTransform)
        
        rect = self.rect.GetRect() + self.rect.offset
        size = rect.max - rect.min
        im = Image.new("RGBA", tuple(size), (255, 255, 255, 0))

        draw = ImageDraw.Draw(im)
        draw.text((0, 0), self.text, font=self.font._font,
            fill=tuple(self.color))
        im.show()
        return im

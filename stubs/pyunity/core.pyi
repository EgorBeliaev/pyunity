## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Component", "GameObject", "SingleComponent",
           "MeshRenderer", "Tag", "Transform", "ShowInInspector",
           "HideInInspector"]

from .scenes import Scene
from .values import Vector3, Quaternion, Material
from .meshes import Mesh
from ctypes import Union
from typing import Dict, Iterator, List as _List, Type, TypeVar

T = TypeVar("T")

class Tag:
    tags: _List[str]
    tag: int
    tagName: str
    @classmethod
    def AddTag(cls, name: str) -> int: ...
    def __init__(self, tagNumOrName: Union[str, int]) -> None: ...

class GameObject:
    name: str
    components: _List[Component]
    transform: Transform
    tag: Tag
    enabled: bool
    scene: Scene
    def __init__(self, name: str = ..., parent: GameObject | None = ...) -> None: ...
    @classmethod
    def BareObject(cls, name: str = ...) -> GameObject: ...
    def AddComponent(self, componentClass: Type[T]) -> T: ...
    def GetComponent(self, componentClass: Type[T]) -> T: ...
    def RemoveComponent(self, componentClass: Type) -> None: ...
    def GetComponents(self, componentClass: Type[T]) -> _List[T]: ...
    def RemoveComponents(self, componentClass: Type[T]) -> None: ...

class HideInInspector:
    type: Type[T] | None
    default: T | None
    name: str | None
    def __init__(self, type_: Type[T] | None = ..., default: T | None = ...) -> None: ...

class ShowInInspector(HideInInspector):
    name: str | None
    def __init__(self, type: Type[T] | None = ..., default: T | None = ..., name: str | None = ...) -> None: ...

class Component:
    shown: Dict[str, HideInInspector]
    saved: Dict[str, HideInInspector]
    gameObject: GameObject
    transform: Transform
    enabled: bool
    def __init__(self, transform: Transform, isDummy: bool = ...) -> None: ...
    @classmethod
    def __init_subclass__(cls): ...
    def AddComponent(self, componentClass: Type[T]) -> T: ...
    def GetComponent(self, componentClass: Type[T]) -> T: ...
    def RemoveComponent(self, componentClass: Type) -> None: ...
    def GetComponents(self, componentClass: Type[T]) -> _List[T]: ...
    def RemoveComponents(self, componentClass: Type[T]) -> None: ...
    @property
    def scene(self) -> Scene: ...

class SingleComponent(Component): ...

class Transform(SingleComponent):
    localPosition: Vector3
    localRotation: Quaternion
    localScale: Vector3
    parent: Transform
    children: _List[Transform]
    def __init__(self, transform: None = ...) -> None: ...
    @property
    def position(self) -> Vector3: ...
    @position.setter
    def position(self, value: Vector3) -> None: ...
    @property
    def rotation(self) -> Quaternion: ...
    @rotation.setter
    def rotation(self, value: Quaternion) -> None: ...
    @property
    def localEulerAngles(self) -> Vector3: ...
    @localEulerAngles.setter
    def localEulerAngles(self, value: Vector3) -> None: ...
    @property
    def eulerAngles(self) -> Vector3: ...
    @eulerAngles.setter
    def eulerAngles(self, value: Vector3) -> None: ...
    @property
    def scale(self) -> Vector3: ...
    @scale.setter
    def scale(self, value: Vector3) -> None: ...
    def ReparentTo(self, parent: Transform) -> None: ...
    def List(self) -> None: ...
    def GetDescendants(self) -> Iterator[Transform]: ...
    def FullPath(self) -> str: ...
    def LookAtTransform(self, transform: Transform) -> None: ...
    def LookAtGameObject(self, gameObject: GameObject) -> None: ...
    def LookAtPoint(self, vec: Vector3) -> None: ...
    def LookInDirection(self, vec: Vector3) -> None: ...

class MeshRenderer(SingleComponent):
    DefaultMaterial: Material
    mesh: Mesh
    mat: Material
    def Render(self) -> None: ...

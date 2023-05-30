## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Utility functions related to loading
and saving PyUnity meshes and scenes.

This will be imported as ``pyunity.Loader``.

"""

from typing import List, Optional, Dict, Type, Tuple, Any, Union, TypeVar, Callable
from pathlib import Path
from .meshes import Mesh, Material
from .scenes import Scene
from .files import Project, Prefab, Asset
from .values import ImmutableStruct
from .core import GameObject, Component
import enum

def LoadObj(filename: str) -> Mesh: ...
def SaveObj(mesh: Mesh, path: Union[str, Path]) -> None: ...
def LoadStl(filename: str) -> Mesh: ...
def SaveStl(mesh: Mesh, path: Union[str, Path]) -> None: ...
def LoadMesh(filename: str) -> Mesh: ...
def SaveMesh(mesh: Mesh, project: Project, path: Union[str, Path]) -> None: ...

class Primitives(metaclass=ImmutableStruct):
    _names: List[str] = ...
    cube: Mesh = ...
    quad: Mesh = ...
    doubleQuad: Mesh = ...
    sphere: Mesh = ...
    capsule: Mesh = ...
    cylinder: Mesh = ...

T = TypeVar("T")

def GetImports(file: str) -> str: ...
def parseString(string: str, project: Optional[Project] = ...) -> Tuple[bool, Any]: ...
def parseStringFallback(string: str, project: Project, fallback: T) -> Union[T, Any]: ...

class ObjectInfo:
    class SkipConv:
        def __init__(self, value: str) -> None: ...

    uuid: str
    type: str
    attrs: Dict[str, str]
    def __init__(self, uuid: str, type: str, attrs: Dict[str, str]) -> None: ...
    @staticmethod
    def convString(v: Union[str, enum.Enum, Any]) -> str: ...
    def __str__(self) -> str: ...
    def __getattr__(self, attr: str) -> str: ...

def SaveMat(material: Material, project: Project, filename: str) -> None: ...
def LoadMat(path: Union[str, Path], project: Project) -> Material: ...
def SavePrefab(prefab: Prefab, path: Union[str, Path], project: Project) -> None: ...
def LoadPrefab(path: Union[str, Path], project: Project) -> Prefab: ...

savable: List[Type] = ...

def SaveGameObjects(gameObjects: List[GameObject], data: List[ObjectInfo], project: Project) -> None: ...
def LoadObjectInfos(file: Union[str, Path]) -> List[ObjectInfo]: ...
def instanceCheck(type_: Type, value: Any) -> bool: ...
def GetComponentMap() -> Dict[str, Type[Component]]: ...
def LoadGameObjects(data: List[ObjectInfo], project: Project) -> List[GameObject]: ...
def SaveScene(scene: Scene, project: Project, path: Union[str, Path]) -> None: ...

AT = TypeVar("AT", bound=Asset)
savers: Dict[Type[AT], Callable[[AT, Project, Union[str, Path]], None]] = ...

def ResaveScene(scene: Scene, project: Project) -> None: ...
def GenerateProject(name: str, force: bool = ...) -> Project: ...
def SaveProject(project: Project) -> None: ...
def LoadProject(folder: Union[str, Path], remove: bool = ...) -> Project: ...
def LoadScene(sceneFile: Union[str, Path], project: Project) -> Scene: ...

from pyunity.values.other import ImmutableStruct
import glm
from typing import Any, Dict, List, Tuple
from .meshes import Mesh
from .files import Skybox
from .values import Color, Vector2, Vector3, Quaternion
from .core import SingleComponent, Transform, MeshRenderer, Light
from .gui import RectTransform, Canvas

float_size: int =...

def gen_buffers(mesh: Mesh) -> Tuple[int, int]: ...
def gen_array() -> int: ...

class Shader:
    vertex: str
    frag: str
    compiled: bool
    name: str
    def __init__(self, vertex: str, frag: str, name: str) -> None: ...
    def compile(self) -> None: ...
    @staticmethod
    def fromFolder(path: str, name: str) -> Shader: ...
    def setVec3(self, var: bytes, val: Any) -> None: ...
    def setMat4(self, var: bytes, val: Any) -> None: ...
    def setInt(self, var: bytes, val: int) -> None: ...
    def setFloat(self, var: bytes, val: float) -> None: ...
    def use(self) -> None: ...

__dir: str = ...
shaders: Dict[str, Shader] = ...
skyboxes: Dict[str, Skybox] = ...

def compile_shaders() -> None: ...

class Camera(SingleComponent):
    near: float = ...
    far: float = ...
    clearColor: Color = ...
    shader: Shader = ...
    skyboxEnabled: bool = ...
    skybox: Skybox = ...
    size: Vector2
    guiShader: Shader
    skyboxShader: Shader
    viewMat: object
    lastPos: Vector3
    lastRot: Quaternion
    renderPass: bool
    _fov: float
    viewMat: glm.mat4x4

    def __init__(self, transform: Transform) -> None: ...
    def setup_buffers(self) -> None: ...
    @property
    def fov(self) -> float: ...
    def Resize(self, width: int, height: int) -> None: ...
    def getMatrix(self, transform: Transform) -> glm.mat4x4: ...
    def get2DMatrix(self, rectTransform: RectTransform) -> glm.mat4x4: ...
    def getViewMat(self) -> glm.mat4x4: ...
    def UseShader(self, name: str) -> None: ...
    def Render(self, renderers: List[MeshRenderer], lights: List[Light]) -> None: ...
    def Render2D(self, canvases: List[Canvas]) -> None: ...

class Screen(metaclass=ImmutableStruct):
    _names: List[str] = ...
    width: int = ...
    height: int = ...
    size: Vector2 = ...
    aspect: float = ...
    @classmethod
    def _edit(cls, width: int, height: int) -> None: ...
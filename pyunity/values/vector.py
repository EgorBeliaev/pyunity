__all__ = ["Vector2", "Vector", "Vector3", "clamp"]

from .abc import ABCMeta, abstractmethod, abstractproperty
import glm
import operator

def clamp(x, _min, _max): return min(_max, max(_min, x))
"""Clamp a value between a minimum and a maximum"""

def conv(num):
    """Convert float to string and removing decimal place as necessary."""
    if isinstance(num, float) and num.is_integer():
        return str(int(num))
    return str(num)

class Vector(metaclass=ABCMeta):
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(map(conv, self))})"
    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(map(conv, self))})"

    def __getitem__(self, i):
        return list(self)[i]

    @abstractmethod
    def __iter__(self):
        pass

    def __list__(self):
        return list(iter(self))
    
    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    def __bool__(self):
        return all(self)

    @abstractmethod
    def _o1(self, f):
        pass

    @abstractmethod
    def _o2(self, other, f):
        pass

    @abstractmethod
    def _r_o2(self, other, f):
        pass

    @abstractmethod
    def _io(self, other, f):
        pass

    def __add__(self, other):
        return self._o2(other, operator.add)
    def __radd__(self, other):
        return self._r_o2(other, operator.add)
    def __iadd__(self, other):
        return self._io(other, operator.add)

    def __sub__(self, other):
        return self._o2(other, operator.sub)
    def __rsub__(self, other):
        return self._r_o2(other, operator.sub)
    def __isub__(self, other):
        return self._io(other, operator.sub)

    def __mul__(self, other):
        return self._o2(other, operator.mul)
    def __rmul__(self, other):
        return self._r_o2(other, operator.mul)
    def __imul__(self, other):
        return self._io(other, operator.mul)

    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.truediv)

    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
    def __imod__(self, other):
        return self._io(other, operator.mod)

    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
    def __ilshift__(self, other):
        return self._io(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
    def __irshift__(self, other):
        return self._io(other, operator.rshift)

    @abstractmethod
    def __eq__(self, other):
        pass
    def __ne__(self, other):
        return any(self._o2(other, operator.ne))
    def __gt__(self, other):
        return all(self._o2(other, operator.gt))
    def __lt__(self, other):
        return all(self._o2(other, operator.lt))
    def __ge__(self, other):
        return all(self._o2(other, operator.ge))
    def __le__(self, other):
        return all(self._o2(other, operator.le))

    def __and__(self, other):
        return self._o2(other, operator.and_)
    def __rand__(self, other):
        return self._r_o2(other, operator.and_)

    def __or__(self, other):
        return self._o2(other, operator.or_)
    def __ror__(self, other):
        return self._r_o2(other, operator.or_)

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    def __rxor__(self, other):
        return self._r_o2(other, operator.xor)

    def __neg__(self):
        return self._o1(operator.neg)

    def __pos__(self):
        return self._o1(operator.pos)

    def __abs__(self):
        return self.length

    def abs(self):
        return self._o1(abs)

    def __round__(self, other):
        return self._r_o2(other, round)

    def __invert__(self):
        return self._o1(operator.invert)

    @abstractproperty
    def length(self):
        pass

class Vector2(Vector):
    def __init__(self, x_or_list=None, y=None):
        if x_or_list is not None:
            if y is None:
                if hasattr(x_or_list, "x") and hasattr(x_or_list, "y"):
                    self.x = x_or_list.x
                    self.y = x_or_list.y
                else:
                    self.x = x_or_list[0]
                    self.y = x_or_list[1]
            else:
                self.x = x_or_list
                self.y = y
        else:
            self.x = 0
            self.y = 0

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2
    
    def __hash__(self):
        return hash((self.x, self.y))

    def _o1(self, f):
        """Unary operator"""
        return Vector2(f(self.x), f(self.y))

    def _o2(self, other, f):
        """Any two-operator operation where the left operand is a Vector2"""
        if hasattr(other, "__getitem__"):
            return Vector2(f(self.x, other[0]), f(self.y, other[1]))
        else:
            return Vector2(f(self.x, other), f(self.y, other))

    def _r_o2(self, other, f):
        """Any two-operator operation where the right operand is a Vector2"""
        if hasattr(other, "__getitem__"):
            return Vector2(f(other[0], self.x), f(other[1], self.y))
        else:
            return Vector2(f(other, self.x), f(other, self.y))

    def _io(self, other, f):
        """Inplace operator"""
        if hasattr(other, "__getitem__"):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def copy(self):
        """Makes a copy of the Vector2"""
        return Vector2(self.x, self.y)

    def get_length_sqrd(self):
        """
        Gets the length of the vector squared. This
        is much faster than finding the length.

        Returns
        -------
        float
            The length of the vector squared

        """
        return self.x ** 2 + self.y ** 2

    @property
    def length(self):
        """Gets or sets the magnitude of the vector"""
        return glm.sqrt(self.x ** 2 + self.y ** 2)

    @length.setter
    def length(self, value):
        length = self.length
        if length != 0:
            self.x *= value / length
            self.y *= value / length

    def normalized(self):
        """
        Get a normalized copy of the vector, or Vector2(0, 0)
        if the length is 0.

        Returns
        -------
        Vector2
            A normalized vector

        """
        length = self.length
        if length != 0:
            return 1 / length * self
        return self.copy()

    def normalize(self):
        """
        Normalize the vector in place.

        """
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length

    def normalize_return_length(self):
        """
        Normalize the vector and return its length before the normalization

        Returns
        -------
        float
            The length before the normalization

        """
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length

    def get_distance(self, other):
        """
        The distance between this vector and the other vector

        Returns
        -------
        float
            The distance

        """
        return glm.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)

    def get_dist_sqrd(self, other):
        """
        The distance between this vector and the other vector, squared.
        It is more efficient to call this than to call `get_distance` and
        square it.

        Returns
        -------
        float
            The squared distance

        """
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2

    @property
    def int_tuple(self):
        """Return the x, y and z values of this vector as ints"""
        return int(self.x), int(self.y)

    @property
    def rounded(self):
        """Return the x, y and z values of this vector rounded to the nearest integer"""
        return round(self.x), round(self.y)

    def clamp(self, min, max):
        """
        Clamps a vector between two other vectors,
        resulting in the vector being as close to the
        edge of a bounding box created as possible.

        Parameters
        ----------
        min : Vector2
            Min vector
        max : Vector2
            Max vector

        """
        self.x = clamp(self.x, min.x, max.x)
        self.y = clamp(self.y, min.y, max.y)

    def dot(self, other):
        """
        Dot product of two vectors.

        Parameters
        ----------
        other : Vector2
            Other vector

        Returns
        -------
        float
            Dot product of the two vectors

        """
        return self.x * other[0] + self.y * other[1]

    def cross(self, other):
        """
        Cross product of two vectors. In 2D this
        is a scalar.

        Parameters
        ----------
        other : Vector2
            Other vector

        Returns
        -------
        float
            Cross product of the two vectors

        """
        z = self.x * other[1] - self.y * other[0]
        return z

    @staticmethod
    def min(a, b):
        return a._o2(b, min)

    @staticmethod
    def max(a, b):
        return a._o2(b, max)

    @staticmethod
    def zero():
        """A vector of zero length"""
        return Vector2(0, 0)

    @staticmethod
    def one():
        """A vector of ones"""
        return Vector2(1, 1)

    @staticmethod
    def left():
        """Vector2 pointing in the negative x axis"""
        return Vector2(-1, 0)

    @staticmethod
    def right():
        """Vector2 pointing in the postive x axis"""
        return Vector2(1, 0)

    @staticmethod
    def up():
        """Vector2 pointing in the postive y axis"""
        return Vector2(0, 1)

    @staticmethod
    def down():
        """Vector2 pointing in the negative y axis"""
        return Vector2(0, -1)

class Vector3(Vector):
    def __init__(self, x_or_list=None, y=None, z=None):
        if x_or_list is not None:
            if y is None:
                if hasattr(x_or_list, "x") and hasattr(x_or_list, "y") and hasattr(x_or_list, "z"):
                    self.x = x_or_list.x
                    self.y = x_or_list.y
                    self.z = x_or_list.z
                else:
                    self.x = x_or_list[0]
                    self.y = x_or_list[1]
                    self.z = x_or_list[2]
            else:
                self.x = x_or_list
                self.y = y
                self.z = z
        else:
            self.x = 0
            self.y = 0
            self.z = 0

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __len__(self):
        return 3
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def _o1(self, f):
        """Unary operator"""
        return Vector3(f(self.x), f(self.y), f(self.z))

    def _o2(self, other, f):
        """Any two-operator operation where the left operand is a Vector3"""
        if isinstance(other, Vector3):
            return Vector3(f(self.x, other.x), f(self.y, other.y), f(self.z, other.z))
        elif hasattr(other, "__getitem__"):
            return Vector3(f(self.x, other[0]), f(self.y, other[1]), f(self.z, other[2]))
        else:
            return Vector3(f(self.x, other), f(self.y, other), f(self.z, other))

    def _r_o2(self, other, f):
        """Any two-operator operation where the right operand is a Vector3"""
        if hasattr(other, "__getitem__"):
            return Vector3(f(other[0], self.x), f(other[1], self.y), f(other[2], self.z))
        else:
            return Vector3(f(other, self.x), f(other, self.y), f(other, self.z))

    def _io(self, other, f):
        """Inplace operator"""
        if hasattr(other, "__getitem__"):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
            self.z = f(self.z, other[2])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
            self.z = f(self.z, other)
        return self
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def copy(self):
        """
        Makes a copy of the Vector3

        Returns
        -------
        Vector3
            A shallow copy of the vector

        """
        return Vector3(self.x, self.y, self.z)

    def get_length_sqrd(self):
        """
        Gets the length of the vector squared. This
        is much faster than finding the length.

        Returns
        -------
        float
            The length of the vector squared

        """
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    @property
    def length(self):
        """Gets or sets the magnitude of the vector"""
        return glm.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @length.setter
    def length(self, value):
        length = self.length
        if length != 0:
            self.x *= value / length
            self.y *= value / length
            self.z *= value / length

    def normalized(self):
        """
        Get a normalized copy of the vector, or Vector3(0, 0, 0)
        if the length is 0.

        Returns
        -------
        Vector3
            A normalized vector

        """
        length = self.length
        if length != 0:
            return 1 / length * self
        return self.copy()

    def normalize(self):
        """
        Normalize the vector in place.

        """
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length

    def normalize_return_length(self):
        """
        Normalize the vector and return its length before the normalization

        Returns
        -------
        float
            The length before the normalization

        """
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return length

    def get_distance(self, other):
        """
        The distance between this vector and the other vector

        Returns
        -------
        float
            The distance

        """
        return glm.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2 + (self.z - other[2]) ** 2)

    def get_dist_sqrd(self, other):
        """
        The distance between this vector and the other vector, squared.
        It is more efficient to call this than to call `get_distance` and
        square it.

        Returns
        -------
        float
            The squared distance

        """
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2 + (self.z - other[2]) ** 2

    @property
    def int_tuple(self):
        """Return the x, y and z values of this vector as ints"""
        return int(self.x), int(self.y), int(self.z)

    @property
    def rounded(self):
        """Return the x, y and z values of this vector rounded to the nearest integer"""
        return round(self.x), round(self.y), round(self.z)

    def clamp(self, min, max):
        """
        Clamps a vector between two other vectors,
        resulting in the vector being as close to the
        edge of a bounding box created as possible.

        Parameters
        ----------
        min : Vector3
            Min vector
        max : Vector3
            Max vector

        """
        self.x = clamp(self.x, min.x, max.x)
        self.y = clamp(self.y, min.y, max.y)
        self.z = clamp(self.z, min.z, max.z)

    def dot(self, other):
        """
        Dot product of two vectors.

        Parameters
        ----------
        other : Vector3
            Other vector

        Returns
        -------
        float
            Dot product of the two vectors

        """
        return self.x * other[0] + self.y * other[1] + self.z * other[2]

    def cross(self, other):
        """
        Cross product of two vectors

        Parameters
        ----------
        other : Vector3
            Other vector

        Returns
        -------
        Vector3
            Cross product of the two vectors

        """
        x = self.y * other[2] - self.z * other[1]
        y = self.z * other[0] - self.x * other[2]
        z = self.x * other[1] - self.y * other[0]
        return Vector3(x, y, z)

    @staticmethod
    def min(a, b):
        return a._o2(b, min)

    @staticmethod
    def max(a, b):
        return a._o2(b, max)

    @staticmethod
    def zero():
        """A vector of zero length"""
        return Vector3(0, 0, 0)

    @staticmethod
    def one():
        """A vector of ones"""
        return Vector3(1, 1, 1)

    @staticmethod
    def forward():
        """Vector3 pointing in the positive z axis"""
        return Vector3(0, 0, 1)

    @staticmethod
    def back():
        """Vector3 pointing in the negative z axis"""
        return Vector3(0, 0, -1)

    @staticmethod
    def left():
        """Vector3 pointing in the negative x axis"""
        return Vector3(-1, 0, 0)

    @staticmethod
    def right():
        """Vector3 pointing in the postive x axis"""
        return Vector3(1, 0, 0)

    @staticmethod
    def up():
        """Vector3 pointing in the postive y axis"""
        return Vector3(0, 1, 0)

    @staticmethod
    def down():
        """Vector3 pointing in the negative y axis"""
        return Vector3(0, -1, 0)

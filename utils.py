from types import UnionType
from typing import Any


class Maybe:
  _inner = None

  def __init__(self, val):
    self._inner = val

  def __getattribute__(self, name: str) -> Any:
    if name in ["_inner", "is_none"]:
      return  super().__getattribute__(name)

    if self._inner is None:
      return None

    return Maybe(getattr(self._inner, name))

  def __getitem__(self, idx):
    if self._inner is None:
      return None

    return Maybe(self._inner[idx])

  def __or__(self, value: Any) -> Any:
    if self._inner is None:
      return value
    return self._inner

  def is_none(self) -> bool:
    return self._inner is None

maybe = lambda val: Maybe(val)
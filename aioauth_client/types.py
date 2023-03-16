from __future__ import annotations

from typing import Dict, List, Union

TRes = Union[Dict[str, "TRes"], List["TRes"], str, int, float, bool, None]
THeaders = Dict[str, str]
TParams = Dict[str, str]

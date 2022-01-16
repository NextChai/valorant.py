"""
MIT License

Copyright (c) 2022 NextChai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import time
import asyncio
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Tuple, TypeVar, Union

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

try:
    import orjson
except ModuleNotFoundError:
    HAS_ORJSON = False
else:
    HAS_ORJSON = True

if TYPE_CHECKING:
    from aiohttp import ClientResponse

T = TypeVar('T')
O = TypeVar('O')
P = ParamSpec('P')
    
    
__all__: Tuple[str, ...] = (
    '_to_json',
    '_from_json',
    'MISSING',
    '_mis_if_not',
    'add_logging',
    'json_or_text',
)

     
if HAS_ORJSON:

    def _to_json(obj: Any) -> str:  # type: ignore
        return orjson.dumps(obj).decode('utf-8')

    _from_json = orjson.loads  # type: ignore
else:
    import json

    def _to_json(obj: Any) -> str:
        return json.dumps(obj, separators=(',', ':'), ensure_ascii=True)

    _from_json = json.loads
    
    
class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '...'

MISSING: Any = _MissingSentinel()


def _mis_if_not(object: T, fallback: Optional[O] = None) -> Optional[Union[O, T]]:
    return object if object is not MISSING else fallback

def add_logging(func: Callable[P, Union[Awaitable[T], T]]) -> Callable[P, Union[Awaitable[T], T]]:
    """
    Used to add logging to a coroutine or function.
    
    
    .. code-block:: python3

        async def foo(a: int, b: int) -> int:
            return a + b
        
        logger = add_logging(foo)
        result = await logger(1, 2)
        print(result)
        >>> 3
        
        def foo(a: int, b: int) -> int:
            return a + b
        
        logger = add_logging(foo)
        result = logger(1, 2)
        print(result)
        >>> 3
    """
    async def _async_wrapped(*args: P.args, **kwargs: P.kwargs) -> Awaitable[T]:
        start = time.time()
        result = await func(*args, **kwargs)  # type: ignore
        print(f'{func.__name__} took {time.time() - start:.2f} seconds')
        
        return result # type: ignore
    
    def _sync_wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.time()
        result = func(*args, **kwargs)
        print(f'{func.__name__} took {time.time() - start:.2f} seconds')
        
        return result # type: ignore
    
    return _async_wrapped if asyncio.iscoroutinefunction(func) else _sync_wrapped # type: ignore

async def json_or_text(response: ClientResponse) -> Any:
    # For now, we're going to assume that the response is json
    if response.headers['Content-Type'] == 'application/json; charset=utf-8':
        return await response.json()
    
    return await response.read()

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

from functools import cached_property
from typing import Tuple

__all__: Tuple[str, ...] = (
    'Hashable',
)
 

class Hashable:
    
    @cached_property
    def id(self) -> str:
        id = getattr(self, 'id', None)
        if id is not None:
            return id
        
        return getattr(self, 'uuid')
    
    def __eq__(self, _o: object) -> bool:
        return isinstance(_o, self.__class__) and self.id == _o.id
    
    def __ne__(self, _o: object) -> bool:
        return not self.__eq__(_o)
    
    def __hash__(self) -> int:
        return hash(self.id)
    
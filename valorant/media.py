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

import re
from functools import cached_property
from typing import Final, Tuple, TypeVar, Type, Literal

from .abc import Hashable

__all__: Tuple[str, ...] = (
    'Icon',
)

I = TypeVar('I', bound='Icon')
    

class Icon(Hashable):
    """
    Represents an icon for an item.
    
    .. container:: operations

        .. describe:: x == y

            Determines if the two icons are the same.
            
        .. describe:: x != y
        
            Determines if the two icons are different.
        
        .. describe:: hash(x)

            Returns the icon's hash.
            
        .. describe:: str(x)

            Returns the complete URL suitable for human use.
    
    .. versionadded:: 1.0.0
    
    Attributes
    ----------
    uuid: :class:`str`
        The uuid of the icon.
    filename: :class:`str`
        The filename of the icon.
    format: :class:`str`
        The format of the icon.
    """
    __slots__: Tuple[str, ...] = (
        'uuid',
        'filename', 
        'format',
        'type'
    )
    
    BASE: Final[str] = 'https://media.valorant-api.com/'

    def __init__(self, *, type: str, uuid: str, filename: str, format: str) -> None:
        self.uuid: str = uuid
        self.filename: str = filename
        self.format: str = format
        self.type: str = type
        
    def __str__(self) -> str:
        return self.url
    
    @classmethod
    def _from_url(cls: Type[I], url: str) -> I:
        icon_regex = re.compile(r'https://media.valorant-api.com/'       # base
                        r'(?P<path>[\w]{1,}\/){1,}'                      # URL Path: EX: /agents
                        r'(?P<uuid>[\w]{8}-([\w]{4}-){3}[\w]{12})'       # Uuid of item
                        r'/((?:[\w]{1,}/){1,})?'                         # Path, if there: EX: 
                        r'(?P<filename>[\w]{1,})'                        # Filename: EX: displayicon
                        r'\.(?P<format>[\w]{1,})')                       # File format: EX: .png
        
        match = icon_regex.match(url)
        if not match:
            raise ValueError(f'Invalid URL: {url}')
        
        path, uuid, _, _, filename, format = match.groups()
        return cls(type=path, uuid=uuid, filename=filename, format=format)
    
    @cached_property
    def url(self) -> str:
        return f'{self.BASE}/{self.uuid}/{self.filename}.{self.format}'
    
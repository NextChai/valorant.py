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

from typing import Callable, Tuple

# Using normal Enum for now is fine.
from enum import Enum 

__all__: Tuple[str, ...] = (
    'PlatformRouting',
)

_format_route: Callable[[str], str] = lambda route: f'https://{route}.api.riotgames.com'

class PlatformRouting(Enum):
    br1 = _format_route('br1')
    eun1 = _format_route('eun1')
    euw1 = _format_route('euw1')
    jp1 = _format_route('jp1')
    kr = _format_route('kr')
    la1 = _format_route('la1')
    la2 = _format_route('la2')
    na1 = _format_route('na1')
    na = _format_route('na')
    oc1 = _format_route('oc1')
    tri = _format_route('tri')
    ru = _format_route('ru')
    americas = _format_route('americas')
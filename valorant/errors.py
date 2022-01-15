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

from typing import Any, Dict, Tuple, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    

__all__: Tuple[str, ...] = (
    'ValorantError',
    'HTTPException',
    'BadRequest',
    'Unauthorized',
    'Forbidden',
    'NotFound',
    'UnsupportedMediaType',
    'InternalServerError',
    'ServiceUnavailable'
)

# Exception Hierarchy:
# ValorantError
# `-- HTTPException
#     |-- BadRequest
#     |-- Unauthorized
#     |-- Forbidden
#     |-- NotFound
#     |-- UnsupportedMediaType
#     |-- InternalServerError
#     `-- ServiceUnavailable

class ValorantError(Exception):
    """
    Base class for all exceptions raised by this package.
    
    Attributes
    ----------
    message: Optional[:class:`str`]
        The error message, if any.
    """
    __slots__: Tuple[str, ...] = ()
    
    def __init__(self, message: Optional[str], *args, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)
        
        self.message = message


class HTTPException(ValorantError):
    """
    Raised when a process invoking the API returns a non-200 HTTP status code.
    
    Attributes
    ----------
    response: :class:`aiohttp.ClientResponse`
        The response from the API.
    data: Optional[Union[:class:`dict`, :class:`str`]]
        The response data, if any.
    """
    __slots__: Tuple[str, ...] = (
        'response',
        'data',
        'message'
    )
    
    def __init__(
        self, 
        response: ClientResponse,
        data: Optional[Union[Dict[str, Any], str]],
        *,
        message: Optional[str] = None
    ) -> None:
        self.response: ClientResponse = response
        self.data: Optional[Union[Dict[str, Any], str]] = data
        self.message: Optional[str] = message


class BadRequest(HTTPException):
    """
    This error indicates that there is a syntax error in the request 
    and the request has therefore been denied. The client should not 
    continue to make similar requests without modifying the syntax 
    or the requests being made.
    """
    pass


class Unauthorized(HTTPException):
    """
    This error indicates that the request being made did not contain the necessary 
    authentication credentials (e.g., an API key) and therefore the client was denied access. 
    The client should not continue to make similar requests without including an API key in the request.
    
    Common Reasons:
    
    - An API key has not been included in the request.
    """
    pass


class Forbidden(HTTPException):
    """
    This error indicates that the server understood the request but refuses to authorize it. There is 
    no distinction made between an invalid path or invalid authorization credentials (e.g., an API key). 
    The client should not continue to make similar reque.
    
    Common Reasons:
    
    - An invalid API key was provided with the API request.
    - A blacklisted API key was provided with the API request.
    - The API request was for an incorrect or unsupported path.
    """
    pass


class NotFound(HTTPException):
    """
    This error indicates that the server has not found a match for the API request being made. 
    No indication is given whether the condition is temporary or permanent.
    
    Common Reasons:
    
    - The ID or name provided does not match any existing resource (e.g., there is no Summoner matching the specified ID).
    - There are no resources that match the parameters specified.
    """
    pass


class UnsupportedMediaType(HTTPException):
    """
    This error indicates that the server is refusing to service the request because the
    body of the request is in a format that is not supported.

    Common Reasons

    - The Content-Type header was not appropriately set.
    """
    pass


class InternalServerError(HTTPException):
    """
    This error indicates an unexpected condition or exception which 
    prevented the server from fulfilling an API request.
    """
    pass


class ServiceUnavailable(HTTPException):
    """
    This error indicates the server is currently unavailable to handle requests because of an unknown reason. 
    The Service Unavailable response implies a temporary condition which will be alleviated after some delay.
    """
    pass


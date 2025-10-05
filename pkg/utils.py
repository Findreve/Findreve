from typing import Any, NoReturn, TYPE_CHECKING

from fastapi import HTTPException

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_501_NOT_IMPLEMENTED,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_504_GATEWAY_TIMEOUT, HTTP_402_PAYMENT_REQUIRED,
)

if TYPE_CHECKING:
    from sqlmodel.ext.asyncio.session import AsyncSession


# --- Request and Response Helpers ---

def ensure_request_param(to_check: Any, detail: str) -> None:
    """
    Ensures a parameter exists. If not, raises a 400 Bad Request.
    This function returns None if the check passes.
    """
    if not to_check:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=detail)

def raise_bad_request(detail: str = '') -> NoReturn:
    """Raises an HTTP 400 Bad Request exception."""
    raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=detail)

def raise_not_found(detail: str) -> NoReturn:
    """Raises an HTTP 404 Not Found exception."""
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=detail)

def raise_internal_error(detail: str = "服务器出现故障，请稍后再试或联系管理员") -> NoReturn:
    """Raises an HTTP 500 Internal Server Error exception."""
    raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

def raise_forbidden(detail: str) -> NoReturn:
    """Raises an HTTP 403 Forbidden exception."""
    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=detail)

def raise_unauthorized(detail: str) -> NoReturn:
    """Raises an HTTP 401 Unauthorized exception."""
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=detail)

def raise_conflict(detail: str) -> NoReturn:
    """Raises an HTTP 409 Conflict exception."""
    raise HTTPException(status_code=HTTP_409_CONFLICT, detail=detail)

def raise_too_many_requests(detail: str) -> NoReturn:
    """Raises an HTTP 429 Too Many Requests exception."""
    raise HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS, detail=detail)

def raise_not_implemented(detail: str = "尚未支持这种方法") -> NoReturn:
    """Raises an HTTP 501 Not Implemented exception."""
    raise HTTPException(status_code=HTTP_501_NOT_IMPLEMENTED, detail=detail)

def raise_service_unavailable(detail: str) -> NoReturn:
    """Raises an HTTP 503 Service Unavailable exception."""
    raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=detail)

def raise_gateway_timeout(detail: str) -> NoReturn:
    """Raises an HTTP 504 Gateway Timeout exception."""
    raise HTTPException(status_code=HTTP_504_GATEWAY_TIMEOUT, detail=detail)

def raise_insufficient_quota(detail: str = "积分不足，请充值") -> NoReturn:
    raise HTTPException(status_code=HTTP_402_PAYMENT_REQUIRED, detail=detail)

# --- End of Request and Response Helpers ---

from functools import wraps
import traceback
from typing import Any, Callable, TypeVar

T = TypeVar('T')

def with_snackbar_err_popup(status_handle):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)

            except Exception as e:
                error_message = f"error: {str(e)}"
                status_handle.pop(error_message)

                traceback.print_exc()
                return None

        return wrapper
    return decorator
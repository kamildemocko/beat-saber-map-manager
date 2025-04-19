from functools import wraps
import traceback
from typing import Any, Callable, TypeVar

from beat_saber_map_manager.ui.status import StatusUI

T = TypeVar('T')

def with_snackbar_err_popup(status_handle: StatusUI):
    """Decorator to handle exceptions and show a snackbar error popup.

    Args:
        status_handle (StatusUI): The status handle to show the snackbar error popup.
    """
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
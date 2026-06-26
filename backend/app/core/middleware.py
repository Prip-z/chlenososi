from functools import wraps
import warnings

from dependency_injector.wiring import DIWiringWarning, inject as di_inject
from loguru import logger

from app.services.base_service import BaseService


def inject(func):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DIWiringWarning)
        injected_func = di_inject(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = injected_func(*args, **kwargs)
        injected_services = [arg for arg in kwargs.values() if isinstance(arg, BaseService)]
        if len(injected_services) == 0:
            return result
        else:
            try:
                injected_services[-1].close_scoped_session()
            except Exception as e:
                logger.error(e)

        return result

    return wrapper

import asyncio
import inspect
import warnings
from functools import wraps

from dependency_injector.wiring import DIWiringWarning, inject as di_inject
from loguru import logger

from app.services.base_service import BaseService


def inject(func):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DIWiringWarning)
        injected_func = di_inject(func)

    # Проверяем, является ли оборачиваемая функция асинхронной (async def)
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await injected_func(*args, **kwargs)  # Честно дожидаемся выполнения!
            
            # Закрываем сессию СУБД после выполнения логики
            injected_services = [arg for arg in kwargs.values() if isinstance(arg, BaseService)]
            if injected_services:
                try:
                    injected_services[-1].close_scoped_session()
                except Exception as e:
                    logger.error(f"Ошибка закрытия асинхронной сессии: {e}")
            return result
        return async_wrapper

    else:
        # Старая синхронная логика для обычных def функций
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            result = injected_func(*args, **kwargs)
            injected_services = [arg for arg in kwargs.values() if isinstance(arg, BaseService)]
            if injected_services:
                try:
                    injected_services[-1].close_scoped_session()
                except Exception as e:
                    logger.error(f"Ошибка закрытия синхронной сессии: {e}")
            return result
        return sync_wrapper
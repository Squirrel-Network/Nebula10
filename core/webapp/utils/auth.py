import functools
import typing

from core.utilities.token_jwt import decode_jwt


def auth_required(func: typing.Callable):
    @functools.wraps(func)
    def wrapper(token: str, *args, **kwargs):
        if token_verify := decode_jwt(token):
            return func(token=token_verify, *args, **kwargs)

        return "Error!"

    return wrapper

from functools import wraps
from time import perf_counter
from typing import Any, Tuple


def time_me(repeats: int=1) -> Tuple[Any, float]:
    '''Decorator that runs a piece of code multiple times and returns **AVERAGE** time taken
    
    Output is a tuple with two values*:
    0: The result of the timed function
    1: The AVERAGE time of each iteration

    *Should be called a Twople?
    '''
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            dt0 = perf_counter()
            for _ in range(repeats):
                result = func(*args, **kwargs)
            dt1 = perf_counter()
            return result, (dt1 - dt0) / repeats
        return inner
    return outer

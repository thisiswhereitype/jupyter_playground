# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_core.ipynb.

# %% auto 0
__all__ = ['DownloadContent', 'attachment_download', 'IncrementalPipeline']

# %% ../00_core.ipynb 3
import dataclasses
import sys
from typing import Any, Callable, Union, List


import joblib
import joblib.memory
import requests as rq
from fastcore.all import *
from tqdm import tqdm


# %% ../00_core.ipynb 5
@dataclasses.dataclass
class DownloadContent:
    """
    Masks the __repr__ with the content's hash to avoid serialising a large string.
    This is useful to stop joblib serialising large json files.
    """

    content: bytes

    def __repr__(self):
        return joblib.hash(self.content)


# %% ../00_core.ipynb 6
class MemoryStandin:
    def cache(self, func):
        return func


# %% ../00_core.ipynb 7
if __name__ != "__main__":
    if sys.platform == "linux":
        cache = joblib.Memory(
            "/mnt/d/.joblib", verbose=0, compress=True, bytes_limit=int(200e9)
        )
    if sys.platform == "win32":
        cache = joblib.Memory(
            "D:\.joblib", verbose=0, compress=True, bytes_limit=int(200e9)
        )
    cache.reduce_size()
else:
    if in_jupyter():
        cache = joblib.Memory(verbose=1, compress=True)
    else:
        cache = MemoryStandin()


# %% ../00_core.ipynb 9
@cache.cache
def attachment_download(href):
    res = rq.get(href)
    res.raise_for_status()
    return DownloadContent(res.content)


# %% ../00_core.ipynb 10
class IncrementalPipeline:
    """
    A class whose instances can dynamically store functions.
    When used as a callable i.e. `pipe(*args)` the functions are called in turn and returned objects
    are passed as args into each successive function. Results are wrapped as tuples if needed.
    """

    def __init__(self, name: str, funcs: List[Callable] = None) -> None:
        self._name = name
        self._funcs = L(funcs)
        self._fuse_cache = None

    def __repr__(self) -> str:
        return f"{IncrementalPipeline.__name__}(name='{self._name}', _funcs={[f.__name__  for f in self._funcs]})"

    def decorate_func(self, func):
        self.append_func(func)
        return func

    def append_func(self, *funcs: List[Callable]):
        self._funcs += funcs
        return self

    def __getitem__(self, idx: Union[int, slice, Iterable]):
        return IncrementalPipeline(self._name, self._funcs[idx])

    def __call__(
        self,
        *args: list[Any],
        tqdm_position: int | None = 0,
        **init_kwargs: dict[Any, Any],
    ):
        try:
            for i, f in tqdm(enumerate(self._funcs), leave=False, position=tqdm_position):
                if not i:
                    res = f(*args, **init_kwargs)
                else:
                    res = f(*res)
                res = res if is_listy(res) else (res,)
        except (ValueError, TypeError) as e:
            raise ValueError(f'{i}: When calling "{f}", args: {args}') from e

        if isinstance(res, (tuple, fastuple)):
            # unwrap redundant tuple
            return res if res.__len__() > 1 else res[0]
        else:
            return res

    @delegates(tqdm)
    def run_group(
        self,
        job_args: Iterable[Tuple[Any]],
        init_kwargs: Dict[str, Any] = None,
        **kwargs,
    ):
        with tqdm(enumerate(job_args), **{**dict(desc="Jobs"), **kwargs}) as ti:
            for _, arg in ti:
                yield self(
                    *arg,
                    **{
                        **dict(
                            init_kwargs=dict() if init_kwargs is None else init_kwargs,
                            tqdm_position=1,
                        ),
                        **kwargs,
                    },
                )


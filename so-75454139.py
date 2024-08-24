#! /usr/bin/env python

"""
https://stackoverflow.com/questions/75454139/creating-and-activating-a-virtual-environment-using-a-python-script
"""


from functools import wraps
import os
import site
import sys
import glob
# from io import StringIO
from io import BytesIO
from pathlib import Path
import subprocess
import sys
import os
import shutil
from typing import List, Callable, TypeVar, ParamSpec, TypeAlias, Optional, Union, Iterator, Iterable, Dict
from types import CodeType, ModuleType
from venv import EnvBuilder
import importlib.util
import zipfile


##
# globals
##

T: TypeVar = TypeVar('T')
P: ParamSpec = ParamSpec('P')
Function: TypeAlias = Callable[P, T]
Wrapper: TypeAlias = Function
Decorator: TypeAlias = Callable[[Function,], Wrapper]
JSON: TypeAlias = Union[str, List['JSON'], Dict[str, 'JSON']]


##
# bootstrap
##

def get_venv() -> Optional[str]:
    """
    https://fann.im/blog/2023/07/26/how-to-know-im-using-venv-python/
    https://discuss.python.org/t/determining-if-code-is-running-in-a-venv/26862/5
    """
    my_venv: Optional[str] = os.getenv('VIRTUAL_ENV')

    is_venv: bool = (my_venv is not None)

    venv_ck: bool = (sys.prefix != sys.base_prefix)

    assert (is_venv == venv_ck)
    return my_venv


def split_path(envvar: str) -> List[str]:
    envstr: str = os.getenv(envvar, "")
    return envstr.split(os.pathsep)


def join_path(envvar: str, *paths: str) -> None:
    assert paths
    os.environ[envvar] = os.pathsep.join(paths)


def prepend_path(bin_dir: str) -> None:
    old_path: List[str] = split_path('PATH')
    # prepend bin to PATH (this file is inside the bin directory)
    join_path('PATH', bin_dir, *old_path)


def activate_venv(env_dir: str) -> None:
    """
    https://stackoverflow.com/questions/25020451/no-activate-this-py-file-in-venv-pyvenv
    https://github.com/usernein/activate-virtualenv/blob/main/src/activate_virtualenv/activate_virtualenv.py
    """

    base: Path = Path(env_dir).resolve()
    assert base.is_dir()
    bin_dir: Path = base / 'bin'
    assert bin_dir.is_dir()

    prepend_path(str(bin_dir))

    # virtual env is right above bin directory
    os.environ["VIRTUAL_ENV"] = str(base)

    # os.environ["VIRTUAL_ENV_PROMPT"] = ("__VIRTUAL_PROMPT__" or os.path.basename(base))  # noqa: SIM222
    os.environ["VIRTUAL_ENV_PROMPT"] = base.stem

    # add the virtual environments libraries to the host python import mechanism
    prev_length = len(sys.path)

    libs: List[str] = split_path('__LIB_FOLDERS__')
    # assert (prev_length == len(libs)), f'oops: prev_length={prev_length}, libs={len(libs)}'

    decode: Optional[str] = os.getenv('__DECODE_PATH__', None)

    for lib in libs:
        path = os.path.realpath(os.path.join(bin_dir, lib))
        site.addsitedir(path.decode("utf-8") if decode else path)

    sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

    sys.real_prefix = sys.prefix
    sys.prefix = base

    venv_ck: str = get_venv()
    assert isinstance(venv_ck, str)
    assert (Path(venv_ck) == Path(env_dir).resolve()
            ), f'oops: venv_ck={venv_ck}, env_dir={env_dir}'


def ensure_venv(env_dir: str = 'venv') -> str:
    my_venv: Optional[str] = get_venv()
    if (my_venv is not None):
        return my_venv
    assert (my_venv is None)
    builder: EnvBuilder = EnvBuilder(with_pip=True)
    builder.create(env_dir)
    activate_venv(env_dir)
    return env_dir

##
# refuse to run outside venv
##

def main()->None:
    """
    https://stackoverflow.com/questions/21641405/replace-a-running-python-script-with-os-execl
    https://stackoverflow.com/questions/4025442/what-does-os-execl-do-exactly-why-am-i-getting-this-error
    """
    my_venv: str = ensure_venv()
    shell:str = os.getenv('SHELL', 'bash')
    os.execvp(shell, ['-i',])

if __name__ == '__main__':
    main()

__author__:str = 'you.com'


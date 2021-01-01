"""Architecture Patterns with Python - 4장 프로젝트."""
from typing import Callable, Any

from typing import Callable, Any
from contextlib import AbstractContextManager

import sys
import inspect
import traceback

from sqlalchemy.orm.session import Session
import pytest

VIOLET = '\033[95m'
ENDC = '\033[0m'
BOLD = '\033[1m'

ScopedSession = AbstractContextManager[Session]


class mytest:
    """Simple test runner for Jupyter Notebook."""
    module = None

    @classmethod
    def init(cls, mod_name: str) -> None:
        cls.module = sys.modules[mod_name]

    @classmethod
    def unit(cls, func: Callable[..., Any]) -> Callable[..., Any]:
        assert cls.module, "mytest.init(mod_name) should be called before a test"

        try:
            args = inspect.getfullargspec(func).args
            argvals = []
            attrs = dir(cls.module)
            for arg in args:
                assert arg in attrs, f'name "{arg}" should be defined in the module'
                fixture = getattr(cls.module, arg)
                assert callable(
                    fixture), f'name "{arg}" should be a callable fixture'
                argvals.append(fixture())

            func(*argvals)  # 함수를 정의할때 바로 실행되도록
            print(f'✅ {VIOLET}{func.__name__}{ENDC}')
        except:
            traceback.print_exc(limit=-1)
        finally:
            # 함수 실행이 실패해도 함수 정의는 그대로 리턴하도록
            return func

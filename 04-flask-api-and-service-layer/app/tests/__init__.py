"""테스트 기본 설정 및 헬퍼 함수를 정의합니다."""
from typing import Callable, Any, Optional
import os, sys, inspect, traceback, types

FAIL = '\033[91m'
VIOLET = '\033[95m'
ENDC = '\033[0m'
BOLD = '\033[1m'

_AnyFunc = Callable[..., Any]

class mytest:
    """pytest 를 흉내내는 간단한 Jupyter Notebook용 테스트 러너 입니다. """
    modules = {}
    tests = {}
        
    @classmethod
    def fixture(cls, func: _AnyFunc) -> _AnyFunc:
        cls.modules[func.__name__] = func
        return func
        
    @classmethod
    def run(cls, func) -> Any:
        assert func in cls.tests, \
               f'{func} should be registered with `@unit` decorator first'
        cls.tests[func]()

    @classmethod
    def test(cls, func) -> _AnyFunc:
        def unit():
            cleanups = []

            def unwrap(func):
                argvals = []
                fixnames: list[str] = inspect.getfullargspec(func).args

                for fixname in fixnames:
                    assert fixname in cls.modules, \
                           f'name "{fixname}" should be registered first with @mytest.fixture' 

                    fixfunc = cls.modules[fixname]
                    fixargs = inspect.getfullargspec(fixfunc).args

                    if not fixargs: # 인자가 없는 fixture라면
                        val = fixfunc()
                        if isinstance(val, types.GeneratorType):
                            argvals.append(next(val))
                            cleanups.append(val)
                        else:
                            argvals.append(val)
                    else: # 인자가 있을경우 재귀적으로 반복합니다.
                        argvals.append(unwrap(fixfunc))

                val = func(*argvals)
                if isinstance(val, types.GeneratorType):
                    cleanups.append(val)
                    return next(val)
                else:
                    return val
                    
            try:
                unwrap(func)
                print(f'✅ {VIOLET}{func.__name__}{ENDC}', flush=True)
            except:
                print(f'❌ {FAIL}{func.__name__}{ENDC}', flush=True)
                traceback.print_exc(limit=-1); sys.stderr.flush()
            finally: # 함수 실행이 실패해도 함수 정의는 그대로 리턴하도록
                for gen in cleanups:
                    try:
                        next(gen)
                    except StopIteration:
                        pass
                return func
            
        cls.tests[func] = unit
        return unit()
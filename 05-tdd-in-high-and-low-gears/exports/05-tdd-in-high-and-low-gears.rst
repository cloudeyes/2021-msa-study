.. raw:: html

   <center style="font-size: 16px; font-weight: normal">

\`21 Microservices Architecture Patterns Study

.. raw:: html

   </center>

.. raw:: html

   <center>

.. raw:: html

   <h1>

Chapter 5. TDD in High and Low Gears

.. raw:: html

   </h1>

.. raw:: html

   </center>

.. raw:: html

   <center>

Joseph Kim <cloudeyes@gmail.com> Jab 12. 2021

.. raw:: html

   </center>

.. raw:: html

   <center>

.. raw:: html

   </center>

.. raw:: html

   <center>

Download Jupyter Notebook

.. raw:: html

   </center>

Introduction
============

TDD Terms
---------

**Test Pyramid** - …

**Test Double** - …

Difference between Various Kinds of Testing
-------------------------------------------

**Unit testing** means testing individual modules of an application in
isolation (without any interaction with dependencies) to confirm that
the code is doing things right.

**Integration testing** means checking if different modules are working
fine when combined together as a group.

**Functional testing** means testing a slice of functionality in the
system (may interact with dependencies) to confirm that the code is
doing the right things.

Integration Tests vs Functional Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Functional tests are related to integration tests, however, they signify
to the tests that check the entire application’s functionality with all
the code running together, nearly *a super integration test*.

*See also*: - `Unit Testing Vs Integration Testing Vs Functional
Testing <https://www.softwaretestinghelp.com/the-difference-between-unit-integration-and-functional-testing/>`__

.. code:: ipython3

    !mypy -p app --strict


.. parsed-literal::

    app/config.py:4: [1m[31merror:[m Skipping analyzing 'sqlalchemy.pool': found module but no type hints or library stubs[m
    app/config.py:42: [1m[31merror:[m Name 'sqlalchemy' is not defined[m
    app/adapters/repository.py:7: [1m[31merror:[m Skipping analyzing 'sqlalchemy.orm': found module but no type hints or library stubs[m
    app/adapters/orm.py:12: [1m[31merror:[m Skipping analyzing 'sqlalchemy': found module but no type hints or library stubs[m
    app/adapters/orm.py:12: [34mnote:[m See [4mhttps://mypy.readthedocs.io/en/latest/running_mypy.html#missing-imports[m
    app/adapters/orm.py:14: [1m[31merror:[m Skipping analyzing 'sqlalchemy.pool.base': found module but no type hints or library stubs[m
    app/adapters/orm.py:15: [1m[31merror:[m Skipping analyzing 'sqlalchemy.engine': found module but no type hints or library stubs[m
    app/adapters/orm.py:16: [1m[31merror:[m Skipping analyzing 'sqlalchemy.orm': found module but no type hints or library stubs[m
    app/adapters/orm.py:22: [1m[31merror:[m Skipping analyzing 'sqlalchemy.orm.session': found module but no type hints or library stubs[m
    app/apps/flask.py:16: [1m[31merror:[m Function is missing a type annotation for one or more arguments[m
    app/apps/flask.py:17: [1m[31merror:[m Skipping analyzing 'sqlalchemy.orm': found module but no type hints or library stubs[m
    app/apps/flask.py:35: [1m[31merror:[m Function is missing a return type annotation[m
    app/apps/flask.py:46: [1m[31merror:[m Cannot find implementation or library stub for module named 'app.routes'[m
    [1m[31mFound 12 errors in 4 files (checked 25 source files)[m


.. code:: ipython3

    !pytest app/tests


.. parsed-literal::

    [1m============================= test session starts ==============================[0m
    platform linux -- Python 3.9.1, pytest-6.1.2, py-1.10.0, pluggy-0.13.1
    rootdir: /home/ykkim/notebooks/2021-msa-study/05-tdd-in-high-and-low-gears
    plugins: flask-1.1.0, anyio-2.0.2
    collected 25 items                                                             [0m
    
    app/tests/e2e/test_flask_api.py [32m.[0m[32m                                        [  4%][0m
    app/tests/integration/test_orm.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m                                 [ 28%][0m
    app/tests/integration/test_repository.py [32m.[0m[32m.[0m[32m                              [ 36%][0m
    app/tests/unit/test_allocate.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m                                     [ 52%][0m
    app/tests/unit/test_batch.py [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m                                   [ 88%][0m
    app/tests/unit/test_services.py [32m.[0m[32m.[0m[32m.[0m[32m                                      [100%][0m
    
    [32m============================== [32m[1m25 passed[0m[32m in 0.76s[0m[32m ==============================[0m


.. code:: ipython3

    !pylint app


.. parsed-literal::

    ************* Module app.__main__
    app/__main__.py:2:10: C0303: Trailing whitespace (trailing-whitespace)
    app/__main__.py:6:0: C0305: Trailing newlines (trailing-newlines)
    app/__main__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    app/__main__.py:2:0: W0611: Unused import sys (unused-import)
    app/__main__.py:2:0: C0411: standard import "import sys" should be placed before "from .apps.flask import init_app" (wrong-import-order)
    ************* Module app.config
    app/config.py:50:0: C0305: Trailing newlines (trailing-newlines)
    app/config.py:42:35: E0602: Undefined variable 'sqlalchemy' (undefined-variable)
    ************* Module app.domain.__init__
    app/domain/__init__.py:1:0: C0304: Final newline missing (missing-final-newline)
    ************* Module app.domain
    app/domain/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    ************* Module app.domain.models
    app/domain/models.py:11:4: W0107: Unnecessary pass statement (unnecessary-pass)
    app/domain/models.py:17:4: C0103: Attribute name "id" doesn't conform to snake_case naming style (invalid-name)
    app/domain/models.py:64:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/domain/models.py:69:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/domain/models.py:73:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/domain/models.py:76:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/domain/models.py:95:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/domain/models.py:101:8: W0707: Consider explicitly re-raising using the 'from' keyword (raise-missing-from)
    app/domain/models.py:4:0: W0611: Unused NewType imported from typing (unused-import)
    ************* Module app.tests.conftest
    app/tests/conftest.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    app/tests/conftest.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/tests/conftest.py:18:4: C0415: Import outside toplevel (sqlalchemy.pool.StaticPool) (import-outside-toplevel)
    app/tests/conftest.py:19:4: C0415: Import outside toplevel (sqlalchemy.orm.sessionmaker) (import-outside-toplevel)
    app/tests/conftest.py:20:4: C0415: Import outside toplevel (sqlalchemy.create_engine) (import-outside-toplevel)
    app/tests/conftest.py:21:4: C0415: Import outside toplevel (adapters.orm.metadata, adapters.orm.start_mappers, adapters.orm.clear_mappers) (import-outside-toplevel)
    app/tests/conftest.py:21:4: W0611: Unused clear_mappers imported from adapters.orm (unused-import)
    app/tests/conftest.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/tests/conftest.py:38:13: W0621: Redefining name 'get_session' from outer scope (line 33) (redefined-outer-name)
    app/tests/conftest.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/tests/conftest.py:43:11: W0621: Redefining name 'get_session' from outer scope (line 33) (redefined-outer-name)
    app/tests/conftest.py:45:4: W0621: Redefining name 'server' from outer scope (line 43) (redefined-outer-name)
    app/tests/conftest.py:43:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/tests/conftest.py:43:11: W0613: Unused argument 'get_session' (unused-argument)
    app/tests/conftest.py:54:14: W0621: Redefining name 'get_repo' from outer scope (line 38) (redefined-outer-name)
    app/tests/conftest.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/tests/conftest.py:71:25: W0212: Access to a protected member _allocations of a client class (protected-access)
    app/tests/conftest.py:72:12: W0212: Access to a protected member _allocations of a client class (protected-access)
    app/tests/conftest.py:1:0: W0611: Unused Optional imported from typing (unused-import)
    app/tests/conftest.py:1:0: W0611: Unused Callable imported from typing (unused-import)
    app/tests/conftest.py:2:0: W0611: Unused date imported from datetime (unused-import)
    app/tests/conftest.py:2:0: W0611: Unused timedelta imported from datetime (unused-import)
    app/tests/conftest.py:3:0: W0611: Unused import uuid (unused-import)
    app/tests/conftest.py:6:0: W0611: Unused import requests (unused-import)
    app/tests/conftest.py:9:0: W0611: Unused SessionMaker imported from adapters.orm (unused-import)
    ************* Module app.tests.__init__
    app/tests/__init__.py:102:0: C0304: Final newline missing (missing-final-newline)
    ************* Module app.tests
    app/tests/__init__.py:4:0: C0410: Multiple imports on one line (os, sys, inspect, traceback, types) (multiple-imports)
    app/tests/__init__.py:18:0: C0103: Class name "mytest" doesn't conform to PascalCase naming style (invalid-name)
    app/tests/__init__.py:24:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/tests/__init__.py:29:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/tests/__init__.py:35:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/tests/__init__.py:61:16: R1705: Unnecessary "else" after "return" (no-else-return)
    app/tests/__init__.py:70:12: W0702: No exception type(s) specified (bare-except)
    app/tests/__init__.py:80:16: W0150: return statement in finally block may swallow exception (lost-exception)
    app/tests/__init__.py:86:0: C0115: Missing class docstring (missing-class-docstring)
    app/tests/__init__.py:87:4: C0415: Import outside toplevel (flask.Flask) (import-outside-toplevel)
    app/tests/__init__.py:100:4: C0116: Missing function or method docstring (missing-function-docstring)
    ************* Module app.tests.unit.__init__
    app/tests/unit/__init__.py:3:0: C0304: Final newline missing (missing-final-newline)
    ************* Module app.tests.unit
    app/tests/unit/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    ************* Module app.apps.fastapi
    app/apps/fastapi.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    app/apps/fastapi.py:1:0: W0611: Unused Optional imported from typing (unused-import)
    ************* Module app.apps.flask
    app/apps/flask.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    app/apps/flask.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/apps/flask.py:17:4: C0415: Import outside toplevel (sqlalchemy.orm.sessionmaker) (import-outside-toplevel)
    app/apps/flask.py:19:4: W0603: Using the global statement (global-statement)
    app/apps/flask.py:19:4: C0103: Constant name "get_session" doesn't conform to UPPER_CASE naming style (invalid-name)
    app/apps/flask.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/apps/flask.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/apps/flask.py:40:4: W0603: Using the global statement (global-statement)
    app/apps/flask.py:40:4: C0103: Constant name "app" doesn't conform to UPPER_CASE naming style (invalid-name)
    app/apps/flask.py:46:4: W0621: Redefining name 'flask' from outer scope (line 4) (redefined-outer-name)
    app/apps/flask.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/apps/flask.py:46:4: C0415: Import outside toplevel (routes.flask) (import-outside-toplevel)
    app/apps/flask.py:47:4: W0603: Using the global statement (global-statement)
    app/apps/flask.py:47:4: C0103: Constant name "get_session" doesn't conform to UPPER_CASE naming style (invalid-name)
    app/apps/flask.py:46:4: W0611: Unused flask imported from routes (unused-import)
    app/apps/flask.py:1:0: W0611: Unused Tuple imported from typing (unused-import)
    app/apps/flask.py:4:0: W0611: Unused import flask (unused-import)
    ************* Module app.services.batch
    app/services/batch.py:10:0: C0115: Missing class docstring (missing-class-docstring)
    app/services/batch.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
    app/services/batch.py:2:0: W0611: Unused Protocol imported from typing (unused-import)
    app/services/batch.py:6:0: W0611: Unused Batch imported from domain.models (unused-import)
    ************* Module app.services.__init__
    app/services/__init__.py:1:0: C0304: Final newline missing (missing-final-newline)
    ************* Module app.services
    app/services/__init__.py:1:0: C0114: Missing module docstring (missing-module-docstring)
    ************* Module app.adapters.orm
    app/adapters/orm.py:37:2: W0511: TODO: 설명을 좀더 자세하게 적어주세요. (fixme)
    ************* Module app.adapters.repository
    app/adapters/repository.py:26:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/adapters/repository.py:30:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/adapters/repository.py:34:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/adapters/repository.py:38:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/adapters/repository.py:42:4: C0116: Missing function or method docstring (missing-function-docstring)
    app/adapters/repository.py:53:8: C0103: Attribute name "db" doesn't conform to snake_case naming style (invalid-name)
    app/adapters/repository.py:51:0: C0115: Missing class docstring (missing-class-docstring)
    
    ------------------------------------------------------------------
    Your code has been rated at 7.31/10 (previous run: 7.26/10, +0.06)
    
    [0m

How is our Test Pyramid Looking?
================================

.. code:: ipython3

    !grep -c test_ -R app/tests | grep -vE ':0|.pyc|.ipynb'


.. parsed-literal::

    app/tests/unit/test_batch.py:9
    app/tests/unit/test_allocate.py:4
    app/tests/unit/test_services.py:3
    app/tests/conftest.py:2
    app/tests/integration/test_orm.py:6
    app/tests/integration/test_repository.py:2
    app/tests/e2e/test_flask_api.py:1


.. code:: ipython3

    def show_test_pyramid(counts, svg_width=400, svg_height=150, 
                          margin_left=150, margin_right=0,
                          margin_top=10, margin_bottom=10):
        from IPython.display import SVG
    
        e2e, intg, unit = [counts.get(it, 0) for it in ('e2e', 'integration', 'unit')]
        max_cnt = max(counts.values())
        max_cnt
        
        width = svg_width - margin_left - margin_right
        height = svg_height - margin_top - margin_bottom
    
        unit_width = width // max_cnt
        unit_height = height // 2
    
        bottom_left = margin_left + (width - unit_width*unit)//2, unit_height*2 + margin_top
        bottom_right = bottom_left[0]+unit_width*unit, unit_height*2 + margin_top
    
        mid_left = margin_left + (width - unit_width*intg)//2, unit_height*1 + margin_top
        mid_right = mid_left[0] + unit_width*intg, unit_height*1 + margin_top
    
        top_left = margin_left + (width - unit_width*e2e)//2, unit_height*0 + margin_top
        top_right = top_left[0] + unit_width*e2e, unit_height*0 + margin_top
        
        points = f'{bottom_left} {mid_left} {top_left} {top_right} {mid_right} {bottom_right}'
        points = points.replace('(', '').replace(')', '').replace(', ', ',')
        
        svg_output = f'''
        <svg width="{svg_width}" height="{svg_height}">
          <polygon points="{points}" 
           style="fill:none;stroke:black;stroke-width:2"/>
           <text x="{0}" y="{bottom_left[1]-5}">unit: {unit}</text>
           <text x="{0}" y="{mid_left[1]+margin_top-10}">integration: {intg}</text>
           <text x="{0}" y="{top_left[1]+margin_top}">e2e: {e2e}</text>
        </svg>
        '''
    
        return SVG(svg_output)

.. code:: ipython3

    from subprocess import Popen, PIPE, STDOUT
    from collections import defaultdict
    proc = Popen("grep -c test_ -R app/tests | grep -vE ':0|conftest|.pyc|.ipynb'", shell=True, stdout=PIPE)
    output = proc.stdout.read().decode().strip()
    stats = defaultdict(lambda: 0)
    for k, v in (it.split(':') for it in output.split('\n')):
        stats[k.split('/')[2]] += int(v)
    dict(stats)




.. parsed-literal::

    {'unit': 16, 'integration': 8, 'e2e': 1}



.. code:: ipython3

    show_test_pyramid(stats)




.. image:: 05-tdd-in-high-and-low-gears_files/05-tdd-in-high-and-low-gears_11_0.svg



역 피라미드 (아이스크림 콘) 테스트 예
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    show_test_pyramid(counts = {
        'e2e': 30,
        'integration': 20,
        'unit': 10,
    })




.. image:: 05-tdd-in-high-and-low-gears_files/05-tdd-in-high-and-low-gears_13_0.svg



Should Domain Layer Tests Move to the Service Layer?
====================================================

Problems can happen from *too many* tests against their domain model. -
Sometime they *DO NOT reflect properties of a system*, but only
low-level implementation of a system. - If we want to change *the design
of our code*, any tests relying directly on the code will also fail.

따라서, 테스트를 서비스 레이어에 한정 지어서 감춰진 메소드나
속성으로부터 깨지기 쉬운 테스트를 보호하는 것이 좋습니다.

On Deciding What Kind of Tests to Write
=======================================

모든 유닛 테스트를 서비스 계층에 대해 재작성 해야 할까요? 도메인 모델에
직접 테스트 하는건 잘못된 것일까요? 이런 질문에 답하기 위해 테스트
종류에 따른 트레이드 오프를(테스트 스펙트럼) 이해해야 합니다.

테스트의 목적은 변경에 대한 피드백을 얻기 위함입니다. 테스트가 실제
구현에 가까울 수록 더 좁은 영역에 대한 강한 피드백을 얻게 됩니다. 높은
단계의 추상화에 가까울 수록 테슽는 대규모 변경에 대한 넓은 피드백
커버리지를 얻게 됩니다.

서비스 계층에 대한 테스트(API 테스트)는 특정 구현에 종속되지 않은
시스템의 특성을 체크하고 대규모 변경에 대한 자신감을 얻기 위해
사용합니다.

특히 도메인 테스트에 대한 피드백은 시스템 세부사항에 대한 즉각적이고
강력한 피드백을 주어 시스템을 이해하는데 큰 도움을 줍니다. 즉, 도메인
테스트는 도메인 언어로 쓰여진 일종의 “살아있는 문서” 역할을 합니다.

신규 프로젝트를 수행하여 아직 도메인에 대해서 잘 알지 못할 경우 “도메인
모델에 대한 테스트”는 시스템의 이해를 돕고 실제 코드를 어덯게 작성할지
감을 찾는데 매우 효과적입니다.

한편 도메인에 대한 이해가 충분히 되고, 설계 개선이 필요하다고 판단되면
세부 구현에 종속된 이런 테스트들을 API 레벨로 교체할 필요가 있습니다.

High Gear(저속 기어) and Low Gear(고속 기어)
============================================

기존 기능을 확장하거나 버그 수정을 할 경우, 도메인 모델의 수정이 거의
필요하지 않다면 효과적으로 달리기 위해 고속 기어(서비스 레벨 테스트)를
놓고 달립니다.

하지만 처음 프로젝트를 시작해서 도메인을 잘 모르거나, 중요하고 어려운
작업을 신중하게 수행해야 할 경우 저속 기어(도메인 레벨 테스트)로
전환하여 어려움을 극복할 수 있습니다.

Fully Decoupling the Service-Layer Tests from the Domain
========================================================


Mitigation: Keep All Domain Dependencies in Fixture Functions
-------------------------------------------------------------


Adding a Missing Service
------------------------


Carrying the Improvment Through to the E2E Tests
================================================


Wrap-Up
=======


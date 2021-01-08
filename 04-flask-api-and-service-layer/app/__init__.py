"""Architecture Patterns with Python - 4장 프로젝트."""
from typing import Callable, Any

from typing import Callable, Any
from contextlib import AbstractContextManager


def livereload_doc() -> None:
    """파이썬 코드와 rst 파일이 변경될 때 자동으로 문서를 빌드하고 브라우저를 리프레시 합니다.

    실행 방법:

    .. code-block:: bash

        $ python -c "import app; app.livereload_doc()"
    """
    from livereload import Server, shell
    server = Server()
    server.watch('app/**/*.py', shell('make html', cwd='docs'))
    server.watch('docs/*.rst', shell('make html', cwd='docs'))
    server.serve(root='docs/_build/html')

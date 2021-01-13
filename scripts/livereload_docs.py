"""파이썬 코드 문서화 스크립트."""

from livereload import Server, shell


def main() -> None:
    """파이썬 코드와 rst 파일이 변경될 때 자동으로 문서를 빌드하고 브라우저를 리프레시 합니다.

    실행 방법:

    .. code-block:: bash

        $ python -m "scripts.livereload_docs"
    """
    server = Server()
    server.watch('src/app/**/*.py', shell('make -W -b html', cwd='src/doc'))
    server.watch('src/doc/**/*.rst', shell('make -W -b html', cwd='src/doc'))
    server.watch('src/doc/**/*.rst', shell('make -W -b html', cwd='src/doc'))
    server.serve(root='src/doc/_build/html', host='0.0.0.0')


if __name__ == '__main__':
    main()

# 4장: Flask API 와 서비스 계층

## 소개

4장 실습 가이드와 Visual Studio Code IDE용 예제 프로젝를를 제공합니다.

책 저자의 프로젝트 구조를 제 취향에 맞는 현실적인 형태로 수정했습니다.

- 작성자: Joseph Kim \<cloudeyes@gmail.com\>

## 시작하기

1. 적한한 가상환경을 활성화하세요. (예: `conda activate lab`)
1. 필요한 파이썬 패키지를 설치하세요

   ```
   pip install -r app/requirements.txt
   ```

1. 테스트를 실행하세요.

   ```
   pytest app
   ```

   또는

   ```
   ptw app         # 소스코드의 변경이 발생되면 자동으로 테스트 재시작하기
   ```

1. 자동으로 빌드되는 문서를 보시면서 코멘트를 다음으세요.

   ```
   python -m scripts.livereload_doc
   ```

## 빌드 방법

### 문서 빌드하기

- `docs/build.sh` : 문서를 빌드합니다.
- `python -m

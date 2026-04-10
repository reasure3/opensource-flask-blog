프로젝트 가이드
================

개요
----

Flask Study Notes Service는 테스트 가능한 Flask API를 중심으로 만든 작은
포트폴리오 프로젝트입니다. 노트 목록 조회, 노트 상세 조회, 노트 생성, 그리고
브라우저에서 직접 입력할 수 있는 작성 페이지를 제공합니다. 입력 검증 규칙은
서버와 클라이언트가 같은 기준을 공유하도록 구성되어 있습니다.

주요 특징
---------

* ``Flask``가 HTTP 애플리케이션과 라우트 등록을 담당합니다.
* ``Flasgger``가 docstring에 작성된 OpenAPI 명세를 읽어 Swagger UI를 보여줍니다.
* ``Sphinx``가 Python docstring과 문서 페이지를 바탕으로 정적 HTML 기술 문서를 생성합니다.
* 노트 저장소는 의도적으로 in-memory 방식으로 유지하여, 데이터베이스보다
  요청 처리 흐름과 문서화 구조에 집중할 수 있게 했습니다.

애플리케이션 흐름
-----------------

1. ``app.create_app`` 이 Flask 앱, Swagger UI, 서비스 객체들을 연결합니다.
2. ``NoteController`` 가 HTTP 요청을 받아 서비스 계층 호출과 응답 형태를 담당합니다.
3. ``NoteService`` 가 입력 검증과 in-memory 노트 저장 로직을 담당합니다.
4. ``NoteFormSpec`` 이 ``/write`` 페이지에서 사용할 클라이언트 검증 규칙을 제공합니다.

문서 및 화면 진입점
-------------------

* 인터랙티브 API 문서: ``/apidocs/``
* JSON API 엔드포인트: ``/``, ``/home``, ``/health``, ``/notes``, ``/notes/<id>``,
  ``/api/notes``
* 브라우저 작성 페이지: ``/write``

문서 빌드 방법
--------------

로컬에서 의존성을 설치한 뒤 HTML 문서를 생성할 수 있습니다.

.. code-block:: bash

   pip install -r requirements.txt
   sphinx-build -b html docs docs/_build/html

생성된 결과물은 ``docs/_build/html`` 폴더에 저장됩니다.

# Mini Project – Flask Study Notes Service

## 1. 프로젝트 개요

본 프로젝트는 **Git의 브랜치 전략, 기능 개발 흐름, 테스트 후 병합 과정**을 연습하기 위한 Mini Project이다.  
Flask를 사용하여 간단한 REST API 형태의 노트 조회 서비스를 구현하였다.

이 프로젝트의 목적은 웹 서비스 자체의 완성도가 아니라 다음과 같은 **Git 활용 과정**을 실습하는 것이다.

- Git 저장소 초기화
- 기능별 브랜치(feature branch) 생성
- 기능 구현 후 로컬 테스트
- main 브랜치로 병합(merge)
- GitHub 원격 저장소에 push

---

## 2. 요구사항 분석

### 2.1 기능 요구사항 (Functional Requirements)

본 서비스는 다음 기능을 제공한다.

1. 사용자는 홈 엔드포인트를 통해 서비스 정보를 확인할 수 있다.
2. 사용자는 노트 목록을 조회할 수 있다.
3. 사용자는 특정 노트의 상세 내용을 조회할 수 있다.
4. 사용자는 서버 상태 확인용 엔드포인트를 사용할 수 있다.

### 2.2 비기능 요구사항 (Non-functional Requirements)

- Python Flask 기반으로 실행되어야 한다.
- 로컬 환경에서 `flask run` 또는 `python app.py`로 실행 가능해야 한다.
- 브라우저 또는 `curl`을 이용한 수동 테스트가 가능해야 한다.
- Git feature branch 기반으로 기능을 분리하여 개발해야 한다.

---

## 3. API 엔드포인트

| Endpoint       | 설명       |
|----------------|----------|
| `/` 또는 `/home` | 서비스 소개   |
| `/notes`       | 노트 목록 조회 |
| `/notes/<id>`  | 특정 노트 조회 |
| `/health`      | 서버 상태 확인 |

---

## 4. 프로젝트 구조
```
flask-blog/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```


| 파일               | 설명                          |
|------------------|-----------------------------|
| app.py           | Flask 애플리케이션 및 API 엔드포인트 구현 |
| requirements.txt | 프로젝트 실행에 필요한 Python 패키지     |
| README.md        | 프로젝트 설명 및 실행/테스트 방법         |

---

## 5. 실행 방법

### 5.1 패키지 설치

```bash
pip install -r requirements.txt.txt
```

### 5.2 서버 실행

```bash
python app.py
```
또는
```bash
flask run
```

서버 실행 후 기본 주소:
```url
http://127.0.0.1:5000
```

---

## 6. 테스트 방법

### curl 테스트

```bash
curl http://127.0.0.1:5000/home
curl http://127.0.0.1:5000/notes
curl http://127.0.0.1:5000/notes/1
curl http://127.0.0.1:5000/notes/999
curl http://127.0.0.1:5000/health
```

### 예상 결과

| 요청           | 결과                      |
|--------------|-------------------------|
| `/home`      | 서비스 정보 JSON 반환          |
| `/notes`     | 노트 목록 반환                |
| `/notes/1`   | 특정 노트 반환                |
| `/notes/999` | 404 오류                  |
| `/health`    | `{ "status": "ok" }` 반환 |

---

## 7. Git Workflow

본 프로젝트는 **Feature Branch Workflow**를 사용하였다.

개발 과정:

1. 프로젝트 초기화
2. 기능별 브랜치 생성
3. 기능 구현 후 로컬 테스트
4. Pull Request 생성
5. Rebase 후 main 브랜치에 병합

사용한 브랜치:
```txt
feature/home
feature/notes
feature/health
docs/readme-update
```

---

## 8. 개발 환경

- Python 3.x
- Flask
- Git
- GitHub
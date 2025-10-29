# 💰 거래내역 조회 앱 (Finance Tracker)

> Django + HTMX + Plotly 기반의 개인 재무 관리 웹 애플리케이션  
> 카테고리별 수입/지출 내역을 시각화하고, 효율적으로 관리할 수 있도록 만든 프로젝트입니다.

---

## 📋 프로젝트 개요
이 프로젝트는 사용자의 거래 내역을 효율적으로 기록하고,  
**카테고리별 통계 차트**를 통해 재무 패턴을 시각적으로 파악할 수 있도록 구현한 웹 앱입니다.  

기존의 단순한 CRUD 가계부 기능을 넘어,  
HTMX를 활용해 페이지 전체 리로드 없이 데이터를 갱신하고,  
Plotly를 통해 데이터 시각화를 직관적으로 표현한 것이 특징입니다.

---

## 🚀 주요 기능
| 기능 | 설명 |
|------|------|
| 💸 **수입/지출 등록 및 관리** | 거래 내역을 카테고리별로 등록/수정/삭제 가능 |
| 📊 **카테고리별 금액 시각화** | Plotly Pie / Bar Chart를 이용한 통계 시각화 |
| 🔍 **필터 및 검색 기능** | 기간별, 카테고리별 필터링 기능 (Django FilterSet) |
| ⚡ **HTMX 비동기 처리** | 일부 섹션만 동적으로 갱신, Spinner로 로딩 표시 |
| 🧾 **사용자 인증 기능** | Django 기본 인증 기반 회원가입, 로그인/로그아웃 |
| 🧪 **테스트 코드 포함** | pytest 기반 단위/뷰 테스트 작성 |

---

## 🧩 기술 스택
- **Backend:** Django 4.2, Django ORM, Pytest  
- **Frontend:** HTMX, TailwindCSS, Plotly.js  
- **DB:** SQLite (개발용)  
- **Template Engine:** Django Templates + Custom Templatetags  
- **Others:** Factory Boy (테스트 데이터 생성), Django Filter

---

## 🏗️ 프로젝트 구조
finance_project/
├── finance_project/
│ ├── settings.py # 전역 설정
│ ├── urls.py # 전체 URL 라우팅
│ └── templates/account/ # 로그인/회원가입 템플릿
│
└── tracker/
├── models.py # Category, Transaction 모델
├── views.py # 주요 비즈니스 로직
├── urls.py # tracker 관련 URL 라우팅
├── charting.py # Plotly 차트 데이터 생성 로직
├── filters.py # Django Filter 기반 거래내역 필터링
├── forms.py # 거래 내역 입력 폼
├── managers.py # QuerySet 헬퍼
├── templates/
│ ├── charts.html # 카테고리별 시각화 페이지
│ └── index.html # 거래 내역 목록
├── templatetags/
│ └── custom_filter.py # 사용자 정의 템플릿 필터
├── tests/
│ ├── test_views.py
│ ├── test_models.py
│ └── conftest.py
└── admin.py

---

## ⚙️ 실행 방법
```bash
# 1. 가상환경 설정 및 진입
python -m venv venv
source venv/bin/activate  # (Windows는 venv\Scripts\activate)

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 마이그레이션 및 실행
python manage.py migrate
python manage.py runserver

서버 실행 후
👉 http://127.0.0.1:8000/ 접속
```

---

## 💡 설계 포인트
-HTMX 활용: Django 템플릿 기반에서도 SPA 수준의 가벼운 비동기 UX 구현
-ORM Aggregation 최적화: annotate, aggregate, Sum 등을 활용한 효율적 집계
-테스트 주도 개발: pytest + Factory Boy를 이용한 단위 테스트 기반 개발

---

## 🧭 배운 점 & 회고
HTMX를 통해 Django에서도 React 수준의 인터랙션을 구현할 수 있음을 체험
ORM 집계 함수와 queryset 최적화에 대한 이해 심화
데이터 시각화(Plotly)를 통해 단순 CRUD를 넘는 “사용자 중심” 인터페이스를 고민하게 됨
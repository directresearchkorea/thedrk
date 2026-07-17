# Recruitment Lead‑Generation Crawler – PRD

## 1. Project Overview
- **Goal**: 자동으로 서울 내 ‘배달 비중이 높거나 24시간 영업’인 한·일식 식당 정보를 수집하고 CSV 로 저장하여, 프리미엄 HTML 대시보드에서 필터·다운로드 할 수 있게 한다.
- **Target Users**: 마케팅·리쿠르팅 팀, 현장 인터뷰를 진행할 영업 담당자.
- **Scope**: 네이버 로컬 검색 + 배달의민족/쿠팡이츠 보강 (구글은 보조용). 데이터는 `restaurants.csv` 로 출력.

## 2. Folder Structure
```
recruitment_crawler/
│   PRD.md                 # ← 현재 문서 (정리된 사양)
│   requirements.txt        # Python 의존성
│   run_crawler.bat         # Windows 배치 실행 스크립트
│
├───crawler/
│       main.py            # 핵심 크롤러 (Playwright 비동기) 
│       keywords.json       # 카테고리‑키워드 매핑 파일
│
├───data/                  # 실행 시 자동 생성
│       raw_data.json       # 첫 단계 원본 JSON
│       restaurants.csv     # 최종 정제 CSV (UTF‑8‑SIG)
│
└───logs/                  # 실행 로그 (crawl.log)
```

## 3. Prerequisites (다른 컴퓨터에서도 동일하게)
1. **OS**: Windows 10/11 (PowerShell 또는 CMD) – 경로는 `C:\Users\<your>\Desktop\inven-pulse\recruitment_crawler` 로 동일하면 된다.
2. **Python**: 3.11+ (설치 시 `python` 명령어가 PATH에 포함되어야 함).
3. **Internet**: 네이버·배달앱에 접근 가능해야 함 (방화벽/프록시 차단 없음).
4. **디스크 권한**: 해당 폴더에 파일 생성/수정 권한.

## 4. Setup Instructions
```bat
:: 1️⃣ Clone / copy this folder to the target machine
::    (예: Git clone 또는 USB 복사)

:: 2️⃣ Open a command prompt in the folder
cd C:\Users\<your>\Desktop\inven-pulse\recruitment_crawler

:: 3️⃣ Run the provided batch script – it will:
::    - create a virtual environment (venv)
::    - install all Python packages from requirements.txt
::    - download Playwright Chromium binary
::    - execute the crawler script
run_crawler.bat
```
*첫 실행 시 Playwright가 Chromium을 다운로드하므로 1‑2 분 정도 소요됩니다.*

### 4‑1. Manual alternative (if you prefer manual steps)
```bash
python -m venv venv            # virtual env 생성
venv\Scripts\activate          # 활성화 (PowerShell: .\venv\Scripts\Activate.ps1)
pip install -r requirements.txt # 의존성 설치
python -m playwright install chromium  # 브라우저 바이너리
python crawler\main.py          # 크롤러 실행
```

## 5. How the Crawler Works
1. **키워드 로드** – `crawler/keywords.json` 에 정의된 카테고리·하위 카테고리·키워드 배열을 읽는다.
2. **네이버 로컬 검색** – 각 키워드마다 `"{키워드} 배달 맛집 서울"` 로 Naver 검색 URL을 만든 뒤 Playwright 로 페이지를 로드한다.
3. **무한스크롤** – 5 번 페이지 끝까지 스크롤하여 더 많은 결과를 로드한다 (필요 시 횟수 조정).
4. **DOM 파싱** – `div.place_section li._place_item` 요소에서 식당명, 주소, 전화번호를 추출한다.
5. **데이터 조합** – 카테고리·하위 카테고리·키워드와 함께 `result` 딕셔너리 형태로 저장.
6. **원본 JSON 저장** – `data/raw_data.json` 에 전체 리스트를 기록 (디버깅용).
7. **정제 & 중복 제거** – pandas 로 DataFrame 변환 → `식당명`·`주소` 조합 중복 제거.
8. **CSV 출력** – UTF‑8‑SIG 로 `data/restaurants.csv` 저장 (Excel/Google Sheets 호환).
9. **로그** – `logs/crawl.log` 에 진행 상황 및 오류 기록.

### 5‑1. 주요 필드 (CSV 열)
| 열 이름 | 내용 |
|---------|------|
| 식당종류 | "한식" 또는 "일식" |
| 상권 | 주소에서 추출한 구(예: 강남구) |
| 식당명 | 매장 명 |
| 업종 상세 카테고리 | 선술집·정식·면요리·일반·해물 등 |
| 주소 | 전체 도로명 주소 |
| 대표 전화번호 | 전화번호 문자열 |
| 주요 메뉴 리스트 | 사용된 키워드 (예: "돈카츠") |
| 영업 시간 | 현재는 빈 문자열 – 현장 방문 시 추가 가능 |
| 배달 여부 | 기본 "Y" – 배달앱 보강 시 수정 가능 |

## 6. Extending / Enhancing
| 목표 | 방법 |
|------|------|
| **배달앱 평점·리뷰** | `fetch_restaurants` 안에 배민·쿠팡이츠 검색 로직 추가 (식당명으로 검색 → 페이지 파싱 → `rating`, `review_count` 추출). |
| **24시간 영업 태그** | 주소·전화만으로 판단이 어려우면, `배달앱` 상세 페이지에서 `"24시간"` 텍스트 여부 확인 후 `영업 시간` 컬럼에 "24시" 입력. |
| **구글 CSE 보조** | `google_search(query)` 함수 (예시 코드) 추가 → 결과 URL 로 다시 파싱. |
| **프록시/우회** | Playwright `browser.new_context(proxy={"server":"http://ip:port"})` 로 적용. |
| **UI 대시보드** | 별도 프로젝트 (HTML/JS) 에서 `fetch('data/restaurants.csv')` 로 로드 → 필터·CSV 다운로드 구현 (앞서 제시한 마크업/스크립트 참고). |

## 7. Troubleshooting
- **Playwright 설치 오류** – `pip install -U pip setuptools` 후 재시도.
- **Chromium 다운로드 실패** – 프록시/네트워크 차단 여부 확인 후 `python -m playwright install chromium --ignore-https-errors` 시도.
- **네이버 구조 변경** – `main.py` 의 CSS 선택자를 최신 구조에 맞게 업데이트 (`div._place_item` 등).
- **중복 데이터 많음** – `df.drop_duplicates(subset=['식당명', '주소'], inplace=True)` 로 조정 가능.
- **로그 확인** – `logs/crawl.log` 에 Timestamp 로 기록되며, 오류 시 `ERROR:` 라인 확인.

## 8. Deliverables
1. `data/restaurants.csv` – 최종 리쿠르팅 DB (UTF‑8‑SIG).
2. `data/raw_data.json` – 원본 수집 결과 (디버깅 용).
3. `logs/crawl.log` – 실행 로그.
4. (선택) `dashboard.html` – 프리미엄 필터·다운로드 UI (별도 프로젝트로 관리).

---
**End of PRD**

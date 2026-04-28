# 4×4 Magic Square — 구현·UI·커버리지 업데이트 보고서

**내보내기일:** 2026-04-28  
**문서 목적:** 이번 작업 세션에서 반영된 구현(Logic/Boundary), GUI(Screen), 테스트 보강, 커버리지 결과를 `Report/`에 고정 기록한다.  
**관련 문서:** [`docs/PRD.md`](../docs/PRD.md), [`README.md`](../README.md), [`07_Magic_Square_Test_Case_Specification_Report.md`](07_Magic_Square_Test_Case_Specification_Report.md)

---

## 1) 작업 개요

이번 업데이트는 다음 4가지를 목표로 진행했다.

1. Domain/Boundary 계약 구현 보강 (`solve`, 검증 파이프라인, 마방진 판정)
2. PyQt6 기반 Screen 레이어 MVP 추가 (`magicsquare/gui/`)
3. 테스트 케이스(TC) 보강으로 Domain/Boundary 커버리지 상향
4. `pytest-cov` 및 HTML 커버리지 리포트(`htmlcov/index.html`) 생성 체계 정착

---

## 2) 코드 변경 내역

### 2.1 Domain (`magicsquare/domain.py`)

- 유지: `find_blank_coords` (row-major, 0-based)
- 추가:
  - `is_magic_square`
  - `solve_grid`
  - 내부 누락값 계산 로직(`_sorted_missing_pair`)
- 계약 반영:
  - 매직 합 `MAGIC_SUM` 기준 행/열/대각선 검증
  - 성공 반환 형식: `[r1,c1,n1,r2,c2,n2]` (좌표 1-index)
  - 실패 시 `ValueError(MSG_NO_SOLUTION)`

### 2.2 Boundary (`magicsquare/boundary.py`)

- 유지: `validate_grid_shape`, `validate_empty_cell_count`
- 추가:
  - `validate_value_range`
  - `validate_no_duplicate_nonzero`
  - `validate_all` (shape → empty count → range → duplicate)
  - `solve` (경계 검증 후 Domain 위임)

### 2.3 Constants (`magicsquare/constants.py`)

- 추가 상수:
  - `CELL_MIN`, `CELL_MAX`, `MAGIC_SUM`
  - `MSG_VALUE_RANGE`, `MSG_DUPLICATE`, `MSG_NO_SOLUTION`

### 2.4 Screen / GUI (`magicsquare/gui/`)

- 추가 파일:
  - `magicsquare/gui/__init__.py`
  - `magicsquare/gui/window.py`
  - `magicsquare/gui/__main__.py`
- 구현 내용(MVP):
  - 4×4 입력(`QSpinBox`, 0~16)
  - 「풀기」 버튼 클릭 시 Boundary `solve` 호출
  - 오류 시 `QMessageBox` 표시
  - 성공 시 6원소 결과 표시
- 공식 실행 경로:
  - `python -m magicsquare.gui`

### 2.5 패키지/문서 설정

- `pyproject.toml`
  - `dev`에 `pytest-cov` 추가
  - `gui` optional dependency에 `PyQt6` 추가
  - coverage 설정(`tool.coverage.run`, `tool.coverage.html`) 추가
- `README.md`
  - GUI 실행 안내 추가
  - 커버리지 HTML 생성 명령 추가
  - 최신 커버리지 스냅샷 섹션 추가
- `.gitignore`
  - `htmlcov/` 추가

---

## 3) 테스트 보강 내역

### 신규/보강 테스트 파일

- `tests/test_magic_contract_solver.py`

### 추가된 테스트 범주

- Boundary:
  - 값 범위 위반(`VALUE_RANGE`)
  - 비영 중복(`DUPLICATE`)
  - `validate_all` 파이프라인
  - `solve` 경계 위임
- Domain:
  - `is_magic_square` 정상/실패 분기(빈칸, 행합 오류, 대각선 분기)
  - `solve_grid` 정방향 성공/역방향 성공/해 없음(`NO_SOLUTION`)
  - 반대 대각선 분기 미커버 보완 TC 추가

---

## 4) 실행 결과 (최신)

실행 명령:

```bash
python -m pytest tests --cov=magicsquare --cov-report=term-missing --cov-report=html -q
```

결과 요약:

- 테스트: **21 passed, 1 skipped**
- 커버리지 합계(`magicsquare`): **72%**
- 파일별:
  - `magicsquare/domain.py`: **100%**
  - `magicsquare/boundary.py`: **100%**
  - `magicsquare/constants.py`: **100%**
  - `magicsquare/gui/__main__.py`: **0%**
  - `magicsquare/gui/window.py`: **0%**

HTML 리포트:

- `htmlcov/index.html`

---

## 5) 확인 메모

- Domain은 UI/프레임워크 의존 없이 유지됨(순수 로직).
- Qt import는 `magicsquare/gui/` 하위에만 위치.
- GUI 자동화 테스트는 이번 범위에서 제외했으며, 총 커버리지의 잔여 부족분은 GUI 모듈 미테스트에 기인함.

---

## 6) 다음 권장 작업

1. `pytest-qt` 기반 GUI smoke test 2~3개 추가(윈도우 생성, 버튼 클릭, 오류 메시지 경로)
2. CI에서 `--cov-fail-under` 기준을 Domain/Boundary 우선으로 단계 도입
3. 보고서(`README`, 본 파일) 커버리지 스냅샷 날짜 동기화 유지


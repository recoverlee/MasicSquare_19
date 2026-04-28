# MagicSquare 코드 분석 보고서

## 1) 테스트 현황 점검

- `test_*.py` 파일은 이미 존재:
  - `tests/test_magic_contract_solver.py`
  - `tests/test_red_l01_u01.py`
  - `tests/test_u_red_02_empty_count.py`
  - `tests/test_red_failure_demo.py`
- 결론:
  - `domain.py`, `boundary.py`는 기본 테스트가 있음
  - GUI 계층(`magicsquare/gui/window.py`) 테스트는 상대적으로 보강 필요

## 2) 테스트 없이 리팩토링을 시작하면 안 되는 이유

- 테스트가 없으면 회귀(regression) 발생 시 깨진 지점을 즉시 감지할 안전망이 없어 변경 신뢰도가 크게 떨어진다.

## 3) Code Smell 분석 결과

> 참고: 요청된 `gui/main_window.py`는 저장소에 없고, 실제 파일은 `magicsquare/gui/window.py`.

| 파일명 | 줄번호 | 스멜 종류 | 문제 설명 | 우선순위 |
|---|---:|---|---|---|
| `magicsquare/domain.py` | 70-97 | 긴 함수 (20줄 초과) | `solve_grid()`가 빈칸 탐색, 누락값 계산, 시도 전략, 결과 포맷, 예외 처리까지 담당 | 높음 |
| `magicsquare/boundary.py` | 44-62 | 중복 코드 | `validate_value_range()`와 `validate_no_duplicate_nonzero()`에 유사 2중 순회 로직 반복 | 중간 |
| `magicsquare/gui/window.py` | 23-57 | 긴 함수 (20줄 초과) | `MainWindow.__init__()`에 UI 초기화 책임이 과도하게 집중 | 높음 |
| `magicsquare/gui/window.py` | 36 | 하드코딩된 매직 넘버 | `setMinimumWidth(52)`의 `52` 의미가 코드에 드러나지 않음 | 중간 |
| `magicsquare/gui/window.py` | 64 | 이해하기 힘든 이름 | `out` 변수명이 결과 의미를 충분히 설명하지 못함 | 낮음 |
| `magicsquare/gui/window.py` | 66 | 하드코딩/인덱스 의존 | `out[0]..out[5]` 직접 접근으로 의미 파악/유지보수 어려움 | 중간 |

## 4) ECB(Entity-Control-Boundary) 관점 분석

### 파일별 현재 역할

- `domain.py`:
  - **Control 중심**
  - 비즈니스 규칙 실행(`is_magic_square`, `solve_grid`)
  - Entity는 명시적 클래스 없이 `list[list[int]]`로 표현됨
- `boundary.py`:
  - **Boundary 역할 적합**
  - 입력 검증 + 도메인 호출 책임 수행
- `magicsquare/gui/window.py`:
  - 주로 UI지만 `_on_solve()`에서 호출 오케스트레이션/결과 포맷/예외 처리까지 함께 수행

### 위치 조정 후보

- `domain.py`의 결과 포맷(1-index 변환 + 6개 벡터 형태)은 Boundary/Application 성격이 강함
- `window.py`의 결과 벡터 문자열 조립은 Presenter/Boundary helper로 이동 가능

### Entity/Control 분리 포인트(`domain.py`)

- Entity 후보:
  - 격자 상태
  - 빈칸 좌표 계산
  - 누락 수 계산
  - 정사각형 판정
- Control 후보:
  - 배치 시도 순서/전략
  - 실패 처리
- 방향:
  - `MagicSquare`(Entity) + `MagicSquareSolver`(Control) 분리 고려

## 5) SRP(단일 책임 원칙) 점검 결과

- 위반 의심:
  - `magicsquare/domain.py:70-97` (`solve_grid`)
  - 다중 책임(탐색 + 전략 + 포맷 + 예외)
- 해당 없음:
  - 데이터 보관+검증 동시 담당 클래스 (클래스 자체 없음)
  - UI에서 직접 비즈니스 계산/판단 (`if total == 34` 형태 없음)

## 6) 리팩토링 계획서

## 리팩토링 대상 목록 (우선순위 순)

| 순번 | 대상 파일 | 문제 | 적용 기법 | 우선순위 |
|---:|---|---|---|---|
| 1 | `magicsquare/domain.py` | `solve_grid()` 다중 책임/긴 함수 | 함수 분해(Extract Function), 결과 포맷 책임 분리, Application/Boundary로 매핑 이동 | 높음 |
| 2 | `magicsquare/gui/window.py` | `MainWindow.__init__()` 과도한 책임 집중 | UI 구성 메서드 분리(`_build_grid`, `_build_actions`, `_build_result`) | 높음 |
| 3 | `magicsquare/gui/window.py` | 결과 벡터 인덱스 의존/매직넘버 | 의미 있는 구조(튜플/DTO) 도입 또는 포맷 helper 추출 | 중간 |
| 4 | `magicsquare/boundary.py` | 반복 순회 로직 중복 | 공통 순회 유틸/검증 파이프라인 정리 | 중간 |
| 5 | `magicsquare/gui/window.py` | `52` 하드코딩 값 | 상수화(예: `SPINBOX_MIN_WIDTH`) | 중간 |
| 6 | `magicsquare/gui/window.py` | 의미 약한 변수명(`out`) | 의도 드러나는 이름으로 변경 | 낮음 |

## 테스트 선행 필요 항목

- 리팩토링 전에 우선 테스트 추가 권장 함수:
  - `magicsquare/gui/window.py`의 `_on_solve()`
  - `magicsquare/gui/window.py`의 `_read_matrix()`
  - `magicsquare/domain.py`의 `solve_grid()` 출력 포맷 계약(1-index 및 순서)
  - `magicsquare/boundary.py`의 `solve()` 경계-도메인 연결 계약

## 리팩토링 후 검증 방법

- 회귀 테스트 실행 명령어:
  - `pytest -q`
  - `pytest -q tests/test_magic_contract_solver.py tests/test_red_l01_u01.py tests/test_u_red_02_empty_count.py`
- 외부 동작 불변 확인:
  - 동일 입력 매트릭스에 대해 `boundary.solve()` 반환 벡터가 리팩토링 전후 동일한지 Golden Case 비교
  - GUI에서 성공 시 결과 라벨 형식(`[r1, c1, n1, r2, c2, n2]`) 유지 확인
  - GUI에서 실패 시 동일 메시지(`ValueError` 메시지) 표시 확인

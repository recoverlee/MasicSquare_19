# MagicSquare (4×4)

**Invariant 기반 사고·Dual-Track TDD·입출력 계약·ECB 계층 분리**를 연습하는 학습용 프로젝트입니다.  
부분적으로 비어 있는 **4×4** 마방진(고전: 1~16 각 1회, 행·열·두 대각 합 **34**)에서 빈칸 두 곳을 채워 완성합니다.

**요구·검수·로드맵의 단일 기준(SSoT)** 은 [`docs/PRD.md`](docs/PRD.md)입니다.

---

## 문서 관계 (한 줄)

[`Report/05_Magic_Square_PRD_Report.md`](Report/05_Magic_Square_PRD_Report.md)는 [`docs/PRD.md`](docs/PRD.md)와 **동기 본**입니다. 요구 본문은 `docs/PRD.md`와 동일하게 유지하고, 갱신 시 **한쪽을 기준으로 정한 뒤** 다른 쪽을 맞춥니다(05에는 해설·매핑 절을 추가할 수 있음).

| 목적 | 참조 |
|------|------|
| 제품 목표·범위·I/O·오류·NFR·Done | **[`docs/PRD.md`](docs/PRD.md)** |
| Epic·여정·User Story·Gherkin | [`Report/04_Magic_Square_Epic_to_Technical_Scenarios.md`](Report/04_Magic_Square_Epic_to_Technical_Scenarios.md) |
| 입력·출력 계약·레이어·Traceability | [`Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md`](Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md) |
| ECB·TDD·테스트 관례(전사 규칙 요약) | [`Report/03_Magic_Square_Cursor_Rules_Report.md`](Report/03_Magic_Square_Cursor_Rules_Report.md) |
| 문제 정의(관찰·Why) | [`Report/01_Magic_Square_Problem_Definition_Report.md`](Report/01_Magic_Square_Problem_Definition_Report.md) |
| 실행·에디터 규칙(원본) | [`.cursorrules`](.cursorrules) |

---

## 프로젝트 목표 (PRD 요약)

| 구분 | 내용 |
|------|------|
| **Epic** | Invariant(불변조건) 기반 사고 훈련 시스템 구축 |
| **제품(코드) 목표** | `0`이 정확히 2칸인 4×4 격자에 대해 누락된 두 수를 규칙에 따라 첫/둘째 빈칸에 배치해 마방진이 되면, **`int[6]`** `[r1,c1,n1,r2,c2,n2]`(좌표 **1-index**)로 반환한다. 잘못된 입력·무해(해 없음)는 스펙된 오류로 알린다. |

도메인 규칙·범위(in/out)의 전체 문구는 [`docs/PRD.md` §5](docs/PRD.md)를 따릅니다.

---

## 사용자 스토리 (Report/4 · PRD §7 정렬)

아래는 [`Report/04_Magic_Square_Epic_to_Technical_Scenarios.md`](Report/04_Magic_Square_Epic_to_Technical_Scenarios.md)의 스토리·Gherkin과 같은 맥락입니다. 상세 시나리오·배경은 Report/4를 참고합니다.

| # | 스토리 요지 | 인수 기준 요지 |
|---|-------------|----------------|
| 1 | 경계에서 4×4 입력 검증 | 크기·빈칸 수·범위·0 제외 중복 위반 시 도메인 미전달 |
| 2 | 빈칸(`0`) 위치 탐색 | row-major 순서로 첫/둘째 빈칸, 정확히 두 좌표 |
| 3 | 1~16 누락 두 수 | 후보 고정(정렬된 `[a,b]`) |
| 4 | 완성 격자 마방진 판정 | 행·열·두 대각 동일(매직 합 34) |
| 5 | 두 배치(정·역) 시도 | 성공 시 6원소·1-index; “역만 성공”은 **A≠B** 픽스처로 검증(Report/4) |

---

## 입출력·오류 계약 요약 (Report/2 · PRD §6)

**입력:** `4×4 int[][]`, `0` = 빈칸(정확히 2개), 값은 `0` 또는 `1~16`, 0이 아닌 값끼리 중복 없음.

**출력(성공):** `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 좌표 1~4. `n1`,`n2`는 누락 두 수이며, (작은수→첫 빈칸, 큰수→둘째)가 마방진이면 그 순서, 아니면 **역** 배치.

**빈칸 순서:** 행·열 오름차순(row-major)으로 앞이 첫 빈칸, 뒤가 둘째 빈칸.

**Boundary `code` / `message` (고정, PRD §6.1):**

| `code` | `message` |
|--------|-----------|
| `SIZE` | `Grid must be 4x4.` |
| `EMPTY_COUNT` | `There must be exactly 2 empty cells (0).` |
| `VALUE_RANGE` | `Each cell must be 0 or in range 1..16.` |
| `DUPLICATE` | `Values 1..16 must not duplicate (excluding zeros).` |
| `NO_SOLUTION` | `No valid placement forms a 4x4 magic square.` |
| `INTERNAL` | `An unexpected error occurred.` |

검증 경로·Invariant-ID·Traceability 표는 [`Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md`](Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md) §1~4를 참고합니다.

---

## 실행·개발 환경 (Report/3 · pyproject.toml · Cursor)

- **언어:** Python 3.10+ · PEP 8 · 타입 힌트 · Google docstring([`Report/03`](Report/03_Magic_Square_Cursor_Rules_Report.md), [`.cursorrules`](.cursorrules)).
- **아키텍처:** ECB — 의존성 `boundary → control → entity` 한 방향([`Report/03`](Report/03_Magic_Square_Cursor_Rules_Report.md) · PRD §9).
- **테스트:** pytest, AAA, `test_` 접두, RED → GREEN → REFACTOR([`Report/03`](Report/03_Magic_Square_Cursor_Rules_Report.md)).
- **`pyproject.toml`:** 의존성·포맷터·pytest·커버리지 등 **실행·품질 설정의 단일 진입점**으로 둡니다. 저장소에 파일이 없으면 추가 시 본 절과 PRD §8·[`Report/03`](Report/03_Magic_Square_Cursor_Rules_Report.md) 기준에 맞춥니다.

```bash
# 저장소 루트에서 (의존성: pip install -e ".[dev]")
python -m pytest tests -v
# PowerShell: .\scripts\run_tests.ps1
# 실패 시: 각 테스트별 FAILED 표시 + 짧은 traceback (--tb=short), 종료 코드 ≠ 0
# RED 단계에서 실패 출력만 확인하려면(의도적 실패 1건):
#   PowerShell: $env:MAGICSQUARE_DEMO_RED="1"; python -m pytest tests/test_red_failure_demo.py -v --tb=short
pytest --cov

# 브라우저용 커버리지 리포트 (저장소 루트에 htmlcov/index.html 생성)
python -m pytest tests --cov=magicsquare --cov-report=html --cov-report=term-missing -q
```

**최신 커버리지 스냅샷 (2026-04-28)**

- 테스트: `21 passed, 1 skipped`
- 패키지 합계(`magicsquare`): **72%**
- `domain.py`: **100%**, `boundary.py`: **100%**, `constants.py`: **100%**
- `gui/__main__.py`, `gui/window.py`: 자동화 테스트 미작성으로 **0%**
- HTML 리포트: `htmlcov/index.html`

**데스크톱 GUI (PyQt6, Screen 레이어):** Qt는 `magicsquare/gui/` 에만 두며, 공식 실행 경로는 아래 한 줄입니다.

```bash
pip install -e ".[gui]"
python -m magicsquare.gui
```

---

## 검증 기준 (PRD §8 · §10)

**비기능·품질([`docs/PRD.md` §8](docs/PRD.md))**

| 항목 | 기준 |
|------|------|
| Domain 로직 커버리지 | **≥95%** |
| 입력 계약 테스트 | **100% 통과**(Epic 기준) |
| 권고(02) | Domain ≥95%, Boundary ≥85%, Data ≥80% |
| 전사 규칙 | 최소 커버리지 **80%** 등([`.cursorrules`](.cursorrules)) |

**Release / Done 체크리스트([`docs/PRD.md` §10](docs/PRD.md))**

- [ ] Epic 성공 기준이 Journey·AC·자동화 테스트와 추적 가능
- [ ] Invariant — 규칙 — 유스케이스 — 계약 — 테스트 ID 매핑(Report/02 Traceability)
- [ ] Positive + 입력 오류 + `NO_SOLUTION` (+ 선택 Data) 시나리오
- [ ] Report/4 Gherkin·Edge(4×4, 빈칸 2, row-major 등) 반영
- [ ] “역시도만 성공”은 **A≠B** 픽스처로 별도 자동화

---

## 구현 To-Do

**추적 방식:** Concept-to-Code — **Task → Req(Invariant/스토리) → Scenario(L0~L3) → Test → Code(ECB)** ([`Report/02`](Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md) Traceability, Dual-Track TDD).

상세 Phase별 체크리스트·변경 이력은 [`docs/MasicSquare_Implementation_TODO.md`](docs/MasicSquare_Implementation_TODO.md)에서 관리한다. 아래는 개발 보드용 **계층형 To-Do**와 **요구 추적 매트릭스**다.

### 완료 정의 (PRD §10 요약)

- [ ] Epic 성공 기준이 Journey·AC·자동화 테스트와 추적 가능하다.
- [ ] Invariant — 규칙 — 유스케이스 — 계약 — 테스트가 매핑 가능하다 (Report/02).
- [ ] 정상 경로 + 입력 오류 + 도메인 무해(`NO_SOLUTION`)가 테스트로 존재한다.
- [ ] “역시도만 성공”은 **A≠B** 픽스처로 별도 검증한다 (Report/04).

### 시나리오 레벨 (Scenario Level)

| 레벨 | 의미 |
|------|------|
| **L0** | 기능 개요·스모크 |
| **L1** | 정상 흐름(Happy path) |
| **L2** | 경계(빈칸 순서, 1/16, row-major 등) |
| **L3** | 실패·거부·무해(`NO_SOLUTION`) |

---

### Epic · User Story · Task (체크리스트)

#### Epic-001 — Magic Square 4×4 완성 시스템

PRD의 제품 목표: 빈칸 2개·누락 두 수·정·역 배치·`int[6]`·Boundary 오류 코드.

---

#### US-001 — 경계 입력 검증 (Boundary)

호출자 입력을 계약에 맞게만 통과시키고, 실패 시 도메인 미호출 ([`docs/PRD.md` §6–7](docs/PRD.md)).

- [ ] **TASK-001** — Boundary 검증 모듈: `SIZE` / `EMPTY_COUNT` / `VALUE_RANGE` / `DUPLICATE` 및 PRD 고정 `message`
  - 대상 코드: `boundary/` (검증만; 비즈니스 규칙 없음)
  - 시나리오: L2/L3 입력 거부 → 단위 테스트에서 Domain Mock **호출 0회**

---

#### US-002 — 보드 Entity·불변식 (MagicSquarePuzzle)

4×4 격자 상태 및 INV-01~03 ([`Report/02`](Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md) §1).

- [ ] **TASK-002** — `MagicSquarePuzzle`(또는 동등 Entity) 생성·불변식: 크기 4×4, `0` 정확히 2칸, 1~16·비중복
  - 연결 테스트(예시 이름): `test_puzzle_rejects_invalid_grid_*`
  - 시나리오: L3 잘못된 보드 거부

---

#### US-003 — 합·마방진 판정 (MagicSquareValidator)

완전히 채운 격자가 행·열·두 대각에서 매직 합 **34**인지 판정 — 첨부 예시의 “합 검증”에 해당하며 클래스명은 Report/02·PRD의 **`MagicSquareValidator`**를 사용한다.

- [ ] **TASK-003** — `MagicSquareValidator`
  - [ ] **TASK-003-1** — **RED:** 완성 마방진 픽스처에서 참 / 한 줄만 훼손 시 거짓 (`test_magic_square_accepts_valid`, `test_magic_square_rejects_invalid_row_sum` 등)
  - [ ] **TASK-003-2** — **GREEN:** 최소 구현으로 위 테스트 통과
  - [ ] **TASK-003-3** — **REFACTOR:** 매직 상수·중복 검사 중복 제거, 관찰 가능 동작 동일

---

#### US-004 — 빈칸 탐색·누락 두 수 (EmptyCellFinder · MissingNumbersFinder)

빈칸 좌표(row-major 첫/둘째), 1~16 중 없는 두 수 ([`docs/PRD.md` §6](docs/PRD.md)).

- [ ] **TASK-004** — `EmptyCellFinder` + `MissingNumbersFinder`
  - 체크포인트: 빈칸 정렬 규칙이 Solver·테스트와 동일한지 전용 테스트로 고정 (L2).
  - **(선택 참고)** 첨부 자료의 “N-Queen”·백트래킹은 **제약 만족 문제 학습용**으로만 참고 가능하다. 본 PRD 스코프는 4×4·빈칸 **2개**로 탐색 공간이 매우 작아 결정적 구현으로 충분하며, PRD는 **알고리즘 효율보다 계약·테스트**를 우선한다 ([`docs/PRD.md` §5.2](docs/PRD.md)).
  - **(선택 NFR)** 회귀 스모크로 상한 시간을 두려면 예: 단일 케이스 **&lt; 100ms**(로컬 CI에서 선택).

---

#### US-005 — 두 배치 솔버 (TwoPlacementSolver)

(작은수→첫 빈칸, 큰수→둘째)와 역배치 시도, 성공 시 `int[6]` 1-index ([`docs/PRD.md` §6](docs/PRD.md)).

- [ ] **TASK-005** — `TwoPlacementSolver` + 무해 시 도메인 결과 타입
  - **RED/GREEN/REFACTOR:** Report/04 픽스처 A(정방향), **A≠B** 픽스처 B(역만 성공), 양쪽 모두 실패 → `NO_SOLUTION` 경로

---

#### US-006 — Control 조율

Boundary 검증 후 Domain 유스케이스 순서만 조율 ([`Report/02`](Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md) §4.1).

- [ ] **TASK-006** — Application/Control 레이어: `trySolve` 파이프라인, Entity에만 규칙 위임

---

#### US-007 — Dual-Track Boundary(UI)·통합

Mock Domain으로 Boundary 단독 RED([`Report/02`](Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md) U-01~U-08).

- [ ] **TASK-007** — Boundary 성공/실패 매핑·`int[6]` 형식 검증
  - 시나리오 예: L1 Boundary + Mock 성공 ([`docs/PRD.md`](docs/PRD.md) 출력 스키마)

---

#### US-008 — 통합·커버리지·(선택) Data

- [ ] **TASK-008** — E2E: 검증 → Domain → `int[6]` / 입력 오류 시 Domain 미실행 ([`Report/02`](Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md) IT-ID)
- [ ] **TASK-009** — 커버리지 게이트: Domain **≥95%**, 입력 계약 **100%**, 전사 최소 **≥80%** ([`docs/PRD.md` §8](docs/PRD.md))
- [ ] **(선택) TASK-010** — Data: `saveSession` / `loadLastSession` / `clear` ([`docs/PRD.md` §5.1](docs/PRD.md))

---

### 요구 추적 매트릭스 (요약)

아래 **테스트 상태** 열은 로컬·CI의 `pytest` 결과에 맞춰 갱신한다 (예: ✅ 통과 · 🔴 RED · ⬜ 미작성).

| Task ID | Req ID | 시나리오 | 테스트 이름(예시) | ECB | 테스트 상태 |
|---------|--------|----------|-------------------|-----|-------------|
| TASK-001 | REQ-BOUND | L3 거부 | `test_boundary_rejects_*`, `test_domain_not_called_on_invalid_input` | Boundary | ⬜ |
| TASK-002 | REQ-INV | L3 거부 | `test_puzzle_rejects_*` | Entity | ⬜ |
| TASK-003 | REQ-VAL | L1/L3 | `test_magic_square_accepts_valid`, `test_magic_square_rejects_invalid_row_sum` | Entity | ⬜ |
| TASK-004 | REQ-FIND | L2 | `test_empty_cells_row_major`, `test_missing_numbers_pair` | Entity | ⬜ |
| TASK-005 | REQ-SOLVE | L1/L2 | `test_solve_fixture_a`, `test_solve_reverse_only_fixture_b`, `test_no_solution_both_fail` | Entity | ⬜ |
| TASK-006 | REQ-UC | L1 | `test_use_case_happy`, `test_use_case_no_solution` | Control | ⬜ |
| TASK-007 | REQ-UI | L1/L3 | `test_boundary_success_mock`, `test_boundary_maps_no_solution` | Boundary | ⬜ |
| TASK-008 | REQ-IT | L1/L3 | `test_integration_e2e`, `test_integration_invalid_skips_domain` | 통합 | ⬜ |

**Req ID 매핑:** `REQ-BOUND` = PRD 경계 검증 · `REQ-INV` = INV-01~03 · `REQ-VAL` = 마방진 판정(INV-04) · `REQ-FIND` = 빈칸·누락 수 · `REQ-SOLVE` = 배치·`int[6]`(INV-06) · `REQ-UC` / `REQ-UI` / `REQ-IT` = Control·Boundary·통합 ([`Report/02`](Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md) §4.5 표와 동기).

---

전체 Phase 요약·체크박스만 필요하면 [`docs/MasicSquare_Implementation_TODO.md`](docs/MasicSquare_Implementation_TODO.md)를 편집한다.

---

## 라이선스

저장소 정책에 따릅니다(미기재 시 프로젝트 유지자에게 확인).

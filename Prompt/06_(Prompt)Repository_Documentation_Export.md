# To-do list creation references
_Exported on 4/28/2026 at 10:58:09 GMT+9 from Cursor (3.2.11)_

---

**User**

to do list를 작성하고 싶습니다. 작성한 문서 중 무엇을 참조해서 만들어야 할까요?

---

**Cursor**

프로젝트 문서를 살펴보고 할 일 목록 작성에 참고할 만한 자료를 찾습니다.



작성하신 문서만 놓고 보면, **할 일 목록(to-do)** 을 만들 때 이렇게 참조하는 것이 맞습니다.

## 우선 참조 (실행 단위로 쪼개기)

1. **`docs/PRD.md`**  
   - 구현·검수·로드맵의 **단일 기준**으로 정리된 제품 요구사항입니다.  
   - 범위(in/out), I/O, 예외 정책 등 **“무엇을 끝내야 하는지”** 를 여기서 가져오면 됩니다.  
   - `Report/05_Magic_Square_PRD_Report.md`는 같은 PRD 본문을 보고서 형태로 둔 것이므로, **한쪽을 기준(SSoT)으로 정하고** 다른 쪽은 그에 맞추면 됩니다(05에 그렇게 적혀 있습니다).

2. **`Report/04_Magic_Square_Epic_to_Technical_Scenarios.md`**  
   - Epic → 여정 → User Story → 기술 시나리오(Gherkin) → 검증·체크리스트까지 **한 흐름**으로 묶인 문서입니다.  
   - **스토리별·시나리오별 체크박스형 할 일**을 만들 때 가장 직접적인 원천입니다.

## 보조 참조 (맥락·품질 기준)

- **`Report/01_Magic_Square_Problem_Definition_Report.md`** — 문제 정의·Why·관찰 (요구가 왜 이런지)  
- **`Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md`** — 계층·Dual-Track TDD 방향 (작업 순서·구조)  
- **`Report/03_Magic_Square_Cursor_Rules_Report.md`** 및 루트 **`.cursorrules`** — 코딩·테스트 관례 (할 일에 “규칙 준수” 항목을 넣을 때)

---

**정리:** 할 일 목록의 **항목 출처**는 **`docs/PRD.md`(또는 그와 동기화된 `05` 보고서)** + **`04` Epic·시나리오 문서**가 중심이고, 나머지는 세부 기준·설명용으로 붙이면 됩니다.

---

**User**

당신은 시니어 소프트웨어 아키텍트이자 TDD 코치입니다. 할 일 목록의 항목과 완료 조건은 docs/5.PRD_MagicSquare_4x4_TDD.md를 주 소스로 두고, 스토리 단위 분해는 Report/4, 계약·오류 세부는 Report/2, 품질·TDD·ECB 준수는 Report/3와 Cursor 규칙을 참조해, 

다음 방법론을 적용하여
"Magic Square 4x4 완성 시스템"의 구현용 To-Do 구조를 작성하세요.

적용 방법론:
- Concept-to-Code Traceability
- Dual-Track UI + Logic TDD
- To-Do → Scenario → Test → Code 구조
- ECB(Entity / Control / Boundary) 모델
- RED → GREEN → REFACTOR

반드시 한국어로 작성하세요.

[시스템 목표]
부분적으로 비어 있는 4x4 Magic Square를 완성하는 시스템의 개발 To-Do를 작성합니다.

[도메인 규칙]
- 보드는 4x4이다.
- 숫자는 1~16만 사용한다.
- 0은 빈칸이다.
- 정확히 2칸이 비어 있다.
- 0을 제외한 중복 숫자는 허용되지 않는다.
- 모든 행, 열, 대각선의 합은 34여야 한다.
- 해결 가능한 경우 빈칸 값을 찾아 채운다.
- 유효하지 않은 보드는 거부한다.

[출력 형식]
다음 구조를 반드시 지켜서 작성하세요.

1. Epic
2. User Story
3. Phase별 Task 목록
4. 각 Task에는 반드시 아래 정보를 포함하세요.
   - Task ID
   - RED / GREEN / REFACTOR 여부
   - 작업 제목
   - Scenario Level (L0/L1/L2/L3)
   - 연결되는 Test 이름
   - 연결되는 Code 대상
   - ECB 스테레오타입 (Entity / Control / Boundary)
   - 필요 시 체크포인트

[표현 스타일]
- Markdown 사용
- 체크박스 형식 사용
- 실제 Cursor.AI 실습용 개발 보드처럼 작성
- 식별자는 Epic-001, US-001, TASK-001 형식 사용
- 유효한 케이스와 실패 케이스를 모두 포함
- 최소한 다음 작업을 포함
  - 보드 생성
  - 보드 유효성 검사
  - 빈칸 탐지
  - 후보값 필터링
  - 완성 로직
  - 잘못된 입력 처리
  - 테스트 커버리지 체크포인트

[Scenario Level 정의]
- L0: 기능 개요
- L1: 정상 흐름
- L2: 경계 상황
- L3: 실패 상황

[추가 제약]
- Logic 책임은 명확히 분리할 것
- UI/Boundary에는 비즈니스 규칙을 넣지 말 것
- Control은 검증과 해결 흐름을 조율할 것
- Entity는 보드 상태를 표현할 것
- 모든 To-Do는 Scenario, Test, Code로 추적 가능해야 함

이제
"Magic Square 4x4 완성 시스템"의 To-Do 구조를 생성하세요

---

**Cursor**

주 소스 문서와 참조 보고서를 읽어 To-Do 구조를 정확히 맞춥니다.



저장소에는 `docs/5.PRD_MagicSquare_4x4_TDD.md`가 없고, 동일한 제품 요구·오류 코드·수용 기준은 `docs/PRD.md`에 정리되어 있습니다. 아래 To-Do는 **주 소스로 `docs/PRD.md`(향후 `docs/5.PRD_MagicSquare_4x4_TDD.md`로 분리·동기화 시 동일 계약)** 를 따릅니다.

---

## 1. Epic

| ID | 제목 | 완료 조건 (Concept → Code Traceability) |
|----|------|----------------------------------------|
| **Epic-001** | Invariant 기반 **4×4 Magic Square 완성 시스템** | `docs/PRD.md` §5~10 및 Report/4 Gherkin·AC가 **Invariant → 유스케이스 → 계약 → 테스트 ID → 컴포넌트**로 추적 가능하고, Domain 커버리지 ≥95%, 입력 계약 테스트 100%, Dual-Track(UI+Logic) RED→GREEN→REFACTOR 완료 |

**추적 메모:** Report/2 §4.5 Traceability Matrix, PRD §8 NFR과 정합.

---

## 2. User Story

| ID | 스토리 | 주요 출처 | ECB 역할 |
|----|--------|-----------|----------|
| **US-001** | 호출자가 `4×4 int[][]`를 주면 **경계에서만** 형태·빈칸·범위·중복을 검증하고, 실패 시 도메인에 넘기지 않는다 | PRD §6, Report/2 §2 | **Boundary** |
| **US-002** | 유효 격자에서 **빈칸(0) 2곳**을 row-major 규칙으로 식별한다 | Report/4 Story 2, PRD §6 빈칸 순서 | **Entity** + **Entity**(서비스 `EmptyCellFinder`) |
| **US-003** | 1~16 중 **격자에 없는 두 수**를 구해 Solver 후보를 고정한다 | Report/4 Story 3 | **Entity**/서비스 `MissingNumbersFinder` |
| **US-004** | **완전히 채워진** 4×4가 행·열·두 대각에서 합 34(매직 상수)인지 판정한다 | Report/4 Story 4, Report/2 INV-04 | **Entity**/서비스 `MagicSquareValidator` |
| **US-005** | 첫/둘째 빈칸에 (작→첫, 큰→둘)와 **역배치**를 시도해, 성립 시 `int[6]` `[r1,c1,n1,r2,c2,n2]`(좌표 1-index)를 반환한다; 둘 다 실패 시 무해 | PRD §6 출력, Report/4 Story 5·Gherkin | **Entity**/서비스 `TwoPlacementSolver` |
| **US-006** | 검증 실패·무해 시 PRD **고정 `code`/`message`** 로 응답한다 | PRD §6.1, Report/2 §2.4 | **Boundary**(매핑) + **Control**(흐름) |
| **US-007** | **Control**이 Boundary 검증 → Domain `trySolve` 호출 → 결과/오류 반환을 조율한다 | Report/2 §4.1 | **Control** |
| **US-008** | (선택, PRD §5.1) 세션 저장/로드 인터페이스 및 테스트 | PRD, Report/2 §3 | **Boundary**/Data |

---

## 3. Phase별 Task 목록

### Phase A — 개요·추적성·상수 (L0)

- [ ] **TASK-001** | **RED** | ECB 패키지 스켈레톤 및 의존성 방향 점검 (`boundary → control → entity`) | **L0** | **Test:** `test_ecb_import_direction_no_entity_to_control` (또는 아키텍처 스모크) | **Code:** `magic_square/` 패키지 초기 트리 | **ECB:** 전 레이어(구조) | **체크포인트:** Report/3·`.cursorrules` architecture와 일치

- [ ] **TASK-002** | **GREEN** | 매직 상수·오류 코드 단일 소스 | **L0** | **Test:** `test_magic_constant_is_34`, `test_error_codes_match_prd` | **Code:** `entity/constants.py` 또는 `boundary/errors.py`(코드만; 메시지는 PRD와 단일화) | **ECB:** Entity(상수) / Boundary(코드 열거) | **체크포인트:** PRD §6.1 문구와 1:1

- [ ] **TASK-003** | **REFACTOR** | Concept→Test→Component 매핑 표(README 아님, 코드 주석 또는 `docs/traceability` 최소) 유지 방법 합의 | **L0** | **Test:** (문서/CI 체크리스트 수동) | **Code:** 주석 또는 팀 규약 | **ECB:** — | **체크포인트:** Report/2 §4.5 열과 동기화 가능

---

### Phase B — 보드 생성·유효성 (Entity + 계약 전제)

- [ ] **TASK-010** | **RED** | `createPuzzle` / `MagicSquarePuzzle` — 크기≠4×4 거부 | **L3** | **Test:** `test_create_puzzle_rejects_non_4x4_grid` (**D-03**) | **Code:** `entity/magic_square_puzzle.py` (또는 동일 책임) | **ECB:** **Entity** | **체크포인트:** INV-01

- [ ] **TASK-011** | **GREEN** | 빈칸 개수 ≠ 2 거부 | **L3** | **Test:** `test_create_puzzle_rejects_blank_count_not_two` (**D-03/D-04**) | **Code:** 동일 Entity 생성 경로 | **ECB:** **Entity** | **체크포인트:** INV-02

- [ ] **TASK-012** | **GREEN** | 0 제외 중복·1~16 범위 위반 거부 | **L2/L3** | **Test:** `test_create_puzzle_rejects_duplicate_nonzero`, `test_create_puzzle_rejects_out_of_range` (**D-05, D-06**) | **Code:** 동일 | **ECB:** **Entity** | **체크포인트:** INV-03

- [ ] **TASK-013** | **REFACTOR** | 퍼즐 불변식 검증 메서드 명확화(규칙은 Entity에만) | **L1** | **Test:** 기존 테스트 유지 | **Code:** `MagicSquarePuzzle` | **ECB:** **Entity** | **체크포인트:** Boundary에 비즈니스 규칙 없음(Report/3)

---

### Phase C — 빈칸 탐지·누락 수·후보 (Logic / Entity 서비스)

- [ ] **TASK-020** | **RED** | `EmptyCellFinder` — 정확히 두 좌표, row-major 첫/둘째 | **L1** | **Test:** `test_find_empty_cells_row_major_order` (**D-08**) | **Code:** `entity/empty_cell_finder.py` | **ECB:** **Entity**(도메인 서비스) | **체크포인트:** Report/4 AC, PRD 빈칸 순서

- [ ] **TASK-021** | **GREEN** | `MissingNumbersFinder` — 누락 2수, 정렬 `[a,b]` | **L1** | **Test:** `test_find_missing_numbers_sorted_pair` | **Code:** `entity/missing_numbers_finder.py` | **ECB:** **Entity** | **체크포인트:** UC-02

- [ ] **TASK-022** | **REFACTOR** | `CellCoordinate` / `CellPair` 값 객체로 좌표 표현 통일(내부 0-index, 외출력 1-index는 mapper) | **L2** | **Test:** `test_cell_pair_ordering_stable` | **Code:** `entity/value_objects.py` | **ECB:** **Entity** | **체크포인트:** INV-05와 분리

---

### Phase D — 완성 판정·후보 배치 (Validator + Solver)

- [ ] **TASK-030** | **RED** | `MagicSquareValidator` — 완성 격자 마방진 참/거짓 | **L1/L2** | **Test:** `test_validator_accepts_classic_magic_square`, `test_validator_rejects_wrong_row_sum` (**D-09, D-10**) | **Code:** `entity/magic_square_validator.py` | **ECB:** **Entity** | **체크포인트:** INV-04, 합 34

- [ ] **TASK-031** | **RED** | `TwoPlacementSolver` — (작,큰)/(큰,작) 시도 및 `int[6]` 생성 | **L1** | **Test:** `test_solve_matches_fixture_a_forward_placement` (**D-01**, Report/4 픽스처 A) | **Code:** `entity/two_placement_solver.py` | **ECB:** **Entity** | **체크포인트:** INV-06

- [ ] **TASK-032** | **GREEN** | 역시도만 성공 — **A≠B** 별도 픽스처 | **L2** | **Test:** `test_solve_reverse_only_succeeds_on_fixture_b` (Report/4 시나리오) | **Code:** `TwoPlacementSolver` | **ECB:** **Entity** | **체크포인트:** PRD §10 “역만 성공”

- [ ] **TASK-033** | **GREEN** | 두 배치 모두 실패 → 도메인 무해 (`NoValidPlacement` 등) | **L3** | **Test:** `test_solve_raises_or_returns_no_solution_when_both_fail` (**D-07**) | **Code:** `TwoPlacementSolver` + 결과 타입 | **ECB:** **Entity** | **체크포인트:** PRD `NO_SOLUTION`으로 Boundary 매핑 전제

- [ ] **TASK-034** | **REFACTOR** | Solver/Validator 중복 제거, 상수·이름 정리(관찰 가능 동작 동일) | **L1** | **Test:** 전 회귀 통과 | **Code:** `entity/*` | **ECB:** **Entity** | **체크포인트:** RED→GREEN→REFACTOR 단계 분리(Report/3)

---

### Phase E — Control (유스케이스 조율)

- [ ] **TASK-040** | **RED** | `SolveMagicSquareUseCase`(명칭 예시): 유효 퍼즐 → Solver 파이프라인 | **L1** | **Test:** `test_use_case_returns_int6_for_valid_puzzle` | **Code:** `control/solve_magic_square.py` | **ECB:** **Control** | **체크포인트:** I/O 없음, 순서만

- [ ] **TASK-041** | **GREEN** | Control이 Domain 실패를 도메인 결과형으로 전달(예외 vs Result) | **L3** | **Test:** `test_use_case_surfaces_no_solution_from_domain` | **Code:** `control/solve_magic_square.py` | **ECB:** **Control** | **체크포인트:** Boundary가 해석만

- [ ] **TASK-042** | **REFACTOR** | Application 경계 명확화(필요 시 퍼사드만) | **L0** | **Test:** 기존 IT 의존 통과 | **Code:** `control/` | **ECB:** **Control** | **체크포인트:** Report/2 §4.1 다이어그램

---

### Phase F — Dual-Track: Boundary (검증·매핑·오류) — UI 트랙

- [ ] **TASK-050** | **RED** | Boundary: 올바른 입력 시 Mock Domain 성공 → `int[6]` 전달 (**U-01**) | **L1** | **Test:** `test_boundary_maps_success_to_int6**` | **Code:** `boundary/magic_square_api.py` (예시) | **ECB:** **Boundary** | **체크포인트:** 비즈니스 규칙 없음

- [ ] **TASK-051** | **GREEN** | `SIZE` / `EMPTY_COUNT` / `VALUE_RANGE` / `DUPLICATE` — 각각 Domain 미호출 (**U-02~U-06**) | **L2/L3** | **Test:** `test_boundary_rejects_*` (4종) | **Code:** `boundary/validation.py` | **ECB:** **Boundary** | **체크포인트:** PRD §6.1 message 동일

- [ ] **TASK-052** | **GREEN** | Domain 무해 → `NO_SOLUTION` (**U-07**) | **L3** | **Test:** `test_boundary_maps_domain_failure_to_no_solution` | **Code:** `boundary/magic_square_api.py` | **ECB:** **Boundary** | **체크포인트:** Mock 실패 주입

- [ ] **TASK-053** | **REFACTOR** | 출력 길이 6·좌표 1~4 최종 검증(필요 시 `INTERNAL`) (**U-08**) | **L2** | **Test:** `test_boundary_validates_output_shape` | **Code:** `boundary/magic_square_api.py` | **ECB:** **Boundary** | **체크포인트:** Dual-Track 독립 RED(Report/2 §문서 완결)

---

### Phase G — 통합·회귀·커버리지 (To-Do → Scenario → Test → Code)

- [ ] **TASK-060** | **RED** | 통합: 검증 통과 → 실제 Domain → `int[6]` (**IT-OK-01**) | **L1** | **Test:** `test_integration_end_to_end_happy_path` | **Code:** `tests/integration/test_e2e_magic_square.py` | **ECB:** **Boundary+Control+Entity** | **체크포인트:** Report/2 §4.2

- [ ] **TASK-061** | **GREEN** | 통합: 입력 오류 시 Domain 미실행 (**IT-FAIL-01**) | **L3** | **Test:** `test_integration_invalid_input_never_calls_domain` | **Code:** spy/mock on use case | **ECB:** **Boundary** | **체크포인트:** PRD 경계 선행 검증

- [ ] **TASK-062** | **GREEN** | Gherkin 시나리오와 동일 데이터로 pytest 매핑(Report/4) | **L0–L3** | **Test:** `test_gherkin_fixture_a`, `test_gherkin_blank_count_error`, … | **Code:** 픽스처 모듈 | **ECB:** 전체 | **체크포인트:** Concept-to-Code Traceability

- [ ] **TASK-063** | **REFACTOR** | 커버리지 게이트: Domain ≥95%, Boundary ≥85%(권고), 전체 ≥80%(**Report/3·PRD §8**) | **L0** | **Test:** `pytest --cov` CI 또는 로컬 | **Code:** `pyproject.toml` / CI | **ECB:** — | **체크포인트:** **테스트 커버리지 체크포인트** 명시적 통과

---

## 4. 요약 표 (Dual-Track·추적)

| 구분 | Logic 트랙 | UI(Boundary) 트랙 |
|------|------------|-------------------|
| RED 우선 | D-01~D-10, Entity 서비스 단위 | U-01~U-08, Mock Domain |
| GREEN | 최소 구현·픽스처 A/B | 검증·오류 코드·매핑 |
| REFACTOR | 이름·중복·값 객체 | 출력 검증·메시지 단일 소스 |
| ECB | Entity=상태·규칙, Control=순서 | Boundary=입력/출력·검증만 |

---

**파일명 안내:** 요청하신 `docs/5.PRD_MagicSquare_4x4_TDD.md`가 아직 없으면 **`docs/PRD.md`를 주 소스(SSoT)로 두고**, 해당 파일을 추가할 때는 §6 오류 표·§8 NFR·§10 Done checklist를 그대로 옮겨 동기화하면 됩니다.

원하시면 다음 단계로 **TASK ID ↔ 구체적 pytest 파일 경로·클래스명**을 저장소 트리에 맞춰 한 장짜리 매트릭스로만추려 드리겠습니다.

---

**User**

Ｔｏ－Ｄｏ　리스트를  포함해 READMD.md 파일을 만들고 싶습니다. 무슨 문서를 참조하면 좋을까요?

---

**Cursor**

`README.md`에 **프로젝트 소개 + 실행 방법 + To-Do**를 넣을 때는 아래를 참조하면 됩니다.

## 필수에 가까운 참조

| 문서 | README에서 쓰기 좋은 내용 |
|------|---------------------------|
| **`docs/PRD.md`** | 한 줄 요약, 범위(in/out), I/O·오류 코드, 품질·커버리지 기준 — **To-Do의 “완료 조건”**을 여기에 맞추기 |
| **`Report/04_Magic_Square_Epic_to_Technical_Scenarios.md`** | Epic → User Story → 시나리오 — **To-Do 항목을 스토리·시나리오 단위로 쪼개기** |
| **루트 `.cursorrules`** (및 **`Report/03_Magic_Square_Cursor_Rules_Report.md`**) | 스택(Python, pytest), ECB 디렉터리, TDD 규칙 — **개발 환경·구조·작업 규칙** 문단 |

## 보조 참조

| 문서 | 용도 |
|------|------|
| **`Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md`** | 계약(입·출력), 레이어 역할, 통합 경로 — README에 **아키텍처 한 단락** 또는 To-Do의 “계약/레이어” 설명 |
| **`Report/01_Magic_Square_Problem_Definition_Report.md`** | 배경·문제 정의 — **왜 이 프로젝트인지**(선택) |
| **`Report/05_Magic_Square_PRD_Report.md`** | `docs/PRD.md`와 같은 PRD 본문을 보고서 형태로 둔 것 — PRD와 **중복되면 한쪽만 링크** |

## README 구성 팁

- **개요·목표:** PRD §1~2 + Report/01 요약  
- **요구·계약 요약:** PRD §5~6 (길면 링크만)  
- **To-Do:** Report/4 스토리 순서 + PRD §10 Done checklist를 **체크박스**로  
- **개발 규칙:** Report/3 또는 `.cursorrules` 요약 + 전체는 파일 링크  

참고: 이전에 말씀하신 `docs/5.PRD_MagicSquare_4x4_TDD.md`는 저장소에 없으면 **`docs/PRD.md`를 주 소스**로 두고 README에서 그 경로를 적으면 됩니다.

원하시면 저장소 구조에 맞춰 **`README.md` 초안(본문 + To-Do 섹션)**까지 바로 작성해 드릴 수 있습니다.

---

**User**

@docs/  폴더에 todo 파일을 만들어줘

---

**Cursor**

`docs/TODO.md`를 생성합니다. `docs/PRD.md`와 `Report/04`의 스토리·수용 기준에 맞춥니다.



`docs/TODO.md` 파일을 만들어 두었습니다.

**포함 내용**
- **근거 문서** 링크: `PRD.md`, Report/04·02·03, `.cursorrules`
- **PRD §10** 기준 완료 정의 체크리스트
- **Phase 1~7** 실무형 작업(보드/유효성, 빈칸·누락, 검증·솔버, Control, Boundary, 통합·커버리지)
- PRD에 있는 **선택 Data** 항목

파일명은 관례적으로 `TODO.md`로 했습니다. `todo.md` 등 다른 이름을 원하시면 알려주세요.

---

**User**

파일명은 MasicSquare_Implementation_TODO로 변경해줘

---

**Cursor**

`docs/TODO.md`를 `docs/MasicSquare_Implementation_TODO.md`로 이름 변경합니다.



변경 반영했습니다.

- **새 파일:** `docs/MasicSquare_Implementation_TODO.md`
- **삭제:** `docs/TODO.md`

확장자는 마크다운 문서로 쓰기 위해 `.md`를 붙였습니다. 확장자 없이 두려면 알려주세요.

변경 이력에 파일명 변경 한 줄도 추가해 두었습니다.

---

**User**

 README 본문·To-Do·검증 기준은 @docs/PRD.md를 중심에 두고, 스토리 표현은 Report/4, 오류·계약 요약은 Report/2, 실행·ECB·TDD는 Report/3 + pyproject.toml + Cursor 규칙, 문서 관계 한 줄은 Report/5를 참조해서 To-Do 리스트를 포함한 MagicSquare를 만들기 위한 README.md 파일을 만들어줘.

---

**Cursor**

PRD, Report/5, pyproject.toml, 기존 To-Do 문서를 읽어 README.md를 작성합니다.



저장소에 `pyproject.toml`이 없습니다. README에 Report/3·`.cursorrules`와의 정렬을 명시하고, `pyproject.toml` 추가 시 같은 기준을 따르도록 적습니다.



루트에 `README.md`를 추가했습니다.

**구성 요약**

1. **중심:** 본문·검증 기준·표는 모두 [`docs/PRD.md`](docs/PRD.md)와 맞춤.
2. **Report/5 한 줄:** `docs/PRD.md`와 `Report/05`의 동기 본·SSoT 관계만 명시.
3. **스토리:** PRD §7 표 + Report/04(Gherkin·픽스처) 참조 문구.
4. **계약·오류:** Report/2 맥락에서 PRD §6 입출력 + §6.1 오류 표 요약.
5. **실행·ECB·TDD:** Report/3 + `.cursorrules` + **`pyproject.toml`을 도구 설정의 단일 진입점으로 둔다**고 적었고, 현재 저장소에 `pyproject.toml`이 없으므로 **추가 시 PRD §8·Report/3에 맞춘다**고 했음.
6. **To-Do:** Phase 요약 체크박스 + 상세는 [`docs/MasicSquare_Implementation_TODO.md`](docs/MasicSquare_Implementation_TODO.md)로 연결.

추가로 `pyproject.toml`을 만들면 README의 `pytest` 예시와 동일한 기준으로 맞추면 됩니다.

---

**User**

실수로 readme 파일을 삭제해버렸어 다시 생성해줘

---

**Cursor**

삭제된 `README.md`를 이전과 동일한 내용으로 복원합니다.



`README.md`를 프로젝트 루트에 다시 만들어 두었습니다. 이전과 같이 `docs/PRD.md` 중심 본문·검증 기준·문서 표·계약 요약·실행/TDD·To-Do 연결(`docs/MasicSquare_Implementation_TODO.md`)이 포함되어 있습니다.

---

**User**

Report 폴더에 작업한 내용을 보고서로 내보내줘

---

**Cursor**

Report 폴더 구조와 최근 생성된 문서를 확인한 뒤 보고서 파일을 작성합니다.



Report 시리즈 형식에 맞춰 저장소 문서화 작업과 Report 폴더 구성을 정리한 내보내기 보고서를 작성합니다.



`Report/06_Magic_Square_Repository_Documentation_Export_Report.md`를 추가해 두었습니다.

**보고서에 들어 있는 내용**
- **요약:** Report 01~05 역할 표, SSoT(`docs/PRD.md` ↔ Report/05)와 `.cursorrules` 관계
- **내보낸 문서 작업:** 루트 `README.md`, `docs/MasicSquare_Implementation_TODO.md` (구 `TODO.md` 대체 반영)
- **추적성 표:** Epic·스토리·계약·ECB·품질·To-Do가 어떤 문서와 연결되는지
- **후속 권장:** `pyproject.toml`·패키지 구조 등 문서 관점 메모

기존 Report 네이밍(`01`~`05`)에 맞춰 **`06`**으로 두었습니다. 다른 번호·제목을 원하면 알려주세요.

---

**User**

첨부한 파일도 참고해서 @README.md 파일 중 To-Do list를 작성해줘. 자세하게 생각해서... 

---

**Cursor**

README.md 전체를 읽고, PRD·기존 To-Do·첨부 대시보드 형식을 반영해 To-Do 섹션을 상세히 갱신합니다.



PRD·Report/02 명명(`MagicSquareValidator`, `EmptyCellFinder` 등)에 맞추고, 첨부 대시보드의 Epic/US/Task·RED/GREEN/REFACTOR·추적 매트릭스 형식을 반영합니다. 구현 코드가 없어 테스트 상태는 ‘계획’ 기준으로 두고, 선택 참고(N-Queen·성능)는 PRD 범위와 함께 명시합니다.



`README.md`의 **「구현 To-Do」** 를 아래에 맞게 다시 썼습니다.

### 반영한 내용
- **C2C 추적:** `Task → Req → Scenario(L0~L3) → Test → Code(ECB)` 설명 + `Report/02` 링크  
- **Epic-001** + **US-001~008** (경계 → Entity·퍼즐 → **MagicSquareValidator** + **RED / GREEN / REFACTOR** 서브태스크 → 빈칸·누락 수 → 솔버 → Control → Boundary → 통합·커버리지·선택 Data)  
- 첨부 자료의 **「합 검증」** → PRD/Report/02 명칭 **`MagicSquareValidator`** 로 통일 (예시의 `SquareValidator` 대신)  
- **N-Queen·&lt;100ms:** 학습용·선택 NFR으로만 명시하고, PRD §5.2에 맞게 **계약·테스트 우선**, 4×4·빈칸 2개는 결정적 구현으로 충분하다고 적음  
- **요구 추적 매트릭스:** Task ID · Req ID(`REQ-BOUND` 등) · 시나리오 · 예시 테스트 이름 · ECB · 테스트 상태(✅/🔴/⬜ 갱신 안내)  
- 상세 Phase 체크는 기존처럼 [`docs/MasicSquare_Implementation_TODO.md`](docs/MasicSquare_Implementation_TODO.md) 로 안내  

저장소에 아직 패키지가 없어 **테스트 상태는 모두 ⬜** 두었고, 구현이 진행되면 표만 업데이트하면 됩니다. 첨부 스크린처럼 **TASK-001 = Entity 완료** 순서를 쓰고 싶다면, PRD의 “경계 먼저”와 맞추기 위해 지금 README 순서(US-001 Boundary = TASK-001)를 유지하는 편이 맞습니다.

---

**User**

Report 폴더에 작업한 내용에대한 보고서를 업데이트 해줘

---

**Cursor**

기존 내보내기 보고서와 최근 README 변경을 확인한 뒤 `Report/06`을 업데이트합니다.



`Report/06_Magic_Square_Repository_Documentation_Export_Report.md`를 README·To-Do 확장 내용으로 갱신합니다.



`Report/06_Magic_Square_Repository_Documentation_Export_Report.md`를 최신 작업 기준으로 고쳐 두었습니다.

**반영한 내용 요약**

1. **Executive summary** — README가 단순 개요가 아니라 **개발 보드형 To-Do·추적 매트릭스**까지 포함한다고 명시했습니다.  
2. **§2** — 내보내기 보고서(`06`) 역할을 표에 추가했습니다.  
3. **§4** — README 갱신 내용: Epic-001, US-001~008, TASK-001~010, L0~L3, Req ID 매트릭스 등을 표로 정리했습니다.  
4. **§5 (신설)**  
   - **5.1** C2C 추적 문구와 README 구성 요소별 출처(Report/02, PRD, 픽스처 등)  
   - **5.2** Task ↔ Req ID ↔ Report/02 개념 매핑 표  
5. **§6** — 추적 표에 README「구현 To-Do」 행 추가  
6. **§7** — 매트릭스 테스트 상태(✅/🔴/⬜) 수동 갱신 권장 추가  
7. **§8 변경 이력** — 같은 날짜로 **개정** 한 줄 추가  

추가로 날짜를 바꾸고 싶으면 알려주세요.


# Magic Square — Product Requirements Document (PRD)

**제품(프로젝트)명:** MagicSquare (4×4)  
**문서 목적:** 구현·검수·로드맵의 단일 기준으로 쓰일 **제품 요구사항**을 `Report/`, `Prompting/` 산출물에 맞춰 한곳에 정리한다.  
**최종 갱신:** 2026-04-28  
**근거 문서:**  
- `Report/01_Magic_Square_Problem_Definition_Report.md`  
- `Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md`  
- `Report/03_Magic_Square_Cursor_Rules_Report.md`  
- `Report/04_Magic_Square_Epic_to_Technical_Scenarios.md`  
- (규칙 원본) 프로젝트 루트 `.cursorrules`  

---

## 1. 개요 (Executive summary)

4×4 마방진(고전: 1~16 각 1회, 행·열·두 대각 합 34)을 **매개**로, **불변조건(Invariant) 기반 사고·Dual-Track TDD·계약(Contract) 명시·ECB(Clean) 계층 분리**를 훈련·습관화하는 **학습/실습용** 소프트웨어 프로젝트다.

**핵심 가치 제안**

- “한 번 손으로 맞추기”가 아니라, **같은 규칙으로 반복·판정·탐색**이 가능한 **명확한 I/O 계약**과 **회귀 가능한 테스트**로 요구를 고정한다.
- **Solver(배치 시도)**와 **Validator(완성 판정)**의 책임을 분리하고, **경계(Boundary)**에서 입력을 먼저 거른다.

---

## 2. 비전·EPIC (Business goal)

| 항목 | 내용 |
|------|------|
| **Epic** | Invariant(불변조건) 기반 사고 훈련 시스템 구축 |
| **학습 목표** | Invariant 중심 설계, Dual-Track TDD(요구/테스트와 구현의 이중 궤적), 입·출력 계약의 명시와 검증, 설계 → 테스트 → 구현 → 리팩터 순서 |
| **제품(코드) 목표** | 4×4, 빈칸(0) 2개인 격자에 대해 누락 두 수를 **규칙에 따라** 첫/둘째 빈칸에 배치해 마방진이 되면 그 결과를 **고정된 6원소** 형식으로 돌려준다. 잘못된 입력·무해(해 없음)는 **스펙된 오류**로 알린다. |

---

## 3. 대상 사용자 (Persona)

- **소프트웨어 개발 학습자** — 작은 시스템을 설계·검증하려는 단계  
- **TDD·리팩터** 연습 — RED → GREEN → REFACTOR를 요구·회귀에 사용  
- **Clean Architecture(계층 경계)** 이해 — UI·응용·도메인·(선택) 영속 I/O의 분리  

---

## 4. 문제 정의 (Product problem statement)

**개선된 문제 정의(요지)**  
주어진 크기 **4**와 1~N²(여기서는 1~16)에 대해, “해만/부분해만/불가”를 **같은 규칙**으로 **판정**할 수 있고, 필요 시 기준을 만족하는 배치를 **탐색**하며, **판정과 절차는 동일한 규칙으로 반복** 가능해야 한다. I/O는 호출자가 이해할 만큼 **납작·명확**하며, 변경 시 **이전 믿음(회귀)을 자동 점검**으로 보호할 수 있어야 한다.  
(상세: `01_Magic_Square_Problem_Definition_Report.md`)

---

## 5. 제품 범위

### 5.1 In scope

| 영역 | 요구 |
|------|------|
| **고정 문제** | 4×4 격자, `0` = 빈칸(정확히 2개), 나머지 칸은 1~16(0 제외 중복 없음) |
| **도메인** | 빈칸 2곳 **행 우선·열 우선** 정렬로 “첫/둘째 빈칸” 정의, 누락 두 수 탐지, 완성 격자 마방진 판정(행·열·두 대각, 매직 합 34) |
| **솔루션** | (작→첫 빈칸, 큰→둘째)와 (역) 중 마방진이 되는 쪽의 `(n1,n2)`와 좌표를 `int[6]` `[r1,c1,n1,r2,c2,n2]`(좌표 **1-index** 1~4)로 반환 |
| **경계** | 4×4/빈칸 수/값/중복 **선행 검증**; 검증 실패 시 도메인 미호출 |
| **(선택)** Data | `saveSession` / `loadLastSession` / `clear` — 메모리 기본, 파일(JSON) 2구현 권장 |
| **엔지니어링** | Python 3.10+, ECB(`.cursorrules`의 boundary→control→entity), pytest, TDD(RED/GREEN/REFACTOR), 타입 힌트·Google docstring, 커버리지 기준(아래) |

### 5.2 Out of scope (본 PRD/보고서 기준)

- **일반 N×N** 마방진(본 트랙은 4×4 고정)  
- DB 트랜잭션·동시성·마이그레이션(“Data”는 **저장/로드 인터페이스** 수준)  
- 실제 화면/프레임워크 상세(UI는 **Boundary**로 **입·출력 계약**만)  
- 알고리즘 효율(난이도)보다 **계층·계약·테스트·리팩터** 훈련이 우선  

---

## 6. I/O 및 계약 (필수 제품 스펙)

**입력**

- `4×4 int[][]` (0은 빈칸)  
- 빈칸은 **정확히 2개**  
- 값: `0` 또는 `1~16`  
- `0`이 아닌 값끼리 **중복 금지**  

**출력(성공)**

- `int[6]` = `[r1, c1, n1, r2, c2, n2]`  
- 좌표 **1-index** (1~4)  
- `n1`, `n2`는 누락된 두 수. 배치: **(작은수 → 첫 빈칸, 큰수 → 둘째 빈칸)** 조합이 마방진이면 그 순서, 아니면 **역**  

**빈칸 순서(모호성 제거)**

- 빈칸 둘을 **행 asc, 열 asc** (row-major)로 정렬했을 때 앞 = 첫 빈칸, 뒤 = 둘째 빈칸.  

**Magic constant (4×4, 1~16)**

- 34.  

(상세 도메인 개념·INV-ID·API 개념: `02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md`)

### 6.1 Boundary 오류 응답(제품이 고정해야 할 메시지)

| `code` | `message` |
|--------|------------|
| `SIZE` | `Grid must be 4x4.` |
| `EMPTY_COUNT` | `There must be exactly 2 empty cells (0).` |
| `VALUE_RANGE` | `Each cell must be 0 or in range 1..16.` |
| `DUPLICATE` | `Values 1..16 must not duplicate (excluding zeros).` |
| `NO_SOLUTION` | `No valid placement forms a 4x4 magic square.` |
| `INTERNAL` | `An unexpected error occurred.` |

---

## 7. 사용자 스토리·AC (요약)

| # | User story (요지) | Acceptance (요지) |
|---|-------------------|-------------------|
| 1 | 경계에서 4×4 입력을 검증 | 4×4 아님·빈칸≠2·0 제외 중복·1~16 범위 → 예외(도메인 미전달) |
| 2 | `0` 위치 탐색 | row-major, 정확히 2좌표 |
| 3 | 1~16 누락 2수 | 후보 고정(정렬된 `[a,b]`) |
| 4 | 완성 격자 마방진 판정 | 행·열·두 대각 동일(34) |
| 5 | 두 배치(정·역) 시도 | 정답 시 6원소, 1-index, 문서와 동일 순서 규칙; “역만 성공” 케이스는 **A≠B** 픽스처로 검증(Report 04) |

(전체: `04_Magic_Square_Epic_to_Technical_Scenarios.md` — Gherkin 시나리오 참조)

---

## 8. 비기능·품질 요구 (NFR)

| 항목 | 기준 |
|------|------|
| **성공(프로젝트)** | Domain 로직 커버리지 **95% 이상**; **입력 계약 테스트 100% 통과**(Epic 기준) |
| **아키텍처 설계(02)** | Domain ≥95%, Boundary ≥85%, Data ≥80% (권고) |
| **전사 규칙(`.cursorrules`)** | pytest, AAA, **최소 커버리지 80%**, `test_` 명명, 매직 값 금지(이름 있는 상수 등) |
| **TDD** | RED → GREEN → REFACTOR, 단계에 맞는 금지 사항(`.cursorrules` / `03_..._Report.md`) |
| **의존성** | boundary → control → entity 한 방향; entity는 I/O·프레임워크에 비의존 |
| **회귀(02)** | 계약 변경은 테스트 선행; GREEN 테스트 임의 삭제 금지; 에러 메시지 변경은 스펙/승인 절차 |

---

## 9. 기술 스택·구조 (요약)

- **언어:** Python 3.10+  
- **스타일:** PEP 8, 88열, Google docstring, public API 타입 힌트  
- **레이어:** ECB — `magic_square/boundary/`, `control/`, `entity/`, `tests/` (`.cursorrules` 트리)  
- **검증 경로(요지):** Caller → Boundary 검증 → (선택) Application — Domain `trySolve`/validators — (선택) Data — Boundary 매핑 (`int[6]` 또는 Error) (`02_..._Report` §4)

---

## 10. 수용 기준(Release / Done checklist)

- [ ] Epic 성공 기준이 **Journey·AC·(자동화) 테스트**와 추적 가능  
- [ ] Invariant(또는 ID) — 규칙 — 유스케이스 — 계약 — **테스트 ID**가 매핑(02의 Traceability 수준)  
- [ ] Positive + 입력 오류 + 도메인 무해(`NO_SOLUTION`) + (선택) Data 실패·통합 시나리오(02 IT-ID)  
- [ ] Gherkin/체크리스트(04) 항목과 **Edge**(4×4, 빈칸 2, 1/16, row-major) 반영  
- [ ] “역시도만 성공” 케이스는 **A≠B** 픽스처로 **별도** 정의·자동화  

---

## 11. 위험·가정

| 항목 | 내용 |
|------|------|
| **가정** | 한 트랙의 핵심이 **2칸 0 + 누락 2수** 완성이며, 02 보고서의 I/O가 **구현 계약**의 기준 |
| **위험** | “완성 = 성공”만 강조하면 **가치·가정**이 비는 문제(01) — **계약·Invariant·팀 합의**로 고정 |
| **프롬프트/보고** | `Prompting/`는 작성 가이드이고, **요구의 최종 권한은** 본 PRD + `Report/` + `.cursorrules`에 맞출 것 |

---

## 12. 변경 이력

| 날짜 | 변경 |
|------|------|
| 2026-04-28 | `Report/`, `Prompting/`·`.cursorrules` 기준으로 PRD 초안 작성 |

---

*문의·요구 정정은 Invariant/계약 변경에 반영한 뒤, 동일 흐름으로 본 섹션과 `Report`를 갱신한다.*

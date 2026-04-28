# 4×4 Magic Square — PRD(제품 요구사항) 보고서

**내보내기일:** 2026-04-28  
**문서 목적:** 구현·검수·로드맵의 단일 기준으로 쓰일 **제품 요구사항(PRD)**을 `Report/`, `Prompting/`·`.cursorrules` 산출물에 맞춰 **보고서 형태**로 보관한다.  
**동기 본:** `docs/PRD.md` — 요구 본문은 해당 파일과 동일하게 유지한다. 갱신 시 **한쪽을 기준(SSoT)으로 정한 뒤** 다른 쪽을 맞춘다(본 보고서는 해설·매핑 절을 추가할 수 있다).  
**관련:** 문제 정의 `01_Magic_Square_Problem_Definition_Report.md`, Dual-Track 설계 `02_...`, Cursor 규칙 `03_...`, Epic·시나리오 `04_...`

---

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

## 12. Dual-Track UI + Logic TDD · MLOps (본 PRD 매핑)

`docs/PRD.md` 및 `02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md`의 방법론을 **요구사항 문장**으로 고정할 때 아래를 참고한다.

### 12.1 핵심 원칙

| 원칙 | 이 PRD에서의 의미 |
|------|-------------------|
| **UI는 UX Contract로 RED** | Boundary·표현 계층에서 **보이는 상태**(메시지·표시·비활성 등)를 먼저 테스트로 고정한다. §6.1 코드·메시지가 UX 측 계약의 기준이다. |
| **로직은 Logic Rule로 RED** | Control·Entity에서 §5~§7의 **판정·반환·차단** 규칙으로 실패 테스트를 먼저 쓴다. |
| **GREEN·REFACTOR는 함께** | §8 TDD·커버리지·리팩터 순서와 동일. |
| **두 트랙 독립** | UI(경계) 테스트는 도메인 구현 세부를, 로직 테스트는 프레임워크·화면을 알지 않는다. §9 의존 방향과 일치. |

### 12.2 언어 구분 (시나리오 작성 시)

- **UX Contract:** 보인다/안 보인다, 활성/비활성, §6.1의 특정 `message` **표시 여부**.
- **Logic Rule:** 허용/거부, 반환/차단, 계산, (선택) 저장 — §5 경계 검증·도메인 `trySolve`·Data 세션 등.

테스트 후보는 **판단(조건 → 시스템 행동)**이 있는 항목만으로 한정한다(단순 할 일 목록은 RED로 바로 연결하지 않음).

### 12.3 시나리오 ↔ UX Contract ↔ Logic Rule (요약)

| 시나리오 (§6·§7 요지) | UX Contract | Logic Rule |
|----------------------|-------------|------------|
| 격자가 4×4가 아님 | `SIZE` 메시지가 **보인다** | 입력 **거부**, 도메인 미호출 |
| 빈칸이 정확히 2개가 아님 | `EMPTY_COUNT`가 **보인다** | 탐색·해결 **중단** |
| 값 범위 위반·중복 | `VALUE_RANGE` / `DUPLICATE`가 **보인다** | 입력 **차단** |
| 유효 입력이나 해 없음 | `NO_SOLUTION`이 **보인다** | 배치 시도 후 **거부** |
| 유효하고 해 있음 | 결과(6원소 또는 완료 표시)가 **보인다** | `int[6]` **반환** |
| (선택) 세션 저장/로드 | 성공·실패 피드백이 **보인다** | JSON 등으로 **저장·로드** |

### 12.4 MLOps 대응(본 트랙의 비‑UI 로직)

본 프로젝트는 학습용 도메인으로 **학습·서빙 파이프라인**을 범위에 두지 않는다(§5.2). 다만 **계약·재현·품질 게이트**는 다음처럼 대응한다.

| MLOps 관점 | PRD 상 대응 |
|------------|-------------|
| 입력 검증 | §6 입력 계약 — 스키마에 맞지 않으면 Boundary에서 차단. |
| 출력·버전 고정 | 성공 시 `int[6]`, 실패 시 §6.1 **결정적** 코드·메시지 — 회귀 테스트로 고정. |
| 아티팩트·재현 | §5 선택 Data(`saveSession` 등), 동일 입력에 대한 동작 기대. |
| 품질 게이트 | §8 커버리지·입력 계약 테스트·CI(pytest). |

UI는 **결과·오류를 표시**하고, 로직·데이터 경로는 **규칙·저장·판정**을 담당한다 — 프론트와 배포·실험 추적을 분리하는 MLOps 원칙과 동일한 **경계**를 유지한다.

---

## 13. 변경 이력

| 날짜 | 변경 |
|------|------|
| 2026-04-28 | `docs/PRD.md`·`Report/`·`Prompting/`·`.cursorrules` 기준 PRD 보고서로 내보내기. 이후 `docs/PRD.md`와 본문 동기화(문서 목적·§11 **본 PRD** 문구), §12 Dual-Track·MLOps 매핑 보고 절 추가 |

---

*요구 정정은 Invariant/계약 변경에 반영한 뒤, **본 섹션**과 `docs/PRD.md`를 동기화한다.*

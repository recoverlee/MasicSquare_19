# 4×4 Magic Square — Dual-Track UI + Logic TDD · Clean Architecture 설계 보고서

**내보내기일:** 2026-04-28  
**문서 목적:** Magic Square(4×4) TDD 연습 프로젝트에 대해 **구현 코드 없이** Logic / UI(Boundary) / Data 레이어의 설계·계약·테스트·통합 검증 계획을 한 파일에 보관한다.  
**범위:** 알고리즘 난이도보다 **레이어 분리**, **계약 기반 테스트**, **리팩토링** 훈련에 초점을 둔다.  
**관련:** 문제 정의는 `01_Magic_Square_Problem_Definition_Report.md`, Epic·시나리오는 `04_Magic_Square_Epic_to_Technical_Scenarios.md`를 참고한다.

**입력 계약(고정)**

- `4x4 int[][]` (0은 빈칸)
- 빈칸은 정확히 2개
- 값 범위: 0 또는 1~16
- 0 제외 중복 금지

**출력 계약(고정)**

- `int[6]`
- 좌표는 **1-index**
- 반환 형식: `[r1,c1,n1,r2,c2,n2]`
- `n1`, `n2`는 두 누락 숫자이며, (작은수→첫 빈칸, 큰수→둘째 빈칸) 조합이 마방진이면 그 순서로, 아니면 반대로

**제약**

- 본 문서는 **설계·계약·테스트·통합 계획만** 포함하며 **구현 코드는 포함하지 않는다.**
- UI는 실제 화면이 아니라 **입력/출력 경계(Boundary)** 로 정의한다.
- Data Layer는 DB가 아니라 **저장/로드 인터페이스**(메모리/파일 교체 가능) 수준만 다룬다.

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

| 구분 | 이름 | 책임(SRP) |
|------|------|-----------|
| Entity | `MagicSquarePuzzle` (또는 `PartialMagicSquare`) | 4×4 격자 상태(값 배치)를 보유하고, “현재 판”에 대한 질의만 담당 |
| Value Object | `CellCoordinate` | 행·열(도메인 내부는 0-index 또는 1-index 중 하나로 통일; 외부 계약과의 변환은 별 책임) |
| Value Object | `CellPair` | 빈칸 두 칸의 좌표 쌍 |
| Value Object | `MissingNumberPair` | 누락된 두 정수(집합 연산 결과) |
| Value Object | `MagicSquareSolution` | `[r1,c1,n1,r2,c2,n2]` 형태의 도메인 표현(좌표 체계는 내부 규약과 일치) |
| Domain Service | `EmptyCellFinder` | 격자에서 값이 0인 칸을 정확히 둘 찾기 |
| Domain Service | `MissingNumbersFinder` | 1~16 중 격자에 없는 두 수 찾기 |
| Domain Service | `MagicSquareValidator` | 완전히 채워진 4×4가 마방진인지 판정(행/열/대각선 Magic Constant) |
| Domain Service | `TwoPlacementSolver` | 두 빈칸에 (n_small→첫 빈칸, n_large→둘째 빈칸)과 그 반대 중 마방진이 되는 순서 결정 및 결과 생성 |

**역할 분리**

- **엔티티:** 상태 보유 + 불변조건 위반 시 생성/갱신 거부.
- **값 객체:** 식별자 없음, 동등성으로 비교, 불변.
- **도메인 서비스:** 여러 값/엔티티에 걸친 순수 규칙(부작용 없음).

## 1.2 도메인 불변조건(Invariants)

| ID | 불변조건 | 검증 시점 | 비고 |
|----|----------|-----------|------|
| INV-01 | 격자 크기는 정확히 4×4 | Puzzle 생성/입력 매핑 시 | 행·열 길이 각각 4 |
| INV-02 | 빈칸(0)의 개수는 정확히 2 | Puzzle 유효화 시 | 그 외 개수면 도메인 입력 실패 |
| INV-03 | 0이 아닌 값은 1~16이며 서로 중복 없음 | Puzzle 유효화 시 | 중복·범위 위반 시 실패 |
| INV-04 | 완전 채움 후 마방진이면 모든 행·열·주대각·부대각 합이 동일 | `MagicSquareValidator` | 4×4 고전 마방진: **Magic Constant = 34** |
| INV-05 | 출력 좌표는 1-index이며 행·열 각각 1~4 | Solution 생성 시 | 외부 출력 계약과 일치 |
| INV-06 | `n1`, `n2`는 누락된 두 수이며, 배치 규칙: (작은수→첫 빈칸, 큰수→둘째 빈칸)이 마방진이면 그 순서, 아니면 반대 | `TwoPlacementSolver` | 첫/둘째 빈칸 순서는 아래 규칙으로 고정 |

**Magic Constant (4×4, 1~16 각 한 번)**

- \(M = \dfrac{n(n^2+1)}{2} = \dfrac{4 \times 17}{2} = 34\).

**“첫 빈칸 / 둘째 빈칸” 정의(모호성 제거)**

- 빈칸 두 개를 **행 우선, 같으면 열 우선**으로 정렬했을 때 앞선 칸 = 첫 빈칸, 나머지 = 둘째 빈칸.
- 동등 규칙: `(r1,c1)`이 `(r2,c2)`보다 사전순 `(row asc, col asc)`에서 먼저 오도록 고정.
- 테스트와 Domain API에 동일 문구로 고정할 것.

## 1.3 핵심 유스케이스(도메인 관점)

| UC-ID | 유스케이스 | 전제 | 결과 |
|-------|------------|------|------|
| UC-01 | 빈칸 찾기 | INV-01~03 만족 격자 | 정확히 두 좌표 |
| UC-02 | 누락 숫자 찾기 | 동일 | `{a,b}` where \(a,b \in [1,16]\), 격자에 없음 |
| UC-03 | 마방진 판정 | 16칸 모두 1~16, 중복 없음 | 참/거짓(+ 선택적 실패 이유) |
| UC-04 | 두 조합 시도 | 두 빈칸 위치 + 두 수 `(min,max)` | 마방진이 되는 배치로 `(n1,n2)` 순서 결정 및 6원소 결과 |

## 1.4 Domain API(내부 계약)

구현 코드가 아닌 **메서드 시그니처 수준**의 계약만 기술한다.

| 메서드(개념) | 입력 | 출력 | 실패 조건 |
|--------------|------|------|-----------|
| `createPuzzle(int[][] grid)` | 4×4, 0/1~16 | `MagicSquarePuzzle` | 크기≠4×4, 빈칸≠2, 범위 위반, 중복 |
| `findEmptyCells(Puzzle)` | — | `CellPair`(내부 인덱스) | 빈칸 수≠2(생성 단계에서 걸러지면 호출 불가) |
| `findMissingNumbers(Puzzle)` | — | `MissingNumberPair` | 누락이 정확히 2개가 아니면 실패 |
| `orderEmptyCellsFirstSecond(Cell, Cell)` | 두 빈칸 | `(first, second)` 고정 순서 | 동일 좌표 등 |
| `trySolve(Puzzle)` | 유효 Puzzle | `MagicSquareSolution` 또는 `NoValidPlacement` | 두 배치 모두 비마방진 등 |
| `toExternalTuple(Solution)` | 내부 Solution | `int[6]`(1-index) | 좌표계 불일치 시 실패 |

**실패 표현:** Result 타입 `(성공 | 검증실패 | 무해)` 또는 도메인 예외 목록을 테스트에서 코드/메시지로 고정.

## 1.5 Domain 단위 테스트 설계(RED 우선)

| TID | 구분 | 내용 | 보호하는 Invariant |
|-----|------|------|-------------------|
| D-01 | 정상 | 알려진 완성 4×4 마방진에서 임의 두 칸을 0으로 바꾼 뒤, 누락 수와 배치가 출력 규약과 일치 | INV-04, INV-05, INV-06 |
| D-02 | 정상 | 동일 퍼즐에 대해 `trySolve` 결과가 항상 동일(결정적) | — |
| D-03 | 비정상 | 빈칸 0개 격자 → `createPuzzle` 실패 | INV-02 |
| D-04 | 비정상 | 빈칸 3개 → 실패 | INV-02 |
| D-05 | 비정상 | 17 또는 음수 등 범위 밖 값 → 실패 | INV-03 |
| D-06 | 비정상 | 1~16 중복(0 제외) → 실패 | INV-03 |
| D-07 | 엣지 | 두 배치 모두 비마방진인 경우 도메인 정책에 따른 명시적 실패 | UC-04 |
| D-08 | 엣지 | `orderEmptyCellsFirstSecond`가 행·열 우선 규칙과 일치하는지 단위 고정 | INV-06 |
| D-09 | 정상 | `isMagicSquare` 완성 격자에 대해 참 | INV-04 |
| D-10 | 정상 | 한 행 합만 틀린 완성 격자 변형에 대해 거짓 | INV-04 |

**체크리스트 (Domain RED)**

- [ ] 모든 INV-ID가 최소 하나의 테스트 TID에 매핑된다.
- [ ] “첫/둘째 빈칸” 순서 규칙이 전용 테스트로 고정된다.
- [ ] 성공 케이스는 공개 예제 마방진(테스트 픽스처) 기반이다.
- [ ] 실패 케이스는 오류 코드/메시지가 스펙과 일치한다(프로젝트에서 메시지를 고정하는 경우).

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 관점 시나리오

| 단계 | 행위 | 산출물 |
|------|------|--------|
| S1 | 호출자가 4×4 `int[][]` 또는 동등 구조 전달 | 원시 입력 |
| S2 | Boundary가 형태·빈칸 수·값·중복 검증 | 통과 시 Domain 호출용 DTO |
| S3 | Domain `trySolve`(또는 유스케이스 파사드) 호출 | 도메인 결과 |
| S4 | 성공 시 `int[6]`으로 매핑·출력; 실패 시 Error schema | 최종 응답 |

## 2.2 UI 계약(외부 계약)

**Input schema**

| 필드 | 타입 | 제약 |
|------|------|------|
| `grid` | `int[4][4]` 또는 길이 4인 행 배열, 각 행 길이 4 | 본 보고서 상단 입력 계약과 동일 |

**Output schema (성공)**

| 필드 | 타입 | 제약 |
|------|------|------|
| `result` | `int[6]` | `[r1,c1,n1,r2,c2,n2]`, 좌표 1~4 |

**Error schema**

| 필드 | 타입 | 의미 |
|------|------|------|
| `code` | 열거 또는 고정 문자열 | 아래 에러 코드 표와 1:1 |
| `message` | 문자열 | 아래 정확한 문구 규칙 준수 |

## 2.3 UI 레벨 테스트(Contract-first, RED 우선)

전제: Domain은 Mock(성공/실패만 주입).

| TID | 시나리오 | 기대 | Mock 설정 |
|-----|----------|------|-----------|
| U-01 | 올바른 입력 → Mock이 유효 Solution 반환 | Boundary 출력이 `int[6]`이며 좌표·순서가 Mock과 동일 | 고정 6원소 |
| U-02 | 행 수 ≠ 4 | `code=SIZE`, 메시지 규약 | Domain 미호출 |
| U-03 | 열 길이 불균일 | `SIZE` | Domain 미호출 |
| U-04 | 빈칸 개수 ≠ 2 | `EMPTY_COUNT` | Domain 미호출 |
| U-05 | 값이 0이 아닌데 1~16 밖 | `VALUE_RANGE` | Domain 미호출 |
| U-06 | 0 제외 중복 | `DUPLICATE` | Domain 미호출 |
| U-07 | Domain이 “해 없음” 반환 | 도메인 실패에 매핑되는 코드·메시지 | Mock 실패 |
| U-08 | Boundary가 최종 포맷을 책임지는 경우 길이 6·좌표 범위 검증 | 실패 시 `INTERNAL` 또는 `FORMAT` | 필요 시 |

**체크리스트 (UI RED)**

- [ ] 검증 실패 시 Domain 호출 0회.
- [ ] 각 오류 코드별 메시지 문자열이 스펙과 동일(프로젝트 정책: 바이트 단위 또는 단일 소스).
- [ ] 성공 경로에서 Mock 호출 인자가 입력과 동일.

## 2.4 UX/출력 규칙 — 에러 메시지 표준

| `code` | 정확한 `message` (프로젝트 단일 소스로 고정; 마침표 유무는 한 가지만 채택) |
|--------|-----------------------------------------------------------------------------|
| `SIZE` | `Grid must be 4x4.` |
| `EMPTY_COUNT` | `There must be exactly 2 empty cells (0).` |
| `VALUE_RANGE` | `Each cell must be 0 or in range 1..16.` |
| `DUPLICATE` | `Values 1..16 must not duplicate (excluding zeros).` |
| `NO_SOLUTION` | `No valid placement forms a 4x4 magic square.` |
| `INTERNAL` | `An unexpected error occurred.` |

---

# 3) Data Layer 설계

## 3.1 목적 정의

| 목적 | 범위 |
|------|------|
| 학습 | 의존성 역전: Domain/UI는 저장소 구현을 모른다. |
| 기능 | 마지막 퍼즐·마지막 결과 선택적 재현(디버그·회귀 재현). |
| 비목표 | DB 트랜잭션·동시성·스키마 마이그레이션. |

## 3.2 인터페이스 계약

| 메서드 | 입력 | 출력 | 실패 |
|--------|------|------|------|
| `saveSession(inputGrid, optional result)` | `int[4][4]`, `int[6]` 또는 null | void 또는 저장 키 | 쓰기 실패 |
| `loadLastSession()` | — | `(grid, result?)` 또는 empty | 없음/손상 |
| `clear()` | — | — | — |

저장 대상: 입력 행렬(필수), 실행 결과(선택).

## 3.3 구현 옵션 비교 및 추천

| 항목 | 옵션 A: InMemory | 옵션 B: File(JSON 권장) |
|------|------------------|-------------------------|
| 속도 | 매우 빠름 | 디스크 I/O |
| 테스트 | 단위/통합 단순 | 임시 디렉터리·파일 정리 |
| 재현성 | 프로세스 종료 시 소실 | 재시작 후 유지 |
| 형식 오류 | 해당 없음 | 파싱 실패 처리 필요 |

**추천:** **옵션 A(InMemory)를 기본**으로 하고, 회귀·수동 검증용으로 **옵션 B를 동일 인터페이스의 두 번째 구현**으로 추가한다.

**이유:** TDD 훈련에서는 속도와 결정성이 우선이며, File은 “교체 가능성” 입증용으로 충분하다.

## 3.4 Data 레이어 테스트

| TID | 내용 | 기대 |
|-----|------|------|
| DA-01 | `save` 후 `load`로 동일 `grid` 복원 | 값 동등 |
| DA-02 | `result` 없이 저장 후 `load` | `result == null` |
| DA-03 | File: 존재하지 않는 경로 `load` | 계약된 실패 |
| DA-04 | File: 손상 JSON | 파싱 실패 처리 |
| DA-05 | 로드된 `grid`가 4×4가 아니면 거부 | INV-01 보호 |

---

# 4) Integration & Verification (통합 및 검증)

## 4.1 통합 경로 정의

```text
[Caller]
   ↓
[UI Boundary] --validate--> (reject early)
   ↓ valid DTO
[Application Service] (선택) --orchestrate-->
   ↓
[Domain] trySolve / validators
   ↓
[Data] saveSession (선택)
   ↓
[UI Boundary] --map--> int[6] 또는 Error
```

**의존성 방향:** UI·Data·Application(있을 경우)은 **Domain을 향한다.** Domain은 다른 레이어에 의존하지 않는다. Data 구현체는 인터페이스로 주입한다.

## 4.2 통합 테스트 시나리오

**정상 (2개 이상)**

| IT-ID | 설명 |
|-------|------|
| IT-OK-01 | End-to-end: 검증 통과 입력 → Domain → `int[6]` 형식·값 검증 |
| IT-OK-02 | 동일 입력 재실행 시 결과 동일; Data 저장 시 reload 후 동일 |

**실패 (3개 이상)**

| IT-ID | 유형 |
|-------|------|
| IT-FAIL-01 | 입력 오류: 빈칸 1개 → UI 검증에서 차단, Domain 미실행 |
| IT-FAIL-02 | 도메인 실패: 해 없는 퍼즐(픽스처) → `NO_SOLUTION` |
| IT-FAIL-03 | 데이터 실패: File repo 쓰기 불가 경로 → 저장 실패 처리 |

## 4.3 회귀 보호 규칙

| 규칙 | 내용 |
|------|------|
| R-01 | 입력/출력 계약 변경 시 ADR + 테스트 선행 |
| R-02 | 기존 GREEN 테스트 삭제 금지; 행위 변경 시 새 요구 반영 테스트를 먼저 추가 |
| R-03 | 에러 메시지 문구 변경은 버전 스펙 또는 스냅샷 승인 |

## 4.4 커버리지 목표

| 레이어 | 목표 |
|--------|------|
| Domain Logic | 95% 이상 |
| UI Boundary | 85% 이상 |
| Data | 80% 이상 |

## 4.5 Traceability Matrix

| Concept (Invariant) | Rule | Use Case | Contract | Test IDs | Component |
|---------------------|------|----------|----------|----------|-----------|
| INV-01 | 4×4만 허용 | 입력 수용 | `createPuzzle`, UI Input schema | D-03, U-02, U-03 | Puzzle, Boundary |
| INV-02 | 빈칸 정확히 2 | UC-01 | `createPuzzle`, UI validation | D-04, U-04 | EmptyCellFinder, Boundary |
| INV-03 | 범위·비중복 | UC-02 | Domain + UI | D-05, D-06, U-05, U-06 | Puzzle, Boundary |
| INV-04 | 합 34 일치 | UC-03 | `MagicSquareValidator` | D-09, D-10, IT-OK-01 | Validator |
| INV-05 | 1-index 출력 | UC-04 | UI Output schema, `toExternalTuple` | D-01, U-01 | Solution mapper |
| INV-06 | 작은수/큰수 배치 규칙 | UC-04 | `TwoPlacementSolver` | D-01, D-08 | TwoPlacementSolver |
| 저장 불변 | 4×4 유지 | — | `MatrixRepository` | DA-05 | Data impl |

---

## 문서 완결 체크리스트

- [ ] Dual-Track: Domain 테스트와 Boundary(Mock) 테스트가 독립적으로 RED 가능하다.
- [ ] 규칙이 TID/IT-ID로 추적 가능하다.
- [ ] 구현 코드를 포함하지 않는다.

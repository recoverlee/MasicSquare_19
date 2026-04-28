# Magic Square (4×4) — 구현 To-Do

**목적:** 부분적으로 비어 있는 4×4 마방진을 완성하는 시스템 구현 진행을 추적한다.  
**주 소스:** [`PRD.md`](./PRD.md) (완료 조건·계약·오류 코드·NFR)  
**스토리·시나리오 분해:** `Report/04_Magic_Square_Epic_to_Technical_Scenarios.md`  
**계약·레이어:** `Report/02_Magic_Square_Dual_Track_Clean_Architecture_Design_Report.md`  
**규칙(ECB·TDD):** `Report/03_Magic_Square_Cursor_Rules_Report.md`, 프로젝트 루트 `.cursorrules`

---

## 완료 정의 (PRD §10 요약)

- [ ] Epic 성공 기준이 Journey·AC·자동화 테스트와 추적 가능하다.
- [ ] Invariant — 규칙 — 유스케이스 — 계약 — 테스트가 매핑 가능하다 (`Report/02` Traceability 참고).
- [ ] 정상 경로 + 입력 오류 + 도메인 무해(`NO_SOLUTION`) 시나리오가 테스트로 존재한다.
- [ ] “역시도만 성공”은 **A≠B** 픽스처로 별도 검증한다 (`Report/04`).

---

## Phase 1 — 프로젝트 뼈대·상수

- [ ] ECB 디렉터리 구조 및 의존성 방향 (`boundary` → `control` → `entity`).
- [ ] 매직 합 **34** 및 오류 `code`/`message` 단일 소스 ([PRD §6.1](./PRD.md)).

---

## Phase 2 — Entity: 보드 생성·유효성

- [ ] 4×4가 아닌 격자 거부 (INV-01).
- [ ] 빈칸(0) 개수가 정확히 2가 아니면 거부 (INV-02).
- [ ] 0 제외 값의 범위(1~16)·중복 검증 (INV-03).

---

## Phase 3 — Entity: 빈칸·누락 수·후보

- [ ] 빈칸 두 칸 탐지, **row-major**로 첫/둘째 빈칸 정의 ([PRD §6](./PRD.md)).
- [ ] 1~16 중 격자에 없는 두 수(누락 쌍) 산출.

---

## Phase 4 — Entity: 판정·완성 로직

- [ ] 완전 채운 격자에 대해 행·열·두 대각선 합이 34인지 판정 (`MagicSquareValidator`).
- [ ] (작은수→첫 빈칸, 큰수→둘째)와 역배치 시도, 성립 시 `int[6]` `[r1,c1,n1,r2,c2,n2]` (좌표 **1-index**).
- [ ] 두 배치 모두 실패 시 무해 처리 → Boundary에서 `NO_SOLUTION` 매핑.

---

## Phase 5 — Control

- [ ] Boundary 검증 통과 후 Domain 파이프라인 조율 (유스케이스/애플리케이션 서비스).
- [ ] Domain 결과를 호출자 관점 형식으로 전달 (I/O 세부 없음).

---

## Phase 6 — Boundary (Dual-Track UI)

- [ ] 입력 계약 검증 실패 시 **도메인 미호출** (크기·빈칸 수·범위·중복).
- [ ] 성공 시 `int[6]` 매핑; 실패 시 PRD 고정 메시지.
- [ ] Domain 무해 → `NO_SOLUTION` 응답.

---

## Phase 7 — 통합·품질

- [ ] End-to-end 시나리오 (검증 → Domain → 출력).
- [ ] 커버리지: Domain 로직 **≥95%**, 입력 계약 테스트 **100%** 통과 목표 ([PRD §8](./PRD.md)).
- [ ] pytest 커버리지 게이트(프로젝트 최소 기준, 예: 전체 80%) 설정.

---

## 선택 (PRD In scope Data)

- [ ] `saveSession` / `loadLastSession` / `clear` — 메모리 구현 + 파일(JSON) 교체 구현 ([PRD §5.1](./PRD.md)).

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-04-28 | 초안 작성 (`PRD.md`, `Report/04` 기준) |
| 2026-04-28 | 파일명 `MasicSquare_Implementation_TODO.md`로 변경 (구 `TODO.md`) |

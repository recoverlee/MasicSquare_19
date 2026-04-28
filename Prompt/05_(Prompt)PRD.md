# PRD.md file creation
_Exported on 4/28/2026 at 08:31:39 GMT+9 from Cursor (3.2.11)_

---

**User**

@Report/ @Prompting 참조해서 docs 폴더에 PRD.md 파일을 만들어줘.

---

**Cursor**

Report와 Prompting 폴더의 자료를 읽어 `docs/PRD.md`를 작성합니다.



Report·Prompting 자료를 통합해 `docs/PRD.md`를 작성합니다.



`docs/PRD.md`를 추가했습니다. **Report** 네 편(문제 정의, Dual-Track 설계, Cursor 규칙, Epic·시나리오)과 **`.cursorrules`**를 묶어서 다음을 담았습니다.

- **개요·EPIC·페르소나** — 불변조건·Dual-Track TDD·계약 훈련 목표  
- **문제 정의·범위(In/Out)** — 4×4 고정, Data 레이어 선택, 비목표(N×N DB 등)  
- **I/O·첫/둘째 빈칸(row-major)·Magic 34·`int[6]` 출력**  
- **Boundary 오류 코드·영문 메시지 표**(Report 02와 동일)  
- **User story·AC 요약**, **NFR**(커버리지, ECB, TDD, 회귀 규칙)  
- **수용 체크리스트**, **위험·가정**, **근거 문서 링크**

파일 위치: `c:\DEV\MasicSquare_XXX\docs\PRD.md`.

---

**User**

Report폴더에 보고서로 내보내줘.

---

**Cursor**

`docs/PRD.md`를 읽어 `Report` 폴더에 보고서 형식으로 내보냅니다.



기존 Report 보고서 서식(내보내기일·문서 목적·관련)에 맞춰 `05_Magic_Square_PRD_Report.md`로 내보냅니다.



`Report/05_Magic_Square_PRD_Report.md`에 PRD를 **보고서 형식**으로 옮겨 두었습니다.

- **상단 메타:** `내보내기일`, `문서 목적`, `docs/PRD.md`와의 **동기 본** 안내, `01`~`04` 보고서 **관련** 링크  
- **본문:** `docs/PRD.md`와 동일한 1~12절 PRD 내용  
- **변경 이력/맺음말:** Report 내보내기에 맞게 한 줄 정리

이후 PRD를 고칠 때는 `docs/PRD.md`와 이 파일을 같이 맞추면 됩니다.


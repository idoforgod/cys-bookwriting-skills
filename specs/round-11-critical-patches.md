# Round 11 #F SPEC 내부 Critical 5건 일괄 Patch

> 저자 /goal — 6차 #F 검증 결과 11 Critical 중 *SPEC 내부 결함 5건* 즉시 처리.
> 외부 표준 6건 (F1.1 도서관 분류·F5.1 라이선스·F6.1 국방·F7.1 재난·F10.1·F10.2 SPDX)은 Phase 3-B로 deferred.

---

## Patch #14 (F1.2): skeleton 결정론 read 모듈 M15 신설

**위반**: content-expand-subs SUB 7이 "skeleton.md §시점 동기화 라인을 결정론 read" 명령하지만 *결정론 read 모듈 부재*.

**Fix (deterministic-modules.md M15 신규)**:
```python
### M15: skeleton_section_reader.py (Round 11 #F1.2 Critical 신규)

import re
from pathlib import Path
from typing import List, Optional

class SkeletonSectionReader:
    """skeleton.md의 특정 섹션을 *결정론 read*. LLM 자연어 추론으로 섹션 추출 영구 금지."""
    
    def __init__(self, skeleton_path: Path):
        self.skeleton_path = skeleton_path
        self.content = skeleton_path.read_text(encoding="utf-8")
        self.lines = self.content.split("\n")
    
    def read_section(self, section_anchor: str) -> str:
        """section_anchor (예: '시점 동기화')에 해당하는 ### 헤더 아래 본문 결정론 추출."""
        in_section = False
        section_lines = []
        for line in self.lines:
            if line.startswith("### ") and section_anchor in line:
                in_section = True
                continue
            if in_section:
                if line.startswith("### "):  # 다음 ### 헤더에서 종료
                    break
                section_lines.append(line)
        return "\n".join(section_lines).strip()
    
    def read_agi_5_stages(self) -> List[str]:
        """AGI 5단계를 저자 skeleton에서 결정론 추출 (Round 9 #E4.1 강제)."""
        section = self.read_section("AGI 5단계 진화 프레임")
        # 정규식: "챗봇 → 추론가 → 대행자 → 혁신가 → 조직" 패턴 추출
        match = re.search(r"챗봇\s*→\s*(.+?)\s*→\s*(.+?)\s*→\s*(.+?)\s*→\s*(.+?)(\(AGI\))?", section)
        if match:
            return ["챗봇"] + list(match.groups()[:4])
        # fallback: 박스 list 형식
        stages = re.findall(r"단계\s*\d+[:\s-]\s*([^\n]+)", section)
        return stages if stages else []
```

---

## Patch #15 (F2.1): voice-yaml.md vocabulary.preferred metaphor_mapping 신규

**위반**: "부트로더·사만다·메타도구" source→target domain mapping 명시 부재 → AI가 은유 자의적 변형.

**Fix (data-schema-voice-yaml.md §4 vocabulary.preferred)**:
```yaml
vocabulary:
  preferred:
    # ⚠ Round 11 #F2.1 Critical 추가 — Lakoff/Johnson conceptual metaphor source→target 명시
    - term: "메타 도구"
      source_domain: "도구 사용 (망치·자동차·인쇄술)"
      target_domain: "AGI = 모든 도구를 만드는 도구 — 인지 자체를 확장하는 메타 차원"
      mapping_invariant: "도구가 *목적*이 아닌 *수단의 수단*으로 작동"
      misuse_warning: "단순 'AI 도구' 의미로 축소 사용 금지"
    
    - term: "부트로더"
      source_domain: "컴퓨터 부팅 시퀀스"
      target_domain: "AGI가 다음 단계 초지능의 디딤돌이 되는 위협 시나리오"
      mapping_invariant: "도구가 자기 목적을 떠나 다음 단계로 넘어가는 매개"
      misuse_warning: "단순 '시작점' 의미로 사용 금지 — 일론 머스크 부트로더 메타포 보존"
      authority_source: "AUTH-D-002"
    
    - term: "사만다"
      source_domain: "영화 〈Her〉 사만다 캐릭터"
      target_domain: "AGI 시대 누구나 자신의 조력자를 갖는 풍요의 표상"
      mapping_invariant: "관계·돌봄·이해를 매개하는 AI 동반자"
      misuse_warning: "감정적 의존·낭만화 회피 — 도구로서의 사만다 명시"
      authority_source: "영화 Her·skeleton.md §풍요의 극"
    
    - term: "기술적 사춘기"
      source_domain: "인간 사춘기 발달기"
      target_domain: "현재 AGI 이행기 — 자멸 위험 + 성장 가능성 공존"
      mapping_invariant: "위험한 전환 단계의 성숙 과제"
      authority_source: "AUTH-A-001 다리오 아모데이"
    
    - term: "UBI(지능)"
      source_domain: "UBI(소득) — Universal Basic Income"
      target_domain: "Universal Basic Intelligence — 모든 사람이 박사급 지능 접근"
      mapping_invariant: "보편적 분배의 대상이 *돈*에서 *지능*으로 확장"
      misuse_warning: "단순 'AI 보편화' 의미로 평탄화 금지"
      authority_source: "AUTH-B-001 {{저자명}} 저자 본인 명제"
```

---

## Patch #16 (F4.1): HITL response parser M16 신설

**위반**: 저자 묶음 응답 `1=a,b / 2=skip` 파싱이 결정론 모듈 없음 → LLM 자연어 추론.

**Fix (deterministic-modules.md M16 신규)**:
```python
### M16: hitl_response_parser.py (Round 11 #F4.1 Critical 신규)

import re
from dataclasses import dataclass
from typing import Dict, List, Union, Literal

@dataclass
class DecisionResponse:
    decision_id: int
    action: Union[List[str], Literal["skip", "defer"]]
    # action = ["a", "b"] (옵션 채택) or "skip" or "defer"

class HITLResponseParser:
    """저자 묶음 응답 `1=a,b / 2=skip / 3=defer` 결정론 파싱.
    LLM 자연어 추론으로 응답 해석 영구 금지."""
    
    # 결정론 정규식 — 캡처: 묶음 번호, 응답 (옵션 콤마 리스트 또는 skip|defer)
    PATTERN = re.compile(r"(\d+)\s*=\s*([a-z](?:,[a-z])*|skip|defer)", re.IGNORECASE)
    
    def parse(self, response: str) -> List[DecisionResponse]:
        """응답 텍스트 → DecisionResponse 리스트."""
        decisions = []
        for match in self.PATTERN.finditer(response):
            decision_id = int(match.group(1))
            raw_action = match.group(2).lower()
            if raw_action in ("skip", "defer"):
                action = raw_action
            else:
                # "a,b,c" → ["a", "b", "c"]
                action = [opt.strip() for opt in raw_action.split(",")]
            decisions.append(DecisionResponse(decision_id, action))
        return decisions
    
    def validate(self, decisions: List[DecisionResponse], 
                 expected_decision_ids: List[int]) -> List[str]:
        """검증: 저자 응답이 모든 묶음을 커버하는가."""
        responded_ids = {d.decision_id for d in decisions}
        missing = [did for did in expected_decision_ids if did not in responded_ids]
        return missing
```

cycle-registry.yaml §11 lib_versions에 `hitl_response_parser: "0.1.0"`·`skeleton_section_reader: "0.1.0"` 추가.

---

## Patch #17 (F4.2): atomic_writer 모듈 + chapter 파일 atomic save

**위반**: 사이클 중단 시 chapter .md 파일이 *반쯤 쓰인 상태*로 남을 위험. atomic write 정책 yaml만 적용.

**Fix (deterministic-modules.md M17 신규 + book-config 정책 확장)**:

**M17 atomic_writer.py**:
```python
### M17: atomic_writer.py (Round 11 #F4.2 Critical 신규)

import os
import tempfile
from pathlib import Path

class AtomicWriter:
    """모든 yaml registry + chapter .md 파일에 *atomic write* 강제.
    부분 작업 결과 보존 + 손상 방지."""
    
    def write(self, target_path: Path, content: str, encoding: str = "utf-8") -> None:
        """tmpfile → fsync → rename (POSIX atomic guarantee)."""
        target_path.parent.mkdir(parents=True, exist_ok=True)
        # 같은 파일시스템 안에 tmpfile 생성 (rename atomic 보장)
        fd, tmp_path = tempfile.mkstemp(
            dir=str(target_path.parent),
            prefix=f".{target_path.name}.",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding=encoding) as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            # rename은 POSIX atomic
            os.replace(tmp_path, str(target_path))
        except Exception:
            # 실패 시 tmpfile 정리
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
```

**book-config.yaml §7 backup_policy 확장**:
```yaml
backup_policy:
  ...
  atomic_write: true
  atomic_write_applies_to:                # Round 11 #F4.2 Critical
    - yaml_registries                      # seed-registry·cycle-registry·forecast-registry
    - chapter_md_files                     # narrative·analysis·implications·manuscript
    - book_config_itself                   # book-config.yaml 자체도 atomic
  atomic_writer_module: M17
```

---

## Patch #18 (F9.1): 생태·비인간 차원 옵션 활성화

**위반**: voice-yaml.md 사상적 척추 4개 모두 인간 중심. 5장 군사·환경 챕터 생태 차원 부재.

**Fix (data-schema-voice-yaml.md §4 vocabulary.preferred + prohibitions)**:
```yaml
vocabulary:
  preferred:
    # Round 11 #F9.1 Critical — 5장·환경 챕터 활성화 시 사용
    - term: "비인간 행위자"
      context: "5장 환경·9장 풍요 비전"
      target_domain: "AGI 시대 생태계·동물·식물의 위치"
      activation_chapters: [ch05, ch09]
    
    - term: "데이터센터 환경 비용"
      authority_source: "AUTH-A-017 IPCC|UNEP|IEA"
      target_domain: "AGI 컴퓨팅의 탄소·전력·물 발자국"
    
    - term: "생물권 정의"
      target_domain: "인간 외 생명의 권리·이해관계자 지위"

prohibitions:
  - id: PROH-007                            # Round 11 #F9.1 Critical 신규
    rule: "5장 군사·환경 챕터에서 생태·비인간 차원 *완전 부재*"
    severity: medium
    activation_chapters: [ch05]
    detection: "환경·기후·생태·비인간·생물권 어휘 카운트 < 3 시 알림"
    fix_action: "Botanist Gatekeeper 페르소나 발동 권장"
```

bookwriting-master.md §13 페르소나 풀에 12번째 페르소나 *Ecological Gatekeeper* 신설 — 5장·환경 챕터 작성 시 자동 발동, 생태 어휘 카운트 검증.

---

## 누적 통계 (전체 작업 — Round 11 patch 포함)

| Round | Critical 발견 | Critical 수정 |
|---|---|---|
| #A | 3 (이전 카운트 정정) | 3 |
| #B | 9 | 5 |
| #C | 9 | 6 |
| #D | 6 | 5 |
| #E | 14 | 14 |
| #F | 11 | **5 (본 patch)** |
| **누적** | **52 Critical** | **38 Critical 수정** |

남은 *deferred* 14건 (Phase 3-B 단계 처리):
- #B 4건 (Mode 2 동시·promote·external research 제약)
- #C 3건 (Layer 5 인용 가이드·세대별 voice·번역)
- #D 1건 (forecast-registry schema PUR-* 보강)
- #F 6건 (외부 표준 영역 — 도서관·라이선스·국방·재난·SPDX 2건)

---

## 수렴 추세 (지속)

- #A·B·C·D Critical 카운트: 3·9·9·6 (평균 ~7)
- #E Critical: 14 (구조적 결함 폭발)
- #F Critical: 11 (외연 확장 영역으로 이동)

**관측**: #F는 *진북 직접 매핑 안 되는 페르소나* 2명이 Critical 0건. 저자 *수렴 가능성 신호*. 다음 Round #G 진행 시 Critical *5건 이하* 가능성 높음.

---

**End of Round 11 Patches**

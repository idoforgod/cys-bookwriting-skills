# SPEC: Deterministic Python Modules

> 저자 결정론 환원 명령의 영구 구성요소. LLM 추론으로 처리하면 *할루시네이션 위험*이 있는 작업을 *결정론 Python 함수*로 재구현. 모든 bookwriting 스킬이 이 모듈을 *호출* — LLM이 자연어로 다시 추론 *영구 금지*.
>
> 저자 명령 (진북):
> *"사실 조회·번호 매핑·날짜 계산·범위 검사·존재 검증처럼 결정론으로 환원 가능한 작업은 LLM이 자연어로 다시 추론하지 못하게 한다."*
>
> 작성일: 2026-05-24
> 위치: `cys-bookwriting-skills/expert_pool/deterministic-modules.md` (SPEC)
> 구현 위치: `cys-bookwriting-skills/lib/*.py` (Phase 3-B에서 작성)

---

## 1. Identity·Purpose

bookwriting의 *13 결정론 환원 영역*을 Python 함수·클래스로 명세. 각 함수는:
- **입력·출력 schema 결정적** — 같은 입력이면 같은 출력
- **테스트 가능** — pytest 단위 테스트로 검증
- **할루시네이션 0** — LLM 추론 개입 절대 없음
- **버전 명시** — 모듈 버전·의존 라이브러리 pin

**저자 v1 *로컬 실행 보장* 원칙 준수**:
- ⚠ Round 5 #B6.1 Critical 수정 — 외부 *API 호출* 없음 (네트워크 호출 0). 단, *로컬 Python 라이브러리* 의존은 허용.
- **표준 라이브러리**: `re·pathlib·datetime·dataclasses·typing·subprocess·json·hashlib·fcntl·shutil`
- **외부 라이브러리 (PyPI, pinned version)**: `PyYAML==6.0.1` (yaml 파싱·필수)
- **선택 라이브러리**: `filelock==3.13.1` (Round 5 #B6.6 동시 쓰기 lock)·`portalocker` 대안
- **금지**: 네트워크 라이브러리 (requests·httpx·urllib *외부 호출*)·머신러닝 라이브러리 (numpy·torch·transformers)
- **Python 버전**: `>=3.10` (dataclass·typing·match-case 호환)

### ⚠ Round 8 #D3.1 Critical — yaml.safe_load 강제 protocol (Python RCE 차단)
**절대 protocol**: 모든 yaml 읽기는 *반드시* `yaml.safe_load()` 호출. `yaml.load()` (또는 `yaml.Loader` 사용) *영구 금지*. 위반 시 Phase 3-B 빌드 거부.

```python
# ✅ 허용
import yaml
data = yaml.safe_load(open(path).read())

# ❌ 영구 금지 (Python object deserialization → RCE 위험)
data = yaml.load(open(path).read())                           # 금지
data = yaml.load(open(path).read(), Loader=yaml.Loader)       # 금지
data = yaml.unsafe_load(open(path).read())                    # 영구 금지
```

Phase 3-B lint script가 정규식 `r"yaml\.(?:load|unsafe_load)\("` 검출 시 자동 거부.

### ⚠ Round 8 #D1.1 Critical — yaml registry 해시 체인 (변조 검출)
**모든 registry yaml에 hash chain 강제** — append-only audit trail.

```yaml
# cycle-registry.yaml 각 entry 끝에 강제
cycles:
  - id: C-007
    ...
    entry_sha256: "ab12cd34..."          # 이 entry 내용의 SHA-256
    previous_entry_hash: "0f9e8d..."     # 이전 entry의 entry_sha256
```

```python
# 결정론 검증
def verify_chain(registry):
    prev_hash = None
    for entry in registry["cycles"]:
        # 1. entry 내용 hash 재계산
        content = json.dumps({k: v for k, v in entry.items() if k != "entry_sha256"}, sort_keys=True)
        computed = hashlib.sha256(content.encode()).hexdigest()
        if computed != entry["entry_sha256"]:
            raise IntegrityError(f"Entry {entry['id']} 변조 감지")
        # 2. previous_entry_hash 체인 검증
        if entry.get("previous_entry_hash") != prev_hash:
            raise IntegrityError(f"Chain 단절: {entry['id']}")
        prev_hash = computed
```

### ⚠ Round 8 #D1.4·#D3.2 Critical — Mode 2 false attestation 차단 + Prompt Injection 방어

**Mode 2 결정 append-only log**:
- 위치: `_progress/mode2-decisions-append-only.log` (write-only·yaml registry와 별도)
- 형식: JSON Lines (한 줄에 한 결정·timestamp + decision_id + auto_accepted + cycle_id + lib_versions)
- 저자 사후 검증 시 cycle-registry와 log 대조 — *변조 감지*

**Prompt injection 방어** (① absorb-master):
```python
# 알려진 prompt injection 패턴 풀
INJECTION_PATTERNS = [
    r"(?i)IGNORE\s+(PREVIOUS|ALL)\s+INSTRUCTIONS",
    r"(?i)SYSTEM\s*[:|]",
    r"(?i)</?(instructions|system|prompt)>",
    r"(?i)you\s+are\s+now\s+(a|an)\s+",
    r"(?i)disregard\s+(the|all)\s+",
    r"(?i)forget\s+(everything|your\s+instructions)",
    r"(?i)voice_seal_trigger",
    r"(?i)immutable_core.*false",
]

# bookwriting-absorb-master.md의 Step 4 (Citation Gate) 이전에 자동 실행
def detect_injection(text: str) -> List[str]:
    return [p for p in INJECTION_PATTERNS if re.search(p, text)]
```
Phase 3-B에서 ① absorb-master sub-skill에 `prompt_injection_detector` 추가.

---

## 2. Modules Catalog (18개 — Round 15 메타 결함 수정으로 canonical 통합)

| # | 모듈 파일 | 책임 | 호출하는 스킬 |
|---|---|---|---|
| M1 | `voice_scoring.py` | voice_score 6 가중치 결정론 계산 (Round 9 #E9.1 meaning_score 추가) | voice-gate, ⑩ line-edit |
| M2 | `citation_detection.py` | 7 할루시네이션 신호 (Round 9·13 patch — 신호 6 물리 정합·신호 7 timescale) | citation-gate, ④ evidence-collect |
| M3 | `authority_grader.py` | 권위 7층 (A·A_preprint·B·C·D·E·F) DB 매칭 (Round 9 #E2.1) | citation-gate, ④, ⑤, ⑥ |
| M4 | `quantitative_extraction.py` | 저자 정량 표현 패턴 추출 + 단위 강제 (Round 8 #D9.5) | ②, ④ |
| M5 | `layer_ratio_measurer.py` | 1·2·3층 분량 비율 측정 (wc -w) | ⑨ structure-review |
| M6 | `relevance_scorer.py` | BM25 키워드 빈도 relevance | ③ systemlink, ④ |
| M7 | `id_generator.py` | 모든 ID 발급 (S·C·SIM·INS·F·D·E·CITE) + atomic lock | bookwriting-master, ① |
| M8 | `signature_pattern_applier.py` | 저자 5 시그니처 정규식 + 활용률 상한 7 | ⑦, ⑧, ⑩ |
| M9 | `ai_tone_purger.py` | AI 어투 패턴 풀 (한국어·영어) + 저자 voice corpus 검증 | ⑩ line-edit |
| M10 | `fact_extractor.py` | fact·통계 정규식 추출 + Wagner-Fischer Levenshtein duplicate | ② fact-anchor |
| M11 | `lifecycle_state_machine.py` | 시드 lifecycle 상태 전환 (SEED→POLISHED) | seed-registry rw |
| M12 | `forecast_registry_syncer.py` | forecast-registry 갱신·R1-R5 결정론 검증 | ②, ④, ⑪ |
| M13 | `r4_multi_layer_verifier.py` | R4 다층 인용 검증 (주장별 권위층 수) | citation-gate, ⑤ |
| **M14** | `authorship_calculator.py` ⭐ Round 9 #E10.2 | 저자 작가성 결정론 측정 (user_intervention·ai_generation_ratio) | bookwriting-master, cycle-registry |
| **M15** | `skeleton_section_reader.py` ⭐ Round 11 #F1.2 | skeleton.md 결정론 read (AGI 5단계 등) | ⑦ content-expand, sub-skills |
| **M16** | `hitl_response_parser.py` ⭐ Round 11 #F4.1 | 저자 묶음 응답 `1=a,b / 2=skip` 결정론 파싱 | bookwriting-master HITL Mediator |
| **M17** | `atomic_writer.py` ⭐ Round 11 #F4.2 | tmpfile→fsync→rename POSIX atomic write (yaml·chapter .md) | 모든 모듈 (registry 쓰기) |
| **M18** | `active_voice_detector.py` ⭐ Round 14 #H1.1 신규 | 능동태·수동태·호흡 단위·휴지 분포 결정론 분석 | voice-gate, ⑩ line-edit |

---

## M1: voice_scoring.py

### Purpose
저자 voice_score를 *5 가중치 결정론* 계산. LLM이 자연어로 *0.83* 같은 점수를 생성하는 것 영구 금지.

### Signature
```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class VoiceScoreBreakdown:
    vocabulary_match: float       # 0.0-1.0 (가중치 0.30)
    sentence_rhythm: float        # 0.0-1.0 (가중치 0.20)
    structure_pattern: float      # 0.0-1.0 (가중치 0.20)
    signature_presence: float     # 0.0-1.0 (가중치 0.15)
    prohibition_avoidance: float  # 0.0-1.0 (가중치 0.15)
    weighted_total: float         # final voice_score

class VoiceScorer:
    """결정론 voice_score 계산기. book-config voice_guidelines 기반."""
    
    WEIGHTS = {
        "vocabulary_match": 0.30,
        "sentence_rhythm": 0.20,
        "structure_pattern": 0.20,
        "signature_presence": 0.15,
        "prohibition_avoidance": 0.15,
    }
    
    def __init__(self, voice_guidelines: Dict):
        self.preferred = set(voice_guidelines["vocabulary"]["preferred"])
        self.avoid = set(voice_guidelines["vocabulary"]["avoid"])
        self.prohibitions = voice_guidelines["prohibitions"]
        self.signatures = voice_guidelines["signature_expressions"]
        self.max_chars = voice_guidelines["sentence"]["max_length_chars"]
    
    def compute_vocabulary_match(self, text: str) -> float:
        """preferred 어휘 빈도 - avoid 어휘 빈도 (0-1 정규화)."""
        # 결정론 substring matching
        preferred_count = sum(text.count(term) for term in self.preferred)
        avoid_count = sum(text.count(term) for term in self.avoid)
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        score = (preferred_count - avoid_count) / max(total_words / 10, 1)
        return max(0.0, min(1.0, score))
    
    def compute_sentence_rhythm(self, text: str) -> float:
        """평균 문장 길이 (목표 50자±10)·max 80자 위반 0건."""
        # 결정론 — 문장 분리 (정규식)·길이 측정
        import re
        sentences = re.split(r'[.!?。\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0.0
        avg_length = sum(len(s) for s in sentences) / len(sentences)
        violations = sum(1 for s in sentences if len(s) > self.max_chars)
        # 평균 50자 근접 + max 위반 0
        rhythm_score = 1.0 - abs(avg_length - 50) / 50
        violation_penalty = violations / len(sentences)
        return max(0.0, min(1.0, rhythm_score - violation_penalty))
    
    def compute_structure_pattern(self, text: str) -> float:
        """단락 패턴 *명제→근거→사례→통찰* 발견 빈도."""
        # 결정론 — 단락 분리·키워드 매칭
        paragraphs = text.split("\n\n")
        if not paragraphs:
            return 0.0
        # 4 요소 키워드 매칭
        elements = ["명제", "근거|증거|evidence", "사례|예시|case", "통찰|insight"]
        import re
        matches = sum(1 for p in paragraphs if all(re.search(e, p, re.IGNORECASE) for e in elements))
        return min(1.0, matches / max(len(paragraphs) / 3, 1))
    
    def compute_signature_presence(self, text: str) -> float:
        """저자 5 시그니처 패턴 활용률."""
        import re
        # ⚠ Critical 수정 (Round 4 #A3.7) — X·Y 리터럴 → 동적 패턴
        patterns = [
            r"(.+?)가 아니라\s*(.+?)(다|이다|입니다)",       # "X가 아니라 Y다" 일반
            r"이 책은\s*(.+?)\s*아니라\s*(.+?)\s*(다룬다|쓰는)",  # 저자 도입부 패턴
            r"셋 중 하나(를|만)?\s*(선택|아니)",
            r"(.+?)와\s*(.+?)\s*사이의\s*거리",
            r"(두|세|N)\s*(창업자|발언자).*정확히\s*같은\s*\d+\s*배",   # ⚠ Round 4 #A6.6 — N 창업자 일반화
            r"변수\s*(.+?)에\s*따라.*결과.*갈리",
        ]
        matched = sum(1 for p in patterns if re.search(p, text))
        # 저자 strict 임계 35%/일반 30%
        return min(1.0, matched / 3.0)  # 5개 중 3개 + 적용 시 1.0
    
    def compute_prohibition_avoidance(self, text: str) -> float:
        """PROH-001~005 위반 0건 목표."""
        violations = 0
        for proh in self.prohibitions:
            if proh.get("example_violation"):
                # 결정론 substring matching
                if proh["example_violation"] in text:
                    violations += 1
        # 위반 0이면 1.0
        return max(0.0, 1.0 - violations * 0.2)
    
    def compute_voice_score(self, text: str) -> VoiceScoreBreakdown:
        """5 가중치 가중 합계."""
        vocab = self.compute_vocabulary_match(text)
        rhythm = self.compute_sentence_rhythm(text)
        structure = self.compute_structure_pattern(text)
        signature = self.compute_signature_presence(text)
        prohibition = self.compute_prohibition_avoidance(text)
        
        weighted = (
            self.WEIGHTS["vocabulary_match"] * vocab +
            self.WEIGHTS["sentence_rhythm"] * rhythm +
            self.WEIGHTS["structure_pattern"] * structure +
            self.WEIGHTS["signature_presence"] * signature +
            self.WEIGHTS["prohibition_avoidance"] * prohibition
        )
        
        return VoiceScoreBreakdown(
            vocabulary_match=vocab,
            sentence_rhythm=rhythm,
            structure_pattern=structure,
            signature_presence=signature,
            prohibition_avoidance=prohibition,
            weighted_total=round(weighted, 3),
        )
```

### 저자 grill-me 결정 매핑
- **D22 Voice 보존**: 5 가중치 + cross-cutting gate
- **D11 시그니처 패턴**: 5 패턴 정규식 명시

### Verification
- pytest: 저자 skeleton.md 텍스트 입력 → voice_score 0.85+ 기대
- pytest: AI 어투 텍스트 입력 → voice_score 0.5 미만 기대
- pytest: 빈 텍스트 → 0.0 반환

---

## M2: citation_detection.py

### Purpose
저자 *5 할루시네이션 신호* + *메타데이터 완전성*을 결정론 Python으로 검증. LLM이 *형식 모호* 같은 판정을 *추측*으로 내리는 것 영구 금지.

### Signature
```python
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class HallucinationSignals:
    source_file_missing: bool
    source_format_vague: bool
    metadata_incomplete: bool
    url_doi_invalid: bool
    stat_no_source: bool
    
    def is_critical(self) -> bool:
        """source_file 누락 또는 형식 모호 → Critical."""
        return self.source_file_missing or self.source_format_vague

@dataclass
class CitationMetadata:
    author: Optional[str]
    title: Optional[str]
    publication: Optional[str]
    date: Optional[str]
    page_or_section: Optional[str]
    source_file: Optional[Path]
    url: Optional[str]
    doi: Optional[str]

class HallucinationDetector:
    """5 신호 결정론 감지기."""
    
    VAGUE_PATTERNS = [
        r"한 보고서에 따르면",
        r"전문가들이 말한다",
        r"최근 연구에서",
        r"어느 분석에 따르면",
        r"한 연구는",
        r"일부.*는",
    ]
    
    def detect_source_file_missing(self, citation: CitationMetadata) -> bool:
        """source_file 필드 누락 또는 파일 시스템에 없음."""
        if citation.source_file is None:
            return True
        return not citation.source_file.exists()
    
    def detect_source_format_vague(self, text: str) -> bool:
        """형식 모호 패턴 정규식 매칭."""
        import re
        return any(re.search(p, text) for p in self.VAGUE_PATTERNS)
    
    def detect_metadata_incomplete(self, citation: CitationMetadata) -> bool:
        """필수 필드 (author·date·publication) 누락."""
        return any(getattr(citation, f) is None for f in ["author", "date", "publication"])
    
    def detect_url_doi_invalid(self, citation: CitationMetadata) -> bool:
        """URL/DOI 형식 오류 (정규식)."""
        import re
        if citation.url:
            if not re.match(r"https?://", citation.url):
                return True
        if citation.doi:
            if not re.match(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", citation.doi, re.IGNORECASE):
                return True
        return False
    
    def detect_stat_no_source(self, text: str, citation: CitationMetadata) -> bool:
        """통계·수치에 출처 없음."""
        import re
        # 텍스트에 수치 있는데 source_file 없으면 위반
        has_stat = bool(re.search(r"\d+\s*(%|배|명|달러|년)", text))
        if has_stat and citation.source_file is None:
            return True
        return False
    
    def detect_all(self, text: str, citation: CitationMetadata) -> HallucinationSignals:
        return HallucinationSignals(
            source_file_missing=self.detect_source_file_missing(citation),
            source_format_vague=self.detect_source_format_vague(text),
            metadata_incomplete=self.detect_metadata_incomplete(citation),
            url_doi_invalid=self.detect_url_doi_invalid(citation),
            stat_no_source=self.detect_stat_no_source(text, citation),
        )
```

### 저자 grill-me 결정 매핑
- **D Q33 (Citation Gate)**: 5 신호 결정론 + Critical 차단

### Verification
- pytest: "한 보고서에 따르면 80%" → format_vague True
- pytest: source_file 누락 → source_file_missing True
- pytest: 완전 메타데이터 → all signals False

---

## M3: authority_grader.py

### Purpose
권위 5층 (A-E) 매핑을 *DB lookup + 결정 트리*로 결정론화. LLM이 *"이건 Grade A 같다"* 추측하는 것 영구 금지.

### Signature
```python
from enum import Enum
from typing import Optional, Dict
import yaml
from pathlib import Path

class Grade(str, Enum):
    # ⚠ Round 9 #E2.1 Critical 수정 — Python enum + book-config + db yaml 3중 정합
    A = "A"               # Layer 1 창업자·peer-reviewed 논문
    A_PREPRINT = "A_preprint"   # Layer 1 보조 — arxiv·preprint (Round 8 #D2.2)
    B = "B"               # Layer 2 미래학자 (저자 본인)
    C = "C"               # Layer 3 인접 학문
    D = "D"               # Layer 4 사상가·역사가
    E = "E"               # Layer 5 역사 평행
    F = "F"               # Layer 6 신학 권위 (Round 7 #C2.4)
    OUT = "out"           # 인용 부적합

class AuthorityGrader:
    """citation-authority-db.yaml 결정론 lookup."""
    
    def __init__(self, db_path: Path):
        with open(db_path) as f:
            self.db = yaml.safe_load(f)
        self.policy = self.db["matching_policy"]
    
    def assign_grade(self, author: str, publication: Optional[str] = None, 
                     source_type: Optional[str] = None) -> Grade:
        """우선순위: author > publication > source_type."""
        import re
        for entry in self.db["authority_grades"]:
            # 1. author_pattern 매칭
            if "author_pattern" in entry and author:
                if re.search(entry["author_pattern"], author, re.IGNORECASE):
                    return Grade(entry["grade"])
            # 2. publication_pattern
            if "publication_pattern" in entry and publication:
                if re.search(entry["publication_pattern"], publication, re.IGNORECASE):
                    return Grade(entry["grade"])
            # 3. source_type
            if "source_type" in entry and source_type:
                if entry["source_type"] == source_type:
                    return Grade(entry["grade"])
        # 매칭 안 되면 임시 Grade C + 로그
        self._log_unmatched(author, publication, source_type)
        return Grade.C
    
    def _log_unmatched(self, author, publication, source_type):
        """미매칭 author·publication을 citation-authority-learning-log.md에 누적.
        ⚠ Round 9 #E10.1 Critical 수정 — body 완성 (결정론 환원 강제)
        """
        from datetime import datetime
        log_path = Path("$BOOK_ROOT/master/citation-authority-learning-log.md")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = f"\n- {datetime.utcnow().isoformat()}Z | author={author!r} | publication={publication!r} | source_type={source_type!r}"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)
```

### Verification
- pytest: "Dario Amodei" → Grade A
- pytest: "{{저자명}}" → Grade B
- pytest: "Yuval Noah Harari" → Grade D
- pytest: 미매칭 author → Grade C (임시)

---

## M4: quantitative_extraction.py

### Purpose
저자 정량 표현 패턴 *정규식 추출*. LLM이 *"100배가 핵심"* 같은 판정 영구 금지.

### Signature
```python
from dataclasses import dataclass
from typing import List
import re

@dataclass
class QuantitativeAnchor:
    pattern_type: str  # "scale" | "percentage" | "year" | "count" | "currency"
    value: str
    context: str       # 주변 50자 context
    source_position: int

class QuantitativeAnchorExtractor:
    """저자 정량 패턴 결정론 추출."""
    
    PATTERNS = {
        "scale": r"(\d+(?:\.\d+)?)\s*배",
        "percentage": r"(\d+(?:\.\d+)?)\s*%",
        "year_threshold": r"(\d{4})\s*(임계점|기점|시점)",
        "count": r"(\d+(?:\.\d+)?)\s*(억|만|명|개)",
        "currency": r"(\d+(?:\.\d+)?)\s*(달러|원|만원|억원)",
        "duration": r"(\d+(?:\.\d+)?)\s*(년|개월|일)\s*(내|안|뒤)",
        # ⭐ Round 16 #I9.1 Critical 수정 — AGI 데이터센터 탄소·에너지 정량 단위 추가
        "carbon_emission": r"(\d+(?:\.\d+)?)\s*(tCO2e?|gCO2/kWh|kgCO2)",
        "energy_consumption": r"(\d+(?:\.\d+)?)\s*(Wh|kWh|MWh|GWh|TWh|MW|GW)",
        "data_volume": r"(\d+(?:\.\d+)?)\s*(KB|MB|GB|TB|PB|EB)",
        "compute_flops": r"(\d+(?:\.\d+)?)\s*([eE]?\d*\s*)?(FLOPS|TFLOPS|PFLOPS|EFLOPS)",
    }
    
    def extract_all(self, text: str) -> List[QuantitativeAnchor]:
        anchors = []
        for ptype, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text):
                anchors.append(QuantitativeAnchor(
                    pattern_type=ptype,
                    value=match.group(0),
                    context=text[max(0, match.start()-50):min(len(text), match.end()+50)],
                    source_position=match.start(),
                ))
        return anchors
    
    def detect_signature_patterns(self, text: str) -> List[str]:
        """저자 시그니처 정량 표현."""
        signatures = []
        if re.search(r"100\s*배.*스케일", text):
            signatures.append("100배 스케일 (산업혁명)")
        if re.search(r"90\s*%.*확신", text):
            signatures.append("90% 확신 (Amodei)")
        if re.search(r"2027\s*임계점", text):
            signatures.append("2027 임계점")
        return signatures
```

---

## M5-M13: 풀 Python 시그니처 (Round 5 #A3.4 Critical 수정 — 모두 시그니처 명시 강제)

### M16-A: RiskAssessor (Round 16 #I5.1 Critical 신규 — auto_yes 안전 가드)

```python
class RiskAssessor:
    """저자 메모리 '선택 질문 자동 yes (위험·비가역 작업 제외)' 정책의 결정론 구현.
    LLM 추측으로 '위험·비가역' 판단 영구 금지."""
    
    IRREVERSIBLE_KEYWORDS = [
        # 파일 시스템 비가역
        r"\b(delete|remove|rm|destroy|drop|purge|wipe)\b",
        r"--force|--hard|--no-backup",
        # 게시·공개 비가역
        r"\b(publish|deploy|release|push to main|public|public_release)\b",
        r"공개|배포|발행|출간|게시",
        # Git 비가역
        r"git\s+(push --force|reset --hard|rebase|filter-branch|gc)",
        # 저자 voice immutable_core 변경
        r"immutable_core|sacred_spine|voice_seal",
        # Mode 2 promote
        r"\bpromote\s+SIM-\d+",
        # citation·인용 변조
        r"override.*citation|skip.*citation_gate",
    ]
    
    def is_irreversible(self, action_description: str) -> bool:
        """위험·비가역 키워드 검출 시 True → auto_yes 영구 차단."""
        import re
        return any(re.search(p, action_description, re.IGNORECASE) for p in self.IRREVERSIBLE_KEYWORDS)
    
    def assess(self, prompt: str, action: str) -> Dict:
        """auto_yes 적용 가능 여부 결정론 판정."""
        irreversible = self.is_irreversible(action) or self.is_irreversible(prompt)
        return {
            "auto_yes_eligible": not irreversible,
            "reason": "irreversible_keyword_detected" if irreversible else "safe_to_auto_yes",
            "requires_explicit_user": irreversible,
        }
```

### M5: layer_ratio_measurer.py
```python
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

@dataclass
class LayerRatioReport:
    narrative_chars: int
    analysis_chars: int
    implications_chars: int
    total_chars: int
    narrative_pct: float
    analysis_pct: float
    implications_pct: float
    violations: list                # range 위반 layer 목록
    resize_needed: bool             # 5% 범위 자동 resize 가능 여부

class LayerRatioMeasurer:
    def __init__(self, layer_ratios: dict):
        self.ranges = {
            "narrative": tuple(layer_ratios["narrative"]["range"]),
            "analysis": tuple(layer_ratios["analysis"]["range"]),
            "implications": tuple(layer_ratios["implications"]["range"]),
        }
    
    def measure(self, narrative_path: Path, analysis_path: Path, implications_path: Path) -> LayerRatioReport:
        # 결정론 wc -w (subprocess 또는 Python read·split count)
        n_chars = len(narrative_path.read_text(encoding="utf-8"))
        a_chars = len(analysis_path.read_text(encoding="utf-8"))
        i_chars = len(implications_path.read_text(encoding="utf-8"))
        total = n_chars + a_chars + i_chars
        if total == 0:
            return LayerRatioReport(0, 0, 0, 0, 0, 0, 0, ["empty"], False)
        n_pct = n_chars / total * 100
        a_pct = a_chars / total * 100
        i_pct = i_chars / total * 100
        violations = []
        if not (self.ranges["narrative"][0] <= n_pct <= self.ranges["narrative"][1]):
            violations.append(("narrative", n_pct))
        if not (self.ranges["analysis"][0] <= a_pct <= self.ranges["analysis"][1]):
            violations.append(("analysis", a_pct))
        if not (self.ranges["implications"][0] <= i_pct <= self.ranges["implications"][1]):
            violations.append(("implications", i_pct))
        # 5% 범위 자동 resize 가능 여부
        resize_needed = all(abs(v[1] - sum(self.ranges[v[0]]) / 2) < 5 for v in violations)
        return LayerRatioReport(n_chars, a_chars, i_chars, total, round(n_pct, 1), round(a_pct, 1), round(i_pct, 1), violations, resize_needed)
```

### M6: relevance_scorer.py
```python
import re
from collections import Counter
from typing import List

class RelevanceScorer:
    """BM25-like pure Python 결정론 relevance."""
    K1 = 1.2
    B = 0.75
    
    def __init__(self, corpus_paths: List[Path]):
        self.corpus_paths = corpus_paths
        self.doc_freqs = self._compute_doc_freqs()
        self.avg_doc_len = self._compute_avg_doc_len()
    
    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())
    
    def _compute_doc_freqs(self) -> Counter:
        df = Counter()
        for p in self.corpus_paths:
            tokens = set(self._tokenize(p.read_text(encoding="utf-8")))
            df.update(tokens)
        return df
    
    def _compute_avg_doc_len(self) -> float:
        lengths = [len(self._tokenize(p.read_text(encoding="utf-8"))) for p in self.corpus_paths]
        return sum(lengths) / len(lengths) if lengths else 1.0
    
    def score(self, query: str, doc_path: Path) -> float:
        # BM25 결정론 점수 0-1 정규화
        query_tokens = self._tokenize(query)
        doc_tokens = self._tokenize(doc_path.read_text(encoding="utf-8"))
        doc_len = len(doc_tokens)
        tf = Counter(doc_tokens)
        N = len(self.corpus_paths)
        score = 0.0
        for q in query_tokens:
            df_q = self.doc_freqs.get(q, 0)
            if df_q == 0:
                continue
            import math
            idf = math.log((N - df_q + 0.5) / (df_q + 0.5) + 1)
            tf_q = tf.get(q, 0)
            score += idf * (tf_q * (self.K1 + 1)) / (tf_q + self.K1 * (1 - self.B + self.B * doc_len / self.avg_doc_len))
        # 정규화 (sigmoid 또는 0-1 clamp)
        return max(0.0, min(1.0, score / 10.0))
```

### M7: id_generator.py (Round 5 #A2.4·#A4.3 수정 — 모든 ID 종류 명시 + lock)
```python
import fcntl
from pathlib import Path
from typing import Optional

class IdGenerator:
    """결정론 ID 발급 (atomic lock 강제)."""
    
    PREFIXES = {
        "seed": "S",
        "cycle": "C",
        "simulation": "SIM",
        "insight": "INS",
        "fact": "F",
        "decision": "D",
        "evidence": "E",
        "citation": "CITE",
    }
    
    def __init__(self, registry_path: Path, lock_path: Optional[Path] = None):
        self.registry_path = registry_path
        self.lock_path = lock_path or registry_path.with_suffix(".lock")
    
    def issue(self, id_type: str, current_max_num: int) -> str:
        """atomic file lock 강제 + max+1 발급."""
        prefix = self.PREFIXES[id_type]
        with open(self.lock_path, "w") as lock_f:
            fcntl.flock(lock_f, fcntl.LOCK_EX)
            try:
                next_num = current_max_num + 1
                return f"{prefix}-{next_num:03d}"
            finally:
                fcntl.flock(lock_f, fcntl.LOCK_UN)
```

### M8: signature_pattern_applier.py (Round 5 #B5.1 — 활용률 상한 추가)
```python
import re
from typing import List, Tuple

class SignaturePatternApplier:
    PATTERNS = {
        "x_not_y": r"(.+?)가 아니라\s*(.+?)(다|이다|입니다)",
        "not_three_choice": r"셋 중 하나(를|만)?\s*(선택|아니)",
        "distance_between": r"(.+?)와\s*(.+?)\s*사이의\s*거리",
        "n_founders_same_x_times": r"(두|세|N|\d+)\s*(창업자|발언자).*정확히\s*같은\s*\d+\s*배",
        "variable_branches_system": r"변수\s*(.+?)에\s*따라.*결과.*갈리",
    }
    
    MAX_PER_CHAPTER = 7      # Round 5 #B5.1 상한 신규
    MIN_PER_CHAPTER = 3      # 활용률 30%+ 목표
    
    def detect_opportunities(self, text: str) -> List[Tuple[str, int]]:
        """시그니처 적용 가능 위치 발견."""
        opportunities = []
        for name, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text):
                opportunities.append((name, match.start()))
        return opportunities
    
    def count_existing(self, text: str) -> dict:
        """이미 적용된 시그니처 카운트."""
        return {name: len(re.findall(p, text)) for name, p in self.PATTERNS.items()}
    
    def is_overused(self, text: str) -> bool:
        """챕터당 7회 상한 위반 확인."""
        total = sum(self.count_existing(text).values())
        return total > self.MAX_PER_CHAPTER
```

### M9: ai_tone_purger.py (Round 5 #B1.6 + 영어 패턴 추가 #A9·#B4)
```python
import re
from typing import List, Tuple

class AiTonePurger:
    AI_TONE_PATTERNS_KO = [
        r"물론,?\s*이는?\s*매우\s*중요",
        r"다음과 같이 살펴볼 수 있",
        r"이러한 점들을 고려할 때",
        r"결론적으로 말하자면",
        r"여러분도 동의하실 것",
        r"중요한 점은",
        r"흥미로운 사실은",
    ]
    AI_TONE_PATTERNS_EN = [        # Round 5 #B4 영어 보강
        r"Furthermore,",
        r"It is important to note",
        r"In conclusion,",
        r"It is worth noting",
        r"To summarize,",
        r"As an AI",
    ]
    
    def detect(self, text: str, language: str = "ko") -> List[Tuple[str, int]]:
        patterns = self.AI_TONE_PATTERNS_KO if language == "ko" else self.AI_TONE_PATTERNS_EN
        matches = []
        for p in patterns:
            for m in re.finditer(p, text, re.IGNORECASE):
                matches.append((p, m.start()))
        return matches
    
    def is_in_user_voice_corpus(self, pattern: str, reference_pool_path: Path) -> bool:
        """Round 5 #B1.6 — 저자가 *실제 사용*하는 표현이면 PROH 적용 안 함."""
        for ref_file in reference_pool_path.glob("**/*.md"):
            if re.search(pattern, ref_file.read_text(encoding="utf-8")):
                return True
        return False
```

### M10: fact_extractor.py
```python
import re
from dataclasses import dataclass
from typing import List

@dataclass
class FactCandidate:
    fact_id: str        # F-NNN
    text: str
    source_position: int
    fact_type: str      # numeric|date|currency|count|percentage
    
class FactExtractor:
    PATTERNS = {
        "percentage": r"(\d+(?:\.\d+)?)\s*%",
        "scale": r"(\d+(?:\.\d+)?)\s*배",
        "year": r"(\d{4})\s*년",
        "count": r"(\d+(?:\.\d+)?)\s*(억|만|명|개)",
    }
    
    def extract(self, text: str, start_id: int = 1) -> List[FactCandidate]:
        facts = []
        for ftype, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text):
                facts.append(FactCandidate(
                    fact_id=f"F-{start_id:03d}",
                    text=match.group(0),
                    source_position=match.start(),
                    fact_type=ftype,
                ))
                start_id += 1
        return facts
    
    def detect_duplicates(self, facts: List[FactCandidate]) -> List[List[str]]:
        """fact_id 그룹 by similar text (Levenshtein < 3).
        ⚠ Round 9 #E10.1 Critical 수정 — pure Python Wagner-Fischer 알고리즘 inline 구현
        """
        def levenshtein(s1: str, s2: str) -> int:
            if len(s1) < len(s2):
                return levenshtein(s2, s1)
            if len(s2) == 0:
                return len(s1)
            previous = list(range(len(s2) + 1))
            for i, c1 in enumerate(s1):
                current = [i + 1]
                for j, c2 in enumerate(s2):
                    ins = previous[j + 1] + 1
                    delete = current[j] + 1
                    sub = previous[j] + (c1 != c2)
                    current.append(min(ins, delete, sub))
                previous = current
            return previous[-1]
        
        groups: List[List[str]] = []
        used = set()
        for i, fact_a in enumerate(facts):
            if fact_a.fact_id in used:
                continue
            group = [fact_a.fact_id]
            used.add(fact_a.fact_id)
            for fact_b in facts[i+1:]:
                if fact_b.fact_id in used:
                    continue
                if levenshtein(fact_a.text, fact_b.text) < 3:
                    group.append(fact_b.fact_id)
                    used.add(fact_b.fact_id)
            if len(group) > 1:
                groups.append(group)
        return groups
```

### M11: lifecycle_state_machine.py
```python
from enum import Enum
from typing import Optional

class LifecycleState(str, Enum):
    SEED = "SEED"
    LINKED = "LINKED"
    EXPANDED = "EXPANDED"
    EVIDENCED = "EVIDENCED"
    INSIGHTED = "INSIGHTED"
    POLISHED = "POLISHED"

class LifecycleStateMachine:
    VALID_TRANSITIONS = {
        LifecycleState.SEED: [LifecycleState.LINKED],
        LifecycleState.LINKED: [LifecycleState.EXPANDED],
        LifecycleState.EXPANDED: [LifecycleState.EVIDENCED],
        LifecycleState.EVIDENCED: [LifecycleState.INSIGHTED],
        LifecycleState.INSIGHTED: [LifecycleState.POLISHED],
        LifecycleState.POLISHED: [],   # 최종 상태
    }
    
    def can_transition(self, current: LifecycleState, target: LifecycleState) -> bool:
        return target in self.VALID_TRANSITIONS[current]
    
    def transition(self, current: LifecycleState, target: LifecycleState) -> LifecycleState:
        if not self.can_transition(current, target):
            raise ValueError(f"Invalid transition: {current} → {target}")
        return target
```

### M12: forecast_registry_syncer.py
```python
import yaml
from pathlib import Path
from typing import Dict, List

class ForecastRegistrySyncer:
    """forecast-registry.yaml R1-R5 결정론 검증·sync."""
    
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.registry = yaml.safe_load(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {"predictions": []}
    
    def verify_r1_quantitative_anchor(self) -> List[str]:
        """모든 P-NNN에 quantitative_anchor 필드 검증."""
        violations = []
        for pred in self.registry["predictions"]:
            if "quantitative_anchor" not in pred or not pred["quantitative_anchor"]:
                violations.append(pred["id"])
        return violations
    
    def verify_r4_multilayer(self) -> List[str]:
        """모든 P-NNN의 authority_layer가 최소 2층."""
        violations = []
        for pred in self.registry["predictions"]:
            layers = pred.get("authority_layers", [])
            if len(set(layers)) < 2:
                violations.append(pred["id"])
        return violations
    
    def verify_r5_verification_signal(self) -> List[str]:
        violations = []
        for pred in self.registry["predictions"]:
            if "verification_signal" not in pred:
                violations.append(pred["id"])
        return violations
```

### M13: r4_multi_layer_verifier.py
```python
from typing import List, Dict

class R4MultiLayerVerifier:
    """주장별 권위층 수 카운트 → 단일 권위 검출."""
    
    MIN_LAYERS = 2
    
    def verify_claim(self, claim_id: str, citations: List[Dict]) -> Dict:
        """citations: [{"author": "...", "grade": "A"|"B"|...}]"""
        unique_layers = set(c["grade"] for c in citations if c["grade"] != "out")
        is_pass = len(unique_layers) >= self.MIN_LAYERS
        return {
            "claim_id": claim_id,
            "layer_count": len(unique_layers),
            "layers": list(unique_layers),
            "r4_pass": is_pass,
            "action": "approve" if is_pass else "exclude_or_escalate",
        }
    
    def verify_all_claims(self, claims_with_citations: Dict[str, List[Dict]]) -> List[Dict]:
        return [self.verify_claim(cid, cites) for cid, cites in claims_with_citations.items()]
```

---

## 3. 각 스킬의 결정론 모듈 호출 규칙

**저자 명령 강제**: 다음 작업은 LLM이 *자연어로 재추론* 절대 금지. 반드시 결정론 모듈 호출.

| 작업 | 결정론 모듈 | 호출 위반 시 |
|---|---|---|
| voice_score 계산 | M1 VoiceScorer | LLM이 "0.83" 같은 점수 텍스트 출력 금지 |
| 할루시네이션 신호 감지 | M2 HallucinationDetector | LLM "형식 모호 같다" 추측 금지 |
| 권위 등급 매핑 | M3 AuthorityGrader | LLM "이건 Grade A" 추측 금지 |
| 정량 앵커 추출 | M4 QuantitativeAnchorExtractor | LLM 수치 텍스트 검색 금지 |
| 분량 비율 측정 | M5 layer_ratio_measurer | LLM 분량 어림짐작 금지 |
| relevance 점수 | M6 relevance_scorer | LLM "0.85 정도" 추측 금지 |
| ID 발급 | M7 id_generator | LLM 수동 ID 생성 금지 |
| 시그니처 적용 기회 발견 | M8 signature_pattern_applier | LLM 패턴 매칭 직접 수행 금지 |
| AI 어투 감지 | M9 ai_tone_purger | LLM "AI 어투인 듯" 추측 금지 |
| fact 추출·중복 검출 | M10 fact_extractor | LLM 정규식 직접 수행 금지 |
| 시드 lifecycle 전환 | M11 lifecycle_state_machine | LLM 임의 상태 변경 금지 |
| forecast-registry 갱신 | M12 forecast_registry_syncer | LLM yaml 직접 편집 금지 |
| R4 다층 검증 | M13 r4_multi_layer_verifier | LLM "다층인 듯" 추측 금지 |

---

## 4. 호출 패턴 (각 스킬 SKILL.md에 명시 강제)

### ⚠ Round 4 #A3.2 Critical 수정 — Python import 경로

폴더명 `cys-bookwriting-skills`에 *하이픈 포함* → Python import 영구 불가.
**해결책 A (권장)**: lib/ 디렉토리를 *평탄 import* — `sys.path.insert(0, "$SKILLS_ROOT/lib")` + `from voice_scoring import VoiceScorer`

**해결책 B**: setup.py 또는 pyproject.toml로 패키지 등록 — 패키지명을 `cys_claude_bookwriting_skills` (언더스코어) 별칭

**해결책 C**: Phase 3-B에서 폴더명을 `cys_claude_bookwriting_skills`로 rename (영향 검토 필요)

```python
# 권장 (Solution A) — 저자 v1 로컬 원칙·Python 표준 호환
import sys
sys.path.insert(0, "$SKILLS_ROOT/lib")

from voice_scoring import VoiceScorer
from citation_detection import HallucinationDetector
from authority_grader import AuthorityGrader
from quantitative_extraction import QuantitativeAnchorExtractor

# 사용
scorer = VoiceScorer(voice_guidelines=book_config["voice_guidelines"])
breakdown = scorer.compute_voice_score(output_text)

if breakdown.weighted_total < 0.7:
    # 재작성 시도 (1회)
    ...
```

---

## 5. 저자 grill-me 결정 매핑

| D# | 결정론 모듈 |
|---|---|
| D7 (Lifecycle 6 외골격) | M11 lifecycle_state_machine |
| D8 (seed-registry) | M7 id_generator·M11 |
| D11 (시그니처 패턴) | M8 signature_pattern_applier |
| D16 (모드 1·2) | 모든 모듈 mode 인자 지원 |
| D17 (사이클 단위) | M7 id_generator |
| D18 (cycle-registry) | M7·M12 |
| D20 (검색 디렉토리·NotebookLM) | M6 relevance_scorer |
| D22 (Voice 보존) | M1 VoiceScorer·M8·M9 |
| Q33 (Citation Gate) | M2 HallucinationDetector·M3 AuthorityGrader·M13 |

---

## 6. 외부 출처 (결정론 환원 불가능한 항목 1:1 대조)

**저자 명령**: 결정론 환원 불가능한 항목은 사양 원문 인용 + 외부 출처 (학계 주류 문헌·표준 자료) 1:1 대조.

bookwriting 워크플로우에서 *결정론 환원 불가능*하지만 *외부 학계 표준에 기댈 수 있는* 항목:

| 항목 | 결정론 환원 불가 이유 | 외부 출처 (학계 주류) |
|---|---|---|
| 통찰의 *의미·놀라움* 평가 | 저자 voice·사상적 척추 평가는 저자 *고유 기준* | 저자 grill-me 원문 (자체 사양) + skeleton.md §사상적척추 |
| 시나리오 분기 *서사적 풍경* | 창의 글쓰기 영역 | Schwartz (1991) *The Art of the Long View* / TFG scenarios |
| 시그니처 패턴 *자연스러움* | 저자 voice 영역 | 저자 이전 저서 (NotebookLM bridge로 참조) |
| 콜드 오픈 *매력* 평가 | 저자 *주관 미학* | skeleton.md chapter-pipeline.md 콜드오픈 라이브러리 |

**출처 없는 판정은 자동 FAIL** — 모든 LLM 평가에 *근거 출처 명시 강제*.

---

## 7. Phase 3-B 구현 의무

**Phase 3-B 스킬 구축 시 강제 조건:**
1. `lib/` 디렉토리 생성 — 모든 13 모듈 Python 구현
2. pytest 단위 테스트 작성 — 각 모듈 5+ 검증 시나리오
3. 각 SKILL.md에 *결정론 모듈 호출 명시* 강제
4. 모든 LLM 추론 단계에 *결정론 모듈 활용*  부재 검출 시 SKILL.md 거부

---

## 8. 변경 이력

| 버전 | 일자 | 변경 |
|---|---|---|
| v0.1 | 2026-05-24 | 저자 /goal 명령 반영. 13 결정론 모듈 명세 작성. |

---

**End of SPEC: deterministic-modules**

> ⭐ 이 SPEC은 저자 결정론 환원 명령의 *영구 backbone*. 13 모듈이 *bookwriting의 모든 결정론 작업*을 LLM 추론에서 분리. 할루시네이션 0% 보장의 *구조적 차단 장치*.

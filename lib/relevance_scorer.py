"""M6: relevance_scorer.py — pure-Python BM25 결정론 relevance
SPEC: expert_pool/deterministic-modules.md §M6
저자 진북 #7 (결정론 환원) — LLM이 relevance 점수 추측 영구 금지.
저자 옵션 A+ 로컬 실행 보장 — 표준 라이브러리만 사용.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path


class RelevanceScorer:
    """BM25-like pure Python 결정론 relevance scorer."""

    K1 = 1.2
    B = 0.75

    def __init__(self, corpus_paths: list[Path]):
        self.corpus_paths = [Path(p) for p in corpus_paths]
        self.doc_freqs = self._compute_doc_freqs()
        self.avg_doc_len = self._compute_avg_doc_len()
        self.N = len(self.corpus_paths)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        # 한국어·영어 단어 결정론 분리
        return re.findall(r"\w+", text.lower())

    def _compute_doc_freqs(self) -> Counter:
        df = Counter()
        for p in self.corpus_paths:
            if not p.exists():
                continue
            tokens = set(self._tokenize(p.read_text(encoding="utf-8")))
            df.update(tokens)
        return df

    def _compute_avg_doc_len(self) -> float:
        lengths = []
        for p in self.corpus_paths:
            if not p.exists():
                continue
            lengths.append(len(self._tokenize(p.read_text(encoding="utf-8"))))
        return sum(lengths) / len(lengths) if lengths else 1.0

    def score(self, query: str, doc_path: Path) -> float:
        """BM25 결정론 점수 0-1 정규화."""
        doc_path = Path(doc_path)
        if not doc_path.exists():
            return 0.0
        query_tokens = self._tokenize(query)
        doc_tokens = self._tokenize(doc_path.read_text(encoding="utf-8"))
        doc_len = len(doc_tokens)
        if doc_len == 0:
            return 0.0
        tf = Counter(doc_tokens)
        score = 0.0
        for q in query_tokens:
            df_q = self.doc_freqs.get(q, 0)
            if df_q == 0:
                continue
            idf = math.log((self.N - df_q + 0.5) / (df_q + 0.5) + 1)
            tf_q = tf.get(q, 0)
            numerator = tf_q * (self.K1 + 1)
            denominator = tf_q + self.K1 * (1 - self.B + self.B * doc_len / self.avg_doc_len)
            score += idf * (numerator / max(denominator, 1e-9))
        # 0-1 sigmoid 정규화
        return round(max(0.0, min(1.0, score / 10.0)), 3)

    def rank(self, query: str, top_n: int = 10) -> list[tuple[Path, float]]:
        """corpus 전체에서 query relevance 정렬."""
        scored = [(p, self.score(query, p)) for p in self.corpus_paths]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_n]

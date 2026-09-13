"""
AgroShield Mesh - Agricultural RAG Retriever
Provides semantic search, metadata filtering, confidence thresholding,
and strict citation provenance against university and meteorological guides.
"""

import math
import re
from typing import List, Dict, Any, Optional
from rag.knowledge_base.tnau_icar_guidelines import get_all_knowledge_documents
from backend.app.schemas.domain import Citation


class AgriculturalRetriever:
    """
    RAG retriever with metadata filtering and strict citation tracking.
    Uses semantic vector embeddings with SentenceTransformer if available,
    with an optimized cosine term-vector fallback for zero-dependency instant execution.
    """

    def __init__(self, use_sentence_transformers: bool = True):
        self.documents = get_all_knowledge_documents()
        self.encoder = None

        if use_sentence_transformers:
            try:
                from sentence_transformers import SentenceTransformer
                # Use lightweight MiniLM
                self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
                texts = [d["title"] + " " + d["content"] for d in self.documents]
                self.embeddings = self.encoder.encode(texts, normalize_embeddings=True)
            except Exception:
                self.encoder = None
                self.embeddings = None
        else:
            self.embeddings = None

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text.lower())
        return words

    def _lexical_similarity(self, query: str, doc_text: str) -> float:
        q_tokens = set(self._tokenize(query))
        d_tokens = set(self._tokenize(doc_text))
        if not q_tokens or not d_tokens:
            return 0.0
        intersection = q_tokens.intersection(d_tokens)
        # Jaccard + keyword boost
        jaccard = len(intersection) / len(q_tokens.union(d_tokens))
        overlap_ratio = len(intersection) / len(q_tokens)
        return (jaccard * 0.4) + (overlap_ratio * 0.6)

    def retrieve_guidance(
        self,
        query: str,
        crop_name: Optional[str] = None,
        crop_stage: Optional[str] = None,
        hazard_type: Optional[str] = None,
        language: str = "en",
        top_k: int = 2,
        similarity_threshold: float = 0.12
    ) -> Dict[str, Any]:
        """
        Retrieves relevant agricultural guidance with metadata filters and citations.
        Returns matched documents and citations, or indicates insufficient evidence.
        """
        scored_candidates = []

        # Vector embedding similarity if model loaded
        query_embedding = None
        if self.encoder is not None and self.embeddings is not None:
            try:
                import numpy as np
                query_embedding = self.encoder.encode([query], normalize_embeddings=True)[0]
            except Exception:
                query_embedding = None

        for idx, doc in enumerate(self.documents):
            # Metadata filter: crop match
            if crop_name:
                crops = [c.lower() for c in doc.get("crop_targets", [])]
                if not any(c in crop_name.lower() or crop_name.lower() in c for c in crops):
                    # Penalize but don't hard reject if it's general
                    if "general" not in crops and len(crops) > 0:
                        continue

            # Metadata filter: hazard type match
            if hazard_type:
                hazards = doc.get("hazard_targets", [])
                if hazard_type not in hazards:
                    continue

            # Calculate score
            doc_full_text = doc["title"] + " " + doc["content"]
            if query_embedding is not None and self.embeddings is not None:
                import numpy as np
                score = float(np.dot(query_embedding, self.embeddings[idx]))
            else:
                score = self._lexical_similarity(query, doc_full_text)

            # Stage boost if matching
            if crop_stage and crop_stage.lower() in [s.lower() for s in doc.get("stage_targets", [])]:
                score = min(1.0, score + 0.15)

            if score >= similarity_threshold:
                scored_candidates.append((score, doc))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        top_matches = scored_candidates[:top_k]

        if not top_matches:
            return {
                "status": "insufficient_evidence",
                "message": "No authoritative university or meteorological guidance met confidence threshold for this specific condition.",
                "guidance_texts": [
                    "Perform routine field observation. Verify soil moisture and crop status manually."
                ],
                "tamil_texts": [
                    "வழக்கமான களப் பரிசோதனையை மேற்கொள்ளவும். மண் ஈரப்பதத்தை நேரடியாக ஆய்வு செய்யவும்."
                ],
                "citations": [],
                "top_similarity_score": 0.0
            }

        guidance_en = []
        guidance_ta = []
        citations: List[Citation] = []

        for score, doc in top_matches:
            guidance_en.append(doc["content"])
            guidance_ta.append(doc.get("tamil_translation", doc["content"]))

            c = Citation(
                source_title=doc["title"],
                author_organization=doc["source"],
                publication_year=doc.get("publication_year", 2024),
                document_section=doc["section"],
                page_or_bulletin_no=doc["page_or_bulletin"],
                document_hash_sha256=doc["document_hash_sha256"],
                uri_or_reference=f"TNAU/ICAR Archive Ref: {doc['doc_id']}"
            )
            citations.append(c)

        return {
            "status": "evidence_found",
            "top_similarity_score": round(top_matches[0][0], 3),
            "guidance_texts": guidance_en,
            "tamil_texts": guidance_ta,
            "citations": citations
        }

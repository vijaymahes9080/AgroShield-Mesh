"""Unit tests for agricultural RAG layer and citations."""
import pytest
from rag.retriever import AgriculturalRetriever


def test_rag_retrieval_and_citations():
    retriever = AgriculturalRetriever(use_sentence_transformers=False)

    res = retriever.retrieve_guidance(
        query="paddy AWD water alternate wetting flowering irrigation",
        crop_name="Paddy (Rice)",
        hazard_type="irrigation_need"
    )

    assert res["status"] == "evidence_found"
    assert len(res["citations"]) > 0
    citation = res["citations"][0]
    assert "TNAU" in citation.author_organization
    assert len(citation.document_hash_sha256) == 64


def test_insufficient_evidence_fallback():
    retriever = AgriculturalRetriever(use_sentence_transformers=False)

    # Nonsense query with no matching keywords
    res = retriever.retrieve_guidance(
        query="superconductor quantum teleportation semiconductor laser",
        similarity_threshold=0.30
    )

    assert res["status"] == "insufficient_evidence"
    assert len(res["citations"]) == 0
    assert "routine field observation" in res["guidance_texts"][0].lower()

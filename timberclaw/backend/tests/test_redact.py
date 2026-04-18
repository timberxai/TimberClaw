from llm.redact import redact_text


def test_redact_masks_bearer():
    s = "Authorization: Bearer sk-secret-123"
    assert "Bearer ***" in redact_text(s) or "***" in redact_text(s)

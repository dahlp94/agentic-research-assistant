import pytest
from ara.core.state import ARAState


def test_state_initialization():
    s = ARAState(user_query="test")
    assert s.user_query == "test"
    assert s.status == "ok"
    assert s.evidence == []

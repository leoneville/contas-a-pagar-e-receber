import pytest
from sqlalchemy.engine import Engine
from shared.database import engine


@pytest.mark.skip(reason="interação com banco de dados")
def test_connect_to_db():
    assert engine is not None
    assert isinstance(engine, Engine)
